"""
Human in the Loop - Confirm Before Taking Action | 人机回环 - 操作前确认
================================================
This example shows how to require user confirmation before executing | 此示例展示了如何在执行某些工具之前要求用户确认。
certain tools. Critical for actions that are irreversible or sensitive. | 对于不可逆或敏感的操作至关重要。

We'll build on our self-learning agent, and ask for user confirmation before saving a learning. | 我们将在自我学习 Agent 的基础上，在保存学习心得之前请求用户确认。

Key concepts: | 核心概念：
- @tool(requires_confirmation=True): Mark tools that need approval | @tool(requires_confirmation=True)：标记需要批准的工具
- run_response.active_requirements: Check for pending confirmations | run_response.active_requirements：检查待处理的确认
- requirement.confirm() / requirement.reject(): Approve or deny | requirement.confirm() / requirement.reject()：批准或拒绝
- agent.continue_run(): Resume execution after decision | agent.continue_run()：决策后恢复执行

Some practical applications: | 一些实际应用：
- Confirming sensitive operations before execution | 执行前确认敏感操作
- Reviewing API calls before they're made | 在进行 API 调用前进行审查
- Validating data transformations | 验证数据转换
- Approving automated actions in critical systems | 在关键系统中批准自动化操作

Example prompts to try: | 可尝试的示例提示词：
- "What's a good P/E ratio for tech stocks? Save that insight."
- "Analyze NVDA and save any insights"
- "What learnings do we have saved?"
"""

import json
from datetime import datetime, timezone

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.text_reader import TextReader
from agno.models.google import Gemini
from agno.tools import tool
from agno.tools.yfinance import YFinanceTools
from agno.utils import pprint
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType
from rich.console import Console
from rich.prompt import Prompt

# ============================================================================
# Storage Configuration | 存储配置
# ============================================================================
agent_db = SqliteDb(db_file="tmp/agents.db")

