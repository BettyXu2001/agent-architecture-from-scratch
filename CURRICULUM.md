# Curriculum / Agent System Architecture 项目大纲

## 1. 项目定位

本项目的主线是 **Agent System Architecture**：从 Workflow、Single Agent 逐步进入 Planning、Context、Memory、Multi-Agent、Orchestration 和 Distributed Agent Systems。

它回答的是：

> 一个 Agent 系统应该如何组织？面对具体问题，什么时候使用 Workflow、Single Agent、Multi-Agent 或分布式 Agent 系统？

它不重复 `learn-dsh / how-deepseek-harness-works` 对 Agent Harness 内部机制的拆解：

| 项目 | 核心问题 | 主要内容 |
|---|---|---|
| `learn-dsh` | How does one agent work internally? | Loop、Tools、Session、Context Construction、Sandbox、Permissions、Persistence、Plugins |
| 本项目 | How should agent components be organized? | Workflow、Planning、Context Flow、Memory Topology、Multi-Agent、Coordination、Orchestration、Protocols |

Context、Memory 等概念可能同时出现，但视角不同：`learn-dsh` 讲内部实现，本项目讲系统中的信息边界、拓扑与架构选择。

## 2. 核心教学逻辑

项目按照系统复杂度逐步增加，而不是按照框架或产品类型组织：

```text
LLM
  -> Augmented LLM
  -> Workflow
  -> Single Agent
  -> Agent + Planning / Context / Memory / Reflection
  -> Multiple Agents
  -> Orchestrated Agent System
  -> Distributed Agent System
```

框架只是架构 pattern 的实现。`docs/` 按稳定架构知识组织，LangGraph、AutoGen、CrewAI、OpenAI Agents SDK 和 Google ADK 等内容放在 framework mapping 中。

## 3. 18 个主线模块

### Part 0 — Agent Architecture Overview

**定位：核心**

核心文章：

1. Agent System Architecture Map
2. Agent、Workflow 与 Agentic System
3. 从 Augmented LLM 到 Distributed Agent System
4. Architecture Decision Framework
5. Control Flow、Data Flow、Context Flow 与 State Flow

理论重点：Agent 系统的层次、代码控制与模型控制、复杂度阶梯、架构组合方式。

简单实践：为客服、研究、内容生成、数据分析和自动化任务选择最小可行架构，并绘制 architecture map。

产品视角：用户价值是否需要动态决策；自主性增加后，用户如何看到进度、确认动作和处理失败。

现有文章映射：

- `P01 从 AI 功能到 Agent 产品`：作为 Agent vs Workflow 的产品向补充。
- `P02 Chat、Workflow 与 Agent`：作为交互层与执行架构的补充，不代替主线架构文章。

### Part 1 — Workflow Patterns

**定位：核心**

核心文章：

1. Sequential / Prompt Chaining
2. Routing
3. Parallelization / Fan-out Fan-in
4. Evaluator-Optimizer
5. Workflow Composition：Branch、Join、Loop 与 Fallback
6. Workflow vs Agent

理论重点：确定性控制流、结构化输入输出、错误传播、代码编排与模型调用的边界。

简单实践：用同一内容生产任务实现 Sequential、Router、Parallel 和 Evaluator 四个版本。

产品视角：稳定性、等待时间、单任务成本、失败步骤展示，以及为什么 Workflow 可能比 Agent 更适合。

### Part 2 — Single-Agent Reasoning

**定位：核心**

核心文章：

1. ReAct Architecture
2. Reason–Act–Observe Loop
3. Reflection / Self-Critique
4. Critic and Revision
5. Tool-Using Agent as an Architecture Boundary
6. Termination、Clarification 与 Budget

理论重点：自主循环、观察反馈、反思与验证、内部推理和外部行动的区别。

简单实践：实现带工具、step budget、停止条件和 critic 的小型研究 Agent。

产品视角：用户是否需要看到计划或步骤；Agent 何时追问、停止、返回部分结果或请求确认。

### Part 3 — Planning & Search

**定位：核心；高级搜索模式放入 Advanced**

核心文章：

1. Plan-and-Execute
2. Planner–Executor
3. Planner–Executor–Replanner
4. Task Decomposition and Dependency Graph
5. Plan Selection and Validation
6. Progress Ledger and Replanning

Advanced Patterns：

- Tree of Thoughts
- LATS
- Beam Search
- MCTS Agent
- LLMCompiler
- Deliberation and Candidate Search

