import httpx
import urllib.parse
import logging
import argparse
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from pydantic import Field

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
                logger.debug(f"请求天气信息: {url}")
                
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                weather_data = response.json()
                logger.info(f"成功获取位置 '{location}' 的天气信息")
                return weather_data
            except Exception as e:
                error_msg = f"查询天气时发生系统错误: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return error_msg

    mcp.run(transport=args.transport)

if __name__ == '__main__':
    run()