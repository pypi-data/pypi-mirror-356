# 本地执行Python代码MCP服务

这是一个基于 MCP (Model Context Protocol) 的本地Python代码执行服务，允许通过MCP协议调用和执行本地Python代码，支持自定义日志级别、传输方式和端口配置。
- **这个工具开发的目的是为了可以让AI动态生成python代码，然后可以本地电脑动态执行，所以需要特别注意安全性的问题，服务一定只能本地运行，不能暴露在公网，否则造成的后果由使用者承担**


## 快速开始 - 使用UVX配置MCP服务（推荐）
- 用uvx的方式配置MCP服务是推荐的方式。
- 因为uvx可以在不同的平台上运行，包括Windows、macOS和Linux。
```json
# 给AI模型提供本地Python代码执行的MCP服务
{
  "mcpServers": {
    "exepython": {
      "command": "uvx",
      "args": [
        "xmcp-server-exepython"
      ],
      "env": {}
    }
  }
}
```

### macOS系统的推荐配置
mac系统如果用uvx启动服务会报错，则可以尝试先安装xmcp-server-exepython，再用下面的配置使用MCP服务。
```json
# 先安装服务package
pip3 install xmcp-server-exepython

# MCP服务的配置
{
  "mcpServers": {
    "exepython": {
      "command": "xmcp-server-exepython"
    }
  }
}
```

### 使用MCP服务
- 接着，将MCP服务配置给你的AI智能体，让AI可以调用这个MCP来执行本地Python代码。
例如
#### 1、执行输出的python脚本
和智能体说：
```
执行Python代码`print("Hello World")`。
```
然后，该MCP会自动执行并返回对应的输出结果Hello World。

#### 2、本地打开浏览器
和智能体说：
```
帮我用MCP服务（exepython）执行这么一段脚本：
import subprocess
subprocess.run(["C:\\Program Files\\Internet Explorer\\iexplore.exe"])
```
然后，该MCP会自动执行，本地电脑会自动弹出一个IE浏览器。

## 本地测试运行MCP服务
- 本步骤主要是为了 本地测试 本地执行Python代码MCP服务。

### 1、Windows环境的配置：
```bash
# 先安装服务
pip install xmcp-server-exepython

# 指定日志级别和传输方式（sse方式）
xmcp-server-exepython --log-level=INFO --transport=sse --port=8004
```
- 然后，就可以配置本地服务来调试MCP
```json
{
  "mcpServers": {
    "exepython": {
      "url": "http://localhost:8004/sse"
    }
  }
}
```

### 2、macOS系统的配置
```bash
# 先安装服务（如果已经安装则忽略）
pip3 install xmcp-server-exepython

# （测试用）指定日志级别和传输方式（sse方式）。
# 下面有显示启动服务说明环境已经安装完毕。
xmcp-server-exepython --log-level=INFO --transport=sse --port=8004
```
- 然后，就可以配置本地服务来调试MCP
```json
# 默认的stdio模式
{
  "mcpServers": {
    "exepython": {
      "command": "xmcp-server-exepython"
    }
  }
}

# 或者sse模式（前提是http服务要打开）
{
  "mcpServers": {
    "exepython": {
      "url": "http://localhost:8004/sse"
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
xmcp-server-exepython --log-level=DEBUG
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
xmcp-server-exepython --transport=sse --port=8004
```

### 服务器端口 (`--port`)
当使用网络传输方式时，指定服务器监听的端口号。

**默认值**：`8004`

**示例**：
```bash
xmcp-server-exepython --transport=sse --port=8004
```


## 完整示例

启动一个具有详细日志记录的网络服务器：
```bash
xmcp-server-exepython --log-level=INFO --transport=sse --port=8004
```

启动一个用于进程间通信的服务器（无日志输出）：
```bash
xmcp-server-exepython --transport=stdio
```


## 常见问题解答

### 1. 为什么 `stdio` 模式下看不到日志？
`stdio` 模式使用标准输入输出流进行通信，日志输出会干扰通信协议，因此默认禁用控制台日志。如需查看日志，请使用 `sse` 模式并设置 `--log-level` 参数。


### 2. 如何在后台运行服务器？

#### Windows
```powershell
# 使用PowerShell后台作业
Start-Job -ScriptBlock { xmcp-server-exepython --transport=sse --port=8004 }
```

#### Linux/macOS
```bash
# 使用nohup命令
nohup xmcp-server-exepython --transport=sse --port=8004 &
```

### 3. 端口被占用怎么办？
```bash
# 查找占用端口的进程
lsof -i:8004

# 终止进程（替换<PID>为实际进程ID）
kill -9 <PID>

# 或使用其他端口
xmcp-server-exepython --transport=sse --port=8084
```

### 4. 执行Python代码时出现权限错误怎么办？
1. 请确保当前用户有执行Python代码的权限
2. 检查代码中是否包含需要特殊权限的操作（如文件系统操作）
3. 在Windows系统中，尝试以管理员身份运行命令

```bash
# 以管理员权限运行PowerShell（Windows）
Start-Process powershell -Verb RunAs
```

### 5. 如何查看服务状态？
```bash
# 查看服务版本
xmcp-server-exepython --version

# 查看实时运行状态（sse模式）
curl http://localhost:8004/status
```


## 技术支持
- 提交问题：[项目GitHub Issues](https://github.com/xmcp-server-exepython/issues)
- 联系邮箱：samt007@qq.com
- 工作时间：周一至周日 8:00-22:00 (GMT+8)