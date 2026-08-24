---
id: pl04-dependency
order: 404
section: planning
status: planned
title: "Task Decomposition and Dependency Graph"
description: "任务列表只表达顺序，无法说明哪些工作可并行、哪些结果阻塞后续，也无法可靠传播取消。"
updated_at: 2026-08-24
---

# PL04：Task Decomposition and Dependency Graph

## 它解决什么问题

任务列表只表达顺序，无法说明哪些工作可并行、哪些结果阻塞后续，也无法可靠传播取消。

## 核心定义

Dependency Graph 以任务为节点、依赖为有向边；节点只有在依赖满足后可运行。DAG 版本禁止循环，复杂图需显式循环语义。

## 工作原理

分解到可委派、可验收的粒度；为节点定义 inputs、artifact、done、priority。拓扑排序发现环并生成 ready queue。

## 架构视图

~~~text
Architecture View
        +-> A -+
Goal -> +-> B -+-> D -> Result
        +-> C ------+
~~~

~~~text
Product View
Goal -> proposed plan -> progress ledger -> result
          | edit/approve    | pause/retry/replan
~~~

## 最小可运行实践

运行 examples/planning/planning_system.py 的 dependency 场景。实验用确定性 Planner 和 Executor 展示计划 schema、依赖、状态、重规划与预算，不依赖模型 API。

## 正常场景

三类资料并行收集，比较任务等待全部完成，写作等待比较 Artifact，调度器可计算真实 ready 项。

## 失败与恢复场景

A 依赖 B、B 又依赖 A 时在执行前拒绝；上游失败后下游标记 blocked，不假装等待。

## 什么时候使用

存在真实依赖、并行机会、取消传播或多执行者时使用。

## 什么时候不要使用

线性短任务无需图；不能定义节点产物时，拆分只是标题列表。

## Trade-offs

图支持并行与恢复，却增加粒度和状态管理；过细节点会让协调成本超过执行。

## 产品视角

### 用户与业务问题

用户可以看到里程碑和阻塞关系，而不是一串跳动日志。

### 产品价值

降低可并行任务等待，并支持局部重跑和影响分析。

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

DAG 调度器、LangGraph、任务队列都可承载；是否允许循环决定用 DAG 还是 Graph。

## Related Patterns

Parallelization、Scheduling、Graph Orchestration。

## 检查清单

- 计划是否是结构化、可验证的 State？
- 每项是否有依赖、完成定义与产物？
- Planner 能否修改已完成事实？
- 是否区分失败重试与目标重规划？
- 用户看到的进度是否可信？

## 延伸练习与参考资料

加入一个环和一个失败依赖，验证执行前检测与阻塞传播。

- [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)
- [ReAct](https://arxiv.org/abs/2210.03629)
- [LangGraph：Plan-and-execute tutorial](https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/)
