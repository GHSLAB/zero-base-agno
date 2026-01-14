import os
import warnings
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.litellm import LiteLLM
from agno.tools.yfinance import YFinanceTools

# 忽略 Pydantic 序列化警告，这些警告通常是由 LiteLLM 和 Agno 之间的响应格式微小差异引起的
warnings.filterwarnings(
    "ignore", category=UserWarning, message="Pydantic serializer warnings"
)

load_dotenv()

# 代理设置
proxy = "http://127.0.0.1:18081"
os.environ["HTTP_PROXY"] = proxy
os.environ["HTTPS_PROXY"] = proxy

# get_current_stock_price,         # 获取当前股票价格
# get_company_info,                # 获取公司信息
# get_stock_fundamentals,          # 获取股票基本面数据
# get_income_statements,           # 获取损益表
# get_key_financial_ratios,        # 获取关键财务比率
# get_analyst_recommendations,      # 获取分析师建议
# get_company_news,                 # 获取公司新闻
# get_technical_indicators,         # 获取技术指标
# get_historical_stock_prices,      # 获取历史股票价格


def run_tool_use_agent():
    """
    运行一个具备工具调用能力的智能体，使用火山引擎模型和 YFinance 工具。
    该函数展示了智能体如何根据用户查询自动决定调用外部工具（如获取股票价格）。
    """
    # 初始化具备 YFinance 工具的智能体
    volcengine_agent = Agent(
        model=LiteLLM(
            id="volcengine/doubao-1-5-pro-32k-250115",
        ),
        markdown=True,
        tools=[YFinanceTools(),],
        instructions=[
            "你是一个专业的金融分析助手。",
            "如果工具调用返回 'Too Many Requests' 或其他错误，请诚实地告诉用户 API 受到限制，并建议稍后再试。",
            "尽可能以简洁、清晰的表格或列表形式展示数据。",
        ],
    )

    # 提出一个可能触发工具使用的问题
    volcengine_agent.print_response("帮我生成一份微软近期投资报告，需要包含当前股票价格，股票基本面数据，损益表，关键财务比率，分析师建议，公司新闻，技术指标，历史股票价格。",stream=True)


if __name__ == "__main__":
    run_tool_use_agent()
