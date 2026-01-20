"""
Agent with Tools - Finance Agent | 带有工具的代理 - 财经代理
=================================
Your first Agno agent: a data-driven financial analyst that retrieves | 你的第一个 Agno 代理：一个数据驱动的财务分析师，负责获取
market data, computes key metrics, and delivers concise insights. | 市场数据、计算关键指标并提供简明见解。

This example shows how to give an agent tools to interact with external | 本示例展示了如何为代理提供与外部数据源交互的工具。
data sources. The agent uses YFinanceTools to fetch real-time market data. | 该代理使用 YFinanceTools 获取实时市场数据。

Example prompts to try: | 尝试示例提示：
- "What's the current price of AAPL?" | “AAPL 的当前价格是多少？”
- "Compare NVDA and AMD — which looks stronger?" | “比较 NVDA 和 AMD — 哪一个看起来更强？”
- "Give me a quick investment brief on Microsoft" | “给我一份关于微软的快速投资简报”
- "What's Tesla's P/E ratio and how does it compare to the industry?" | “特斯拉的市盈率是多少，与行业相比如何？”
- "Show me the key metrics for the FAANG stocks" | “向我展示 FAANG 股票的关键指标”
"""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

# ============================================================================
# Agent Instructions | 代理指令
# ============================================================================
instructions = """\
You are a Finance Agent — a data-driven analyst who retrieves market data,
computes key ratios, and produces concise, decision-ready insights.

## Workflow

1. Clarify
   - Identify tickers from company names (e.g., Apple → AAPL)
   - If ambiguous, ask

2. Retrieve
   - Fetch: price, change %, market cap, P/E, EPS, 52-week range
   - For comparisons, pull the same fields for each ticker

3. Analyze
   - Compute ratios (P/E, P/S, margins) when not already provided
   - Key drivers and risks — 2-3 bullets max
   - Facts only, no speculation

4. Present
   - Lead with a one-line summary
   - Use tables for multi-stock comparisons
   - Keep it tight

## Rules

- Source: Yahoo Finance. Always note the timestamp.
- Missing data? Say "N/A" and move on.
- No personalized advice — add disclaimer when relevant.
- No emojis.\
"""

# ============================================================================
# Create the Agent | 创建代理
# ============================================================================
agent_with_tools = Agent(
    name="Agent with Tools",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[YFinanceTools()],
    add_datetime_to_context=True,
    markdown=True,
)

# ============================================================================
# Run the Agent | 运行代理
# ============================================================================
if __name__ == "__main__":
    agent_with_tools.print_response(
        "Give me a quick investment brief on NVIDIA", stream=True
    )

# ============================================================================
# More Examples | 更多示例
# ============================================================================
"""
Try these prompts: | 尝试这些提示：

1. Single Stock Analysis | 单只股票分析
   "What's Apple's current valuation? Is it expensive?"

2. Comparison | 比较
   "Compare Google and Microsoft as investments"

3. Sector Overview | 行业概览
   "Show me key metrics for the top AI stocks: NVDA, AMD, GOOGL, MSFT"

4. Quick Check | 快速检查
   "What's Tesla trading at today?"

5. Deep Dive | 深入研究
   "Break down Amazon's financials — revenue, margins, and growth"
"""
