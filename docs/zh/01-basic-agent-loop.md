---
title: 01 - 基础 Agent 循环
lang: zh
---

# 01 - 基础 Agent 循环

基础 Agent 循环是最小可用的 Agent Harness。它负责把用户输入交给模型，判断模型要不要调用工具，把工具结果写回上下文，然后继续让模型生成下一步。

```text
model -> tool call -> tool result -> updated context -> model -> final answer
```

这个例子故意不接真实 LLM API，而是使用 `ScriptedModel` 模拟一个确定性的模型。这样可以先专注理解架构，而不是被 API Key、网络延迟或模型随机性干扰。

## 运行示例

```bash
python examples/01-basic-agent-loop/basic_agent_loop.py
```

输出应该类似：

```text
User: What is 12 * 7, then add 6?
Assistant requested tool: calculator
Tool result: 84
Assistant requested tool: calculator
Tool result: 90
Assistant: 12 * 7 + 6 = 90.
```

## 关键角色

- `Message`：上下文里的消息，包含 `role` 和 `content`。
- `ToolCall`：模型请求 Harness 执行的动作。
- `FinalAnswer`：模型给出的最终回答。
- `ScriptedModel`：一个可预测的模型替身，只负责决定下一步。
- `calculator`：工具函数，只负责执行计算。
- `run_agent`：Harness，负责循环、工具分发、上下文更新和停止条件。

## 架构图

```text
User Message
    |
    v
ScriptedModel
    |
    +-- FinalAnswer -----------------> stop
    |
    +-- ToolCall
          |
          v
      Tool Registry
          |
          v
      Observation
          |
          v
      Context
          |
          +--------------------------> ScriptedModel
```

## 需要注意什么

第一，模型不直接执行工具。模型只返回一个结构化意图，例如调用 `calculator` 并传入表达式。

第二，Harness 执行工具。`run_agent` 检查工具名是否存在，调用对应函数，并把结果作为 `tool` 消息追加到上下文。

第三，观察结果会影响下一次模型输出。第一次计算得到 `84` 后，模型看到工具观察结果，才继续请求 `84 + 6`。

第四，循环必须有停止条件。这个示例同时使用 `FinalAnswer` 和 `max_steps`，避免 Agent 无限循环。

## 生产系统里的对应关系

真实 Agent 系统通常会把 `ScriptedModel` 换成 LLM API，把 `calculator` 扩展成多个工具，把 `messages` 接入上下文管理和追踪系统。但核心控制流仍然类似：

1. 准备上下文。
2. 调用模型。
3. 如果模型返回最终答案，结束。
4. 如果模型请求工具，执行工具。
5. 把工具结果写回上下文。
6. 回到模型继续生成。

## 下一步

下一章会把硬编码的工具调用升级成更通用的工具调用协议，包括工具 schema、类型化参数、工具注册表、参数校验和更清晰的错误处理。
