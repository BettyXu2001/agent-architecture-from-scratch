---
id: RS06
slug: zh/17-real-system/rs06-supervisor
order: 1806
section: real-system
status: complete
title: "版本 6：Supervisor 与 Specialist Agents"
description: "当研究、数据分析、风险判断和编辑需要不同工具、提示、权限与评估标准时，单 Agent 的上下文和权限过宽。Supervisor 负责分解、委派、合并和预算，Specialist 只完成边界清晰的专业任务。"
updated_at: 2026-08-25
lang: zh
module: 17-real-system
prerequisites: [Part 0, Part 6, Part 11]
concepts: [supervisor,specialists,multi-agent]
example: enterprise-research
last_reviewed: 2026-08-25
---

# 版本 6：Supervisor 与 Specialist Agents

> 用能力边界拆分复杂任务，而不是用角色数量制造复杂度。

## 它解决什么问题

当研究、数据分析、风险判断和编辑需要不同工具、提示、权限与评估标准时，单 Agent 的上下文和权限过宽。Supervisor 负责分解、委派、合并和预算，Specialist 只完成边界清晰的专业任务。

## 核心定义与工作原理

团队包含 Research Specialist、Data Specialist、Risk Specialist 和 Editor。Supervisor 通过任务契约委派，不共享完整对话；每个专家拥有最小工具权限和私有工作区，只返回 artifact、摘要、证据与置信度。Supervisor 不代替质量门，也不能无限转派。

### 架构视图（Architecture View）

分析时固定追问：谁拥有控制权，状态存在哪里，模型能决定什么，失败从哪里恢复，人工在哪个边界介入，运行证据如何被观察。

### 产品视图（Product View）

对用户可保持一个统一助手，也可展示“研究/风险/编辑”阶段。价值来自专业质量、权限隔离和独立迭代；指标包括委派准确率、专家一次通过率、跨 Agent 消息量、合并冲突率与总成本。

## 简单实践

为四个专家制作 capability card：输入、输出、工具、数据范围、SLA 和拒绝条件。推演 Supervisor 错派给 Data Specialist 后如何退回并改派，而不丢失任务账本。

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

仅靠不同人设、但使用相同模型、工具和上下文时，不需要多 Agent。不要让 Supervisor 成为所有信息的巨大瓶颈，也不要让子 Agent 相互调用形成不可见网络。

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

Supervisor/manager；agents-as-tools；capability registry；private context；artifact contract；delegation ledger。

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