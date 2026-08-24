---
id: system-flows
order: 140
section: overview
status: planned
title: "Control Flow、Data Flow、Context Flow 与 State Flow"
description: "一张“Agent A → Agent B”的箭头图常混合四件事：谁决定调用、传了什么业务数据、模型看到了什么、系统状态如何变化。混在一起后，权限泄漏、恢复错误和结果归属都难以发现。"
updated_at: 2026-08-24
---

# OV05：Control Flow、Data Flow、Context Flow 与 State Flow

## 它解决什么问题

一张“Agent A → Agent B”的箭头图常混合四件事：谁决定调用、传了什么业务数据、模型看到了什么、系统状态如何变化。混在一起后，权限泄漏、恢复错误和结果归属都难以发现。

## 核心定义

| Flow | 回答的问题 | 典型对象 |
|---|---|---|
| Control Flow | 谁决定下一步？ | 分支、循环、调度、审批 |
| Data Flow | 哪些业务数据在哪里移动？ | 文档、记录、工具参数、Artifact |
| Context Flow | 某次模型调用能看到什么？ | 指令、历史、摘要、检索片段 |
| State Flow | 哪些持久事实发生变化？ | task status、plan、budget、checkpoint |

Communication 是载体，Message、Event、Shared State 和 Artifact 都可能承载一种或多种 Flow。

## 工作原理

以“研究并发布报告”为例：Supervisor 决定并行调用研究 Agent 是 Control Flow；原始资料进入解析器是 Data Flow；研究 Agent 只收到问题和相关片段是 Context Flow；任务由 researching 进入 review_pending 是 State Flow。

建议为每条箭头标注 initiator、payload、visibility、state transition 和 failure behavior。

## 架构视图

~~~text
Control: User -> Orchestrator -> Researcher -> Evaluator -> Approval
Data:    Sources -------------> Artifact Store -------------> Publisher
Context: Goal + scoped sources -> Research context -> summary-only review
State:   created -> running -> review_pending -> approved -> published
~~~

~~~text
Product View
User sees: goal -> researching -> draft ready -> approval -> published
Controls:  edit scope / cancel / reject / retry / partial artifact
~~~

## 最小可运行实践

选择一个产品流程建立四列表格。若某条箭头无法说明属于哪个 Flow，就继续拆分；若 State 只存在于消息文本中，为它定义结构化字段。

## 正常场景

客服系统中，Router 的决定属于 Control；订单详情属于 Data；退款 Specialist 只看到必要订单字段属于 Context；案件状态与退款幂等键属于 State。拆开后，可以单独测试数据最小化和状态恢复。

## 失败与恢复场景

典型失败是把聊天历史当 State：重启后无法可靠判断工具是否已执行，重试可能重复退款。应把副作用结果、幂等键、审批和任务状态写入显式 Store，消息只作为输入或审计记录。

另一个错误是把 Context 等同 Data：系统保存完整合同，并不意味着每个 Agent 都应看到完整合同。Context 必须按任务和权限选择。

## 什么时候使用

用于跨 Agent、跨服务、含副作用或需要暂停恢复的系统，也适用于架构评审、隐私评估和 Trace 设计。

## 什么时候不要使用

单次无工具生成无需画四张复杂图，但仍应区分输入数据与模型上下文。不要让图替代字段 schema 和状态机定义。

## Trade-offs

显式分流增加设计和存储成本，却换来可测试性、最小权限、可恢复性和可观测性。过度共享减少传递代码，却增加噪声、泄漏和上下文污染；过度隔离则增加摘要损失与协调成本。

## 产品视角

### 用户与业务问题

四种 Flow 把“系统在做什么、使用了什么、记住了什么”变成可解释的产品承诺。

### 产品价值

它支持准确进度、可靠恢复、数据最小化和清晰审计，降低复杂 Agent 的信任成本。

### 用户体验

用户看到稳定状态和重要 Artifact，不应直接暴露内部消息洪流；每个可取消点必须对应真实控制与状态转换。

### 自主性边界

模型可以建议 Control Flow，Runtime 必须验证权限和合法状态转换。

### 数据与权限

Data Flow 记录数据位置，Context Flow 记录可见范围；二者共同接受数据分类和最小权限约束。

### 失败与降级

恢复以显式 State 和已保存 Artifact 为基础；Context 可重建，副作用不可凭聊天记录猜测。

### 产品指标

观察恢复成功率、重复副作用率、进度准确度、上下文泄漏事件、取消生效率和错误定位时间。

## 框架中的对应实现

LangGraph 的 State/Graph 强调状态与控制；OpenAI Agents SDK 的 Run Items、Handoffs 和 Context 分别承载运行轨迹与上下文；事件编排系统将 Control 与 State 持久化。无论框架如何命名，都应映射回四种 Flow。

## Related Patterns

后续：Context Passing、Shared State、Blackboard、State Machine、Durable Execution、Trace。

## 检查清单

- 每条箭头表示哪一种 Flow？
- 决策者和执行者是否分开？
- 保存的数据与模型可见数据是否分开？
- 关键状态能否在进程重启后恢复？
- 副作用是否有幂等与审计记录？

## 延伸练习与参考资料

为一次失败运行分别重建四种 Flow，判断问题源于错误决策、错误数据、错误上下文还是错误状态。

- [LangGraph：Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
- [OpenAI Agents SDK：Running agents](https://openai.github.io/openai-agents-python/running_agents/)
