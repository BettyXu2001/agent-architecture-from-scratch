---
id: pl06-ledger
slug: zh/03-planning/pl06-ledger
order: 406
section: planning
status: planned
title: "Progress Ledger and Replanning"
description: "消息历史无法可靠回答完成了什么、产物在哪里、还剩多少工作。长任务需要独立于对话的进度账本。"
updated_at: 2026-08-24
---

# PL06：Progress Ledger and Replanning

## 它解决什么问题

消息历史无法可靠回答完成了什么、产物在哪里、还剩多少工作。长任务需要独立于对话的进度账本。

## 核心定义

Progress Ledger 是结构化运行状态：计划版本、任务状态、Artifact 引用、尝试、错误、成本和变更原因。它是 State，不是给模型看的完整 Context。

## 工作原理

状态转换限制为 pending→ready→running→completed/failed/blocked/cancelled；每次变更带版本和时间。Replanner 从 Ledger 读取事实，Context 只取相关摘要。

## 架构视图

~~~text
Architecture View
Events -> Ledger(state + artifacts + budget) -> progress UI
                   |-> Replanner -> plan diff
~~~

~~~text
Product View
Goal -> proposed plan -> progress ledger -> result
          | edit/approve    | pause/retry/replan
~~~

## 最小可运行实践

运行 examples/planning/planning_system.py 的 ledger 场景。实验用确定性 Planner 和 Executor 展示计划 schema、依赖、状态、重规划与预算，不依赖模型 API。

## 正常场景

进程重启后从 Ledger 找到已完成研究与待执行合成，恢复时不重复外部调用。

## 失败与恢复场景

工具完成但 Ledger 未提交会产生不确定状态。通过幂等查询、两阶段记录或人工核对恢复，绝不凭模型猜测。

## 什么时候使用

任务跨多分钟、需要暂停恢复、多人/多 Agent 协作或向用户展示可信进度时使用。

## 什么时候不要使用

短请求无需持久账本；不要把每个 token 或内部思维写成业务进度。

## Trade-offs

持久状态带来一致性与迁移成本，却是恢复、审计和真实进度的基础。

## 产品视角

### 用户与业务问题

用户可以离开、回来、暂停和继续，并看到可验证产物而非“正在努力”。

### 产品价值

降低长任务流失和重做，支持可承诺的后台执行。

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

图状态、工作流引擎和数据库事件表都可实现；框架内存对象不足以覆盖进程重启。

## Related Patterns

Durable Execution、Trace、Task Board、Recovery。

## 检查清单

- 计划是否是结构化、可验证的 State？
- 每项是否有依赖、完成定义与产物？
- Planner 能否修改已完成事实？
- 是否区分失败重试与目标重规划？
- 用户看到的进度是否可信？

## 延伸练习与参考资料

执行一半序列化 Ledger，再用新进程恢复并验证不重复完成项。

- [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)
- [ReAct](https://arxiv.org/abs/2210.03629)
- [LangGraph：Plan-and-execute tutorial](https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/)
