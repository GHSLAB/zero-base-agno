"""
Custom Tool for Self-Learning - Write Your Own Tools | 用于自我学习的自定义工具 - 编写您自己的工具
=====================================================
This example shows how to write custom tools for your agent. | 此示例展示了如何为您的 Agent 编写自定义工具。
A tool is just a Python function — the agent calls it when needed. | 工具就是一个 Python 函数 —— Agent 在需要时调用它。

We'll build a self-learning agent that can save insights to a knowledge base. | 我们将构建一个能够将见解保存到知识库的自我学习 Agent。
The key concept: any function can become a tool. | 核心概念：任何函数都可以成为一个工具。

Key concepts: | 核心概念：
- Tools are Python functions with docstrings (the docstring tells the agent what the tool does) | 工具是带有文档字符串的 Python 函数（文档字符串告诉 Agent 工具的作用）
- The agent decides when to call your tool based on the conversation | Agent 根据对话内容决定何时调用您的工具
- Return a string to communicate results back to the agent | 返回一个字符串以将结果传回给 Agent

Example prompts to try: | 可尝试的示例提示词：
- "What's a good P/E ratio for tech stocks? Save that insight."
- "Remember that NVDA's data center revenue is the key growth driver"
- "What learnings do we have saved?"
"""

import json
from datetime import datetime, timezone

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge import Knowledge
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.reader.text_reader import TextReader
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType

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
        hybrid_rrf_k=60,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
    max_results=5,
    contents_db=agent_db,
)


# ============================================================================
# Custom Tool: Save Learning | 自定义工具：保存学习心得
# ============================================================================
def save_learning(title: str, learning: str) -> str:
    """
    Save a reusable insight to the knowledge base for future reference. | 将可重复使用的见解保存到知识库中以供将来参考。

    Args:
        title: Short descriptive title (e.g., "Tech stock P/E benchmarks") | 简短的描述性标题（例如：“科技股 P/E 基准”）
        learning: The insight to save — be specific and actionable | 要保存的见解 —— 需具体且具有可操作性

    Returns:
        Confirmation message | 确认信息
    """
    # Validate inputs | 验证输入
    if not title or not title.strip():
        return "Cannot save: title is required"
    if not learning or not learning.strip():
        return "Cannot save: learning content is required"

    # Build the payload | 构建负载
    payload = {
        "title": title.strip(),
        "learning": learning.strip(),
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }

    # Save to knowledge base | 保存到知识库
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

3. Propose Learnings | 提出学习建议
   - After answering, consider: is there a reusable insight here? | 回答后，考虑：这里是否有可重复使用的见解？
   - If yes, propose it in this format: | 如果是，请按此格式提出：

---
**Proposed Learning**

Title: [concise title]
Learning: [the insight — specific and actionable]

Save this? (yes/no)
---

- Only call save_learning AFTER the user says "yes" | 仅在用户说 "yes" 之后调用 save_learning
- If user says "no", acknowledge and move on | 如果用户说 "no"，确认并继续

## What Makes a Good Learning | 什么是好的学习心得

- Specific: "Tech P/E ratios typically range 20-35x" not "P/E varies" | 具体：“科技股 P/E 比率通常在 20-35 倍之间”，而不是“P/E 各不相同”
- Actionable: Can be applied to future questions | 可操作：可以应用于未来的问题
- Reusable: Useful beyond this one conversation | 可重复使用：在本次对话之外也有用

Don't save: Raw data, one-off facts, or obvious information. | 不要保存：原始数据、一次性事实或显而易见的信息。\
"""

# ============================================================================
# Create the Agent | 创建 Agent
# ============================================================================
self_learning_agent = Agent(
    name="Self-Learning Agent",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[
        YFinanceTools(),
        save_learning,  # Our custom tool — just a Python function! | 我们的自定义工具 —— 只是一个 Python 函数！
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
    # Ask a question that might produce a learning | 提出一个可能产生学习心得的问题
    self_learning_agent.print_response(
        "What's a healthy P/E ratio for tech stocks?",
        stream=True,
    )

    # If the agent proposed a learning, approve it | 如果 Agent 提出了学习建议，批准它
    self_learning_agent.print_response(
        "yes",
        stream=True,
    )

    # Later, the agent can recall the learning | 稍后，Agent 可以回想起该学习心得
    self_learning_agent.print_response(
        "What learnings do we have saved?",
        stream=True,
    )

# ============================================================================
# More Examples | 更多示例
# ============================================================================
"""
Writing custom tools: | 编写自定义工具：

1. Define a function with type hints and a docstring | 定义一个带有类型提示和文档字符串的函数
   def my_tool(param: str) -> str:
       '''Description of what this tool does. | 此工具作用的描述。

       Args:
           param: What this parameter is for | 此参数的用途

       Returns:
           What the tool returns | 工具返回的内容
       '''
       # Your logic here
       return "Result"

2. Add it to the agent's tools list | 将其添加到 Agent 的工具列表中
   agent = Agent(
       tools=[my_tool],
       ...
   )

The docstring is critical — it tells the agent: | 文档字符串至关重要 —— 它告诉 Agent：
- What the tool does | 工具的作用
- What parameters it needs | 它需要什么参数
- What it returns | 它返回什么

The agent uses this to decide when and how to call your tool. | Agent 使用它来决定何时以及如何调用您的工具。
"""
