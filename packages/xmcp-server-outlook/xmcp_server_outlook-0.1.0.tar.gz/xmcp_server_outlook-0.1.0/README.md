# Outlook 操作MCP服务

这是一个基于 MCP (Model Context Protocol) 的Outlook操作服务，通过命令行参数可以灵活配置服务器运行模式和日志级别，主要功能包括发送邮箱和操作日历。

## 快速开始 - 使用UVX配置MCP服务（推荐）
- 用uvx的方式配置MCP服务是推荐的方式。
- 因为uvx可以在不同的平台上运行，包括Windows、macOS和Linux。
```json
# 给AI模型提供Outlook操作的MCP服务
{
  "mcpServers": {
    "outlook": {
      "command": "uvx",
      "args": [
        "xmcp-server-outlook"
      ],
      "env": {}
    }
  }
}
```
### macOS系统的推荐配置
抱歉通知您，mac系统不支持该MCP功能。
mac系统虽然是有Outlook for Mac。但是不支持用python代码操作日历。
原因是：
Outlook for Mac不支持COM 接口的日历应用。COM 接口是 Windows 系统下的组件对象模型，用于进程间通信和软件组件的交互，而 macOS 系统采用的是不同的技术架构，不支持 COM 接口。因此，在 macOS 系统上，Outlook for Mac 无法直接与基于 COM 接口的日历应用进行交互。

**如果有别的建议请反馈给我：samt007@qq.com。**

### 使用MCP服务
接着，将MCP服务配置给你的AI智能体，让AI可以调用这个MCP来操作Outlook，典型的是创建日历事件，更新事件，查询邮箱，发Email等等的动作。
举例子：
1、和智能体说：给samt007@xinyiglass.com发送主题为"会议邀请"的邮件。然后，该MCP会自动调用Outlook执行对应的操作。
2、和智能体说：明天晚上8点有个饭局，地点在迎宾楼。然后，该MCP会自动调用Outlook创建日历事件。
3、还可以配合别的MCP协同完成一系列的动作。假设您也配置了天气查询的MCP服务（见链接https://pypi.org/project/xmcp-server-weather）。就可以和智能体说：将芜湖的天气发邮件给samt007@xinyiglass.com。然后，智能体先调用天气查询的MCP服务，查询到了芜湖的天气，然后再将天气的内容自动发送给对应的邮箱。

*邮件效果如下：*
```
发件人: samt007 <samt007@qq.com>
收件人: samt007@xinyiglass.com<samt007@xinyiglass.com>
时间: 2025年6月19日 (周四) 11:31
大小: 6 KB
您好，

以下是芜湖的最新天气信息：

- 地点：芜湖 
- 当前温度：28.7°C 
- 湿度：74% 
- 风向：东南风 
- 风速：3.3米/秒（微风） 
- 体感温度：31.7°C 
- 更新时间：2025年6月19日 11:20

祝好！
```

## 本地测试运行MCP服务
- 本步骤主要是为了 本地测试 Outlook操作MCP服务。
### 1、Windows环境的配置：
```bash
# 先安装服务
pip install xmcp-server-outlook

# 指定日志级别和传输方式（sse方式）
xmcp-server-outlook --log-level=INFO --transport=sse --port=8003
```
- 然后，就可以配置本地服务来调试MCP
```json
{
  "mcpServers": {
    "outlook": {
      "url": "http://localhost:8003/sse"
    }
  }
}
```
### 2、macOS系统的配置
**由于不支持mac系统，所以这里忽略。**

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
xmcp-server-outlook --log-level=DEBUG
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
xmcp-server-outlook --transport=sse
```

### 服务器端口 (`--port`)
当使用网络传输方式时，指定服务器监听的端口号。

**默认值**：`8003`

**示例**：
```bash
xmcp-server-outlook --transport=sse --port=8080
```

## 完整示例

启动一个具有详细日志记录的网络服务器：
```bash
xmcp-server-outlook --log-level=INFO --transport=sse --port=8003
```

启动一个用于进程间通信的服务器（无日志输出）：
```bash
xmcp-server-outlook --transport=stdio
```

## 常见问题

1. **为什么 `stdio` 模式下看不到日志？**
   - `stdio` 模式使用标准输入输出进行通信，日志输出会干扰通信协议，因此默认禁用控制台日志。

2. **如何在后台运行服务器？**
   - 可以使用 `nohup` 或 `systemd` 等工具将服务器作为守护进程运行。

3. **端口被占用怎么办？**
   - 使用 `--port` 参数指定其他可用端口，或使用 `lsof` 命令查找并关闭占用端口的进程。

```bash
# 查找占用8003端口的进程
lsof -i:8003

# 终止进程（PID为进程ID）
kill -9 <PID>
```

4. **如果操作Outlook服务时报权限错误怎么办？**
   - 请检查是否以管理员/root权限运行，或确认Outlook应用是否已正确安装并授权。