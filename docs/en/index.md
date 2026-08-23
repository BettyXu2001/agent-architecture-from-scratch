---
title: Agent System Architecture from Scratch
lang: en
source: ../zh/index.md
source_hash: 509f4f800e7cefa6
---

# Agent System Architecture from Scratch

This is an agent system architecture tutorial for AI product managers, AI application designers, and engineers. It does not begin with a specific framework or repeat the internal implementation of an agent harness. It studies how agent components should be organized into a complete system.

## What This Project Solves

```text
Agent Internals
    = Loop / Tools / Session / Sandbox / Permissions
    -> covered in depth by learn-dsh

Agent System Architecture
    = Workflow / Planning / Context Flow / Memory Topology
      / Multi-Agent / Communication / Orchestration / Protocols
    -> covered by this project
```

The project focuses on these questions:

- When should a system use a workflow, single agent, or multi-agent architecture?
- What problems do planners, supervisors, handoffs, and evaluators solve?
- How should context and memory flow between agents or remain isolated?
- How do multiple agents communicate, divide work, schedule tasks, and terminate?
- How do graphs, state machines, events, and protocols organize complex systems?
- How do we evaluate, observe, and improve agent-system reliability?

## Complexity-Driven Learning Path

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

The core path contains 18 modules:

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

## Theory, Practice, and Product Perspective

Every module combines architectural theory, diagrams, a minimal implementation, failure cases, use and avoidance conditions, trade-offs, and framework mappings.

Every core article also contains a dedicated product perspective explaining:

- which user or business problem the architecture addresses;
- which plans, progress, results, and errors users can see;
- the agent's autonomy, data, and permission boundaries;
- how the system degrades, recovers, or hands off to a human;
- which product metrics show whether the added complexity is worthwhile.

The product perspective is a cross-cutting section within architecture articles. It does not replace the agent system architecture learning path.

## Current Content

- [From AI Feature to Agent Product (Chinese draft)](../zh/product-foundations/from-ai-feature-to-agent-product.md): a product-oriented supplement to the overview.
- [Chat, Workflow, and Agent (Chinese draft)](../zh/product-foundations/chat-workflow-and-agent.md): a supplement about interaction interfaces and execution architecture.
- [Basic Agent Loop](01-basic-agent-loop.md): an optional technical warm-up that will later move to the appendices.

The first formal article in the main path will be `Agent System Architecture Map`.

## Content Maintenance Rule

Chinese is the canonical content source, and English maintains a complete mirror. The main tutorial is organized by stable architectural concepts; framework details, protocol versions, and advanced patterns live in separate extension areas.
