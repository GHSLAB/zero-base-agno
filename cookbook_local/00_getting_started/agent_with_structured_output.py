"""
Agent with Structured Output - Finance Agent with Typed Responses | 带有结构化输出的代理 - 带有类型响应的财经代理
==================================================================
This example shows how to get structured, typed responses from your agent. | 本示例展示了如何从代理获取结构化、有类型的响应。
Instead of free-form text, you get a Pydantic model you can trust. | 你将获得一个可以信任的 Pydantic 模型，而不是自由格式的文本。

Perfect for building pipelines, UIs, or integrations where you need | 非常适合构建管道、UI 或集成，在这些场景中你需要
predictable data shapes. Parse it, store it, display it — no regex required. | 可预测的数据形状。解析、存储、显示它 — 无需正则表达式。

Key concepts: | 核心概念：
- output_schema: A Pydantic model defining the response structure | output_schema：定义响应结构的 Pydantic 模型
- The agent's response will always match this schema | 代理的响应将始终符合此架构
- Access structured data via response.content | 通过 response.content 访问结构化数据

Example prompts to try: | 尝试示例提示：
- "Analyze NVDA" | “分析 NVDA”
- "Give me a report on Tesla" | “给我一份关于特斯拉的报告”
- "What's the investment case for Apple?" | “苹果的投资案例是什么？”
"""

from typing import List, Optional

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
# Structured Output Schema | 结构化输出架构
# ============================================================================
class StockAnalysis(BaseModel):
    """Structured output for stock analysis. | 股票分析的结构化输出。"""

    ticker: str = Field(..., description="Stock ticker symbol (e.g., NVDA) | 股票代码（例如 NVDA）")
    company_name: str = Field(..., description="Full company name | 公司全称")
    current_price: float = Field(..., description="Current stock price in USD | 当前股价（美元）")
    market_cap: str = Field(..., description="Market cap (e.g., '3.2T' or '150B') | 市值（例如 '3.2T' 或 '150B'）")
    pe_ratio: Optional[float] = Field(None, description="P/E ratio, if available | 市盈率（如果有）")
    week_52_high: float = Field(..., description="52-week high price | 52 周最高价")
    week_52_low: float = Field(..., description="52-week low price | 52 周最低价")
    summary: str = Field(..., description="One-line summary of the stock | 股票的一句话总结")
    key_drivers: List[str] = Field(..., description="2-3 key growth drivers | 2-3 个关键增长驱动因素")
    key_risks: List[str] = Field(..., description="2-3 key risks | 2-3 个关键风险")
    recommendation: str = Field(
        ..., description="One of: Strong Buy, Buy, Hold, Sell, Strong Sell | 以下之一：强烈买入、买入、持有、卖出、强烈卖出"
    )


# ============================================================================
# Agent Instructions | 代理指令
# ============================================================================
instructions = """\
You are a Finance Agent — a data-driven analyst who retrieves market data,
computes key ratios, and produces concise, decision-ready insights.

## Workflow

1. Retrieve
   - Fetch: price, change %, market cap, P/E, EPS, 52-week range
   - Get all required fields for the analysis

2. Analyze
   - Identify 2-3 key drivers (what's working)
   - Identify 2-3 key risks (what could go wrong)
   - Facts only, no speculation

3. Recommend
   - Based on the data, provide a clear recommendation
   - Be decisive but note this is not personalized advice

## Rules

- Source: Yahoo Finance
- Missing data? Use null for optional fields, estimate for required
- Recommendation must be one of: Strong Buy, Buy, Hold, Sell, Strong Sell\
"""

# ============================================================================
# Create the Agent | 创建代理
# ============================================================================
agent_with_structured_output = Agent(
    name="Agent with Structured Output",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[YFinanceTools()],
    output_schema=StockAnalysis,
    db=agent_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ============================================================================
# Run the Agent | 运行代理
# ============================================================================
if __name__ == "__main__":
    # Get structured output | 获取结构化输出
    response = agent_with_structured_output.run("Analyze NVIDIA")

    # Access the typed data | 访问有类型的数据
    analysis: StockAnalysis = response.content

    # Use it programmatically | 以编程方式使用它
    print(f"\n{'=' * 60}")
    print(f"Stock Analysis: {analysis.company_name} ({analysis.ticker})")
    print(f"{'=' * 60}")
    print(f"Price: ${analysis.current_price:.2f}")
    print(f"Market Cap: {analysis.market_cap}")
    print(f"P/E Ratio: {analysis.pe_ratio or 'N/A'}")
    print(f"52-Week Range: ${analysis.week_52_low:.2f} - ${analysis.week_52_high:.2f}")
    print(f"\nSummary: {analysis.summary}")
    print("\nKey Drivers:")
    for driver in analysis.key_drivers:
        print(f"  • {driver}")
    print("\nKey Risks:")
    for risk in analysis.key_risks:
        print(f"  • {risk}")
    print(f"\nRecommendation: {analysis.recommendation}")
    print(f"{'=' * 60}\n")

# ============================================================================
# More Examples | 更多示例
# ============================================================================
"""
Structured output is perfect for: | 结构化输出非常适合：

1. Building UIs | 构建 UI
   analysis = agent.run("Analyze TSLA").content
   render_stock_card(analysis)

2. Storing in databases | 存储到数据库
   db.insert("analyses", analysis.model_dump())

3. Comparing stocks | 比较股票
   nvda = agent.run("Analyze NVDA").content
   amd = agent.run("Analyze AMD").content
   if nvda.pe_ratio < amd.pe_ratio:
       print(f"{nvda.ticker} is cheaper by P/E")

4. Building pipelines | 构建管道
   tickers = ["AAPL", "GOOGL", "MSFT"]
   analyses = [agent.run(f"Analyze {t}").content for t in tickers]

The schema guarantees you always get the fields you expect. | 该架构保证你始终获得预期的字段。
No parsing, no surprises. | 无需解析，没有意外。
"""
