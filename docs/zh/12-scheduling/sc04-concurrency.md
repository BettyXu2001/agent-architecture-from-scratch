---
id: SC04
slug: zh/12-scheduling/sc04-concurrency
order: 1304
section: scheduling
status: complete
title: "Parallelism and Concurrency Limits"
description: "无限并行会触发模型限流、数据库压力和成本峰值；过低并发又浪费时间。"
updated_at: 2026-08-24
lang: zh
module: coordination-scheduling
prerequisites: [PL04, MA06]
concepts: [coordination, scheduling, task]
example: examples/scheduling/task_board.py
last_reviewed: 2026-08-24
---

# SC04：Parallelism and Concurrency Limits

## 它解决什么问题

无限并行会触发模型限流、数据库压力和成本峰值；过低并发又浪费时间。

## 核心定义

Parallelism 是可同时执行的独立工作；Concurrency Limit 是按全局、租户、Agent、工具或资源设置的在途上限。

## 工作原理

任务包含稳定 ID、依赖、要求、priority、deadline、budget、attempt 和 cancellation token。调度与分配写入版本化 State，Worker 使用 lease 防止重复领取。

## 架构视图

~~~text
Architecture View
Task DAG -> semaphores/pools -> workers -> join
~~~

~~~text
Product View
User submits -> admitted/queued -> progress/ETA -> result
                 | reprioritize/cancel | partial/failure
~~~

## 最小可运行实践

运行 examples/scheduling/task_board.py。实验实现依赖 ready queue、能力匹配、优先级与 aging、并发限制、Backpressure、冲突解决和取消传播。

## 正常场景

适用于独立耗时任务与有限资源。

## 失败与恢复场景

重试风暴占满并发时区分新请求/重试池并加入指数退避与 jitter。

## 什么时候使用

当任务数量、依赖、执行者或资源限制使简单循环无法满足 SLA 和取消承诺时使用。

## 什么时候不要使用

单用户短任务无需复杂队列；不要用调度器修复不可分解任务，也不要把模型自报优先级直接用于资源政策。

## Trade-offs

更高利用率与公平性需要排队状态、配额和预测；并行降低墙钟时间但增加资源峰值；严格背压保护系统却会拒绝部分用户请求。

## 产品视角

### 用户与业务问题

产品要承诺何时开始、为何等待、能否加急和取消，而不是只显示“Agent 正在工作”。

### 产品价值

独立耗时任务与有限资源。带来的价值应表现为更短等待、更高 SLA 或更少资源浪费。

### 用户体验

展示 queued/running/blocked/partial/completed 等真实状态与粗粒度 ETA；取消和优先级变更必须确认是否已生效。

### 自主性边界

Agent 可建议任务分解和候选执行者，Scheduler 依据配额、权限、成本和业务等级作最终决定。

### 数据与权限

任务只能分配给有数据域权限的 Agent；队列 payload 最小化、加密并有 TTL。

### 失败与降级

重试使用预算和退避；容量不足时降级模型/范围、延迟执行或明确拒绝；取消向下传播并处理在途副作用。

### 产品指标

观察排队时间、完成时间、并发利用率、饥饿率、拒绝率、取消滞后、重复执行和 SLA 达成率。

## 框架中的对应实现

Agent 框架负责决策，任务队列/工作流引擎负责 lease、并发和恢复；不要用群聊消息充当生产调度器。

## Related Patterns

Task Graph、Parallelization、Event-driven、Durable Execution、Reliability。

## 检查清单

- ready 的定义是否来自依赖 State？
- 分配是否同时检查能力和权限？
- 是否有全局/租户/工具并发限制？
- 背压时产品如何承诺？
- 取消是否传播到在途与后代任务？

## 延伸练习与参考资料

在低容量下同时提交不同优先级任务，验证高优先、aging、公平与取消。

- [Temporal：Task Queues](https://docs.temporal.io/task-queue)
- [Google Cloud：Backpressure overview](https://cloud.google.com/pubsub/docs/flow-control-messages)
