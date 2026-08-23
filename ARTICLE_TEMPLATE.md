# Agent 架构技术文章模板

```yaml
---
id: PL03
title: Planner–Executor–Replanner
lang: zh
status: planned
module: planning
prerequisites: [PL01, PL02]
concepts: [planning, execution, replanning]
example: labs/planning/replanner
last_reviewed: YYYY-MM-DD
---
```

# 文章标题

## 它解决什么问题

用一个具体任务说明现有架构的限制，以及为什么需要当前 pattern。

## 核心定义

给出最小、框架无关的定义，明确它与相邻 pattern 的边界。

## 工作原理

说明参与组件、控制权、输入输出、状态变化和停止条件。

## 架构视图

至少画出适用的视图：

- Control Flow
- Context Flow
- State Flow
- Communication Topology

## 最小可运行实践

提供小而完整、优先不依赖 API Key 的 from-scratch 实现。

## 正常场景

记录输入、关键状态转换、trace 和预期结果。

## 失败与恢复场景

主动触发至少一个典型失败，说明其根因、检测和恢复方式。

## 什么时候使用

列出采用该架构需要满足的任务和系统条件。

## 什么时候不要使用

说明什么情况下更简单或相邻的架构更合适。

## Trade-offs

至少分析：

- determinism vs autonomy
- quality vs cost
- latency vs parallelism
- context sharing vs isolation
- flexibility vs operability

## 产品视角

产品视角是架构文章的横向栏目，不取代前面的架构讲解。

### 用户与业务问题

该架构在产品中解决什么用户或业务问题？

### 产品价值

与更简单架构相比，增加了什么可验证价值？

### 用户体验

用户能看到哪些计划、进度、结果、错误和接管状态？

### 自主性边界

Agent 可以自行决定和执行什么？哪些动作必须确认？

### 数据与权限

需要读取、保存或发送什么数据？组件之间如何隔离？

### 失败与降级

失败时如何重试、返回部分结果、降级、恢复或转人工？

### 产品指标

如何用任务成功率、完成时间、用户修正率、人工介入率和单成功任务成本验证？

## 框架中的对应实现

将 LangGraph、AutoGen、CrewAI、OpenAI Agents SDK、Google ADK 等实现映射到本文架构，不把 API 当作主线。

## Related Patterns

说明前置 pattern、替代 pattern、可组合 pattern 和高级扩展。

## 检查清单

- 架构定义是否独立于具体框架？
- 控制权、Context、State 和停止条件是否明确？
- 示例是否验证了核心机制？
- 是否包含失败而不只有 happy path？
- 是否说明使用与避免条件？
- 是否分析关键 trade-offs？
- 是否包含完整产品视角？

## 延伸练习与参考资料

提供架构练习、产品练习和经过筛选的原始资料。
