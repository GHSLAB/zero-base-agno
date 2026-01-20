"""
Agent with Memory - Finance Agent that Remembers You | 带有记忆的代理 - 记得你的财经代理
=====================================================
This example shows how to give your agent memory of user preferences. | 本示例展示了如何让代理记住用户偏好。
The agent remembers facts about you across all conversations. | 代理会在所有对话中记住关于你的事实。

Different from storage (which persists conversation history), memory | 与存储（持久化对话历史）不同，记忆
persists user-level information: preferences, facts, context. | 持久化用户级信息：偏好、事实、上下文。

Key concepts: | 核心概念：
- MemoryManager: Extracts and stores user memories from conversations | MemoryManager：从对话中提取并存储用户记忆
- enable_agentic_memory: Agent decides when to store/recall via tool calls (efficient) | enable_agentic_memory：代理决定何时通过工具调用存储/召回（高效）
- enable_user_memories: Memory manager runs after every response (guaranteed capture) | enable_user_memories：记忆管理器在每次响应后运行（确保捕获）
- user_id: Links memories to a specific user | user_id：将记忆链接到特定用户

Example prompts to try: | 尝试示例提示：
- "I'm interested in tech stocks, especially AI companies" | “我对科技股感兴趣，尤其是 AI 公司”
- "My risk tolerance is moderate" | “我的风险承受能力是中等的”
- "What stocks would you recommend for me?" | “你会给我推荐哪些股票？”
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from rich.pretty import pprint

# ============================================================================
# Storage Configuration | 存储配置
# ============================================================================
agent_db = SqliteDb(db_file="tmp/agents.db")

# ============================================================================
# Memory Manager Configuration | 记忆管理器配置
# ============================================================================
memory_manager = MemoryManager(
    model=Gemini(id="gemini-3-flash-preview"),
    db=agent_db,
    additional_instructions="""
    Capture the user's favorite stocks, their risk tolerance, and their investment goals.
    """,
)

# ============================================================================
# Agent Instructions | 代理指令
# ============================================================================
instructions = """\
You are a Finance Agent — a data-driven analyst who retrieves market data,
computes key ratios, and produces concise, decision-ready insights.

## Memory

You have memory of user preferences (automatically provided in context). Use this to:
- Tailor recommendations to their interests
- Consider their risk tolerance
- Reference their investment goals

## Workflow

1. Retrieve
   - Fetch: price, change %, market cap, P/E, EPS, 52-week range
   - For comparisons, pull the same fields for each ticker

2. Analyze
   - Compute ratios (P/E, P/S, margins) when not already provided
   - Key drivers and risks — 2-3 bullets max
   - Facts only, no speculation

3. Present
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
user_id = "investor@example.com"

agent_with_memory = Agent(
    name="Agent with Memory",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[YFinanceTools()],
    db=agent_db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ============================================================================
# Run the Agent | 运行代理
# ============================================================================
if __name__ == "__main__":
    # Tell the agent about yourself | 告诉代理关于你自己的信息
    agent_with_memory.print_response(
        "I'm interested in AI and semiconductor stocks. My risk tolerance is moderate.",
        user_id=user_id,
        stream=True,
    )

    # The agent now knows your preferences | 代理现在知道你的偏好了
    agent_with_memory.print_response(
        "What stocks would you recommend for me?",
        user_id=user_id,
        stream=True,
    )

    # View stored memories | 查看存储的记忆
    memories = agent_with_memory.get_user_memories(user_id=user_id)
    print("\n" + "=" * 60)
    print("Stored Memories:")
    print("=" * 60)
    pprint(memories)

# ============================================================================
# More Examples | 更多示例
# ============================================================================
"""
Memory vs Storage: | 记忆 vs 存储：

- Storage: "What did we discuss?" (conversation history) | 存储：“我们讨论了什么？”（对话历史）
- Memory: "What do you know about me?" (user preferences) | 记忆：“你对我了解多少？”（用户偏好）

Memory persists across sessions: | 记忆在不同会话间持久存在：

1. Run this script — agent learns your preferences | 1. 运行此脚本 — 代理学习你的偏好
2. Start a NEW session with the same user_id | 2. 使用相同的 user_id 启动新会话
3. Agent still remembers you like AI stocks | 3. 代理仍然记得你喜欢 AI 股票

Useful for: | 适用于：
- Personalized recommendations | 个性化推荐
- Remembering user context (job, goals, constraints) | 记住用户上下文（工作、目标、约束）
- Building rapport across conversations | 在对话中建立良好关系

Two ways to enable memory: | 启用记忆的两种方式：

1. enable_agentic_memory=True (used in this example) | 1. enable_agentic_memory=True（本示例中使用）
   - Agent decides when to store/recall via tool calls | - 代理决定何时通过工具调用存储/召回
   - More efficient — only runs when needed | - 更高效 — 仅在需要时运行

2. enable_user_memories=True | 2. enable_user_memories=True
   - Memory manager runs after every agent response | - 记忆管理器在代理每次响应后运行
   - Guaranteed capture — never misses user info | - 确保捕获 — 绝不会错过用户信息
   - Higher latency and cost | - 延迟和成本更高
"""
