---
id: FC06
title: Google ADK：LLM Agent 与确定性 Workflow Agent
lang: zh
status: complete
module: 16-framework-comparison
prerequisites: [Part 0, Part 6, Part 11]
concepts: [google-adk,workflow-agent,sequential,parallel,loop]
example: framework-comparison
last_reviewed: 2026-08-25
---

# Google ADK：LLM Agent 与确定性 Workflow Agent

> 理解生成式决策与确定性编排在同一体系中的分工。

## 它解决什么问题

Google ADK 区分依赖模型推理的 LLM Agent 与负责确定性控制的 Workflow Agent。Sequential、Parallel、Loop 等组合原语让团队把确定流程写清，再在合适节点引入模型自主性，并可通过多 Agent 和 A2A 扩展。

## 核心定义与工作原理

SequentialAgent 保证子 Agent 顺序，ParallelAgent 同时执行独立分支，LoopAgent 重复直到条件满足。共享 session state 连接阶段，但每个子 Agent 应声明读写字段。LLM Agent 负责语义判断，Workflow Agent 负责时序、并发和边界。

### 架构视图（Architecture View）

分析时固定追问：谁拥有控制权，状态存在哪里，模型能决定什么，失败从哪里恢复，人工在哪个边界介入，运行证据如何被观察。

### 产品视图（Product View）

组合原语容易映射成用户可见进度。面向 Google Cloud 生态的团队还会考虑部署、模型与云服务集成；同时应评估跨云可移植性和 A2A 互操作边界。

## 简单实践

用 Sequential 组织“理解需求→并行研究→编辑→审核”；并行研究由多个子 Agent 执行；审核失败进入最多两轮 Loop。标出循环预算、合并冲突和 session state 字段。

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

如果产品只需一次模型调用，不必建立 Agent 树。不要用 LoopAgent 代替明确重试策略，也不要让并行子 Agent 同时无约束地覆盖同一状态。

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

LlmAgent；SequentialAgent、ParallelAgent、LoopAgent；session state；tools；multi-agent composition 与 A2A。

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