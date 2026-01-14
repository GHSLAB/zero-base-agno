# Agno 食谱集 (Cookbook) 概览

本目录包含了数百个示例，旨在帮助开发者快速上手并构建功能强大的 AI 代理系统。

## 目录结构说明

### [00_getting_started](file:///d:/Agents/agno/cookbook/00_getting_started) - 入门指南
基础入门教程，循序渐进地介绍 Agno 的核心概念。
- [run.py](file:///d:/Agents/agno/cookbook/00_getting_started/run.py): 运行示例的入口。
- [README.md](file:///d:/Agents/agno/cookbook/00_getting_started/README.md): 详细的入门指导。

### [01_demo](file:///d:/Agents/agno/cookbook/01_demo) - 演示项目
一个完整的多代理系统示例，展示了如何使用 AgentOS 构建复杂的应用。
- `agents/`: 包含 SQL 代理、财务代理、研究代理等。
- `teams/`: 多代理协作的示例。
- `workflows/`: 自动化工作流示例。

### [02_examples](file:///d:/Agents/agno/cookbook/02_examples) - 实用案例
涵盖了各种实际应用场景的生产级代码示例。
- `01_agents/`: 提供了各种功能的单代理示例，包括：
    - [finance_agent.py](file:///d:/Agents/agno/cookbook/02_examples/01_agents/finance_agent.py): 财务分析代理。
    - [research_agent.py](file:///d:/Agents/agno/cookbook/02_examples/01_agents/research_agent.py): 网页搜索与研究代理。
    - [youtube_agent.py](file:///d:/Agents/agno/cookbook/02_examples/01_agents/youtube_agent.py): YouTube 视频总结代理。
    - [legal_consultant.py](file:///d:/Agents/agno/cookbook/02_examples/01_agents/legal_consultant.py): 法律咨询代理。
- `02_teams/`: 展示了多个代理如何协同工作：
    - [content_team.py](file:///d:/Agents/agno/cookbook/02_examples/02_teams/content_team.py): 内容创作团队。
    - [travel_planner_mcp_team.py](file:///d:/Agents/agno/cookbook/02_examples/02_teams/travel_planner_mcp_team.py): 使用 MCP 的旅行规划团队。
- `03_workflows/`: 编排复杂业务流程，如 [investment_report_generator.py](file:///d:/Agents/agno/cookbook/02_examples/03_workflows/investment_report_generator.py)。
- `04_gemini/`: 专门针对 Google Gemini 模型的高级应用。
- `05_streamlit_apps/`: 将代理转化为交互式 Web 应用，例如：
    - `agentic_rag/`: 具备代理能力的 RAG 应用。
    - `chess_team/`: AI 象棋对弈团队。
- `06_spotify_agent/`: 与 Spotify API 集成的音乐控制代理。
- `other/`: 包含 `chainlit_apps` (对话应用) 和 `speech_to_text` (语音转文本) 等其他实用集成。

### [03_agents](file:///d:/Agents/agno/cookbook/03_agents) - 核心代理功能
深入探讨单代理的各种高级特性。
- `async/`: 异步代理操作。
- `rag/`: 检索增强生成 (RAG) 的实现。
- `multimodal/`: 多模态代理示例。
- `skills/`: 为代理添加自定义技能。

### [04_teams](file:///d:/Agents/agno/cookbook/04_teams) - 多代理协作
展示如何让多个代理协同工作。
- `async_flows/`: 异步协作流。
- `distributed_rag/`: 分布式 RAG 模式。
- `reasoning/`: 具备推理能力的代理团队。

### [05_workflows](file:///d:/Agents/agno/cookbook/05_workflows) - 工作流编排
将多个步骤和代理串联成自动化的业务流程。

### [06_agent_os](file:///d:/Agents/agno/cookbook/06_agent_os) - 代理操作系统
部署、管理和监控代理的控制平面。
- `dbs/`: 各种数据库作为存储后端的示例。
- `remote/`: 远程代理服务器实现。

### [07_database](file:///d:/Agents/agno/cookbook/07_database) - 数据库集成
展示如何将 Agno 与各种主流数据库集成。
- 支持 Postgres, SQLite, MongoDB, Redis, DynamoDB, Firestore 等。

### [08_knowledge](file:///d:/Agents/agno/cookbook/08_knowledge) - 知识库与 RAG 深度探索
专注于如何为代理提供私有知识。
- `chunking/`: 文本分块策略。
- `embedders/`: 嵌入模型集成。
- `vector_db/`: 各种向量数据库支持。

### [09_memory](file:///d:/Agents/agno/cookbook/09_memory) - 记忆管理
实现具备长期和短期记忆的代理。
- `01_agent_with_memory.py`: 基础记忆示例。
- `02_agentic_memory.py`: 代理式记忆管理。

### [10_reasoning](file:///d:/Agents/agno/cookbook/10_reasoning) - 推理能力
让代理具备思考和逻辑推理的能力。
- `agents/`: 推理代理示例（如 Strawberry）。
- `tools/`: 推理辅助工具。

### [11_models](file:///d:/Agents/agno/cookbook/11_models) - 模型适配器
支持超过 40 种模型提供商的集成示例。
- 涵盖 Gemini, Claude, OpenAI, Groq, DeepSeek, Azure, AWS Bedrock 等。

### [12_evals](file:///d:/Agents/agno/cookbook/12_evals) - 评估与测试
用于测量和优化代理性能的工具。
- `accuracy/`: 准确性测试。
- `performance/`: 性能与延迟分析。
- `reliability/`: 工具调用可靠性测试。

### [13_integrations](file:///d:/Agents/agno/cookbook/13_integrations) - 第三方集成
与外部平台和工具的连接示例。
- `observability/`: 监控工具集成（Langfuse, Arize Phoenix 等）。
- `discord/`: Discord 机器人集成。

### [14_tools](file:///d:/Agents/agno/cookbook/14_tools) - 工具扩展库
极其丰富的内置工具库，扩展代理的能力边界。
- 涵盖搜索 (Google, Brave, Tavily)、财务 (YFinance)、办公 (Google Drive, Notion)、开发 (GitHub, Docker) 等。

---
*注：本概览仅列出主要分类，每个子目录下均有详细的代码实现和 README 说明。*
