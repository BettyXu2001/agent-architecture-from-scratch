---
id: RL07
slug: zh/14-reliability/rl07-multi-agent
order: 1507
section: reliability
status: complete
title: "Multi-Agent Failure Modes"
description: "多个 Agent 新增角色漂移、错误委派、上下文丢失、冲突、群体偏差、级联错误和通信爆炸。"
updated_at: 2026-08-24
lang: zh
module: reliability
prerequisites: [OR07, SC07]
concepts: [reliability, failure, recovery]
example: examples/reliability/fault_injection.py
last_reviewed: 2026-08-24
---

# RL07：Multi-Agent Failure Modes

## 它解决什么问题

多个 Agent 新增角色漂移、错误委派、上下文丢失、冲突、群体偏差、级联错误和通信爆炸。

## 核心定义

Multi-Agent Reliability 同时限制每个 Agent 与协作图：角色契约、ownership、depth、global budget、message schema、conflict handling 和 termination。

## 工作原理

先定义 failure detector、影响范围和可接受终态，再选择 retry、fallback、partial、compensation、human 或 stop。恢复动作本身也受预算、权限和审计约束。

## 架构视图

~~~text
Architecture View
Delegation graph -> local guards + global invariants -> contained result
~~~

~~~text
Product View
Task -> progress -> failure detected -> retry/partial/recover/human
                                   -> clear terminal state + artifacts
~~~

## 最小可运行实践

运行 examples/reliability/fault_injection.py。故障矩阵注入瞬时/永久工具错误、超时、重复 Action、Handoff 环、并行部分失败、重复副作用和 Checkpoint 恢复。

## 正常场景

适用于Supervisor、Handoff、Group Chat 和 Hierarchy。

## 失败与恢复场景

错误 Router 将敏感任务交给无权限 Specialist 时，接收者拒绝且全局重新路由。

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

Supervisor、Handoff、Group Chat 和 Hierarchy。应减少整单失败、重复损失与人工重做。

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
