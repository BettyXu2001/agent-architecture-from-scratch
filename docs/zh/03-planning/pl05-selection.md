---
id: pl05-selection
slug: zh/03-planning/pl05-selection
order: 405
section: planning
status: planned
title: "Plan Selection and Validation"
description: "Planner 给出的第一份计划可能不可执行、过贵或忽略关键约束。执行前需要硬校验，必要时比较候选。"
updated_at: 2026-08-24
---

# PL05：Plan Selection and Validation

## 它解决什么问题

Planner 给出的第一份计划可能不可执行、过贵或忽略关键约束。执行前需要硬校验，必要时比较候选。

## 核心定义

Validation 检查能力、依赖、预算、权限和覆盖等硬约束；Selection 在多个合法候选中按质量、成本和风险选择。两者不能只交给同一语言判断。

## 工作原理

先用确定性规则淘汰非法计划，再用评分或模型评价软指标；评分包含估算不确定性，并保留选择理由。

## 架构视图

~~~text
Architecture View
Candidate plans -> hard validator -> feasible set -> scorer -> chosen plan
~~~

~~~text
Product View
Goal -> proposed plan -> progress ledger -> result
          | edit/approve    | pause/retry/replan
~~~

## 最小可运行实践

运行 examples/planning/planning_system.py 的 selection 场景。实验用确定性 Planner 和 Executor 展示计划 schema、依赖、状态、重规划与预算，不依赖模型 API。

## 正常场景

两个合法研究计划中，系统选择覆盖相同但调用更少的方案，并保留高风险步骤的审批。

## 失败与恢复场景

候选都违反预算时返回 infeasible 和需要用户选择的范围，不自动降低核心质量要求。

## 什么时候使用

计划成本高、风险大、选择对结果影响显著，或 Planner 经常生成非法步骤时使用。

## 什么时候不要使用

低成本短任务不需要多候选搜索；没有可靠评分时不要伪造精确最优。

## Trade-offs

候选增加方案质量也成倍增加规划成本；硬约束安全但可能排除创造性路径。

## 产品视角

### 用户与业务问题

让产品在执行前给出范围、预计成本和关键风险，并允许用户选速度或质量。

### 产品价值

减少执行到一半才发现不可行的浪费。

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

结构化输出配合普通验证器即可；高级候选搜索可放到 Tree Search 等扩展。

## Related Patterns

Architecture Decision、Budget、Approval、Advanced Search。

## 检查清单

- 计划是否是结构化、可验证的 State？
- 每项是否有依赖、完成定义与产物？
- Planner 能否修改已完成事实？
- 是否区分失败重试与目标重规划？
- 用户看到的进度是否可信？

## 延伸练习与参考资料

设计 fast、balanced、thorough 三个候选并用同一约束集筛选。

- [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)
- [ReAct](https://arxiv.org/abs/2210.03629)
- [LangGraph：Plan-and-execute tutorial](https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/)
