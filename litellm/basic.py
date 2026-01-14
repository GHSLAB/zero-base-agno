import os
import warnings
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.litellm import LiteLLM

# 忽略 Pydantic 序列化警告
warnings.filterwarnings("ignore", category=UserWarning)

def run_basic_agent():
    """
    运行一个基础智能体，使用火山引擎模型进行简单的问答。
    """
    # 加载环境变量
    load_dotenv()

    volcengine_agent = Agent(
        model=LiteLLM(
            id="volcengine/doubao-1-5-pro-32k-250115",
        ),
        markdown=True,
    )

    volcengine_agent.print_response("请分享一个两句话的恐怖故事")

if __name__ == "__main__":
    run_basic_agent()
