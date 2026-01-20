"""
Agentic Search over Knowledge - Agent with a Knowledge Base | 知识库代理搜索 - 带有知识库的代理
============================================================
This example shows how to give an agent a searchable knowledge base. | 本示例展示了如何为代理提供可搜索的知识库。
The agent can search through documents (PDFs, text, URLs) to answer questions. | 代理可以搜索文档（PDF、文本、URL）来回答问题。

Key concepts: | 核心概念：
- Knowledge: A searchable collection of documents (PDFs, text, URLs) | 知识：文档的可搜索集合（PDF、文本、URL）
- Agentic search: The agent decides when to search the knowledge base | 代理搜索：代理决定何时搜索知识库
- Hybrid search: Combines semantic similarity with keyword matching. | 混合搜索：结合语义相似度与关键词匹配。

Example prompts to try: | 尝试示例提示：
- "What is Agno?" | “什么是 Agno？”
- "What is the AgentOS?" | “什么是 AgentOS？”
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.google import Gemini
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType

# ============================================================================
# Storage Configuration | 存储配置
# ============================================================================
agent_db = SqliteDb(db_file="tmp/agents.db")

# ============================================================================
# Knowledge Configuration | 知识库配置
# ============================================================================
knowledge = Knowledge(
    name="Agno Documentation",
    vector_db=ChromaDb(
        name="agno_docs",
        collection="agno_docs",
        path="tmp/chromadb",
        persistent_client=True,
        # Enable hybrid search - combines vector similarity with keyword matching using RRF | 启用混合搜索 - 使用 RRF 结合向量相似度和关键词匹配
        search_type=SearchType.hybrid,
        # RRF (Reciprocal Rank Fusion) constant - controls ranking smoothness. | RRF（倒数排名融合）常数 - 控制排名平滑度。
        # Higher values (e.g., 60) give more weight to lower-ranked results, | 较高的值（例如 60）赋予较低排名的结果更多权重，
        # Lower values make top results more dominant. Default is 60 (per original RRF paper). | 较低的值使排名靠前的结果更占主导地位。默认值为 60（根据原始 RRF 论文）。
        hybrid_rrf_k=60,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
    # Return 5 results on query | 查询时返回 5 个结果
    max_results=5,
    # Store metadata about the contents in the agent database, table_name="agno_knowledge" | 在代理数据库中存储有关内容的元数据，表名为 "agno_knowledge"
    contents_db=agent_db,
)

# ============================================================================
# Agent Instructions | Agent 指令
# ============================================================================
instructions = """\
You are an expert on the Agno framework and building AI agents. | 您是 Agno 框架和构建 AI Agent 的专家。

## Workflow | 工作流

1. Search | 搜索
   - For questions about Agno, always search your knowledge base first | 对于有关 Agno 的问题，始终先搜索您的知识库
   - Extract key concepts from the query to search effectively | 从查询中提取核心概念以进行有效搜索

2. Synthesize | 综合
   - Combine information from multiple search results | 结合多个搜索结果的信息
   - Prioritize official documentation over general knowledge | 优先考虑官方文档而非通用知识

3. Present | 展示
   - Lead with a direct answer | 以直接回答开始
   - Include code examples when helpful | 在有帮助时包含代码示例
   - Keep it practical and actionable | 保持实用且具有可操作性

## Rules | 规则

- Always search knowledge before answering Agno questions | 在回答 Agno 问题之前始终搜索知识库
- If the answer isn't in the knowledge base, say so | 如果答案不在知识库中，请如实说明
- Include code snippets for implementation questions | 对于实现类问题，包含代码片段
- Be concise — developers want answers, not essays | 保持简洁 —— 开发者想要的是答案，而不是长篇大论\
"""

# ============================================================================
# Create the Agent | 创建 Agent
# ============================================================================
agent_with_knowledge = Agent(
    name="Agent with Knowledge",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    knowledge=knowledge,
    search_knowledge=True,
    db=agent_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ============================================================================
# Load Knowledge and Run the Agent | 加载知识并运行 Agent
# ============================================================================
if __name__ == "__main__":
    # Load the introduction from the Agno documentation into the knowledge base | 将 Agno 文档中的介绍加载到知识库中
    # We're only loading 1 file to keep this example simple. | 我们仅加载 1 个文件以保持此示例简单。
    knowledge.add_content(
        name="Agno Introduction", url="https://docs.agno.com/introduction.md"
    )

    agent_with_knowledge.print_response(
        "What is Agno?",
        stream=True,
    )

# ============================================================================
# More Examples | 更多示例
# ============================================================================
"""
Load your own knowledge: | 加载您自己的知识：

1. From a URL | 从 URL
   knowledge.add_content(url="https://example.com/docs.pdf")

2. From a local file | 从本地文件
   knowledge.add_content(path="path/to/document.pdf")

3. From text directly | 直接从文本
   knowledge.add_content(text_content="Your content here...")

Hybrid search combines: | 混合搜索结合：
- Semantic search: Finds conceptually similar content | 语义搜索：查找概念相似的内容
- Keyword search: Finds exact term matches | 关键词搜索：查找精确术语匹配
- Results fused using Reciprocal Rank Fusion (RRF) | 使用倒数排名融合 (RRF) 融合结果

The agent automatically searches when relevant (agentic search). | Agent 在相关时自动搜索（Agent 搜索）。
"""
