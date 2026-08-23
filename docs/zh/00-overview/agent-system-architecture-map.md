---
id: OV01
title: Agent System Architecture Map
lang: zh
status: draft
module: overview
prerequisites: []
concepts: [workflow, single-agent, multi-agent, orchestration, architecture-map]
example: examples/architecture-map/architecture_card.py
last_reviewed: 2026-08-24
---

# OV01：Agent System Architecture Map

Agent、Workflow、Planner、Supervisor、Handoff、Graph、Memory、MCP——这些词经常同时出现在一个系统里，却不属于同一层级。

如果把它们简单排列成一张 pattern 清单，很快会遇到三个问题：

1. 不知道哪些概念可以组合；
2. 不知道两个系统真正不同在哪里；
3. 新技术出现后，只能继续增加一级目录。

本章建立整套教程的中心地图。后续每种 Agent 架构都会放回这张地图，回答它改变了系统的哪个维度。

## 它解决什么问题

考虑下面这个系统：

```text
User Request
    -> Router
    -> Planner
    -> Supervisor
         ├─ Research Agent
         ├─ Data Agent
         └─ Writing Agent
    -> Evaluator
    -> Final Report
```

应该如何分类它？

- 它是 Workflow，因为存在 Router 和 Evaluator；
- 它是 Planning System，因为 Planner 维护计划；
- 它是 Multi-Agent，因为 Supervisor 调用多个 Specialist；
- 它可能使用 Graph Orchestration；
- 它还可能通过 MCP 使用工具，通过 A2A 调用远程 Agent。

这些判断可以同时成立。Agent System Architecture 不是一棵互斥分类树，而是一组可以组合的架构维度。

## 核心定义

### Agent System

在本项目中，Agent System 指一个围绕目标组织模型、工具、状态、记忆和控制逻辑的系统。系统中的下一步可能由代码、模型、人，或者三者共同决定。

```text
Agent System
    = Goal
    + Control
    + Reasoning / Planning
    + Context / State / Memory
    + Tools / Environment
    + Communication / Coordination
    + Runtime / Governance / Evaluation
```

### Workflow

Workflow 的主要执行路径由代码或显式规则控制。模型可以参与分类、生成和评价，但不拥有整体控制权。

### Agent

Agent 能够根据目标、当前状态和观察结果，动态选择下一步行动。自主性来自决策权，而不是来自模型调用次数。

### Multi-Agent System

Multi-Agent System 包含多个具有独立角色、上下文或决策能力的 Agent，并需要额外的通信、协调和终止机制。

## 第一张地图：复杂度演进

学习 Agent Architecture 最自然的顺序，是观察系统复杂度如何增加：

```text
LLM Call
   |
   v
Augmented LLM
Model + Retrieval + Tools + Memory
   |
   v
Workflow
Chain / Router / Parallel / Evaluator
   |
   v
Single Agent
Reason -> Act -> Observe
   |
   v
Planned Agent
Plan / Execute / Reflect / Replan
   |
   v
Multi-Agent System
Supervisor / Handoff / Group Chat / Hierarchy
   |
   v
Orchestrated Agent System
Graph / State Machine / Events / Durable Runtime
   |
   v
Distributed Agent System
Discovery / Identity / MCP / A2A / Async Tasks
```

这不是成熟度排名。复杂度更高不代表产品更好。每向下一层移动，系统获得新的能力，也增加新的状态、调用、延迟和失败方式。