# ============================================================================
# Knowledge Base for Learnings | 学习心得知识库
# ============================================================================
learnings_kb = Knowledge(
    name="Agent Learnings",
    vector_db=ChromaDb(
        name="learnings",
        collection="learnings",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
    max_results=5,
    contents_db=agent_db,
)


# ============================================================================
# Custom Tool: Save Learning (requires confirmation) | 自定义工具：保存学习心得（需要确认）
# ============================================================================
@tool(requires_confirmation=True)
def save_learning(title: str, learning: str) -> str:
    """
    Save a reusable insight to the knowledge base for future reference. | 将可重复使用的见解保存到知识库中以供将来参考。
    This action requires user confirmation before executing. | 此操作在执行前需要用户确认。

    Args:
        title: Short descriptive title (e.g., "Tech stock P/E benchmarks") | 简短的描述性标题（例如：“科技股 P/E 基准”）
        learning: The insight to save — be specific and actionable | 要保存的见解 —— 需具体且具有可操作性

    Returns:
        Confirmation message | 确认信息
    """
    if not title or not title.strip():
        return "Cannot save: title is required"
    if not learning or not learning.strip():
        return "Cannot save: learning content is required"

    payload = {
        "title": title.strip(),
        "learning": learning.strip(),
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }

    learnings_kb.add_content(
        name=payload["title"],
        text_content=json.dumps(payload, ensure_ascii=False),
        reader=TextReader(),
        skip_if_exists=True,
    )

    return f"Saved: '{title}'"


# ============================================================================
# Agent Instructions | Agent 指令
# ============================================================================
instructions = """\
You are a Finance Agent that learns and improves over time. | 您是一个会随着时间推移不断学习和进步的财务 Agent。

You have two special abilities: | 您有两种特殊能力：
1. Search your knowledge base for previously saved learnings | 搜索知识库中以前保存的学习心得
2. Save new insights using the save_learning tool | 使用 save_learning 工具保存新的见解

## Workflow | 工作流

1. Check Knowledge First | 首先检查知识库
   - Before answering, search for relevant prior learnings | 在回答之前，搜索相关的先前学习心得
   - Apply any relevant insights to your response | 将任何相关的见解应用于您的回答

2. Gather Information | 收集信息
   - Use YFinance tools for market data | 使用 YFinance 工具获取市场数据
   - Combine with your knowledge base insights | 与您的知识库见解相结合

3. Save Valuable Insights | 保存有价值的见解
   - If you discover something reusable, save it with save_learning | 如果您发现了一些可重复使用的内容，请使用 save_learning 保存它
   - The user will be asked to confirm before it's saved | 在保存之前，系统会要求用户确认
   - Good learnings are specific, actionable, and generalizable | 好的学习心得应该是具体的、可操作的和可推广的

## What Makes a Good Learning | 什么是好的学习心得

- Specific: "Tech P/E ratios typically range 20-35x" not "P/E varies" | 具体：“科技股 P/E 比率通常在 20-35 倍之间”，而不是“P/E 各不相同”
- Actionable: Can be applied to future questions | 可操作：可以应用于未来的问题
- Reusable: Useful beyond this one conversation | 可重复使用：在本次对话之外也有用

Don't save: Raw data, one-off facts, or obvious information. | 不要保存：原始数据、一次性事实或显而易见的信息。\
"""

# ============================================================================
# Create the Agent | 创建 Agent
# ============================================================================
human_in_the_loop_agent = Agent(
    name="Agent with Human in the Loop",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[
        YFinanceTools(),
        save_learning,
    ],
    knowledge=learnings_kb,
    search_knowledge=True,
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
    console = Console()

    # Ask a question that might trigger a save | 提出一个可能触发保存操作的问题
    run_response = human_in_the_loop_agent.run(
        "What's a healthy P/E ratio for tech stocks? Save that insight."
    )

    # Handle any confirmation requirements | 处理任何确认要求
    for requirement in run_response.active_requirements:
        if requirement.needs_confirmation:
            console.print(
                f"\n[bold yellow]🛑 Confirmation Required | 需要确认[/bold yellow]\n"
                f"Tool | 工具: [bold blue]{requirement.tool_execution.tool_name}[/bold blue]\n"
                f"Args | 参数: {requirement.tool_execution.tool_args}"
            )

            choice = (
                Prompt.ask(
                    "Do you want to continue? | 您想继续吗？",
                    choices=["y", "n"],
                    default="y",
                )
                .strip()
                .lower()
            )

            if choice == "n":
                requirement.reject()
                console.print("[red]❌ Rejected | 已拒绝[/red]")
            else:
                requirement.confirm()
                console.print("[green]✅ Approved | 已批准[/green]")

    # Continue the run with the user's decisions | 根据用户的决定继续运行
    run_response = human_in_the_loop_agent.continue_run(
        run_id=run_response.run_id,
        requirements=run_response.requirements,
    )

    pprint.pprint_run_response(run_response)

# ============================================================================
# More Examples | 更多示例
# ============================================================================
"""
Human-in-the-loop patterns: | 人机回环模式：

1. Confirmation for sensitive actions | 敏感操作确认
   @tool(requires_confirmation=True)
   def delete_file(path: str) -> str:
       ...

2. Confirmation for external calls | 外部调用确认
   @tool(requires_confirmation=True)
   def send_email(to: str, subject: str, body: str) -> str:
       ...

3. Confirmation for financial transactions | 金融交易确认
   @tool(requires_confirmation=True)
   def place_order(ticker: str, quantity: int, side: str) -> str:
       ...

The pattern: | 模式：
1. Mark tool with @tool(requires_confirmation=True) | 使用 @tool(requires_confirmation=True) 标记工具
2. Run agent with agent.run() | 使用 agent.run() 运行 Agent
3. Loop through run_response.active_requirements | 遍历 run_response.active_requirements
4. Check requirement.needs_confirmation | 检查 requirement.needs_confirmation
5. Call requirement.confirm() or requirement.reject() | 调用 requirement.confirm() 或 requirement.reject()
6. Call agent.continue_run() with requirements | 使用 requirements 调用 agent.continue_run()

This gives you full control over which actions execute. | 这让您可以完全控制执行哪些操作。
"""
