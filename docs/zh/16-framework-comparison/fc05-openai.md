---
id: FC05
title: OpenAI Agents SDK：轻量 Agent、工具与 Handoff
lang: zh
status: complete
module: 16-framework-comparison
prerequisites: [Part 0, Part 6, Part 11]
concepts: [openai-agents-sdk,handoff,agents-as-tools,guardrails]
example: framework-comparison
last_reviewed: 2026-08-25
---

# OpenAI Agents SDK：轻量 Agent、工具与 Handoff

> 理解以少量核心原语组织 Agent 产品的方法。

## 它解决什么问题

OpenAI Agents SDK 以 Agent、tools、handoffs、guardrails、sessions 和 tracing 为核心。它不强迫使用图；团队可以让代码决定编排，也可让模型在工具调用和 Handoff 中决定下一步。

## 核心定义与工作原理

有两种关键协作：Manager 把专家当工具调用，始终保留用户会话控制权；Handoff 把当前回合控制权交给另一 Agent。代码驱动适合确定的顺序与并行，LLM 驱动适合输入难预判的路由。Guardrail 应围绕输入、输出和工具边界配置。

### 架构视图（Architecture View）

分析时固定追问：谁拥有控制权，状态存在哪里，模型能决定什么，失败从哪里恢复，人工在哪个边界介入，运行证据如何被观察。

### 产品视图（Product View）

轻量原语有利于快速上线和渐进增强。产品重点是何时展示专家切换、Handoff 后历史是否连续、Guardrail 拒绝如何解释，以及 trace 是否足以支持客服定位。

## 简单实践

为报告助手各画一个版本：Manager 调用 research_agent 与 risk_agent 后统一答复；Triage Agent 根据请求 Handoff 给研究或合规专家。写出用户看到的身份、上下文传递和返回主 Agent 的规则。

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

需要复杂持久状态图、跨日恢复和大量人工节点时，仅靠轻量 Runner 可能需要自建更多基础设施。不要把 Handoff 当普通函数调用，也不要让工具权限随 Agent 名称自动继承。

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

Agent、Runner、function tools、agents-as-tools、handoffs、guardrails、sessions、tracing。

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