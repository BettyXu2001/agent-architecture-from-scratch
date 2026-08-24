---
id: hy01-supervisor
order: 901
section: hierarchical
status: planned
title: "Hierarchical Supervisor"
description: "单层 Supervisor 的 Worker 太多、上下文过载时，需要把控制分成全局与团队两级。"
updated_at: 2026-08-24
---

# HY01：Hierarchical Supervisor

## 它解决什么问题

单层 Supervisor 的 Worker 太多、上下文过载时，需要把控制分成全局与团队两级。

## 核心定义

层级系统把委派、Context 和预算分布到多个层次。每层只拥有局部任务和明确上级，最终答案、全局策略与总预算仍有唯一责任主体。

## 工作原理

委派契约包含 task_id、parent_id、depth、goal、constraints、budget、done 和 expected_artifact。子层只能从分配预算继续拆分；结果沿父链聚合，错误也必须向上传播。

## 架构视图

~~~text
Architecture View
Global Coordinator -> Team Leads -> Workers -> Leads -> Coordinator
~~~

~~~text
Product View
User goal -> one visible plan -> team milestones -> unified result
              | cancel/approve  | partial failures / escalation
~~~

## 最小可运行实践

运行 examples/hierarchical/hierarchical_system.py。Coordinator 向两个 Team Lead 委派，Team Lead 再调用 Worker；实验验证最大深度、预算守恒、任务去重、局部失败和 Result Packet 聚合。

## 正常场景

按领域建立两层负责人并保持一个最终 Owner。

## 失败与恢复场景

Team Lead 失败时只影响其团队，Coordinator 可返回其他团队成果。

## 什么时候使用

当任务规模、领域数量或上下文确实超过单层 Supervisor，并且能定义稳定团队边界与局部验收时使用。

## 什么时候不要使用

两三个 Specialist 无需层级；职责重叠、任务高度紧耦合或顶层仍需读取全部细节时，层级只会增加延迟。

## Trade-offs

层级扩大管理跨度和 Context 隔离，却增加摘要损失、委派调用、总延迟和故障定位。更深不等于更强；默认限制两层并用数据证明升级。

## 产品视角

### 用户与业务问题

层级应帮助产品完成更大、更长或跨领域任务，而不是向用户展示虚拟组织结构。

### 产品价值

按领域建立两层负责人并保持一个最终 Owner。，并以成功率、并行收益或上下文下降证明价值。

### 用户体验

用户看到目标、团队级里程碑、阻塞和统一结果，不需要阅读内部层级消息；进度基于 Ledger 的完成项。

### 自主性边界

上层分配目标与预算，下层只在局部范围自治；跨团队数据、扩大范围和高风险行动必须向上升级。

### 数据与权限

Context 随层级最小化，凭据不向下复制；结果通过带 provenance 的 Artifact 回传。

### 失败与降级

团队失败可局部重试、替换 Lead、返回部分 Artifact 或扁平化由 Coordinator 接管；全局取消向下传播。

### 产品指标

关注总成功、最长路径延迟、委派深度、重复任务率、团队失败隔离率、聚合遗漏率和总成本。

## 框架中的对应实现

递归 Agent、Supervisor Tree 与 Teams of Teams 可由图或自定义 Runtime 实现；框架提供嵌套不代表应允许无限深度。

## Related Patterns

Supervisor、Task Graph、Context Packet、Scheduling、Durable Execution。

## 检查清单

- 每层任务是否严格更小？
- 全局与局部控制权是否明确？
- 深度和总预算是否由 Runtime 强制？
- 结果是否包含证据、缺口与来源？
- 取消和失败能否跨层传播？

## 延伸练习与参考资料

把两层系统压平成单层并比较调用、Context、延迟和成功率；若无收益，删除层级。

- [AutoGen：Magentic-One](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/magentic-one.html)
- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
