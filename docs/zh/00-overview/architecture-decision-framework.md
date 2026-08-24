---
id: architecture-decision-framework
order: 130
section: overview
status: planned
title: "Architecture Decision Framework"
description: "“这个需求要不要 Multi-Agent？”问得太早。正确顺序是先确定任务、验收和风险，再决定控制、推理、上下文、拓扑与运行时。"
updated_at: 2026-08-24
---

# OV04：Architecture Decision Framework

## 它解决什么问题

“这个需求要不要 Multi-Agent？”问得太早。正确顺序是先确定任务、验收和风险，再决定控制、推理、上下文、拓扑与运行时。

## 核心定义

Architecture Decision Framework 是一组有顺序的约束问题：

1. Outcome：完成的定义能否验证？
2. Path：执行路径能否预先枚举？
3. Environment：是否必须观察或改变外部环境？
4. Horizon：任务是否跨多步、长等待或进程重启？
5. Context：一个上下文能否容纳全部工作？
6. Specialization：拆角色是否提高质量或隔离数据？
7. Risk：行动是否可逆，影响范围多大？
8. Economics：新增质量是否覆盖成本与延迟？

## 工作原理

~~~text
Can one model call solve it?
  yes -> LLM feature
  no  -> Is the path enumerable?
          yes -> Workflow
          no  -> Is dynamic action safe and evaluable?
                  no -> Workflow + clarification/human
                  yes -> Single Agent
                         Is context/specialization a proven bottleneck?
                           no -> keep single
                           yes -> Multi-Agent
                                  Need pause/resume or remote ownership?
                                    yes -> durable/distributed runtime
~~~

该流程坚持“复杂度举证责任”：提出升级的人需要说明更简单架构为何失败。

## 架构视图

~~~text
Architecture View
Task properties -> control -> context/topology -> runtime
                -> governance -> measurable hypothesis
~~~

~~~text
Product View
User problem -> success criterion -> acceptable wait/risk
             -> visible control -> fallback promise -> metrics
~~~

## 最小可运行实践

运行 examples/overview/architecture_decision.py。输出给出推荐、触发因素和保护措施。修改 path_known、side_effects 与 long_running，观察建议如何变化。

## 正常场景

对“客服退款”评审：意图分类和政策查询路径可枚举，退款有资金副作用。适合以 Workflow 为骨架，模型负责理解和生成，代码验证政策，人或权限规则批准退款；而不是让自由 Agent 直接操作支付系统。

## 失败与恢复场景

常见失败有三类：用 Demo 成功替代场景集；只比较答案质量而忽略成本与非预期行动；先选框架再反推需求。恢复方法是建立最小基线、离线任务集和 Architecture Decision Record，逐项记录假设、证据与回退条件。

## 什么时候使用

用于新项目方案评审、Workflow 升级 Agent、Single 升级 Multi-Agent、引入长期 Memory 或 Durable Runtime，以及线上成本或故障异常后的架构回退。

## 什么时候不要使用

它不能替代威胁建模、数据合规、容量规划和 API 设计。低成本探索可以先做限时验证，但上线前仍需完成决策记录。

## Trade-offs

严格决策会减慢早期试验，却降低错误复杂度长期固化；基线方案可能在少数长尾任务上较弱，但更容易可靠评价。允许局部 Agent 自主性，通常比把整个产品变成 Agent 更平衡。

## 产品视角

### 用户与业务问题

决策输入应是用户任务和失败代价，不是竞争对手功能清单。

### 产品价值

架构假设必须可验证，例如“动态规划使复杂研究成功率提升 15%，且单成功任务成本不超过基线 1.5 倍”。

### 用户体验

把最长等待、可取消点、审批点、部分结果和人工接管写入方案，而不是上线后补界面。

### 自主性边界

用行动的可逆性、金额、数据敏感度和影响对象决定确认级别。

### 数据与权限

决策记录列出每个组件读取、写入和外发的数据，以及凭据最小作用域。

### 失败与降级

每份决策记录包含回退架构和触发阈值，例如超时后返回草稿、远程服务失败后改本地流程。

### 产品指标

同时衡量成功、时间、成本、修正、介入、非预期行动与恢复率，避免单一答案质量指标。

## 框架中的对应实现

框架调研放在决策末段：先用架构维度过滤，再比较实现成本。代码编排、结构化输出和有限状态通常无需完整 Multi-Agent 框架；长任务恢复和复杂图才更依赖 Runtime。

## Related Patterns

前置：复杂度阶梯。后续：Workflow vs Agent、Multi-Agent Fundamentals、Architecture Comparison。

## 检查清单

- 是否有最简单可用基线？
- 成功和失败能否判定？
- 是否记录升级假设与回退阈值？
- 是否包含风险、数据、延迟和成本？
- 是否在选框架之前确定架构？

## 延伸练习与参考资料

为一个真实需求写一页决策记录，并要求每项新增组件都对应一个失败样本。

- [OpenAI Agents SDK：Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [Anthropic：Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
