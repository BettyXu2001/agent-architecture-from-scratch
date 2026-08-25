---
id: cx04-isolation
slug: zh/04-context/cx04-isolation
order: 504
section: context
status: planned
title: "Context Isolation"
description: "多 Agent 共享全部历史会造成角色干扰、敏感数据横向扩散和上下文竞争。"
updated_at: 2026-08-24
---

# CX04：Context Isolation

## 它解决什么问题

多 Agent 共享全部历史会造成角色干扰、敏感数据横向扩散和上下文竞争。

## 核心定义

Context Isolation 为每个角色或子任务创建最小独立视图，只通过受控 Packet、State 或 Artifact 交换必要结果。

## 工作原理

按角色定义可见数据分类与工具；创建 subcontext；输出先清洗再汇入共享层。

## 架构视图

~~~text
Architecture View
Shared goal -> [private A] -> sanitized artifact
            -> [private B] -> sanitized artifact
~~~

~~~text
Product View
User data -> scope/consent -> task context -> result with sources
                | revoke        | correct / inspect
~~~

## 最小可运行实践

运行 examples/context/context_architecture.py 的 isolation 场景，比较全量历史、选择、摘要、Context Packet 与隔离上下文，并检查来源与访问标签。

## 正常场景

财务 Agent 看到金额不见个人备注，写作 Agent 看到汇总不见原始账户。

## 失败与恢复场景

共享缓存错误复用其他用户 Context 时，租户键与访问标签阻断并记录事件。

## 什么时候使用

角色专业化、隐私、提示冲突或上下文容量成为瓶颈时使用。

## 什么时候不要使用

拆分没有数据或专业边界时，隔离只增加协调损失。

## Trade-offs

隔离降低干扰和风险，却需要传递摘要并可能丢失跨域线索。

## 产品视角

### 用户与业务问题

让产品可承诺不同能力只访问必要数据。

### 产品价值

支持专业化同时控制数据影响范围。

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

Multi-Agent、Shared vs Private Memory、Permission Boundary。

## 检查清单

- 每次模型调用为什么能看到这些信息？
- 来源、时间和权限是否保留？
- 摘要能否追溯原文？
- 不同 Agent 是否默认隔离？
- 用户能否排除和纠正数据？

## 延伸练习与参考资料

为两个 Specialist 写 allow/deny 数据矩阵并测试越权。

- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [Anthropic：Building Effective Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
