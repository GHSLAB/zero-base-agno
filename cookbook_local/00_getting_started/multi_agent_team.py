"""
Multi-Agent Team - Investment Research Team | 多 Agent 团队 - 投资研究团队
============================================
This example shows how to create a team of agents that work together. | 此示例展示了如何创建一个协同工作的 Agent 团队。
Each agent has a specialized role, and the team leader coordinates. | 每个 Agent 都有专门的角色，由团队负责人进行协调。

We'll build an investment research team with opposing perspectives: | 我们将构建一个具有对立视角的投资研究团队：
- Bull Agent: Makes the case FOR investing | 看多 Agent：提出投资理由
- Bear Agent: Makes the case AGAINST investing | 看空 Agent：提出反对投资的理由
- Lead Analyst: Synthesizes into a balanced recommendation | 首席分析师：综合各方意见，给出平衡的建议

This adversarial approach produces better analysis than a single agent. | 这种对抗性方法比单个 Agent 能产生更好的分析结果。

Key concepts: | 核心概念：
- Team: A group of agents coordinated by a leader | Team：由负责人协调的一组 Agent
- Members: Specialized agents with distinct roles | Members：具有不同角色的专业 Agent
- The leader delegates, synthesizes, and produces final output | 负责人负责委派任务、综合意见并生成最终输出

Example prompts to try: | 可尝试的示例提示词：
- "Should I invest in NVIDIA?"
- "Analyze Tesla as a long-term investment"
- "Is Apple overvalued right now?"
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.team.team import Team
from agno.tools.yfinance import YFinanceTools

# ============================================================================
# Storage Configuration | 存储配置
# ============================================================================
team_db = SqliteDb(db_file="tmp/agents.db")

# ============================================================================
# Bull Agent — Makes the Case FOR | 看多分析师 —— 提出投资理由
# ============================================================================
bull_agent = Agent(
    name="Bull Analyst",
    role="Make the investment case FOR a stock | 提出看好某只股票的投资理由",
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools()],
    db=team_db,
    instructions="""\
You are a bull analyst. Your job is to make the strongest possible case
FOR investing in a stock. Find the positives: | 您是一个看多分析师。您的工作是尽可能提出最强有力的理由来支持投资某只股票。寻找积极因素：
- Growth drivers and catalysts | 增长驱动因素和催化剂
- Competitive advantages | 竞争优势
- Strong financials and metrics | 强劲的财务状况和指标
- Market opportunities | 市场机会

Be persuasive but grounded in data. Use the tools to get real numbers. | 具有说服力但要基于数据。使用工具获取真实数据。\
""",
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
)

# ============================================================================
# Bear Agent — Makes the Case AGAINST | 看空分析师 —— 提出反对投资的理由
# ============================================================================
bear_agent = Agent(
    name="Bear Analyst",
    role="Make the investment case AGAINST a stock | 提出反对投资某只股票的理由",
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools()],
    db=team_db,
    instructions="""\
You are a bear analyst. Your job is to make the strongest possible case
AGAINST investing in a stock. Find the risks: | 您是一个看空分析师。您的工作是尽可能提出最强有力的理由来反对投资某只股票。寻找风险：
- Valuation concerns | 估值担忧
- Competitive threats | 竞争威胁
- Weak spots in financials | 财务状况中的薄弱环节
- Market or macro risks | 市场或宏观风险

Be critical but fair. Use the tools to get real numbers to support your concerns. | 保持批判性但要公平。使用工具获取真实数据来支持您的担忧。\
""",
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
)

# ============================================================================
# Team Leader — Synthesizes Both Views | 团队负责人 —— 综合双方观点
# ============================================================================
multi_agent_team = Team(
    name="Multi-Agent Team",
    model=Gemini(id="gemini-3-flash-preview"),
    members=[bull_agent, bear_agent],
    instructions="""\
You lead an investment research team with a Bull Analyst and Bear Analyst. | 您领导着一个由看多分析师和看空分析师组成的投资研究团队。

## Process | 流程

1. Send the stock to BOTH analysts | 将股票发送给两位分析师
2. Let each make their case independently | 让每位分析师独立提出自己的理由
3. Synthesize their arguments into a balanced recommendation | 将他们的论点综合成一个平衡的建议

## Output Format | 输出格式

After hearing from both analysts, provide: | 在听取两位分析师的意见后，请提供：
- **Bull Case Summary**: Key points from the bull analyst | **看多理由摘要**：看多分析师的关键点
- **Bear Case Summary**: Key points from the bear analyst | **看空理由摘要**：看空分析师的关键点
- **Synthesis**: Where do they agree? Where do they disagree? | **综合分析**：他们在哪里达成一致？在哪里存在分歧？
- **Recommendation**: Your balanced view (Buy/Hold/Sell) with confidence level | **投资建议**：您的平衡观点（买入/持有/卖出）及信心水平
- **Key Metrics**: A table of the important numbers | **关键指标**：重要数据表格

Be decisive but acknowledge uncertainty. | 果断决策但要承认不确定性。\
""",
    db=team_db,
    show_members_responses=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ============================================================================
# Run the Team | 运行团队
# ============================================================================
if __name__ == "__main__":
    # First analysis | 第一次分析
    multi_agent_team.print_response(
        "Should I invest in NVIDIA (NVDA)?",
        stream=True,
    )

    # Follow-up question — team remembers the previous analysis | 后续问题 —— 团队记得之前的分析
    multi_agent_team.print_response(
        "How does AMD compare to that?",
        stream=True,
    )

# ============================================================================
# More Examples | 更多示例
# ============================================================================
"""
When to use Teams vs single Agent: | 何时使用 Team 而不是单个 Agent：

Single Agent: | 单个 Agent：
- One coherent task | 单一连贯的任务
- No need for opposing views | 不需要对立的观点
- Simpler is better | 越简单越好

Team: | 团队：
- Multiple perspectives needed | 需要多重视角
- Specialized expertise | 专业知识
- Complex tasks that benefit from division of labor | 受益于分工的复杂任务
- Adversarial reasoning (like this example) | 对抗性推理（如本示例）

Other team patterns: | 其他团队模式：

1. Research → Analysis → Writing pipeline | 研究 → 分析 → 写作流水线
   researcher = Agent(role="Gather information")
   analyst = Agent(role="Analyze data")
   writer = Agent(role="Write report")

2. Checker pattern | 检查者模式
   worker = Agent(role="Do the task")
   checker = Agent(role="Verify the work")

3. Specialist routing | 专家路由
   classifier = Agent(role="Route to specialist")
   specialists = [finance_agent, legal_agent, tech_agent]
"""
