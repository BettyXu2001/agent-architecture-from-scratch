---
id: mp05-group-chat
slug: zh/07-multi-agent-patterns/mp05-group-chat
order: 805
section: multi-agent-patterns
status: planned
title: "Round Robin and Selector Group Chat"
description: "一些任务需要多个角色基于彼此结果迭代，而不是独立返回一次；需要定义谁下一位发言。"
updated_at: 2026-08-24
---

# MP05：Round Robin and Selector Group Chat

## 它解决什么问题

一些任务需要多个角色基于彼此结果迭代，而不是独立返回一次；需要定义谁下一位发言。

## 核心定义

Round Robin 按固定顺序轮流；Selector 根据状态动态选择下一发言者。Group Chat 共享消息空间，但必须有唯一终止与最终化机制。

## 工作原理

每轮选择 speaker、构造其可见 Context、记录消息并检查 termination。Round Robin 可预测；Selector 灵活但需防重复和偏置。

## 架构视图

~~~text
Architecture View
Shared thread -> speaker policy -> Agent -> message -> termination
                    ^                         |
~~~

~~~text
Product View
User -> collaborative review -> bounded rounds -> finalizer result
~~~

## 最小可运行实践

运行 examples/multi-agent/patterns.py 的 group-chat 场景。相同客服任务分别采用 Manager、Router+Parallel、Handoff、Selector Group Chat、Swarm 与 Hybrid，Trace 明确记录控制权、发言者和终止原因。

## 正常场景

Writer、Reviewer、Fact Checker 按轮次修订两轮，Finalizer 在全部通过后输出。

## 失败与恢复场景

角色礼貌性复述而无状态变化时，no-progress 检测停止；共享消息过长则转 Artifact+摘要。

## 什么时候使用

工作确实需要互相读取并迭代、发言协议可定义时使用。

## 什么时候不要使用

独立任务用 Parallel；只需中心合成用 Supervisor；高隐私场景避免全共享。

## Trade-offs

协作信息丰富，却最容易产生 Token 洪流、群体偏差和终止困难。

## 产品视角

### 用户与业务问题

适合需要多角度审阅的高价值成果，而不是普通客服。

### 产品价值

通过相互挑战减少单一角色遗漏。

### 用户体验

向用户展示审阅轮次和结论变化，不直播内部全部消息。

### 自主性边界

控制权转移必须是显式状态；任何 Agent 的工具权限、委派目标、步骤和全局预算均由 Runtime 强制。

### 数据与权限

每次调用或转移只传完成目标所需的 Context Packet；Handoff 前重新计算数据范围，不默认转发完整历史。

### 失败与降级

超时、无人可处理、发言循环或 Specialist 失败时，回到协调者、有限路由、部分结果或人工；保留已产生 Artifact。

### 产品指标

比较任务成功率、路由/转移正确率、轮数、协调 Token、P95 延迟、部分失败恢复率、用户重复描述率和单成功任务成本。

## 框架中的对应实现

AutoGen RoundRobinGroupChat、SelectorGroupChat；其他框架可用 speaker policy+shared state 实现。

## Related Patterns

Blackboard、Debate、Evaluator、Termination。

## 检查清单

- 当前控制权属于谁？
- 谁可以直接回复用户？
- Context 在调用或转移时如何裁剪？
- 是否有全局终止与委派预算？
- 冲突和部分失败由谁处理？

## 延伸练习与参考资料

设置最大轮数和无进展哈希，验证群聊一定终止。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：AgentChat teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
