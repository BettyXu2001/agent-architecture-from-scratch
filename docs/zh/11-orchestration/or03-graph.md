---
id: OR03
slug: zh/11-orchestration/or03-graph
order: 1203
section: orchestration
status: complete
title: "Graph"
description: "Agent 流程包含条件分支、回边和动态路径，DAG 不足以表达。"
updated_at: 2026-08-24
lang: zh
module: orchestration
prerequisites: [PL06, CM04]
concepts: [orchestration, graph, state]
example: examples/orchestration/orchestration_runtime.py
last_reviewed: 2026-08-24
---

# OR03：Graph

## 它解决什么问题

Agent 流程包含条件分支、回边和动态路径，DAG 不足以表达。

## 核心定义

Graph 允许条件边与循环；State 和路由函数共同决定下一节点，每条回边必须有终止语义。

## 工作原理

节点声明输入、输出、State 读写、副作用、超时和幂等；边声明条件与合法转换。Runtime 记录 node start/result/error、State version 和 terminal reason。

## 架构视图

~~~text
Architecture View
State -> node -> conditional edge -> node/END
~~~

~~~text
Product View
User goal -> durable task state -> progress/approval -> result
                 | pause/cancel/resume | recover/partial
~~~

## 最小可运行实践

运行 examples/orchestration/orchestration_runtime.py。相同任务分别用 DAG ready queue、有限状态机、条件 Graph、有界循环和 Checkpoint 恢复实现，并注入进程中断与重复事件。

## 正常场景

适用于规划、工具、评价和人工节点的可组合运行。

## 失败与恢复场景

状态与消息混在一起导致路由不可重现时，定义 typed State 与纯路由函数。

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

规划、工具、评价和人工节点的可组合运行。应带来更高恢复率、更短等待或更少人工协调。

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
