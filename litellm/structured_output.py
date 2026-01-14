import os
import warnings
from typing import List
from dotenv import load_dotenv
from agno.agent import Agent  # noqa
from agno.models.litellm import LiteLLM
from pydantic import BaseModel, Field
from rich.pretty import pprint  # noqa

# 加载环境变量
load_dotenv()
# 忽略 Pydantic 序列化相关的警告
warnings.filterwarnings("ignore", category=UserWarning)


class MovieScript(BaseModel):
    """
    电影剧本的数据模型，定义了剧本的基本结构
    """

    setting: str = Field(..., description="为一部大片提供一个优美的背景设定。")
    ending: str = Field(
        ...,
        description="电影的结局。如果未提供，请提供一个圆满的结局。",
    )
    genre: str = Field(
        ...,
        description="电影的类型。如果未提供，请选择动作、惊悚或浪漫喜剧。",
    )
    name: str = Field(..., description="为这部电影命名")
    characters: List[str] = Field(..., description="这部电影的角色名称。")
    storyline: str = Field(..., description="电影的三句话剧情梗概。要写得引人入胜！")


def run_structured_output_agent():
    """
    创建并运行一个结构化输出智能体，用于生成电影剧本
    """
    json_mode_agent = Agent(
        model=LiteLLM(id="volcengine/doubao-1-5-pro-32k-250115"),
        description="你是一个电影剧本作家。",
        output_schema=MovieScript,
    )

    json_mode_agent.print_response("纽约")


if __name__ == "__main__":
    run_structured_output_agent()
