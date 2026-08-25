---
id: RS04
slug: zh/17-real-system/rs04-planner
order: 1804
section: real-system
status: complete
title: "版本 4：Planner–Executor–Replanner"
description: "当报告跨多个公司、地区和时间段时，单个 ReAct Agent 容易局部探索过深、遗漏任务或重复劳动。Planner 提供全局任务图，Executor 完成原子任务，Replanner 只根据新证据修订未完成部分。"
updated_at: 2026-08-25
lang: zh
module: 17-real-system
prerequisites: [Part 0, Part 6, Part 11]
concepts: [planning,planner-executor,replanner,ledger]
example: enterprise-research
last_reviewed: 2026-08-25
---

# 版本 4：Planner–Executor–Replanner

> 把复杂目标拆成可检查、可并行和可修正的任务计划。

## 它解决什么问题

当报告跨多个公司、地区和时间段时，单个 ReAct Agent 容易局部探索过深、遗漏任务或重复劳动。Planner 提供全局任务图，Executor 完成原子任务，Replanner 只根据新证据修订未完成部分。

## 核心定义与工作原理

计划项包含目标、依赖、期望产物、负责人能力、预算和完成条件。任务账本记录 pending、running、done、failed、blocked。Executor 不得偷偷改计划；Replanner 读取产物和失败原因，保留已验证结果并产生带版本号的增量计划。

### 架构视图（Architecture View）

分析时固定追问：谁拥有控制权，状态存在哪里，模型能决定什么，失败从哪里恢复，人工在哪个边界介入，运行证据如何被观察。

### 产品视图（Product View）

用户可以在执行前确认范围，在过程中查看计划和修改优先级。产品指标增加计划接受率、计划变更次数、重复任务率、阻塞解除率、按期完成率及用户改计划比例。

## 简单实践

把“比较三家供应商并给出进入建议”拆成依赖图。模拟一家缺少数据：标记 blocked，Replanner 将任务改为代理指标研究，并保留其他已完成任务。

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

简单任务的规划成本高于执行时，不应升级。不要生成几十条看似完整但无法验证的计划，也不要每完成一步就无条件重新规划。

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

Planner、Executor、Replanner、task ledger；可映射为状态图、队列任务或层级 Agent，但计划应是独立领域对象。

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