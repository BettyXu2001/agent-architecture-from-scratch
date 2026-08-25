---
id: cm04-events
slug: zh/09-communication/cm04-events
order: 1004
section: communication
status: planned
title: "Event / Publish–Subscribe"
description: "组件不应知道所有下游，但任务状态变化需异步通知多个消费者。"
updated_at: 2026-08-24
---

# CM04：Event / Publish–Subscribe

## 它解决什么问题

组件不应知道所有下游，但任务状态变化需异步通知多个消费者。

## 核心定义

Event 是已发生事实；Publisher 写入后由 Broker 分发，Subscriber 独立处理。事件不等于命令，也不保证立即完成。

## 工作原理

通信契约明确 identity、task/correlation ID、schema、delivery、ordering、ack、timeout、authorization 和 retention。接收者验证来源与版本后再更新 State 或执行动作。

## 架构视图

~~~text
Architecture View
Publisher -> Event Log/Broker -> Subscribers
~~~

~~~text
Product View
User request -> reliable internal coordination -> progress/artifact/result
                    | retries hidden but failures visible
~~~

## 最小可运行实践

运行 examples/communication/communication_patterns.py。实验实现 Direct Message、版本化 Shared State、Blackboard、Event Bus 与 Artifact Store，并注入重复、冲突和缺失 Artifact。

## 正常场景

适用于进度、审计、索引与通知等松耦合反应。

## 失败与恢复场景

至少一次投递产生重复副作用时，消费者以 event_id 幂等；乱序时用 aggregate version。

## 什么时候使用

当多个组件跨上下文、进程或时间协作，需要可靠来源、状态或 Artifact 引用时使用本模式。

## 什么时候不要使用

同一进程内的纯函数调用无需消息基础设施；不要用共享聊天替代 State，也不要为低规模系统提前引入消息总线。

## Trade-offs

更强的可靠性、一致性和解耦需要消息 ID、版本、存储与重放成本。同步更直接但耦合等待；异步更弹性但状态更多。

## 产品视角

### 用户与业务问题

通信架构应让产品提供可信进度、部分成果与恢复，而不是把内部消息数量当“智能协作”。

### 产品价值

进度、审计、索引与通知等松耦合反应。带来的用户收益必须体现在等待、恢复或一致性上。

### 用户体验

对用户展示业务状态与 Artifact，不展示内部消息洪流；重试和乱序由系统吸收，无法恢复的缺口要明确。

### 自主性边界

收到消息不等于获准行动；每个消费者按当前身份、策略和 State 重新验证。

### 数据与权限

payload 最小化并带来源、主体和保留期；拓扑上的每条边都是潜在数据边界。

### 失败与降级

重复用幂等吸收，丢失靠重试/重放，冲突靠版本解决；基础设施不可用时保留 outbox 或降级同步路径。

### 产品指标

观察投递延迟、重复率、冲突率、积压、恢复时间、Artifact 缺失率和用户可见失败率。

## 框架中的对应实现

Agent 框架消息对象、图 State、任务队列和事件总线各覆盖不同语义；不要因一个 API 叫 message 就让它承担全部职责。

## Related Patterns

Context Packet、Blackboard、Event-driven Orchestration、A2A Task、Durable Execution。

## 检查清单

- 通信对象是命令、事件、状态还是 Artifact？
- 是否有 ID、来源、版本和权限？
- 重复、丢失、乱序和冲突如何处理？
- 当前事实能否独立于消息重建？
- 用户可见状态是否来自可靠 State？

## 延伸练习与参考资料

为同一协作任务分别实现点对点、共享状态和 Blackboard，比较恢复路径。

- [A2A：Core concepts](https://a2a-protocol.org/latest/topics/key-concepts/)
- [LangGraph：Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