理论重点：计划表示、任务依赖、静态与动态计划、搜索空间、预算和进度判断。

简单实践：比较 ReAct、静态 Plan-and-Execute 和动态 Replanner 完成同一长任务。

产品视角：计划是否应向用户展示和编辑；长任务如何估算进度、处理中断并控制调用成本。

### Part 4 — Context Architecture

**定位：核心**

核心文章：

1. Context Engineering for Agent Systems
2. Context Selection and Progressive Disclosure
3. Context Passing between Components
4. Context Isolation
5. Context Compression and Summarization
6. Context Provenance and Access Boundary

理论重点：复杂 Agent 系统中谁应该看到什么、何时看到、以何种形式传递，而不是重复讲上下文窗口的底层拼装。

简单实践：比较全量历史、摘要传递、结构化 context packet 和隔离 subcontext。

产品视角：数据范围、隐私、个性化、用户可见来源，以及错误上下文如何影响产品结果。

### Part 5 — Memory Architecture

**定位：核心**

核心文章：

1. Working Memory
2. Episodic Memory
3. Semantic Memory
4. Procedural / Skill Memory
5. Shared vs Private Memory
6. Memory Retrieval、Write Policy and Forgetting
7. Artifact / Workspace as Memory

理论重点：Memory 类型、读写责任、生命周期、一致性、长期经验与当前 Context 的区别。

简单实践：为同一个 Agent 添加工作记忆、长期偏好记忆和可共享 artifact workspace。

产品视角：产品应该记住什么、允许用户查看和删除什么、错误记忆如何修正，以及记忆带来的信任风险。

### Part 6 — Multi-Agent Fundamentals

**定位：核心**

核心文章：

1. Why Multi-Agent?
2. When Not to Use Multi-Agent
3. Single Agent vs Modular Single Agent vs Multi-Agent
4. Agent Specialization and Role Boundary
5. Final Answer Ownership
6. Context、Cost and Failure Radius

理论重点：专业化、Context Isolation、并行、组织边界，以及 Multi-Agent 的额外通信和验证成本。

简单实践：用 Single Agent 和多个 Specialists 完成同一任务，比较成功率、调用数和上下文使用。

产品视角：拆分 Agent 是否创造可衡量的用户价值；系统如何向用户呈现统一结果而不是内部组织结构。

### Part 7 — Multi-Agent Patterns

**定位：核心**

核心文章：

1. Subagents / Agents as Tools
2. Supervisor / Manager
3. Router and Parallel Specialists
4. Handoff
5. Round Robin and Selector Group Chat
6. Swarm
7. Hybrid Multi-Agent Patterns

Advanced Patterns：Debate、Voting、Mixture-of-Agents、Magentic-One、Dynamic Agent Generation。

理论重点：控制权、路由方式、消息历史、最终答案所有权和终止条件。

简单实践：实现 Manager、Handoff 和 Selector Group Chat，并使用相同场景比较。

产品视角：用户是始终面对一个产品身份，还是直接进入 Specialist；Handoff 后如何保持体验连续。

### Part 8 — Hierarchical Systems

**定位：核心**

核心文章：

1. Hierarchical Supervisor
2. Supervisor Tree
3. Teams of Teams
4. Recursive Delegation
5. Local Autonomy and Global Control
6. Hierarchical Context and Result Aggregation

理论重点：多层任务分解、局部自治、跨层 Context、汇总、预算和递归终止。

简单实践：构建 Coordinator → Team Lead → Worker 的两层系统，并限制委派深度。

产品视角：什么规模的任务值得层级化；层级结构是否显著增加等待时间和故障定位难度。

### Part 9 — Agent Communication

**定位：核心**

核心文章：

1. Direct Message
2. Shared State
3. Blackboard
4. Event / Publish–Subscribe
5. Private State and Context Packets
6. Message vs State vs Artifact
7. Communication Topology

理论重点：通信载体、消息可靠性、共享状态冲突、Artifact、信息来源与通信成本。

简单实践：用 direct message、shared state 和 blackboard 实现同一协作任务。

产品视角：通信方式如何影响结果一致性、可追溯性、实时进度和故障恢复。

### Part 10 — Agent Protocols

**定位：推荐；Distributed Agent Systems 的基础**

核心文章：

