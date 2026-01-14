import os
import warnings
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.litellm import LiteLLM

load_dotenv()
warnings.filterwarnings(
    "ignore", category=UserWarning, message="Pydantic serializer warnings"
)


def run_streaming_agent():
    """
    运行一个具备流式输出能力的智能体，使用火山引擎模型。
    """

    volcengine_agent = Agent(
        model=LiteLLM(
            id="volcengine/doubao-1-5-pro-32k-250115",
        ),
        markdown=True,
    )

    volcengine_agent.print_response("请分享一个两句话的恐怖故事", stream=True)


if __name__ == "__main__":
    run_streaming_agent()
