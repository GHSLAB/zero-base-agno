# Agno 食谱集

数百个示例。复制、粘贴、运行。构建真正有效的智能体。

## 从哪里开始

**刚接触 Agno？** 从 [00_getting_started](./00_getting_started) 开始 — 它会引导你了解基础知识，每个食谱都建立在前一个的基础上。

**想看看真实案例？** 跳到 [01_demo](./01_demo) — 一个使用 AgentOS 的完整多智能体系统。运行它，拆解它，从中学习。

**知道你要构建什么？** 在下面找到你的用例。

---

## 按用例构建

### 我想构建单个智能体
→ [03_agents](./03_agents) — Agno 的原子单元。从这里开始学习工具、RAG、结构化输出、多模态、护栏等。

### 我想让智能体协同工作
→ [04_teams](./04_teams) — 协调多个智能体。异步流程、共享内存、分布式 RAG、推理模式。

### 我想编排复杂流程
→ [05_workflows](./05_workflows) — 将智能体、团队和函数链接到自动化管道中。

### 我想部署和管理智能体
→ [06_agent_os](./06_agent_os) — 部署到 Web API、Slack、WhatsApp 等。你的智能体系统的控制平面。

---

## 深度探索

### 知识与 RAG
[08_knowledge](./08_knowledge) — 为你的智能体提供运行时可搜索的信息。涵盖分块策略（语义、递归、智能体驱动）、嵌入器、向量数据库、混合搜索，以及从 URL、S3、GCS、YouTube、PDF 等加载内容。

### 记忆
[09_memory](./09_memory) — 有记忆的智能体。在对话中存储关于用户的见解和事实，以提供个性化响应。

### 推理
[10_reasoning](./10_reasoning) — 让智能体在行动前思考。三种方法：
- **推理模型** — 使用预训练用于推理的模型（o1、o3 等）
- **推理工具** — 为任何智能体提供启用推理的工具
- **推理智能体** — 设置 `reasoning=True` 以获得带工具使用的思维链

### 数据库
[07_database](./07_database) — 推荐 Postgres 和 SQLite。还支持 DynamoDB、Firestore、MongoDB、Redis、SingleStore、SurrealDB 等。

### 模型
[11_models](./11_models) — 40+ 模型提供商。Gemini、Claude、GPT、Llama、Mistral、DeepSeek、Groq、Ollama、vLLM — 如果它存在，我们可能支持它。

### 工具
[14_tools](./14_tools) — 扩展智能体的能力。Web 搜索、SQL、电子邮件、API、MCP、Discord、Slack、Docker，以及使用 `@tool` 装饰器的自定义工具。

---

## 生产就绪

### 评估
[12_evals](./12_evals) — 衡量重要指标：准确性（LLM 作为评判者）、性能（延迟、内存）、可靠性（预期工具调用）和智能体作为评判者的模式。

### 集成
[13_integrations](./13_integrations) — 连接到 Discord、可观察性工具（Langfuse、Arize Phoenix、AgentOps、LangSmith）、内存提供商和 A2A 协议。

## 真实世界示例

[02_examples](./02_examples) — 完整的、生产级别的示例。停止阅读文档，开始构建。

---

## 贡献

我们一直在添加新的食谱。想贡献吗？请参阅 [CONTRIBUTING.md](./CONTRIBUTING.md)。