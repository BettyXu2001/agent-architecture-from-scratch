---
id: pl02-planner-executor
slug: zh/03-planning/pl02-planner-executor
order: 402
section: planning
status: planned
title: "Planner–Executor"
description: "同一模型一边规划一边执行会混淆全局目标与局部工具细节。角色分离让计划可校验、执行可替换。"
updated_at: 2026-08-24
---

# PL02：Planner–Executor

## 它解决什么问题

同一模型一边规划一边执行会混淆全局目标与局部工具细节。角色分离让计划可校验、执行可替换。

## 核心定义

Planner 负责分解和依赖，不直接调用业务工具；Executor 接受单个已验证任务并产出结果；Controller 持有状态和调度权。

## 工作原理

Planner 输出任务图，Validator 检查能力、依赖和预算，Executor 只能从允许动作中选择，Controller 原子提交结果。

## 架构视图

~~~text
Architecture View
Goal -> Planner -> Validator -> Controller -> Executor
                         ^          -> Artifact Store
~~~

~~~text
Product View
Goal -> proposed plan -> progress ledger -> result
          | edit/approve    | pause/retry/replan
~~~

## 最小可运行实践

运行 examples/planning/planning_system.py 的 planner-executor 场景。实验用确定性 Planner 和 Executor 展示计划 schema、依赖、状态、重规划与预算，不依赖模型 API。

## 正常场景

Planner 将报告拆为三个研究项和一次合成；Executor 可并行处理独立项，最终合成只读取结构化 Artifact。

## 失败与恢复场景

Planner 发明不存在的能力时，Validator 返回 capability_missing；可重写计划或请求用户，而不是让 Executor 猜。

## 什么时候使用

规划与执行需要不同上下文、模型、权限或成本配置时使用。

## 什么时候不要使用

计划只有两步或 Planner 不能比固定模板产生更好分解时不要额外分层。

## Trade-offs

分工提高可测试与模型路由，却增加调用和接口契约；计划信息传递可能丢失隐含意图。

## 产品视角

### 用户与业务问题

适合用户提交目标后希望系统主动组织工作，但仍能审阅范围。

### 产品价值

可单独优化计划质量和执行成功率，故障更容易定位。

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

Agents-as-tools、Graph 节点或普通服务都能实现；最终控制者必须唯一。

## Related Patterns

与 Supervisor 相似但 Executor 不必是独立 Agent；后续 Replanner。

## 检查清单

- 计划是否是结构化、可验证的 State？
- 每项是否有依赖、完成定义与产物？
- Planner 能否修改已完成事实？
- 是否区分失败重试与目标重规划？
- 用户看到的进度是否可信？

## 延伸练习与参考资料

让 Validator 拒绝一个虚构工具，并返回可执行替代。

- [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)
- [ReAct](https://arxiv.org/abs/2210.03629)
- [LangGraph：Plan-and-execute tutorial](https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/)
