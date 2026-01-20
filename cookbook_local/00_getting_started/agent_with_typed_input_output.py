"""
Agent with Typed Input and Output - Full Type Safety | 具有类型化输入和输出的 Agent - 全程类型安全
=====================================================
This example shows how to define both input and output schemas for your agent. | 此示例展示了如何为您的 Agent 定义输入和输出架构。
You get end-to-end type safety: validate what goes in, guarantee what comes out. | 您可以获得端到端的类型安全：验证输入内容，保证输出结构。

Perfect for building robust pipelines where you need contracts on both ends. | 非常适合构建在两端都需要契约的健壮流水线。
The agent validates inputs and guarantees output structure. | Agent 验证输入并保证输出结构。

Key concepts: | 核心概念：
- input_schema: A Pydantic model defining what the agent accepts | input_schema：定义 Agent 接受内容的 Pydantic 模型
- output_schema: A Pydantic model defining what the agent returns | output_schema：定义 Agent 返回内容的 Pydantic 模型
- Pass input as a dict or Pydantic model — both work | 以字典或 Pydantic 模型形式传递输入 —— 两者均可

Example inputs to try: | 可尝试的示例输入：
- {"ticker": "NVDA", "analysis_type": "quick", "include_risks": True}
- {"ticker": "TSLA", "analysis_type": "deep", "include_risks": True}
"""

from typing import List, Literal, Optional

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from pydantic import BaseModel, Field

# ============================================================================
# Storage Configuration | 存储配置
# ============================================================================
agent_db = SqliteDb(db_file="tmp/agents.db")


# ============================================================================
# Input Schema — what the agent accepts | 输入架构 —— Agent 接受的内容
# ============================================================================
class AnalysisRequest(BaseModel):
    """Structured input for requesting a stock analysis. | 用于请求股票分析的结构化输入。"""

    ticker: str = Field(..., description="Stock ticker symbol (e.g., NVDA, AAPL) | 股票代码（例如：NVDA, AAPL）")
    analysis_type: Literal["quick", "deep"] = Field(
        default="quick",
        description="quick = summary only, deep = full analysis with drivers/risks | quick = 仅摘要，deep = 包含驱动因素/风险的全面分析",
    )
    include_risks: bool = Field(
        default=True, description="Whether to include risk analysis | 是否包含风险分析"
    )


# ============================================================================
# Output Schema — what the agent returns | 输出架构 —— Agent 返回的内容
# ============================================================================
class StockAnalysis(BaseModel):
    """Structured output for stock analysis. | 股票分析的结构化输出。"""

    ticker: str = Field(..., description="Stock ticker symbol | 股票代码")
    company_name: str = Field(..., description="Full company name | 公司全称")
    current_price: float = Field(..., description="Current stock price in USD | 当前股价（美元）")
    summary: str = Field(..., description="One-line summary of the stock | 股票的一句话摘要")
    key_drivers: Optional[List[str]] = Field(
        None, description="Key growth drivers (if deep analysis) | 关键增长驱动因素（如果是深度分析）"
    )
    key_risks: Optional[List[str]] = Field(
        None, description="Key risks (if include_risks=True) | 关键风险（如果 include_risks=True）"
    )
    recommendation: str = Field(
        ..., description="One of: Strong Buy, Buy, Hold, Sell, Strong Sell | 建议之一：强烈买入、买入、持有、卖出、强烈卖出"
    )


# ============================================================================
# Agent Instructions | Agent 指令
# ============================================================================
instructions = """\
You are a Finance Agent that produces structured stock analyses. | 您是一个生成结构化股票分析的财务 Agent。

## Input Parameters | 输入参数

You receive structured requests with: | 您收到的结构化请求包含：
- ticker: The stock to analyze | ticker：要分析的股票
- analysis_type: "quick" (summary only) or "deep" (full analysis) | analysis_type："quick"（仅摘要）或 "deep"（全面分析）
- include_risks: Whether to include risk analysis | include_risks：是否包含风险分析

## Workflow | 工作流

1. Fetch data for the requested ticker | 获取所请求股票代码的数据
2. If analysis_type is "deep", identify key drivers | 如果 analysis_type 是 "deep"，识别关键驱动因素
3. If include_risks is True, identify key risks | 如果 include_risks 为 True，识别关键风险
4. Provide a clear recommendation | 提供明确的建议

## Rules | 规则

- Source: Yahoo Finance | 数据源：雅虎财经
- Match output to input parameters — don't include drivers for "quick" analysis | 使输出与输入参数匹配 —— 对于 "quick" 分析，不要包含驱动因素
- Recommendation must be one of: Strong Buy, Buy, Hold, Sell, Strong Sell | 建议必须是以下之一：强烈买入、买入、持有、卖出、强烈卖出\
"""

