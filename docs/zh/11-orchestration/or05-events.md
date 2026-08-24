---
id: OR05
title: Event-driven Architecture
lang: zh
status: complete
module: orchestration
prerequisites: [PL06, CM04]
concepts: [orchestration, graph, state]
example: examples/orchestration/orchestration_runtime.py
last_reviewed: 2026-08-24
---

# OR05：Event-driven Architecture

## 它解决什么问题

组件需异步响应已发生事实，且生产者不应等待或知道所有消费者。

## 核心定义

Event-driven 架构以不可变事件驱动独立消费者；事件通过 Log/Broker 投递，State 由消费结果构建。

## 工作原理

节点声明输入、输出、State 读写、副作用、超时和幂等；边声明条件与合法转换。Runtime 记录 node start/result/error、State version 和 terminal reason。

## 架构视图

~~~text
Architecture View
Publisher -> durable event log -> subscribers -> projections/actions
~~~

~~~text
Product View
User goal -> durable task state -> progress/approval -> result
                 | pause/cancel/resume | recover/partial
~~~

## 最小可运行实践

运行 examples/orchestration/orchestration_runtime.py。相同任务分别用 DAG ready queue、有限状态机、条件 Graph、有界循环和 Checkpoint 恢复实现，并注入进程中断与重复事件。

## 正常场景

适用于进度、通知、审计、索引和长任务解耦。

## 失败与恢复场景

重复与乱序通过 event_id、aggregate version、幂等消费者和 dead-letter 处理。

## 什么时候使用

当执行顺序、分支、循环、人工等待或恢复需要成为显式、可测试系统事实时使用。

## 什么时候不要使用

短同步请求和简单线性链无需图引擎；不要把每个函数都变成节点，也不要让框架图替代业务状态设计。

## Trade-offs

显式编排提高可预测、可恢复和可观察性，却增加 State schema、迁移和 Runtime 运维。LLM 路由更灵活，代码/状态机更易验证。

## 产品视角

### 用户与业务问题

编排架构为用户提供可信进度、暂停、取消、审批和恢复，而不是只服务开发者画图。

### 产品价值

进度、通知、审计、索引和长任务解耦。应带来更高恢复率、更短等待或更少人工协调。

### 用户体验

用户状态映射到稳定业务阶段；内部节点可折叠。取消、恢复和审批按钮必须对应真实事件与合法转换。

### 自主性边界

模型只能选择允许边或提出事件，Runtime 验证 guard；终态、高风险边和预算不能由 Prompt 覆盖。

### 数据与权限

Checkpoint 加密并按租户隔离；恢复时重新检查当前权限，不复用过期授权执行后续动作。

### 失败与降级

局部重试、Fallback、补偿、人工处理或从最后安全 Checkpoint 恢复；不确定副作用进入 reconciliation。

### 产品指标

衡量任务成功、恢复成功率、状态停留时间、非法转换、重复副作用、取消生效时间和 P95 端到端延迟。

## 框架中的对应实现

LangGraph 强调 State/Graph/checkpoint，Temporal、Dapr、Restate 等强调 durable workflow；选择取决于恢复和事件语义，不是节点 UI。

## Related Patterns

Workflow Composition、Progress Ledger、State Flow、Reliability、Human Approval。

## 检查清单

- State 是否独立于聊天记录？
- 边与转换是否显式可测试？
- 循环是否有进展与预算？
- 副作用是否幂等或可补偿？
- 重启后能否证明从哪里继续？

## 延伸练习与参考资料

在任意副作用前后注入崩溃，验证恢复不会漏做或重复做。

- [LangGraph：Durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)
- [OpenAI Agents SDK：Running agents](https://openai.github.io/openai-agents-python/running_agents/)
