# 天气查询MCP服务

这是一个基于 MCP (Micro Controller Protocol) 的天气查询服务，通过命令行参数可以灵活配置服务器运行模式和日志级别。

## 快速开始 - 使用UVX配置MCP服务（推荐）
* 用uvx的方式配置MCP服务是推荐的方式。
* 因为uvx可以在不同的平台上运行，包括Windows、macOS和Linux。
```json
# 给AI模型提供天气查询的MCP服务
{
  "mcpServers": {
    "weather": {
      "command": "uvx",
      "args": [
        "xmcp-server-weather"
      ],
      "env": {}
    }
  }
}
```
### macOS系统的推荐配置
mac系统如果用uvx启动服务会报错，则可以尝试先安装xmcp-server-weather，再用下面的配置使用MCP服务。
```json
# 先安装服务package
pip3 install xmcp-server-weather

# MCP服务的配置
{
  "mcpServers": {
    "weather": {
      "command": "xmcp-server-weather"
    }
  }
}
```
### 使用MCP服务
* 接着，将MCP服务配置给你的AI智能体，让AI可以调用这个MCP来查询天气。
例如，和智能体说：查询北京的天气。然后，该MCP会自动查询并返回对应的天气信息。

## 本地测试运行MCP服务
* 本步骤主要是为了 本地测试 天气查询MCP服务。
### 1、Windows环境的配置：
```bash
# 先安装服务
pip install xmcp-server-weather

# 指定日志级别和传输方式（sse方式）
xmcp-server-weather --log-level=INFO --transport=sse --port=8001
```
* 然后，就可以配置本地服务来调试MCP
```json
{
  "mcpServers": {
    "weather": {
      "url": "http://localhost:8001/sse"
    }
  }
}
```
### 2、macOS系统的配置
```bash
# 先安装服务（如果已经安装则忽略）
pip3 install  xmcp-server-weather

# （测试用）指定日志级别和传输方式（sse方式）。
# 下面有显示启动服务说明环境已经安装完毕。
xmcp-server-weather --log-level=INFO --transport=sse --port=8001
```
* 然后，就可以配置本地服务来调试MCP
```json
# 默认的stdio模式
{
  "mcpServers": {
    "weather": {
      "command": "xmcp-server-weather"
    }
  }
}

# 或者sse模式（前提是http服务要打开）
{
  "mcpServers": {
    "weather": {
      "url": "http://localhost:8001/sse"
    }
  }
}
```

## 命令行参数

### 日志级别 (`--log-level`)
设置服务器的日志输出级别，可选值：
- `DEBUG`：详细的调试信息，用于开发和问题排查
- `INFO`：正常运行的信息，显示关键操作
- `WARNING`：警告信息，可能影响功能但不影响运行
- `ERROR`：错误信息，功能无法正常执行
- `CRITICAL`：严重错误，可能导致程序崩溃

**默认值**：`ERROR`

**示例**：
```bash
xmcp-server-weather --log-level=DEBUG
```

### 传输方式 (`--transport`)
设置服务器与客户端之间的通信协议，可选值：
- `stdio`：使用标准输入输出进行通信，适用于进程间通信
- `sse`：使用 Server-Sent Events 进行实时通信，适用于网络环境
- `streamable-http`：使用可流式的HTTP协议进行通信

**默认值**：`stdio`

**注意**：
- `stdio` 模式下日志不会输出到控制台，避免干扰通信
- 网络传输模式需要指定端口参数

**示例**：
```bash
xmcp-server-weather --transport=sse
```

### 服务器端口 (`--port`)
当使用网络传输方式时，指定服务器监听的端口号。

**默认值**：`8001`

**示例**：
```bash
xmcp-server-weather --transport=sse --port=8080
```

## 完整示例

启动一个具有详细日志记录的网络服务器：
```bash
xmcp-server-weather --log-level=INFO --transport=sse --port=8001
```

启动一个用于进程间通信的服务器（无日志输出）：
```bash
xmcp-server-weather --transport=stdio
```

## 常见问题

1. **为什么 `stdio` 模式下看不到日志？**
   - `stdio` 模式使用标准输入输出进行通信，日志输出会干扰通信协议，因此默认禁用控制台日志。

2. **如何在后台运行服务器？**
   - 可以使用 `nohup` 或 `systemd` 等工具将服务器作为守护进程运行。

3. **端口被占用怎么办？**
   - 使用 `--port` 参数指定其他可用端口，或使用 `lsof` 命令查找并关闭占用端口的进程。

```bash
# 查找占用8001端口的进程
lsof -i:8001

# 终止进程（PID为进程ID）
kill -9 <PID>
```

4. **如果访问天气服务的时候报网络错误怎么办？**
   - 请检查网络配置，或者如果有打开代理工具，请尝试关闭它再测试。
