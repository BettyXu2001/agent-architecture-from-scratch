---
id: mm07-artifact
slug: zh/05-memory/mm07-artifact
order: 607
section: memory
status: planned
title: "Artifact / Workspace as Memory"
description: "长任务的大文件和中间成果不适合反复塞进消息，也不应被自由摘要替代。"
updated_at: 2026-08-24
---

# MM07：Artifact / Workspace as Memory

## 它解决什么问题

长任务的大文件和中间成果不适合反复塞进消息，也不应被自由摘要替代。

## 核心定义

Artifact Workspace 保存文档、表格、代码和报告等可寻址成果；Context 只传引用、摘要和所需片段。 Memory 与 Context 的边界是：Memory 是可被保存和检索的信息，Context 是某次调用实际可见的视图。

## 工作原理

为每条记录定义 owner、type、source、created_at、valid_until、confidence、access_scope 和 version。写入、读取、纠正与删除分别通过策略门。

## 架构视图

~~~text
Architecture View
Agent -> artifact store(versioned) -> reference -> other agent/user
~~~

~~~text
Product View
User action -> memory notice/control -> personalized work -> inspect/correct/delete
~~~

## 最小可运行实践

运行 examples/memory/memory_architecture.py，观察工作记忆、情节、语义、私有/共享记录和 Artifact 引用如何通过统一策略读写。

## 正常场景

支持长任务、协作、恢复与用户交付。检索结果保留来源，并只在当前任务和主体权限匹配时进入 Context。

## 失败与恢复场景

覆盖版本或引用失效时，使用不可变版本、内容哈希、权限和 lineage 恢复。

## 什么时候使用

当跨步骤或跨任务保留信息能带来可测成功率、连续性或恢复收益，并且可以定义所有者与生命周期时使用。

## 什么时候不要使用

单次任务不需长期记忆；敏感内容、未经确认推断和可从权威源实时获得的信息不应默认永久保存。

## Trade-offs

更多记忆提高连续性，却增加错误固化、隐私、检索噪声与治理成本。宁可少而可解释，也不要无限积累。

## 产品视角

### 用户与业务问题

产品应明确“为什么记住、记住多久、用于什么”，而不是把 Memory 当神秘个性化。

### 产品价值

支持长任务、协作、恢复与用户交付，并通过与无记忆基线对比验证。

### 用户体验

用户可查看、纠正、删除和关闭记忆；系统引用记忆影响重要结果时应给出来源或提示。

### 自主性边界

低风险临时状态可自动写；长期偏好、敏感事实和可执行 Skill 需要更严格验证或确认。

### 数据与权限

按主体、租户、角色和用途隔离；共享、外发与训练用途不得由一次任务授权自动推导。

### 失败与降级

检索不确定时忽略或询问；冲突时优先权威新来源；Memory 服务不可用时回到无记忆模式。

### 产品指标

衡量记忆命中后的成功提升、错误记忆率、纠正率、删除生效率、检索延迟和用户关闭率。

## 框架中的对应实现

向量库、数据库、Session Store 和文件工作区分别适合不同类型；Memory 架构不能简化为“接一个向量库”。

## Related Patterns

Context Selection、Progress Ledger、Shared State、Artifact、Data Governance。

## 检查清单

- 记录类型、所有者和生命周期是否明确？
- 写入是否经过验证？
- 检索是否检查权限与相关性？
- 用户能否查看、纠正和删除？
- 失败时能否无记忆降级？

## 延伸练习与参考资料

为同一条信息设计工作、情节和语义三种表示，比较错误影响半径。

- [CoALA：Cognitive Architectures for Language Agents](https://arxiv.org/abs/2309.02427)
- [LangGraph Memory](https://docs.langchain.com/oss/python/langgraph/add-memory)
