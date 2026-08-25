---
id: cx03-passing
slug: zh/04-context/cx03-passing
order: 503
section: context
status: planned
title: "Context Passing between Components"
description: "组件直接转发整段对话会传播噪声和隐私，也让接收者不知道什么是要求、证据或猜测。"
updated_at: 2026-08-24
---

# CX03：Context Passing between Components

## 它解决什么问题

组件直接转发整段对话会传播噪声和隐私，也让接收者不知道什么是要求、证据或猜测。

## 核心定义

Context Packet 是组件间的结构化交接：task、constraints、inputs、artifacts、provenance、permissions 与 expected_output。

## 工作原理

发送者按契约提取，Runtime 校验大小和权限，接收者只基于 Packet 工作，结果以新 Packet 或 Artifact 返回。

## 架构视图

~~~text
Architecture View
Agent A -> validated Context Packet -> Agent B -> Result Packet
~~~

~~~text
Product View
User data -> scope/consent -> task context -> result with sources
                | revoke        | correct / inspect
~~~

## 最小可运行实践

运行 examples/context/context_architecture.py 的 passing 场景，比较全量历史、选择、摘要、Context Packet 与隔离上下文，并检查来源与访问标签。

## 正常场景

Planner 给研究者任务、范围和来源 ID，不传用户其他对话；研究者返回结论、证据和未解决项。

## 失败与恢复场景

Packet 缺少关键约束时接收者返回 needs_context，而不是猜测；Controller 补充后重试。

## 什么时候使用

跨模块、Agent、进程或信任边界传递任务时使用。

## 什么时候不要使用

同一纯函数内部无需包装复杂 Packet。

## Trade-offs

契约提高隔离与测试，却增加 schema 演进和摘要成本。

## 产品视角

### 用户与业务问题

交接后仍保持目标连续，结果可解释来源。

### 产品价值

减少角色漂移和上下文泄漏。

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

Handoff、Direct Message、A2A Artifact。

## 检查清单

- 每次模型调用为什么能看到这些信息？
- 来源、时间和权限是否保留？
- 摘要能否追溯原文？
- 不同 Agent 是否默认隔离？
- 用户能否排除和纠正数据？

## 延伸练习与参考资料

删除 Packet 中一个必需字段，验证接收者明确拒绝。

- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [Anthropic：Building Effective Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