# ============================================================================
# Create the Agent | 创建 Agent
# ============================================================================
agent_with_typed_input_output = Agent(
    name="Agent with Typed Input Output",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[YFinanceTools()],
    input_schema=AnalysisRequest,
    output_schema=StockAnalysis,
    db=agent_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ============================================================================
# Run the Agent | 运行 Agent
# ============================================================================
if __name__ == "__main__":
    # Option 1: Pass input as a dict | 选项 1：以字典形式传递输入
    response_1 = agent_with_typed_input_output.run(
        input={
            "ticker": "NVDA",
            "analysis_type": "deep",
            "include_risks": True,
        }
    )

    # Access the typed output | 访问类型化输出
    analysis_1: StockAnalysis = response_1.content

    print(f"\n{'=' * 60}")
    print(f"Stock Analysis: {analysis_1.company_name} ({analysis_1.ticker})")
    print(f"{'=' * 60}")
    print(f"Price: ${analysis_1.current_price:.2f}")
    print(f"Summary: {analysis_1.summary}")
    if analysis_1.key_drivers:
        print("\nKey Drivers:")
        for driver in analysis_1.key_drivers:
            print(f"  • {driver}")
    if analysis_1.key_risks:
        print("\nKey Risks:")
        for risk in analysis_1.key_risks:
            print(f"  • {risk}")
    print(f"\nRecommendation: {analysis_1.recommendation}")
    print(f"{'=' * 60}\n")

    # Option 2: Pass input as a Pydantic model | 选项 2：以 Pydantic 模型形式传递输入
    request = AnalysisRequest(
        ticker="AAPL",
        analysis_type="quick",
        include_risks=False,
    )
    response_2 = agent_with_typed_input_output.run(input=request)

    # Access the typed output | 访问类型化输出
    analysis_2: StockAnalysis = response_2.content

    print(f"\n{'=' * 60}")
    print(f"Stock Analysis: {analysis_2.company_name} ({analysis_2.ticker})")
    print(f"{'=' * 60}")
    print(f"Price: ${analysis_2.current_price:.2f}")
    print(f"Summary: {analysis_2.summary}")
    if analysis_2.key_drivers:
        print("\nKey Drivers:")
        for driver in analysis_2.key_drivers:
            print(f"  • {driver}")
    if analysis_2.key_risks:
        print("\nKey Risks:")
        for risk in analysis_2.key_risks:
            print(f"  • {risk}")
    print(f"\nRecommendation: {analysis_2.recommendation}")
    print(f"{'=' * 60}\n")

# ============================================================================
# More Examples | 更多示例
# ============================================================================
"""
Typed input + output is perfect for: | 类型化输入 + 输出非常适合：

1. API endpoints | API 端点
   @app.post("/analyze")
   def analyze(request: AnalysisRequest) -> StockAnalysis:
       return agent.run(input=request).content

2. Batch processing | 批量处理
   requests = [
       AnalysisRequest(ticker="NVDA", analysis_type="quick"),
       AnalysisRequest(ticker="AMD", analysis_type="quick"),
       AnalysisRequest(ticker="INTC", analysis_type="quick"),
   ]
   results = [agent.run(input=r).content for r in requests]

3. Pipeline composition | 流水线组合
   # Agent 1 outputs what Agent 2 expects as input | Agent 1 的输出正是 Agent 2 期望的输入
   screening_result = screener_agent.run(input=criteria).content
   analysis_result = analysis_agent.run(input=screening_result).content

Type safety on both ends = fewer bugs, better tooling, clearer contracts. | 两端的类型安全 = 更少的错误、更好的工具支持、更清晰的契约。
"""
