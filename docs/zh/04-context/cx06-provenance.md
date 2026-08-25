---
id: cx06-provenance
slug: zh/04-context/cx06-provenance
order: 506
section: context
status: planned
title: "Context Provenance and Access Boundary"
description: "Agent 看到一段内容却不知道来源、时间、所有者和可信度，既无法引用，也无法正确执行权限与注入防护。"
updated_at: 2026-08-24
---

# CX06：Context Provenance and Access Boundary

## 它解决什么问题

Agent 看到一段内容却不知道来源、时间、所有者和可信度，既无法引用，也无法正确执行权限与注入防护。

## 核心定义

Provenance 为每个 Context 单元附加 source、owner、timestamp、trust、access_scope 与 transformation；Access Boundary 在装配和工具执行时强制检查。

## 工作原理

摄取时标注来源，转换时保留 lineage，选择时验证主体与目的，输出时生成引用并阻止受限数据外发。

## 架构视图

~~~text
Architecture View
Source -> label -> transform(lineage) -> authorize -> context -> cited output
~~~

~~~text
Product View
User data -> scope/consent -> task context -> result with sources
                | revoke        | correct / inspect
~~~

## 最小可运行实践

运行 examples/context/context_architecture.py 的 provenance 场景，比较全量历史、选择、摘要、Context Packet 与隔离上下文，并检查来源与访问标签。

## 正常场景

结论引用可追溯到原始文档段落，用户撤销数据后后续 Context 不再包含它。

## 失败与恢复场景

网页中的工具指令被标记为 untrusted_content，不能覆盖系统策略或触发外发工具。

## 什么时候使用

使用外部资料、个人/企业数据、跨 Agent 或需要审计的系统必须使用。

## 什么时候不要使用

不要只给整份 Prompt 一个来源标签；粒度过粗无法判断派生内容。

## Trade-offs

细粒度 lineage 增加存储和传递成本，却是引用、删除、权限和安全的基础。

## 产品视角

### 用户与业务问题

用户能理解答案来自哪里，并控制自己的数据。

### 产品价值

提高信任、合规与错误纠正效率。

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

RAG、Prompt Injection Defense、Data Governance、A2A Trust。

## 检查清单

- 每次模型调用为什么能看到这些信息？
- 来源、时间和权限是否保留？
- 摘要能否追溯原文？
- 不同 Agent 是否默认隔离？
- 用户能否排除和纠正数据？

## 延伸练习与参考资料

构造可信规则与不可信网页冲突，验证规则优先且来源可见。

- [LangChain：Multi-agent overview](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [Anthropic：Building Effective Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