1. MCP Architecture：Host、Client、Server
2. A2A Architecture：Client Agent and Remote Agent
3. MCP vs A2A
4. Agent Card and Capability Discovery
5. Task、Message、Part and Artifact
6. Agent Identity、Authentication and Trust
7. Sync、Streaming and Async Tasks

理论重点：Agent-to-Tool 与 Agent-to-Agent 的边界、发现、能力描述、远程任务生命周期和安全域。

简单实践：本地 Agent 通过 MCP 风格接口使用工具，再通过 A2A 风格 Task/Artifact 调用 Remote Agent。

产品视角：协议是否降低集成成本；外部 Agent 的身份、权限、SLA、失败和用户数据责任由谁承担。

### Part 11 — Orchestration Architecture

**定位：核心**

核心文章：

1. Code-driven vs LLM-driven Orchestration
2. DAG
3. Graph
4. State Machine
5. Event-driven Architecture
6. GraphFlow and Cyclic Workflows
7. Durable Execution、Checkpoint and Resume

理论重点：执行顺序由谁决定、显式状态转换、分支循环、事件与长任务恢复。

简单实践：把同一 Agent 流程分别实现为代码 Workflow、State Machine 和 Graph。

产品视角：确定性、延迟、可恢复性、进度展示，以及用户是否能暂停、修改和继续任务。

### Part 12 — Coordination & Scheduling

**定位：推荐**

核心文章：

1. Task Graph and Delegation Contract
2. Task Allocation and Capability Matching
3. Scheduler and Priority
4. Parallelism and Concurrency Limits
5. Queue and Backpressure
6. Consensus、Voting and Conflict Resolution
7. Cancellation and Dependency Propagation

理论重点：谁做什么、何时执行、依赖关系、资源预算、冲突和任务完成定义。

简单实践：实现带依赖、优先级、并发限制和取消传播的 Multi-Agent Task Board。

产品视角：并行是否真的降低用户等待；任务优先级和资源限制如何影响用户承诺与 SLA。

### Part 13 — Human & Governance

**定位：推荐**

核心文章：

1. Human-in-the-Loop
2. Approval Gates
3. Human Handoff and Escalation
4. Mixed-Initiative Collaboration
5. Guardrails and Policy Layer
6. Permission and Action Boundaries
7. Audit、Accountability and Data Governance

理论重点：人与 Agent 的任务分配、审批、介入、责任边界和外部策略控制。

简单实践：为高风险工具加入 preview、approval、reject、edit 和 audit trail。

产品视角：用户如何理解和控制 Agent；什么情况下系统必须停下来请求确认或转人工。

### Part 14 — Reliability

**定位：核心**

核心文章：

1. Agent Failure Taxonomy
2. Retry and Fallback
3. Timeout and Cancellation
4. Termination and Loop Detection
5. Idempotency and Side-Effect Safety
6. Partial Failure and Compensation
7. Multi-Agent Failure Modes
8. Recovery、Checkpoint and Resume

理论重点：死循环、重复行动、角色漂移、上下文污染、通信错误、级联失败和恢复策略。

简单实践：建立故障注入矩阵，主动触发工具超时、Agent 重复、错误 Handoff 和部分失败。

产品视角：用户看到什么失败状态；能否获得部分结果、重试、恢复、降级或人工帮助。

### Part 15 — Evaluation & Observability

**定位：核心**

核心文章：

1. Trace、Span and Agent Run Model
2. Task-level Evaluation
3. Trajectory Evaluation
4. Tool and Handoff Evaluation
5. Multi-Agent Evaluation
6. Offline Evals and Golden Set
7. Online Evaluation and Human Feedback
8. Cost、Latency and Quality Attribution

理论重点：不仅评价最终答案，还评价计划、轨迹、工具选择、通信、Handoff 和停止行为。

简单实践：为前面构建的 Agent System 增加 trace、场景集、trajectory grader 和成本统计。

产品视角：Task Success、Time to Outcome、用户修正率、人工介入率和单成功任务成本。

### Part 16 — Architecture Comparison

**定位：核心**

比较对象：

- LangGraph
- AutoGen / Microsoft Agent Framework
- CrewAI
- OpenAI Agents SDK
- Google ADK
- 其他有代表性的框架

统一比较维度：

1. Core abstraction
2. Control and orchestration model
3. State and context model
4. Multi-Agent patterns
5. Communication and protocol support
6. Durability and human intervention
7. Observability and evaluation
8. Cost、complexity and vendor coupling

简单实践：使用至少两个框架实现相同 Supervisor/Handoff 场景，并映射到同一架构图。

