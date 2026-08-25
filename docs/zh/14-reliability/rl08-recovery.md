---
id: RL08
slug: zh/14-reliability/rl08-recovery
order: 1508
section: reliability
status: complete
title: "Recovery、Checkpoint and Resume"
description: "进程或依赖故障后，从头运行浪费成本且可能重复副作用。"
updated_at: 2026-08-24
lang: zh
module: reliability
prerequisites: [OR07, SC07]
concepts: [reliability, failure, recovery]
example: examples/reliability/fault_injection.py
last_reviewed: 2026-08-24
---

# RL08：Recovery、Checkpoint and Resume

## 它解决什么问题

进程或依赖故障后，从头运行浪费成本且可能重复副作用。

## 核心定义

Recovery 从持久 State、Artifact 和操作记录重建；Checkpoint 是一致快照；Resume 跳过已完成幂等节点并核对不确定操作。

## 工作原理

先定义 failure detector、影响范围和可接受终态，再选择 retry、fallback、partial、compensation、human 或 stop。恢复动作本身也受预算、权限和审计约束。

## 架构视图

~~~text
Architecture View
Checkpoint + event/effect log -> reconcile -> resume plan -> outcome
~~~

~~~text
Product View
Task -> progress -> failure detected -> retry/partial/recover/human
                                   -> clear terminal state + artifacts
~~~

## 最小可运行实践

运行 examples/reliability/fault_injection.py。故障矩阵注入瞬时/永久工具错误、超时、重复 Action、Handoff 环、并行部分失败、重复副作用和 Checkpoint 恢复。

## 正常场景

适用于长任务、审批和远程异步 Agent。

## 失败与恢复场景

Checkpoint schema 升级不兼容时，通过版本迁移或安全终止，不能猜字段。

## 什么时候使用

可靠性不是可选 Pattern；所有上线 Agent 都应按风险选择本文机制，并通过故障注入证明。

## 什么时候不要使用

不要对所有错误统一重试；不要用更大 max_steps 掩盖循环；低风险草稿无需昂贵补偿，但仍需诚实终态。

## Trade-offs

冗余、Checkpoint 和验证提高恢复，却增加延迟、成本与状态；严格 fail-closed 更安全但可能降低可用性。按影响半径分级。

## 产品视角

### 用户与业务问题

可靠性意味着用户不必猜系统是否还在运行、是否做了两次、能否拿回部分成果或继续。

### 产品价值

长任务、审批和远程异步 Agent。应减少整单失败、重复损失与人工重做。

### 用户体验

错误说明发生在哪个业务阶段、已完成什么、是否自动重试、用户能做什么；不要暴露堆栈，也不要假装成功。

### 自主性边界

Agent 可在低风险瞬时错误上有限重试；扩大范围、补偿高风险动作或继续不确定副作用需策略或人工。

### 数据与权限

故障日志和 Checkpoint 同样包含敏感数据，按最小化、加密、TTL 和访问控制处理。

### 失败与降级

提供缓存/备用工具/较小范围/只读/草稿/部分 Artifact/人工等分层降级，并保留来源和缺口。

### 产品指标

观察整单与分步失败率、重复副作用、自动恢复率、MTTR、部分结果采用率、循环率、人工介入和每次恢复成本。

## 框架中的对应实现

SDK 的 max turns/retry/tracing 只是局部能力；幂等、补偿、持久恢复和产品终态必须跨 Runtime 与业务系统设计。

## Related Patterns

Timeout、Idempotency、Durable Execution、Task Cancellation、Evals、HITL。

## 检查清单

- 是否区分瞬时、永久、语义和安全错误？
- 重试是否幂等且有预算？
- 部分成功是否被保留和标注？
- 循环是否通过进展检测而非仅步数？
- 崩溃后副作用能否核对？

## 延伸练习与参考资料

在每个外部调用前后随机崩溃，证明最终不会重复副作用且能给出诚实状态。

- [AWS Builders Library：Timeouts, retries and backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [LangGraph：Durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)
