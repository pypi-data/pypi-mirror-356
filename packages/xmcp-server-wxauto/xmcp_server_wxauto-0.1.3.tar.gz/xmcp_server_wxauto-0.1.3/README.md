# 微信消息发送服务器

这是一个基于 MCP (Micro Controller Protocol) 的微信消息发送服务器，通过命令行参数可以灵活配置服务器运行模式和日志级别。

## 快速开始（本地运行）
* 本步骤主要是为了 本地测试 自动操作微信MCP服务。测试环境是Windows系统。
```bash
# 先安装服务
pip install xmcp-server-wxauto

# 以默认配置启动服务
xmcp-server-wxauto

# 指定日志级别和传输方式（sse方式）
xmcp-server-wxauto --log-level=INFO --transport=sse --port=8080
```
* 然后，就可以配置本地服务来调试MCP
```bash
{
  "mcpServers": {
    "wechat": {
      "url": "http://localhost:8080/sse"
    }
  }
}
```
* 接着，将MCP服务配置给你的AI智能体，让AI可以调用这个MCP来自动操作微信。
例如，和智能体说：将“你好”发送到“测试群”。然后，该MCP会自动将对应的消息发到对应的群组。
** 需要注意的是，这个是模拟人工操作微信发消息的，而不是通过微信的API接口发送信息。


## 使用UVX配置MCP服务（推荐）
* 用uvx的方式配置MCP服务是推荐的方式。
* 因为uvx可以在不同的平台上运行，包括Windows、macOS和Linux。
```bash
# 给AI模型提供自动操作微信的MCP服务
{
  "mcpServers": {
    "wechat": {
      "command": "uvx",
      "args": [
        "xmcp-server-wxauto"
      ],
      "env": {}
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
xmcp-server-wxauto --log-level=DEBUG
```

### 传输方式 (`--transport`)
设置服务器与客户端之间的通信协议，可选值：
- `stdio`：使用标准输入输出进行通信，适用于进程间通信
- `sse`：使用 Server-Sent Events 进行实时通信，适用于网络环境

**默认值**：`stdio`

**注意**：
- `stdio` 模式下日志不会输出到控制台，避免干扰通信
- `sse` 模式需要指定端口参数

**示例**：
```bash
xmcp-server-wxauto --transport=sse
```

### 服务器端口 (`--port`)
当使用 `sse` 传输方式时，指定服务器监听的端口号。

**默认值**：`8000`

**示例**：
```bash
xmcp-server-wxauto --transport=sse --port=8080
```

## 完整示例

启动一个具有详细日志记录的网络服务器：
```bash
xmcp-server-wxauto --log-level=INFO --transport=sse --port=8080
```

启动一个用于进程间通信的服务器（无日志输出）：
```bash
xmcp-server-wxauto --transport=stdio
```

## 常见问题

1. **为什么 `stdio` 模式下看不到日志？**
   - `stdio` 模式使用标准输入输出进行通信，日志输出会干扰通信协议，因此默认禁用控制台日志。

2. **如何在后台运行服务器？**
   - 可以使用 `nohup` 或 `systemd` 等工具将服务器作为守护进程运行。

3. **端口被占用怎么办？**
   - 使用 `--port` 参数指定其他可用端口，或使用 `lsof` 命令查找并关闭占用端口的进程。

```bash
# 查找占用8000端口的进程
lsof -i:8000

# 终止进程（PID为进程ID）
kill -9 <PID>
```