产品视角：团队能力、上市时间、可维护性、可迁移性和生态集成，而不是只比较功能数量。

### Part 17 — Build a Real Agent System

**定位：核心收官项目**

使用同一个任务逐步演进：

1. Deterministic Workflow
2. Router + Parallel + Evaluator
3. ReAct Single Agent
4. Planner–Executor–Replanner
5. Context Isolation and Memory
6. Supervisor + Specialists
7. Handoff / Hierarchical Team
8. Graph Orchestration
9. MCP Tools + A2A Remote Agent
10. Reliability、HITL、Observability and Evals

每一步保留上一版本，用同一任务集比较成功率、调用次数、token、延迟、故障恢复和用户控制。

产品视角：每次架构升级必须对应可测量的产品收益，而不是为了展示更多 Agent 技术。

## 4. Advanced 与应用专题

这些内容重要，但不改变 18 个主线模块：

### Advanced Patterns

- Tree Search、LATS、MCTS、Beam Search
- Debate、Mixture-of-Agents、Magentic-One
- Dynamic Agent Generation
- Federated / Decentralized Agent Systems
- Learning Agent and Workflow Memory

### Application Architectures

- Basic / Routed / Agentic / Corrective / Graph RAG
- Deep Research Agent
- Customer Support Agent
- Coding Agent
- Data Analysis Agent
- Browser / Computer-use Agent
- Workflow Automation Agent
- Personal / Proactive Agent
- Voice and Multimodal Agent

应用专题的作用是组合主线 pattern。例如 Deep Research 可以由 Planning + Agentic RAG + Parallel Workers + Evaluator + Artifact Workspace 组成，而不是成为新的一级架构分类。

## 5. 每个模块的理论与实践要求

每个模块至少包含：

1. Architecture Overview
2. Core Concepts
3. Control Flow / Context Flow / State Flow 图
4. From-scratch Minimal Implementation
5. 正常场景
6. 失败与降级场景
7. When to Use / When Not to Use
8. Trade-offs
9. Framework Mapping
10. Related Patterns

一个模块可以使用同一个 Lab 逐步覆盖多篇文章，避免为每个小概念重复创建项目。

## 6. 每篇文章必须包含产品视角

产品视角是横向栏目，不取代 Agent Architecture 主线。每篇核心文章必须包含 `## 产品视角`，回答：

1. 该架构解决什么用户或业务问题？
2. 与更简单架构相比增加了什么价值？
3. 用户能看到哪些计划、进度、结果和错误？
4. Agent 可以自主决定什么，什么需要确认？
5. 需要哪些数据、权限和外部系统？
6. 失败时如何重试、降级、恢复或转人工？
7. 使用什么产品指标验证？
8. 增加的成本、延迟和维护复杂度是否值得？

每篇至少提供两张视图：

```text
Architecture View：Components -> Control / Context / State / Communication
Product View：User -> Goal -> Progress / Approval -> Result / Failure / Handoff
```

## 7. 目录规划

```text
docs/
├─ zh/
│  ├─ 00-overview/
│  ├─ 01-workflows/
│  ├─ 02-single-agent/
│  ├─ 03-planning/
│  ├─ 04-context/
│  ├─ 05-memory/
│  ├─ 06-multi-agent/
│  ├─ 07-communication/
│  ├─ 08-protocols/
│  ├─ 09-orchestration/
│  ├─ 10-reliability/
│  ├─ 11-evaluation/
│  ├─ 12-framework-comparison/
│  ├─ 13-real-system/
│  └─ appendices/
└─ en/                       # 与中文完整镜像

patterns/
├─ react/
├─ plan-and-execute/
├─ reflection/
├─ router/
├─ supervisor/
├─ handoff/
├─ swarm/
├─ blackboard/
└─ ...

advanced/
├─ tree-search/
├─ debate/
├─ magentic-one/
├─ mixture-of-agents/
└─ dynamic-agent-generation/

protocols/
├─ mcp/
└─ a2a/

frameworks/
├─ langgraph/
├─ autogen/
├─ crewai/
├─ openai-agents-sdk/
└─ google-adk/

labs/
└─ ...
```

主教程按稳定架构知识组织；易变化的框架和协议版本材料独立维护。新增技术时先判断它改变的是 Reasoning、Planning、Context、Memory、Communication、Coordination、Orchestration、Reliability、Evaluation 还是 Protocol，再放入相应位置。
