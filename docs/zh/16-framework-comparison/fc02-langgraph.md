---
id: FC02
slug: zh/16-framework-comparison/fc02-langgraph
order: 1702
section: framework-comparison
status: complete
title: "LangGraph：把 Agent 建模为有状态图"
description: "LangGraph 的核心不是“很多 Agent”，而是持久化的 StateGraph：节点读取和更新状态，边决定下一步。显式控制流、检查点和可恢复执行适合长任务、审批与复杂分支。"
updated_at: 2026-08-25
lang: zh
module: 16-framework-comparison
prerequisites: [Part 0, Part 6, Part 11]
concepts: [langgraph,graph,state,durable-execution]
example: framework-comparison
last_reviewed: 2026-08-25
---

# LangGraph：把 Agent 建模为有状态图

> 理解 LangGraph 适合解决什么，以及它不替产品做哪些决定。

## 它解决什么问题

LangGraph 的核心不是“很多 Agent”，而是持久化的 StateGraph：节点读取和更新状态，边决定下一步。显式控制流、检查点和可恢复执行适合长任务、审批与复杂分支。

## 核心定义与工作原理

把业务状态、对话状态和运行状态分开；节点保持职责单一；条件边只表达路由；副作用节点设计幂等键。检查点让暂停、恢复、时间旅行和人工介入成为运行时能力，但状态结构、权限和终止策略仍需团队定义。

### 架构视图（Architecture View）

分析时固定追问：谁拥有控制权，状态存在哪里，模型能决定什么，失败从哪里恢复，人工在哪个边界介入，运行证据如何被观察。

### 产品视图（Product View）

用户能看到明确阶段、可暂停审批和失败续跑；代价是状态迁移与边界条件变成产品的一部分。重点指标包括阶段成功率、恢复成功率、人工等待时长、每节点成本和端到端时延。

## 简单实践

将研究报告画成 scope→parallel_research→merge→draft→review→approval→publish。为 review 增加“通过/返工/人工确认”三条边，并列出每个节点的输入、输出和可重试边界。

实践只要求架构图、状态或消息契约、失败路径和产品指标，不要求安装依赖或运行代码。

## 正常场景

任务按约定入口进入，编排层保留业务状态，各节点或 Agent 产出结构化结果，质量门控制下一阶段，用户获得可理解的进度与最终产物。

## 失败与恢复场景

模型超时、工具失败或子任务质量不足时，区分可重试、可降级和必须人工接管的错误。恢复应依赖业务状态或检查点，而不是把整段任务盲目重跑。

## 什么时候使用

- 核心抽象与任务形态一致。
- 团队能运维它的状态、观测和升级路径。
- 能满足审批、权限、恢复与成本约束。

## 什么时候不要使用

简单的问答或固定三步流程通常无需引入图运行时。不要把每个函数都包装成节点，也不要用循环边掩盖缺失的预算与终止条件。

## Trade-offs

| 获得 | 代价 |
| --- | --- |
| 更清晰地表达目标架构 | 增加建模和治理成本 |
| 复用运行与生态能力 | 接受版本、依赖和迁移成本 |
| 提升自主性或协作能力 | 增加时延、成本与故障面 |

## 产品视角

- **用户与业务问题**：解决哪个可量化瓶颈？
- **产品价值**：提升成功率、速度、可控性还是覆盖范围？
- **用户体验**：进度、等待、切换和失败是否可理解？
- **自主性边界**：哪些判断交给模型，哪些由代码或人决定？
- **数据与权限**：状态、敏感数据和工具权限如何隔离？
- **失败与降级**：能否重试、续跑、切回简单流程或人工处理？
- **产品指标**：完成率、P95 时延、单任务成本、人工介入率、恢复成功率。

## 框架中的对应实现

StateGraph；checkpointer 与 thread；interrupt；streaming；LangSmith 可观测。

## Related Patterns

Workflow、Graph Orchestration、Supervisor、Handoff、Context Isolation、HITL、Durable Execution、Evals。

## 检查清单

- [ ] 产品约束先于实现选择
- [ ] 区分代码控制与模型控制
- [ ] 明确状态事实源、预算和恢复点
- [ ] 覆盖权限、审计和可观测性
- [ ] 记录组织成本与退出方案

## 延伸练习与参考资料

用同一产品场景改画另一种架构，比较运行语义而非 API 长短；继续阅读对应框架的官方架构、持久化、HITL 与观测文档。