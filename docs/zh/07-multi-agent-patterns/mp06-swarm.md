---
id: mp06-swarm
order: 806
section: multi-agent-patterns
status: planned
title: "Swarm"
description: "中心 Supervisor 可能成为瓶颈；在角色网络中，当前 Agent 可更快判断应该把控制交给哪个邻居。"
updated_at: 2026-08-24
---

# MP06：Swarm

## 它解决什么问题

中心 Supervisor 可能成为瓶颈；在角色网络中，当前 Agent 可更快判断应该把控制交给哪个邻居。

## 核心定义

Swarm 是基于局部 Handoff 的去中心化协作：Agent 知道有限邻居并可转移控制，没有单一 Agent 规划全部路径；共享 Runtime 仍负责预算和安全。

## 工作原理

每个角色声明可交接邻居、条件和输出；全局层记录路径、visited、预算和终止，防止局部决定形成环。

## 架构视图

~~~text
Architecture View
A <-> B <-> C
|     local handoff | + global runtime/termination
~~~

~~~text
Product View
User -> one request -> capability changes as needed -> active specialist result
~~~

## 最小可运行实践

运行 examples/multi-agent/patterns.py 的 swarm 场景。相同客服任务分别采用 Manager、Router+Parallel、Handoff、Selector Group Chat、Swarm 与 Hybrid，Trace 明确记录控制权、发言者和终止原因。

## 正常场景

旅行 Agent 转给航班，再转酒店，最后由行程 Agent收束，路径随用户需求变化。

## 失败与恢复场景

局部 Agent 只看到邻居而把任务绕圈；全局 visited+edge budget 返回协调者或人工。

## 什么时候使用

路由高度动态、角色能基于局部状态可靠交接、中心规划成本高时使用。

## 什么时候不要使用

任务需要全局最优依赖、统一合成或高风险集中审批时不要去中心化。

## Trade-offs

扩展灵活、局部上下文小，却更难预测路径、解释责任和保证终止。

## 产品视角

### 用户与业务问题

跨领域请求可自然流转，无需回到入口反复路由。

### 产品价值

降低中心瓶颈并支持角色网络扩展。

### 用户体验

始终显示当前负责能力与返回入口，避免用户感觉被踢来踢去。

### 自主性边界

控制权转移必须是显式状态；任何 Agent 的工具权限、委派目标、步骤和全局预算均由 Runtime 强制。

### 数据与权限

每次调用或转移只传完成目标所需的 Context Packet；Handoff 前重新计算数据范围，不默认转发完整历史。

### 失败与降级

超时、无人可处理、发言循环或 Specialist 失败时，回到协调者、有限路由、部分结果或人工；保留已产生 Artifact。

### 产品指标

比较任务成功率、路由/转移正确率、轮数、协调 Token、P95 延迟、部分失败恢复率、用户重复描述率和单成功任务成本。

## 框架中的对应实现

AutoGen Swarm 和基于 handoff 的自定义网络最接近；名字不代表没有全局 Runtime。

## Related Patterns

Handoff、Peer-to-Peer、Graph、Distributed Agents。

## 检查清单

- 当前控制权属于谁？
- 谁可以直接回复用户？
- Context 在调用或转移时如何裁剪？
- 是否有全局终止与委派预算？
- 冲突和部分失败由谁处理？

## 延伸练习与参考资料

构造三节点环并验证全局运行时而非 Prompt 终止。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [LangChain：Multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [AutoGen：AgentChat teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
