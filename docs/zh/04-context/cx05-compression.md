---
id: cx05-compression
order: 505
section: context
status: planned
title: "Context Compression and Summarization"
description: "长任务轨迹不断增长，成本上升且早期约束可能被挤出。Compression 将历史转成可继续工作的紧凑状态。"
updated_at: 2026-08-24
---

# CX05：Context Compression and Summarization

## 它解决什么问题

长任务轨迹不断增长，成本上升且早期约束可能被挤出。Compression 将历史转成可继续工作的紧凑状态。

## 核心定义

Compression 是有损或无损缩减；Summarization 是语义压缩。可靠摘要应分离事实、决策、约束、未解决项和 Artifact 引用。

## 工作原理

固定保留目标和安全约束，按阶段将旧轨迹压缩，记录覆盖范围与原始引用，并对关键字段做确定性校验。

## 架构视图

~~~text
Architecture View
Long trace -> structured compactor -> summary + references -> next context
~~~

~~~text
Product View
User data -> scope/consent -> task context -> result with sources
                | revoke        | correct / inspect
~~~

## 最小可运行实践

运行 examples/context/context_architecture.py 的 compression 场景，比较全量历史、选择、摘要、Context Packet 与隔离上下文，并检查来源与访问标签。

## 正常场景

研究完成一个阶段后，仅保留结论、证据 ID、失败查询与后续问题。

## 失败与恢复场景

摘要把“不得发布”压成“准备发布”时，固定约束校验发现冲突并拒绝替换。

## 什么时候使用

长对话、长任务和多轮工具轨迹接近预算时使用。

## 什么时候不要使用

法律文本、数值和权限不能只保留自由摘要；必须保留原文引用。

## Trade-offs

显著省 Token，却引入语义漂移；频繁压缩也会增加调用。

## 产品视角

### 用户与业务问题

使长任务保持连贯且响应不随历史无限变慢。

### 产品价值

延长任务跨度并稳定成本。

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

Progress Ledger、Memory、Provenance。

## 检查清单

- 每次模型调用为什么能看到这些信息？
- 来源、时间和权限是否保留？
- 摘要能否追溯原文？
- 不同 Agent 是否默认隔离？
- 用户能否排除和纠正数据？

## 延伸练习与参考资料

对包含否定约束的轨迹压缩，并验证固定字段不变。

- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [Anthropic：Building Effective Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
