---
id: augmented-llm-to-distributed-system
order: 120
section: overview
status: planned
title: "从 Augmented LLM 到 Distributed Agent System"
description: "团队常把 RAG、工具、Memory、Multi-Agent 和 A2A 一次塞入方案，在需求尚未验证时就承担分布式系统成本。本章用复杂度阶梯回答：下一层到底新增什么能力与责任？"
updated_at: 2026-08-24
---

# OV03：从 Augmented LLM 到 Distributed Agent System

## 它解决什么问题

团队常把 RAG、工具、Memory、Multi-Agent 和 A2A 一次塞入方案，在需求尚未验证时就承担分布式系统成本。本章用复杂度阶梯回答：下一层到底新增什么能力与责任？

## 核心定义

~~~text
L0 LLM Call              生成或判断
L1 Augmented LLM         + retrieval / tools / memory
L2 Workflow              + predefined control flow
L3 Single Agent          + model-directed next action
L4 Planned Agent         + explicit plan / replan / ledger
L5 Multi-Agent           + role and context boundaries
L6 Orchestrated System   + graph / events / durable state
L7 Distributed Agents    + discovery / identity / protocol / network
~~~

这是能力与责任阶梯，不是成熟度排行榜。一个 L2 系统可能比 L6 系统创造更高的产品价值。

## 工作原理

| 升级 | 触发条件 | 新增状态 | 新增失败 |
|---|---|---|---|
| L0→L1 | 模型缺知识或行动能力 | 检索、工具结果 | 错误来源、工具异常 |
| L1→L2 | 任务需要稳定多步处理 | 步骤与分支 | 错误传播 |
| L2→L3 | 路径无法预先枚举 | 轨迹与预算 | 循环、误操作 |
| L3→L4 | 长任务需要依赖与重规划 | 计划、进度账本 | 计划过期 |
| L4→L5 | 单一上下文或角色成为瓶颈 | 消息、角色、归属 | 协调和级联错误 |
| L5→L6 | 任务跨等待、重启或复杂循环 | checkpoint、事件 | 恢复不一致 |
| L6→L7 | 能力跨团队、进程或厂商 | 身份、远程任务 | 网络、信任、SLA |

## 架构视图

~~~text
Architecture View
Capability -> Control -> Autonomy -> Planning -> Topology -> Runtime -> Network
    L1          L2          L3          L4          L5         L6        L7
~~~

~~~text
Product View
User goal -> answer -> stages -> dynamic progress -> editable plan
          -> unified result -> pause/resume -> external responsibility
~~~

## 最小可运行实践

使用 examples/overview/architecture_decision.py 给五类任务打分，并记录“为什么不能停在更简单一层”。若理由只有“更先进”或“框架支持”，升级不成立。

## 正常场景

深度研究从带搜索的 L1 开始；固定研究流程可提升到 L2；查询方向依赖中间发现时进入 L3；任务跨度大且需要重规划时进入 L4；只有专业上下文隔离或并行带来收益时才进入 L5。

## 失败与恢复场景

过度设计表现为调用数上升、等待变长、结果归属不清和难以复现。恢复方式是沿阶梯回退：远程能力改本地工具，多 Agent 合并为模块化单 Agent，动态路由改有限分类，长循环改明确 Workflow。

## 什么时候使用

在架构评审、MVP 切分、能力演进和故障复盘时使用复杂度阶梯，为每次升级附上用户价值、状态变化和运维成本。

## 什么时候不要使用

不要用层级直接估算质量，也不要认为所有产品最终都应达到 L7。阶梯无法替代具体的数据、权限和部署设计。

## Trade-offs

更高层获得长任务、长尾和组织扩展能力，同时增加延迟、成本、状态空间、权限面和故障组合。并行可能降低墙钟时间，却增加总资源；分布式可以解耦团队，却放大身份和版本治理。

## 产品视角

### 用户与业务问题

产品路线图应从“当前用户任务在哪一层失败”出发，避免把技术层级当卖点。

### 产品价值

每次升级至少绑定一个指标假设：覆盖更多任务、减少操作、缩短时间、提高质量或支持跨系统协作。

### 用户体验

系统越复杂，越需要暴露目标、阶段、可验证中间成果和真实恢复状态；内部拓扑不必直接展示。

### 自主性边界

能力扩大不等于权限扩大。跨层升级必须重新评估动作风险和人工确认点。

### 数据与权限

从 L5 开始明确上下文在角色间的流动；L7 还要明确远程主体、数据责任和留存边界。

### 失败与降级

为每层设计向下一层回退的路径，并确保已完成 Artifact 可继续使用。

### 产品指标

按层比较任务成功率、端到端耗时、P95 延迟、人工介入率、恢复率和单成功任务成本。

## 框架中的对应实现

多数 Agent 框架横跨多个层级：LangGraph 可表达 L2–L6，OpenAI Agents SDK 可表达 L3–L6，AutoGen 强调 L5–L6，MCP 和 A2A 分别处理能力边界与远程 Agent 互操作。先确定层级需求，再选择实现。

## Related Patterns

前置：Agent vs Workflow。组合：Planning、Supervisor、Graph、Durable Execution、MCP、A2A。

## 检查清单

- 当前层的结构性限制是什么？
- 升级增加了什么显式状态？
- 新失败能否检测与恢复？
- 用户能感知什么新增价值？
- 是否存在更低一层的实现？

## 延伸练习与参考资料

画出一个现有 AI 产品的层级，并给每次升级写一条可证伪假设。

- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
- [A2A Core Concepts](https://a2a-protocol.org/latest/topics/key-concepts/)
