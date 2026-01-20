"""
Agent with State Management - Finance Agent with Watchlist | 带有状态管理的代理 - 带有自选股列表的财经代理
===========================================================
This example shows how to give your agent persistent state that it can | 本示例展示了如何为代理提供可读写的持久状态。
read and modify. The agent maintains a stock watchlist across conversations. | 代理会在对话中维护一个股票自选列表。

Different from storage (conversation history) and memory (user preferences), | 与存储（对话历史）和记忆（用户偏好）不同，
state is structured data the agent actively manages: counters, lists, flags. | 状态是代理主动管理的结构化数据：计数器、列表、标志位。

Key concepts: | 核心概念：
- session_state: A dict that persists across runs | session_state：跨运行持久化的字典
- Tools can read/write state via run_context.session_state | 工具可以通过 run_context.session_state 读写状态
- State variables can be injected into instructions with {variable_name} | 状态变量可以通过 {variable_name} 注入到指令中

Example prompts to try: | 尝试示例提示：
- "Add NVDA and AMD to my watchlist" | “将 NVDA 和 AMD 添加到我的自选股”
- "What's on my watchlist?" | “我的自选股列表里有什么？”
- "Remove AMD from the list" | “从列表中移除 AMD”
- "How are my watched stocks doing today?" | “我自选的股票今天表现如何？”
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.run import RunContext
from agno.tools.yfinance import YFinanceTools

# ============================================================================
# Storage Configuration | 存储配置
# ============================================================================
agent_db = SqliteDb(db_file="tmp/agents.db")


# ============================================================================
# Custom Tools that Modify State | 修改状态的自定义工具
# ============================================================================
def add_to_watchlist(run_context: RunContext, ticker: str) -> str:
    """
    Add a stock ticker to the watchlist. | 将股票代码添加到自选股列表。

    Args:
        ticker: Stock ticker symbol (e.g., NVDA, AAPL) | 股票代码（例如 NVDA, AAPL）

    Returns:
        Confirmation message | 确认消息
    """
    ticker = ticker.upper().strip()
    watchlist = run_context.session_state.get("watchlist", [])

    if ticker in watchlist:
        return f"{ticker} is already on your watchlist"

    watchlist.append(ticker)
    run_context.session_state["watchlist"] = watchlist

    return f"Added {ticker} to watchlist. Current watchlist: {', '.join(watchlist)}"


def remove_from_watchlist(run_context: RunContext, ticker: str) -> str:
    """
    Remove a stock ticker from the watchlist. | 从自选股列表中移除股票代码。

    Args:
        ticker: Stock ticker symbol to remove | 要移除的股票代码

    Returns:
        Confirmation message | 确认消息
    """
    ticker = ticker.upper().strip()
    watchlist = run_context.session_state.get("watchlist", [])

    if ticker not in watchlist:
        return f"{ticker} is not on your watchlist"

    watchlist.remove(ticker)
    run_context.session_state["watchlist"] = watchlist

    if watchlist:
        return f"Removed {ticker}. Remaining watchlist: {', '.join(watchlist)}"
    return f"Removed {ticker}. Watchlist is now empty."


# ============================================================================
# Agent Instructions | 代理指令
# ============================================================================
instructions = """\
You are a Finance Agent that manages a stock watchlist.

## Current Watchlist
{watchlist}

## Capabilities

1. Manage watchlist
   - Add stocks: use add_to_watchlist tool
   - Remove stocks: use remove_from_watchlist tool

2. Get stock data
   - Use YFinance tools to fetch prices and metrics for watched stocks
   - Compare stocks on the watchlist

## Rules

- Always confirm watchlist changes
- When asked about "my stocks" or "watchlist", refer to the current state
- Fetch fresh data when reporting on watchlist performance\
"""

# ============================================================================
# Create the Agent | 创建代理
# ============================================================================
agent_with_state_management = Agent(
    name="Agent with State Management",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[
        add_to_watchlist,
        remove_from_watchlist,
        YFinanceTools(),
    ],
    session_state={"watchlist": []},
    add_session_state_to_context=True,
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
    # Add some stocks | 添加一些股票
    agent_with_state_management.print_response(
        "Add NVDA, AAPL, and GOOGL to my watchlist",
        stream=True,
    )

    # Check the watchlist | 检查自选股
    agent_with_state_management.print_response(
        "How are my watched stocks doing today?",
        stream=True,
    )

    # View the state directly | 直接查看状态
    print("\n" + "=" * 60)
    print("Session State:")
    print(
        f"  Watchlist: {agent_with_state_management.get_session_state().get('watchlist', [])}"
    )
    print("=" * 60)

# ============================================================================
# More Examples | 更多示例
# ============================================================================
"""
State vs Storage vs Memory: | 状态 vs 存储 vs 记忆：

- State: Structured data the agent manages (watchlist, counters, flags) | 状态：代理管理的结构化数据（自选股、计数器、标志位）
- Storage: Conversation history ("what did we discuss?") | 存储：对话历史（“我们讨论了什么？”）
- Memory: User preferences ("what do I like?") | 记忆：用户偏好（“我喜欢什么？”）

State is perfect for: | 状态非常适合：
- Tracking items (watchlists, todos, carts) | 跟踪项目（自选股、待办事项、购物车）
- Counters and progress | 计数器和进度
- Multi-step workflows | 多步工作流
- Any structured data that changes during conversation | 对话过程中变化的任何结构化数据

Accessing state: | 访问状态：

1. In tools: run_context.session_state["key"] | 1. 在工具中：run_context.session_state["key"]
2. In instructions: {key} (with add_session_state_to_context=True) | 2. 在指令中：{key}（需设置 add_session_state_to_context=True）
3. After run: agent.get_session_state() or response.session_state | 3. 运行后：agent.get_session_state() 或 response.session_state
"""
