# Agent Architecture from Scratch

一个面向 AI 产品经理、AI 应用设计者和工程师的双语教程项目：从零学习 Agent System Architecture，覆盖 Workflow、Single Agent、Planning、Context、Memory、Multi-Agent、Communication、Orchestration 与 Distributed Agent Systems。

它关注的不是“某个 Agent Harness 如何实现每一行代码”，而是：

> Agent 组件应该如何组织成一个系统？面对具体问题，应该使用 Workflow、Single Agent、Multi-Agent，还是分布式 Agent 系统？

## 项目边界

本项目将 `Agent System Architecture` 作为知识主线，同时在每篇文章中加入产品视角。它避免重复展开 Harness 底层实现，也不按照某个快速变化的框架组织知识。

| 本项目重点 | 仅作前置知识或附录 |
|---|---|
| Agent、Workflow 与 Agentic System | 最小 Agent loop 的逐行实现 |
| Planning、Context Flow 与 Memory Topology | Session、Sandbox 和插件内部机制 |
| Multi-Agent Fundamentals、Patterns、Hierarchy | 通用工具注册表实现 |
| Communication、Coordination 与 Scheduling | 特定模型 API 教程 |
| MCP、A2A 与 Distributed Agent Systems | 单一框架完整手册 |
| Orchestration、Reliability、Evaluation | Harness 源码逐层拆解 |

## 学习主线

```text
Agent Architecture Overview
    -> Workflow Patterns
    -> Single-Agent Reasoning
    -> Planning, Context and Memory
    -> Multi-Agent Fundamentals and Patterns
    -> Hierarchical Systems and Communication
    -> Protocols, Orchestration and Coordination
    -> Governance, Reliability and Evaluation
    -> Framework Comparison
    -> Build a Real Agent System
```

课程由 18 个稳定模块组成，并预留 Advanced Patterns、Application Architectures、Protocols 和 Frameworks 扩展区。详细架构地图见 [CURRICULUM.md](CURRICULUM.md)，执行顺序见 [ROADMAP.md](ROADMAP.md)，写作要求见 [ARTICLE_TEMPLATE.md](ARTICLE_TEMPLATE.md)。

## 内容形态

每个模块必须同时包含架构理论和简单实践；每篇文章还必须设置明确的“产品视角”章节，并包含：

- 用户问题与可验证的产品价值
- 产品体验流与系统执行流
- 一个不依赖框架的最小实现
- 正常场景以及失败、降级或人工接管场景
- 自主性、数据和权限边界
- “什么时候用 / 什么时候不用”以及产品指标
- 调用成本、延迟和维护复杂度
- 主流框架中的对应概念，但不把框架 API 当作主线

每个 Part 至少交付一个可运行的最小实验，并使用同一组输入比较相邻架构。实践代码以小、可读、依赖少为优先，不追求直接搭建完整生产框架。

## 目标目录

```text
agent-architecture-from-scratch/
├─ docs/
│  ├─ zh/                    # 中文主内容
│  │  ├─ 00-overview/
│  │  ├─ 01-workflows/
│  │  ├─ 02-single-agent/
│  │  ├─ 03-planning/
│  │  ├─ 04-context/
│  │  ├─ 05-memory/
│  │  ├─ 06-multi-agent/
│  │  ├─ 07-communication/
│  │  ├─ 08-protocols/
│  │  ├─ 09-orchestration/
│  │  ├─ 10-reliability/
│  │  ├─ 11-evaluation/
│  │  ├─ 12-framework-comparison/
│  │  ├─ 13-real-system/
│  │  ├─ extensions/         # 可独立增加的专题
│  │  └─ appendices/         # 前置知识、术语、框架映射
│  └─ en/                    # 与中文目录镜像
├─ examples/                 # 与语义化章节路径对应
├─ tests/                    # 单元、场景、故障注入与 eval
├─ references/               # 公开资料索引，不存放大段复制内容
├─ scripts/                  # 文档同步和项目检查
└─ mkdocs.yml
```

目录使用语义化名称，课程顺序由 MkDocs 导航和章节元数据控制。这样可以在任意 Part 内增加章节，而不需要重命名后续文件或破坏已有链接。

## 当前状态

仓库中的 `01-basic-agent-loop` 是早期原型，暂时作为前置热身保留。正式主线从 `Agent System Architecture Map` 开始；现有 P01、P02 作为 Overview 的产品向补充文章保留。

## Quick Start

运行现有的前置示例：

```bash
python examples/01-basic-agent-loop/basic_agent_loop.py
```

运行测试：

```bash
python -m unittest
```

中文是内容源，英文保持镜像结构。当前同步方式见 [docs/README.md](docs/README.md)。

## License

MIT
