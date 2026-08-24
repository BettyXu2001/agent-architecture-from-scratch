---
id: pl03-replanner
order: 403
section: planning
status: planned
title: "Planner–Executor–Replanner"
description: "静态计划遇到新证据、工具失败或目标变化后会失效。Replanner 根据已完成事实更新剩余工作。"
updated_at: 2026-08-24
---

# PL03：Planner–Executor–Replanner

## 它解决什么问题

静态计划遇到新证据、工具失败或目标变化后会失效。Replanner 根据已完成事实更新剩余工作。

## 核心定义

Replanner 读取原目标、当前计划、完成 Artifact、错误与预算，只能修改未完成部分；Controller 决定接受新计划或停止。

## 工作原理

每次重规划标注 trigger、diff 和 rationale。已完成条目不可回退为未完成；新增工作接受预算和权限校验。

## 架构视图

~~~text
Architecture View
Plan -> Execute -> Observe -> continue
  ^                    |
  +---- Replanner <----+ (diff remaining plan)
~~~

~~~text
Product View
Goal -> proposed plan -> progress ledger -> result
          | edit/approve    | pause/retry/replan
~~~

## 最小可运行实践

运行 examples/planning/planning_system.py 的 replanner 场景。实验用确定性 Planner 和 Executor 展示计划 schema、依赖、状态、重规划与预算，不依赖模型 API。

## 正常场景

原计划依赖付费来源，访问失败后 Replanner 选择公开来源，保留已完成数据清洗并继续。

## 失败与恢复场景

Replanner 每轮改写整个计划造成震荡。使用最小 diff、冷却、最大重规划次数和无进展检测停止。

## 什么时候使用

环境不稳定、任务长、失败有替代路径且中间 Artifact 可复用时使用。

## 什么时候不要使用

固定合规流程、目标不可变或无法验证计划变更时不要允许动态重规划。

## Trade-offs

适应性更强，却增加不可预测成本和计划漂移。严格 diff 降低灵活性但便于审计。

## 产品视角

### 用户与业务问题

让长任务遇到障碍时能继续，而不是整单失败或从头开始。

### 产品价值

提高恢复率并减少已完成工作的浪费。

### 用户体验

只展示用户可理解的目标、里程碑、依赖、当前状态和变更原因，不展示私有推理。计划百分比必须来自完成项和已知工作，而不是语言生成。

### 自主性边界

Agent 可调整低风险研究顺序；新增高成本范围、改变用户目标或执行副作用时需要规则限制或确认。

### 数据与权限

计划条目不得成为绕过权限的自由文本。Executor 对每个动作重新鉴权，结果以 Artifact 或结构化 State 保存。

### 失败与降级

单步失败可重试、替换或标记阻塞；重规划保留已完成成果，不静默删除用户要求。预算不足时返回部分成果和剩余计划。

### 产品指标

衡量长任务成功率、计划有效率、重规划率、里程碑按时率、用户改计划比例、浪费步骤和单成功任务成本。

## 框架中的对应实现

LangGraph 条件循环、状态机和 durable workflow 可实现；Replanner 只是决策组件，Runtime 负责持久化。

## Related Patterns

Progress Ledger、Retry/Fallback、Human Approval。

## 检查清单

- 计划是否是结构化、可验证的 State？
- 每项是否有依赖、完成定义与产物？
- Planner 能否修改已完成事实？
- 是否区分失败重试与目标重规划？
- 用户看到的进度是否可信？

## 延伸练习与参考资料

注入工具不可用，验证重规划不重复已完成步骤。

- [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)
- [ReAct](https://arxiv.org/abs/2210.03629)
- [LangGraph：Plan-and-execute tutorial](https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/)
