---
id: cx01-engineering
order: 501
section: context
status: planned
title: "Context Engineering for Agent Systems"
description: "模型不是缺少所有信息，而是缺少当前决策所需的正确信息。把全部历史塞入上下文会引入噪声、泄漏和成本。"
updated_at: 2026-08-24
---

# CX01：Context Engineering for Agent Systems

## 它解决什么问题

模型不是缺少所有信息，而是缺少当前决策所需的正确信息。把全部历史塞入上下文会引入噪声、泄漏和成本。

## 核心定义

Context Engineering 是为每次决策选择、组织、标注和限制可见信息的系统策略。Context 是运行时视图，不等于数据库、State 或 Memory。

## 工作原理

从 goal、role、step、permissions 和 budget 生成需求，再从 State、Memory、Artifacts 与 Retrieval 选择内容，最后按优先级装配并记录 provenance。

## 架构视图

~~~text
Architecture View
State/Memory/Artifacts -> policy + selector -> context view -> model
~~~

~~~text
Product View
User data -> scope/consent -> task context -> result with sources
                | revoke        | correct / inspect
~~~

## 最小可运行实践

运行 examples/context/context_architecture.py 的 engineering 场景，比较全量历史、选择、摘要、Context Packet 与隔离上下文，并检查来源与访问标签。

## 正常场景

研究 Agent 只获得目标、当前计划项、相关来源和预算，而不是其他 Specialist 的全部聊天。

## 失败与恢复场景

无关历史挤掉关键约束时，按优先级重建 Context，并把约束作为结构化固定区。

## 什么时候使用

多步、长任务、多数据源或多 Agent 系统都应使用。

## 什么时候不要使用

单次短请求无需复杂流水线，但仍要遵守权限。

## Trade-offs

精确选择提高信噪比却可能遗漏；全量传递简单却昂贵且危险。

## 产品视角

### 用户与业务问题

让 AI 在正确数据范围内稳定完成任务，而不是偶尔想起关键信息。

### 产品价值

提高质量、降低 Token 和数据风险。

### 用户体验

用户应知道系统使用了哪些来源、个人数据和时间范围，并能纠正、排除或撤回；内部 Token 管理不应转嫁给用户。

### 自主性边界

Agent 可在授权范围内选择相关内容，扩大数据源、跨角色共享或外发数据必须受策略和确认控制。

### 数据与权限

Context 构建执行最小化、目的限制、来源标记和访问检查；保存数据不等于允许所有组件查看。

### 失败与降级

来源缺失时请求补充；超窗时优先保留目标、约束和证据；压缩不可信时返回缺口或回退原文校验。

### 产品指标

观察任务成功率、来源命中率、上下文利用率、遗漏关键约束率、数据越界事件、纠正率与 Token 成本。

## 框架中的对应实现

Context API、图状态和 Agent handoff 都只是载体；关键是选择策略、Packet 契约、隔离与来源边界能够独立测试。

## Related Patterns

Selection、Passing、Isolation、Memory Retrieval。

## 检查清单

- 每次模型调用为什么能看到这些信息？
- 来源、时间和权限是否保留？
- 摘要能否追溯原文？
- 不同 Agent 是否默认隔离？
- 用户能否排除和纠正数据？

## 延伸练习与参考资料

记录每段 Context 的来源和使用理由，删除无法解释的部分。

- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [Anthropic：Building Effective Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
