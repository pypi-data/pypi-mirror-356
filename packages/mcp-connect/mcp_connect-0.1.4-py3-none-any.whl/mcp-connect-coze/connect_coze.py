import os
import logging
from typing import Dict, Any, Generator
from cozepy import COZE_CN_BASE_URL
from cozepy import Coze, TokenAuth, Message, ChatEventType
from mcp.server.fastmcp import FastMCP

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 获取访问令牌和基础URL
coze_api_token = os.environ.get('COZE_API_TOKEN', 'pat_gJWs5jZjr3FSinYHt5fquYNYR3G31RkDBz0LFZ3vtseTqUFFTGhIPKeLVBG2iOPC')
coze_api_base = COZE_CN_BASE_URL

# 初始化Coze客户端
coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

# 机器人和用户ID
bot_id = os.environ.get('COZE_BOT_ID', '7483357727020924938')
user_id = os.environ.get('COZE_USER_ID', 'test_user_001')

# 初始化MCP服务器
mcp = FastMCP("mcp-connect-coze")

@mcp.tool()
def chat_coze(question: str) -> Generator[Dict[str, Any], None, None]:
    """与Coze AI机器人对话并流式返回结果"""
    try:
        logger.info(f"开始流式对话，问题: {question}")
        
        # 立即返回问题接收确认
        yield {
            "status": "started",
            "question": question,
            "chunk_type": "system",
            "content": "正在获取AI回复..."
        }
        
        # 流式处理Coze响应
        for event in coze.chat.stream(
            bot_id=bot_id,
            user_id=user_id,
            additional_messages=[
                Message.build_user_question_text(question),
            ],
        ):
            if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                # 立即返回消息片段
                yield {
                    "status": "streaming",
                    "question": question,
                    "chunk_type": "content",
                    "content": event.message.content,
                    "is_final": False
                }
                logger.info(f"发送消息片段: {event.message.content[:30]}...")
                
            elif event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                # 返回对话完成信息
                yield {
                    "status": "completed",
                    "question": question,
                    "chunk_type": "metadata",
                    "token_usage": event.chat.usage.token_count,
                    "is_final": True
                }
                logger.info(f"对话完成，使用令牌数: {event.chat.usage.token_count}")
                
    except Exception as e:
        error_msg = f"对话过程中发生错误: {str(e)}"
        logger.error(error_msg, exc_info=True)
        
        # 返回错误信息
        yield {
            "status": "error",
            "question": question,
            "chunk_type": "error",
            "error": error_msg,
            "is_final": True
        }

if __name__ == "__main__":
    try:
        logger.info("启动MCP服务器...")
        mcp.run(transport='stdio')
    except Exception as e:
        logger.critical(f"程序全局异常: {str(e)}", exc_info=True)
        print(f"程序全局异常: {str(e)}")