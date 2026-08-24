---
id: pl01-static
order: 401
section: planning
status: planned
title: "Plan-and-Execute"
description: "ReAct 一步一决策容易局部贪心，用户也难以预判长任务范围。Plan-and-Execute 先形成显式步骤，再按计划执行。"
updated_at: 2026-08-24
---

# PL01：Plan-and-Execute

## 它解决什么问题

ReAct 一步一决策容易局部贪心，用户也难以预判长任务范围。Plan-and-Execute 先形成显式步骤，再按计划执行。

## 核心定义

Planner 生成有序、有限、带完成条件的计划；Executor 逐项执行并记录结果。静态版本执行中不改计划，失败由外层策略处理。

## 工作原理

计划至少包含 id、goal、dependencies、status 和 expected_artifact。Controller 校验无环、预算和权限后才开始执行。

## 架构视图

~~~text
Architecture View
Goal -> Planner -> validated plan -> Executor -> artifacts -> Result
~~~

~~~text
Product View
Goal -> proposed plan -> progress ledger -> result
          | edit/approve    | pause/retry/replan
~~~

## 最小可运行实践

运行 examples/planning/planning_system.py 的 static 场景。实验用确定性 Planner 和 Executor 展示计划 schema、依赖、状态、重规划与预算，不依赖模型 API。

## 正常场景

市场研究先确定范围、收集、比较、撰写和校验五步，Executor 顺序产出 Artifact，用户能查看真实完成项。

## 失败与恢复场景

计划包含无法执行的“深入研究”空步骤时，校验器拒绝并要求拆成可判定任务；中途来源不可用则明确阻塞。

## 什么时候使用

任务跨度长、步骤可大致预知、用户需要范围和进度时使用。

## 什么时候不要使用

简单任务、环境变化快或规划成本接近执行成本时，ReAct 或 Workflow 更直接。

## Trade-offs

全局计划提升一致性，却可能在第一步观察后过期；计划越细，管理成本越高。

## 产品视角

### 用户与业务问题

减少用户亲自拆任务，并在长等待前给出范围预期。

### 产品价值

提高长任务可理解性、可暂停性和局部恢复能力。

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

可用普通列表与循环实现；图框架适合计划项形成动态节点时使用。

## Related Patterns

后续 Planner–Executor、Replanner、Dependency Graph。

## 检查清单

- 计划是否是结构化、可验证的 State？
- 每项是否有依赖、完成定义与产物？
- Planner 能否修改已完成事实？
- 是否区分失败重试与目标重规划？
- 用户看到的进度是否可信？

## 延伸练习与参考资料

给每个计划项添加可自动检查的 done 条件。

- [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)
- [ReAct](https://arxiv.org/abs/2210.03629)
- [LangGraph：Plan-and-execute tutorial](https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/)