Anthropic 对 Agentic Systems 的工程建议同样从简单、可组合的 Workflow 开始，再进入自主 Agent；OpenAI Agents SDK 也明确区分由代码决定流程和由 LLM 决定流程。[Anthropic：Building Effective AI Agents](https://resources.anthropic.com/building-effective-ai-agents)、[OpenAI：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)

## 第二张地图：系统分层

复杂度演进图回答“系统如何逐步变复杂”，分层图回答“一个完整系统由什么组成”。

```text
┌──────────────────────────────────────────────────────┐
│ Experience & Governance                              │
│ User Goal / Progress / Approval / Policy / Handoff   │
├──────────────────────────────────────────────────────┤
│ Orchestration & Control                              │
│ Workflow / Router / Graph / State Machine / Scheduler│
├──────────────────────────────────────────────────────┤
│ Reasoning & Collaboration                            │
│ ReAct / Planner / Critic / Supervisor / Handoff      │
├──────────────────────────────────────────────────────┤
│ Context, State & Memory                              │
│ Context Packets / Typed State / Working & Long Memory│
├──────────────────────────────────────────────────────┤
│ Capabilities & Environment                           │
│ Tools / Retrieval / Code / Computer / Remote Agents  │
├──────────────────────────────────────────────────────┤
│ Runtime & Operations                                 │
│ Execution / Checkpoint / Trace / Eval / Recovery     │
└──────────────────────────────────────────────────────┘
```

### Experience & Governance

定义用户目标如何进入系统、系统可以自主做什么，以及何时需要审批、人工接管或策略阻断。

### Orchestration & Control

决定哪些组件运行、运行顺序和下一步由谁选择。控制可以由代码、LLM 或混合逻辑完成。

### Reasoning & Collaboration

包含 ReAct、Planning、Reflection 等单 Agent 认知模式，也包含 Supervisor、Handoff 等 Multi-Agent 协作模式。

### Context、State 与 Memory

Context 是某次模型调用能够看到的信息；State 是系统当前的显式状态；Memory 是跨步骤或跨任务保留的信息。三者不能混为同一个消息列表。

CoALA 将语言 Agent 描述为包含模块化 Memory、内部与外部 Action，以及重复 Decision Cycle 的认知架构，这也说明 LLM 只是更大系统中的一个组件。[CoALA](https://arxiv.org/abs/2309.02427)

### Capabilities & Environment

Agent 通过工具、检索、代码执行、计算机操作或远程 Agent 观察和改变环境。模型提出行动意图，Runtime 负责验证和执行。

### Runtime & Operations

负责执行、超时、重试、持久化、恢复、追踪、评价和成本统计。它保证架构不仅能在一次 Demo 中运行，也能被测试和运营。

## 第三张地图：八个描述维度

仅说“这是一个 Multi-Agent 系统”远远不够。描述一个 Agent System 时，至少回答八个问题：

| 维度 | 核心问题 | 常见选择 |
|---|---|---|
| Control | 谁决定下一步？ | Code / LLM / Human / Hybrid |
| Reasoning | 如何选择行动？ | Direct / ReAct / Plan / Search / Reflect |
| Topology | 决策主体如何组织？ | Workflow / Single / Supervisor / Handoff / Hierarchy |
| Context | 信息如何分配？ | Shared / Isolated / Context Packet / Progressive |
| Memory | 什么跨步骤保留？ | Working / Episodic / Semantic / Shared / Private |
| Communication | 组件如何交换信息？ | Message / State / Blackboard / Event / Artifact |
| Orchestration | 执行结构是什么？ | Chain / DAG / Graph / State Machine / Event-driven |
| Runtime | 如何持续和恢复？ | Request / Async / Durable / Distributed |

Protocols、Governance、Reliability 和 Evaluation 会进一步约束这些维度，但它们不是某一种 Agent Topology。

例如，一个研究系统可以被完整描述为：

```text
Control: hybrid
Reasoning: planner-executor-replanner
Topology: supervisor with parallel specialists
Context: isolated specialist contexts + structured result packets
Memory: private working memory + shared artifact workspace
Communication: agent-as-tool results and artifacts
Orchestration: graph with parallel fan-out and evaluator loop
Runtime: durable background task with checkpoints
```

这比“我们用了 Multi-Agent”提供了更多可评审、可实现的信息。

## Pattern 在地图中的位置

```text
Agentic Systems
├─ Workflow Patterns
│  ├─ Sequential
│  ├─ Router
│  ├─ Parallel
│  └─ Evaluator-Optimizer
├─ Single-Agent Patterns
│  ├─ ReAct
│  ├─ Plan-and-Execute
│  ├─ Reflection
│  └─ Search / Deliberation
├─ Multi-Agent Patterns
│  ├─ Subagents / Supervisor
│  ├─ Handoff
│  ├─ Group Chat / Swarm
│  ├─ Blackboard
│  └─ Hierarchical Teams
└─ System Architecture
   ├─ Context / Memory
   ├─ Communication / Coordination
   ├─ Graph / State Machine / Events
   ├─ Reliability / Evaluation
   └─ MCP / A2A / Distributed Runtime
```

LangChain 当前把 Subagents、Handoffs、Skills、Router 和 Custom Workflow 作为可组合的 Multi-Agent pattern，并强调核心问题是 Context Engineering。[LangChain：Multi-agent overview](https://docs.langchain.com/oss/javascript/langchain/multi-agent/index)

## MCP 和 A2A 放在哪里

MCP 与 A2A 都不等于 Multi-Agent Pattern：

```text
MCP
Agent Host <-> Tool / Resource / Prompt Provider

A2A
Client Agent <-> Remote Agent System
```

MCP 主要位于 Capabilities 与 Integration 边界，采用 Host–Client–Server 架构；A2A 位于 Distributed Agent Communication 边界，通过 Agent Card、Task、Message 和 Artifact 描述远程协作。[MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)、[A2A Core Concepts](https://a2a-protocol.org/latest/topics/key-concepts/)

协议让系统互操作，但不会替你决定应该采用 Supervisor、Handoff、Graph 还是其他架构。

## 最小可运行实践

本章的实践不是实现完整 Agent，而是创建一张可比较的 Architecture Card：

```bash
python examples/architecture-map/architecture_card.py
```

Architecture Card 使用八个维度描述系统，并比较一个确定性 Workflow 与一个 Agent Research System 的差异。

示例不调用模型，因为本章需要验证的是架构描述方法，而不是模型能力。

## 正常场景

假设内容生产系统从固定 Workflow 演进为研究 Agent：

```text
Before
Control: code
Topology: workflow
Orchestration: sequential
Runtime: request-response

After
Control: hybrid
Reasoning: plan-and-reflect
Topology: supervisor
Context: isolated
Orchestration: graph
Runtime: durable
```

这张差异表能帮助团队看到：升级的不只是“Agent 数量”，还包括 Control、Context、Orchestration 和 Runtime。

## 失败场景

### 只用 Pattern 名称描述系统

“我们使用 Supervisor”没有说明 Supervisor 是否拥有最终答案、Specialist 是否共享历史、失败如何返回，以及执行能否恢复。

### 把框架当作架构

“我们使用 LangGraph”没有说明系统是 Router、Handoff 还是 Hierarchical Team。框架选择不能替代架构设计。

### 把消息历史当作全部 State

如果计划、审批、任务状态和 Artifact 都只存在聊天记录中，系统很难暂停、恢复、测试和审计。

### 为了完整而一次加入所有层

Architecture Map 是观察工具，不是要求每个系统必须拥有所有组件。简单 Workflow 不需要长期 Memory、A2A 或 Hierarchical Agents。

## 什么时候使用 Architecture Map

- 项目开始时建立共同术语；
- 评审从 Workflow 升级为 Agent 的理由；
- 比较两个框架实现是否表达相同架构；
- 分析 Context、通信或 Runtime 故障；
- 规划系统演进和测试范围。

## 什么时候不要使用它代替详细设计

Architecture Map 不能替代：

- 工具 schema 和 API 契约；
- State 数据结构；
- 权限模型；
- 错误处理策略；
- 部署和容量设计。

它负责确定设计空间，后续模块负责把各个维度展开。

## Trade-offs

| 选择 | 获得 | 付出 |
|---|---|---|
| Code → LLM Control | 灵活性 | 不确定性和验证成本 |
| Shared → Isolated Context | 专注和隐私 | 信息传递与合成成本 |
| Single → Multi-Agent | 专业化和并行 | 通信、延迟和级联失败 |
| Request → Durable Runtime | 长任务恢复 | 状态和基础设施复杂度 |
| Local → Distributed | 独立扩展和互操作 | 身份、网络和协议故障 |

架构选择的目标不是最大化自主性，而是在任务价值、可控性和系统成本之间取得合适平衡。

## 产品视角

### 用户与业务问题

Architecture Map 帮助产品团队把“做一个 Agent”改写为具体能力：动态规划、并行专业处理、长期任务、外部行动或跨系统协作。

### 产品价值

每次复杂度升级都应该对应可测量收益，例如减少用户操作、提高任务完成率、缩短总耗时或扩大任务覆盖范围。

### 用户体验

用户不需要看到内部 Agent 拓扑，但需要看到与架构复杂度对应的计划、进度、来源、审批、Artifact、失败和恢复入口。

### 自主性边界

Control 维度必须映射到产品权限：模型可以建议、准备还是执行；高风险动作不能只依赖 Prompt 约束。

### 数据与权限

Context、Memory 和 Communication 维度决定数据会流向哪些组件。架构评审应明确用户数据是否进入 Specialist、共享状态或 Remote Agent。

### 失败与降级

复杂系统应能够降级：Multi-Agent 失败时回到 Single Agent，Agent 无法继续时返回部分 Artifact，远程能力不可用时使用本地 Workflow 或转人工。

### 产品指标

至少观察 Task Success、Time to Outcome、用户修正率、人工介入率、单成功任务成本，以及非预期行动率。

## 框架中的对应实现

不同框架强调不同抽象：

- LangGraph 强调 State 与 Graph；
- AutoGen 强调 Agent、Team、Group Chat 与 GraphFlow；
- OpenAI Agents SDK 强调 Agent、Agents as Tools、Handoff、Guardrails 与 Runner；
- Google ADK 提供 LLM Agent 与 Sequential、Parallel、Loop 等 Workflow Agent；
- CrewAI 区分 Crew 与 Flow。

这些概念都应先映射到 Architecture Map，再比较 API 和运行能力。

## Related Patterns

后续阅读顺序：

1. Workflow Patterns
2. ReAct Architecture
3. Planning & Search
4. Context Architecture
5. Memory Architecture
6. Multi-Agent Fundamentals
7. Orchestration Architecture

## 检查清单

- 是否明确下一步由代码、模型还是人决定？
- 是否说明 Reasoning / Planning pattern？
- 是否说明 Agent Topology 和最终答案所有权？
- 是否说明 Context 与 Memory 的边界？
- 是否说明组件如何通信？
- 是否说明 Orchestration 和 Runtime？
- 是否定义停止、失败和恢复方式？
- 是否能解释新增复杂度带来的产品收益？

## 小结

Agent System Architecture 不能只用一个 pattern 或框架名称描述。

一套完整描述至少需要覆盖 Control、Reasoning、Topology、Context、Memory、Communication、Orchestration 和 Runtime。后续所有章节都将在这张地图上展开某一个维度，再通过完整项目把它们重新组合起来。

下一篇将正式区分 Agent、Workflow 与 Agentic System，并讨论系统从确定性控制走向自主决策时发生了什么。
