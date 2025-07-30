import httpx
import urllib.parse
import logging
import argparse
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from bs4 import BeautifulSoup
import re
import json

def parse_args():
    parser = argparse.ArgumentParser(description='天气查询MCP服务')
    parser.add_argument('--log-level', type=str, default='ERROR', 
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='日志级别 (默认: ERROR)')
    parser.add_argument('--transport', type=str, default='stdio', 
                        choices=['stdio', 'sse', 'streamable-http'],
                        help='传输方式 (默认: stdio)')
    parser.add_argument('--port', type=int, default=8001, 
                        help='服务器端口 (仅在使用网络传输时有效，默认: 8001)')
    return parser.parse_args()

def setup_logger(log_level, transport):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    
    # 仅在非stdio模式下添加控制台处理器
    if transport != 'stdio':
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    # 避免日志传播到父记录器
    logger.propagate = False
    
    return logger

def extract_weather_from_daylist(html_content):
    """通过id="dayList"节点提取7天天气预报"""
    try:
        # 解析HTML并定位dayList节点
        soup = BeautifulSoup(html_content, 'html.parser')
        daylist_node = soup.find(id='dayList')
        
        if not daylist_node:
            return {"错误": "未找到id='dayList'的节点"}
        
        # 提取发布时间（增强错误处理）
        publish_time = "未知发布时间"
        publish_div = daylist_node.find_previous_sibling('div', class_='hd')
        
        if publish_div:
            # 尝试多种可能的时间格式
            time_match = re.search(r'\((.*?)\)', publish_div.text)
            if time_match:
                publish_time = time_match.group(1)
            else:
                # 尝试其他可能的格式，如"发布时间：2025-06-19 12:00"
                time_match = re.search(r'(\d{4}[\s/-]*\d{1,2}[\s/-]*\d{1,2}[\s:]*\d{0,2}:\d{0,2})', publish_div.text)
                if time_match:
                    publish_time = time_match.group(1)

        # 提取每天的天气数据
        day_divs = daylist_node.find_all('div', class_='day')
        weather_data = []
        
        for day_div in day_divs:
            # 提取日期和星期
            date_node = day_div.find('div', class_='day-item')
            date_text = date_node.text.strip()
            week, date = date_text.split('<br/>') if '<br/>' in date_text else ('', date_text)
            
            # 提取白天天气信息（索引从2开始：0=日期，1=图标，2=天气，3=风向，4=风力）
            day_weather = day_div.find_all('div', class_='day-item')[2].text.strip()
            day_wind_dir = day_div.find_all('div', class_='day-item')[3].text.strip()
            day_wind_power = day_div.find_all('div', class_='day-item')[4].text.strip()
            
            # 提取温度
            temp_node = day_div.find('div', class_='bardiv')
            high_temp = temp_node.find('div', class_='high').text.strip() if temp_node else "N/A"
            low_temp = temp_node.find('div', class_='low').text.strip() if temp_node else "N/A"
            
            # 提取夜间天气信息（倒数第3个是夜间天气，倒数第2个是夜间风向，倒数第1个是风力）
            night_weather = day_div.find_all('div', class_='day-item')[-3].text.strip()
            night_wind_dir = day_div.find_all('div', class_='day-item')[-2].text.strip()
            night_wind_power = day_div.find_all('div', class_='day-item')[-1].text.strip()
            
            # 整理数据
            weather_data.append({
                "week": week,
                "date": date,
                "dayWeather": day_weather,    #白天天气
                "dayWindDir": day_wind_dir,  #白天风向
                "dayWindPower": day_wind_power,   #白天风力
                "highTemp": high_temp,   #最高温度
                "lowTemp": low_temp,   #最低温度
                "nightWeather": night_weather,  #夜间天气
                "nightWindDir": night_wind_dir,   #夜间风向
                "nightWindPower": night_wind_power   #夜间风力
            })
        
        return {
            "publishTime": publish_time,   #发布时间
            "weatherData": weather_data   #天气预报
        }
        
    except Exception as e:
        return {"错误": f"数据提取失败: {str(e)}"}

def run():
    args = parse_args()
    
    # 配置日志
    logger = setup_logger(args.log_level, args.transport)
    
    settings = {
        'log_level': args.log_level
    }
    
    # 初始化mcp服务
    mcp = FastMCP(port=args.port, settings=settings)

    @mcp.tool()
    async def get_weather(
        location: str = Field(description='要查询的地点，如"北京"、"北京天气"、"101010100"等')
        ) -> str:
        """获取指定地点的天气信息.
        Returns:
            天气信息字符串
        """
        logger.info(f"收到天气查询请求: location={location}")
        
        # 第一步：获取位置编码
        url = "http://weather.cma.cn/api/autocomplete?q=" + urllib.parse.quote(location)
        logger.debug(f"请求位置编码: {url}")

        async with httpx.AsyncClient() as client:
            try:
                # 调用自动完成API获取位置信息
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                logger.debug(f"位置编码API返回: {data}")
                
                # 检查API返回状态
                if data["code"] != 0:
                    logger.warning(f"位置编码API返回错误: code={data['code']}")
                    return "系统错误，请稍后重试"
                
                location_code = ""
                # 解析返回数据，查找匹配的位置编码
                for item in data["data"]:
                    str_array = item.split("|")
                    # 支持多种匹配方式：精确匹配、带"市"字匹配、拼音匹配
                    if (
                        str_array[1] == location
                        or str_array[1] + "市" == location
                        or str_array[2] == location
                    ):
                        location_code = str_array[0]
                        break
                
                # 未找到匹配的位置
                if location_code == "":
                    logger.warning(f"未找到位置 '{location}' 的编码信息")
                    return "没找到该位置的信息"

                logger.info(f"成功获取位置 '{location}' 的编码: {location_code}")
                
                # 第二步：使用位置编码获取实时天气
                url = f"http://weather.cma.cn/api/now/{location_code}"
                logger.debug(f"请求实时天气信息: {url}")
                
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                weather_data_now = response.json()

                # 获取7天的天气预报
                url = f"http://weather.cma.cn/web/weather/{location_code}"
                logger.debug(f"请求7天的天气预报信息: {url}")
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                weather_data_7days = extract_weather_from_daylist(response.text)

                logger.info(f"成功获取位置 '{location}' 的天气信息")
                return json.dumps({"weatherDataNow": weather_data_now, "weatherData7days": weather_data_7days})
            except Exception as e:
                error_msg = f"查询天气时发生系统错误: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return error_msg

    mcp.run(transport=args.transport)

if __name__ == '__main__':
    run()