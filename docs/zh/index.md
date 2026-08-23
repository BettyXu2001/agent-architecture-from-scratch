---
title: Agent System Architecture from Scratch
lang: zh
---

# Agent System Architecture from Scratch

这是一套面向 AI 产品经理、AI 应用设计者和工程师的 Agent 系统架构教程。它不从某个框架开始，也不重复拆解 Agent Harness 内部实现，而是研究 Agent 组件应该如何组织成一个完整系统。

## 项目解决什么问题

```text
Agent Internals
    = Loop / Tools / Session / Sandbox / Permissions
    -> 由 learn-dsh 深入讲解

Agent System Architecture
    = Workflow / Planning / Context Flow / Memory Topology
      / Multi-Agent / Communication / Orchestration / Protocols
    -> 由本项目讲解
```

本项目重点回答：

- 什么时候使用 Workflow、Single Agent 或 Multi-Agent？
- Planner、Supervisor、Handoff 和 Evaluator 分别解决什么问题？
- Context 和 Memory 应该如何在 Agent 之间流动或隔离？
- 多个 Agent 如何通信、分工、调度和停止？
- Graph、State Machine、Event-driven 与协议如何组织复杂系统？
- 如何评价、观察并提高 Agent System 的可靠性？

## 复杂度递增的学习路径

```text
LLM
  -> Augmented LLM
  -> Workflow
  -> Single Agent
  -> Planning / Context / Memory
  -> Multiple Agents
  -> Orchestrated Agent System
  -> Distributed Agent System
```

主线包含 18 个模块：

1. Agent Architecture Overview
2. Workflow Patterns
3. Single-Agent Reasoning
4. Planning & Search
5. Context Architecture
6. Memory Architecture
7. Multi-Agent Fundamentals
8. Multi-Agent Patterns
9. Hierarchical Systems
10. Agent Communication
11. Agent Protocols
12. Orchestration Architecture
13. Coordination & Scheduling
14. Human & Governance
15. Reliability
16. Evaluation & Observability
17. Architecture Comparison
18. Build a Real Agent System

## 理论、实践与产品视角

每个模块都同时包含架构理论、架构图、最小实现、失败案例、使用与避免条件、Trade-offs 和框架映射。

每篇核心文章还会设置独立的“产品视角”，说明：

- 该架构解决什么用户或业务问题；
- 用户能看到哪些计划、进度、结果和错误；
- Agent 的自主性、数据和权限边界；
- 失败后如何降级、恢复或转人工；
- 如何用产品指标判断增加的复杂度是否值得。

产品视角是架构文章的横向栏目，不取代 Agent System Architecture 主线。

## 当前内容

- [从 AI 功能到 Agent 产品](product-foundations/from-ai-feature-to-agent-product.md)：Overview 的产品向补充。
- [Chat、Workflow 与 Agent](product-foundations/chat-workflow-and-agent.md)：交互界面与执行架构的补充。
- [基础 Agent 循环](01-basic-agent-loop.md)：可选技术热身，后续迁移至附录。

正式主线的第一篇将是 `Agent System Architecture Map`。

## 内容维护规则

中文是主内容源，英文保持完整镜像。主教程按稳定的架构概念组织；框架、协议版本和高级 pattern 分别放在独立扩展区。
