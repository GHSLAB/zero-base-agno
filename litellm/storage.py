import os
import warnings
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.litellm import LiteLLM
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools

# 加载环境变量
load_dotenv()
# 忽略 Pydantic 序列化警告
warnings.filterwarnings("ignore", category=UserWarning)


def run_storage_agent():
    """
    运行一个具备持久化存储功能的智能体，使用火山引擎模型和 DuckDuckGo 工具。
    该函数展示了如何将会话历史存储在 SQLite 数据库中，并通过固定的 session_id 实现跨运行的上下文记忆。
    """
    # 确保存储目录存在
    os.makedirs("tmp", exist_ok=True)

    # 1. 定义固定的会话 ID，确保多次运行脚本时能恢复同一个会话
    session_id = "my-shared-session-001"

    # 2. 使用 Sqlite 数据库创建存储后端
    storage = SqliteDb(
        session_table="agent_sessions_storage",
        db_file="tmp/data.db",
    )

    # 3. 为智能体添加存储功能
    agent = Agent(
        model=LiteLLM(id="volcengine/doubao-1-5-pro-32k-250115"),
        db=storage,
        session_id=session_id,
        tools=[DuckDuckGoTools()],
        description="你是一个知识渊博的助手。如果你在使用工具搜索时遇到错误或没有结果，请诚实地告诉用户，并尝试根据你已有的知识库进行回答。",
        instructions=[
            "始终检查对话历史记录以获取上下文。",
            "如果搜索工具返回 'No results found'，这可能是由于网络限制。请尝试根据你的训练数据回答，并说明这是基于你的内置知识。",
        ],
        add_history_to_context=True,
        read_chat_history=True,
        markdown=True,
    )

    # 4. 执行多轮对话测试存储功能
    # 第一轮：询问一个事实并让智能体存储到数据库
    print("\n--- 第一轮对话 ---")
    agent.print_response("告诉我 2024 年巴黎奥运会的主题是什么？", stream=True)

    # 第二轮：询问相关问题，测试智能体是否记得之前的上下文
    print("\n--- 第二轮对话 ---")
    agent.print_response("那届奥运会的吉祥物叫什么？", stream=True)


if __name__ == "__main__":
    run_storage_agent()
