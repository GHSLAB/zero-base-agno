"""
Agent with Storage - Finance Agent with Storage | 带有存储的代理 - 带有存储功能的财经代理
====================================================
Building on the Finance Agent from 01, this example adds persistent storage. | 在 01 财经代理的基础上，本示例添加了持久化存储。
Your agent now remembers conversations across runs. | 你的代理现在可以跨运行记住对话内容。

Ask about NVDA, close the script, come back later — pick up where you left off. | 询问关于 NVDA 的信息，关闭脚本，稍后再回来 — 从你离开的地方继续。
The conversation history is saved to SQLite and restored automatically. | 对话历史记录保存在 SQLite 中并自动恢复。

Key concepts: | 核心概念：
- Run: Each time you run the agent (via agent.print_response() or agent.run()) | 运行 (Run)：每次你运行代理（通过 agent.print_response() 或 agent.run()）
- Session: A conversation thread, identified by session_id | 会话 (Session)：一个对话线程，由 session_id 标识
- Same session_id = continuous conversation, even across runs | 相同的 session_id = 连续对话，即使跨运行也是如此

Example prompts to try: | 尝试示例提示：
- "What's the current price of AAPL?" | “AAPL 的当前价格是多少？”
- "Compare that to Microsoft" (it remembers AAPL) | “将其与微软进行比较”（它记得 AAPL）
- "Based on our discussion, which looks better?" | “根据我们的讨论，哪一个看起来更好？”
- "What stocks have we analyzed so far?" | “到目前为止我们分析了哪些股票？”
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

# ============================================================================
# Storage Configuration | 存储配置
# ============================================================================
agent_db = SqliteDb(db_file="tmp/agents.db")

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
- No emojis.
- Reference previous analyses when relevant.\
"""

# ============================================================================
# Create the Agent | 创建代理
# ============================================================================
agent_with_storage = Agent(
    name="Agent with Storage",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[YFinanceTools()],
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
    # Use a consistent session_id to persist conversation across runs | 使用一致的 session_id 以在不同运行间持久化对话
    # Note: session_id is auto-generated if not set | 注意：如果未设置，session_id 将自动生成
    session_id = "finance-agent-session"

    # Turn 1: Analyze a stock | 第 1 轮：分析一只股票
    agent_with_storage.print_response(
        "Give me a quick investment brief on NVIDIA",
        session_id=session_id,
        stream=True,
    )

    # Turn 2: Compare — the agent remembers NVDA from turn 1 | 第 2 轮：比较 — 代理记得第 1 轮中的 NVDA
    agent_with_storage.print_response(
        "Compare that to Tesla",
        session_id=session_id,
        stream=True,
    )

    # Turn 3: Ask for a recommendation based on the full conversation | 第 3 轮：根据整个对话请求建议
    agent_with_storage.print_response(
        "Based on our discussion, which looks like the better investment?",
        session_id=session_id,
        stream=True,
    )

# ============================================================================
# More Examples | 更多示例
# ============================================================================
"""
Try this flow: | 尝试这个流程：

1. Run the script — it analyzes NVDA, compares to TSLA, then recommends | 1. 运行脚本 — 它分析 NVDA，与 TSLA 进行比较，然后给出建议
2. Comment out all three prompts above | 2. 注释掉上面的所有三个提示
3. Add: agent.print_response("What about AMD?", session_id=session_id, stream=True) | 3. 添加：agent.print_response("AMD 怎么样？", session_id=session_id, stream=True)
4. Run again — it remembers the full NVDA vs TSLA conversation | 4. 再次运行 — 它记得完整的 NVDA vs TSLA 对话

The storage layer persists your conversation history to SQLite. | 存储层将你的对话历史持久化到 SQLite。
Restart the script anytime and pick up where you left off. | 随时重启脚本并从你离开的地方继续。
"""
