from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
import warnings
from dotenv import load_dotenv
from agno.models.litellm import LiteLLM


load_dotenv()
warnings.filterwarnings(
    "ignore", category=UserWarning, message="Pydantic serializer warnings"
)


volcengine_agent = Agent(
    model=LiteLLM(
        id="volcengine/doubao-1-5-pro-32k-250115",
    ),
    tools=[DuckDuckGoTools()],
    markdown=True,
)

volcengine_agent.print_response("最近有什么关于伊朗的新闻？", stream=False)
