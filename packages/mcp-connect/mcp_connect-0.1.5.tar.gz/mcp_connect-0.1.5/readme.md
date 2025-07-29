Coze-MCP 集成工具
将 Coze 智能体集成到 MCP (Model Context Protocol) 平台的工具，实现流式对话功能，使 Coze AI 能够作为 MCP 客户端的工具资源。
功能特点
✅ 集成 Coze 智能体到 MCP 平台
✅ 支持流式对话，实时返回回复片段
✅ 完整的日志记录和错误处理
✅ 支持环境变量配置，便于生产环境部署
✅ 可扩展的工具函数设计
安装要求
依赖环境
Python 3.7+
Coze Python SDK
MCP SDK
安装步骤
安装 Coze SDK:
bash
pip install cozepy
安装 MCP SDK:
bash
pip install mcp
环境变量配置
在运行前，需要设置以下环境变量:
bash
# Coze API 访问令牌
export COZE_API_TOKEN=你的Coze_API令牌

# Coze 机器人ID
export COZE_BOT_ID=你的Coze机器人ID

# 用户ID (可选)
export COZE_USER_ID=用户标识
快速开始
启动 MCP 服务器
bash
python src\mcp-connect-coze\connect_coze.py
使用 MCP 客户端调用工具
python
from mcp.client import MCPClient

# 初始化 MCP 客户端
client = MCPClient(transport='stdio')

# 调用 chat_coze 工具
question = "请介绍一下人工智能在企业管理中的应用"
response = client.call("chat_coze", question=question)

# 处理流式响应
for chunk in response:
    if chunk["status"] == "streaming":
        print(chunk["content"], end="", flush=True)
    elif chunk["status"] == "completed":
        print(f"\n对话完成，使用令牌: {chunk['token_usage']}")
代码结构说明
核心组件
python
from mcp.server.fastmcp import FastMCP
from cozepy import Coze, TokenAuth, Message, ChatEventType
FastMCP: MCP 服务器核心类
Coze: Coze Python SDK 客户端
TokenAuth: Coze 认证类
Message: Coze 消息类
ChatEventType: Coze 聊天事件类型
主要函数
python
@mcp.tool()
def chat_coze(question: str) -> Generator[Dict[str, Any], None, None]:
这是核心工具函数，接收用户问题并返回流式响应。使用生成器 (Generator) 实现实时响应功能。
工具函数说明
chat_coze 函数
功能: 与 Coze AI 机器人对话并流式返回结果
参数:
question (str): 用户提问的问题文本
返回:
Generator[Dict[str, Any], None, None]: 流式返回的消息片段，每个片段包含以下字段:
status: 状态 (started/streaming/completed/error)
question: 原始问题
chunk_type: 片段类型 (system/content/metadata/error)
content: 消息内容 (仅当 chunk_type 为 content 时存在)
token_usage: 令牌使用量 (仅当对话完成时存在)
is_final: 是否为最终片段
error: 错误信息 (仅当发生错误时存在)
日志说明
本工具使用 Python 标准 logging 模块，日志配置如下:
python
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)