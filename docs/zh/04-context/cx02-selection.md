---
id: cx02-selection
order: 502
section: context
status: planned
title: "Context Selection and Progressive Disclosure"
description: "一次给出所有工具说明、文档和历史会稀释当前目标。Progressive Disclosure 按需逐层开放。"
updated_at: 2026-08-24
---

# CX02：Context Selection and Progressive Disclosure

## 它解决什么问题

一次给出所有工具说明、文档和历史会稀释当前目标。Progressive Disclosure 按需逐层开放。

## 核心定义

Selection 决定本轮需要哪些信息；Progressive Disclosure 先提供索引或摘要，只有决策需要时再展开细节。

## 工作原理

先用元数据筛选，再取摘要，最后按明确引用加载原文；每次扩展消耗预算并保留来源。

## 架构视图

~~~text
Architecture View
Catalog -> metadata filter -> summary -> selected full content
~~~

~~~text
Product View
User data -> scope/consent -> task context -> result with sources
                | revoke        | correct / inspect
~~~

## 最小可运行实践

运行 examples/context/context_architecture.py 的 selection 场景，比较全量历史、选择、摘要、Context Packet 与隔离上下文，并检查来源与访问标签。

## 正常场景

Agent 先看到十份合同标题，只展开与当前客户相关的两份条款。

## 失败与恢复场景

摘要遗漏否定条件时，引用校验要求回读原文；不能用摘要直接执行高风险动作。

## 什么时候使用

资料多、工具多、上下文贵或数据敏感时使用。

## 什么时候不要使用

核心约束不能延迟披露；安全规则始终在固定 Context。

## Trade-offs

节省上下文但增加检索轮次；摘要提高速度却可能损失细节。

## 产品视角

### 用户与业务问题

用户获得更快、更相关结果，并可查看真正使用的来源。

### 产品价值

以较低成本扩大可用知识范围。

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

Retrieval、Compression、Provenance。

## 检查清单

- 每次模型调用为什么能看到这些信息？
- 来源、时间和权限是否保留？
- 摘要能否追溯原文？
- 不同 Agent 是否默认隔离？
- 用户能否排除和纠正数据？

## 延伸练习与参考资料

比较全量、摘要和按需展开三种策略的遗漏与成本。

- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [Anthropic：Building Effective Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
