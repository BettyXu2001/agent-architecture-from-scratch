---
title: 01 - Basic Agent Loop
lang: en
source: ../zh/01-basic-agent-loop.md
source_hash: 8ba421a05238c882
---

# 01 - Basic Agent Loop

The basic agent loop is the smallest useful Agent Harness. It sends the user input to the model, decides whether the model wants to call a tool, writes tool results back into context, and then asks the model to generate the next step.

```text
model -> tool call -> tool result -> updated context -> model -> final answer
```

This example intentionally avoids a real LLM API. It uses `ScriptedModel` as a deterministic model stand-in, so you can focus on architecture before dealing with API keys, latency, or model variance.

## Run The Example

```bash
python examples/01-basic-agent-loop/basic_agent_loop.py
```

The output should look like this:

```text
User: What is 12 * 7, then add 6?
Assistant requested tool: calculator
Tool result: 84
Assistant requested tool: calculator
Tool result: 90
Assistant: 12 * 7 + 6 = 90.
```

## Key Roles

- `Message`: A message in context, with `role` and `content`.
- `ToolCall`: The action the model asks the Harness to execute.
- `FinalAnswer`: The final answer returned by the model.
- `ScriptedModel`: A predictable model stand-in that only decides the next step.
- `calculator`: A tool function that only performs calculation.
- `run_agent`: The Harness that owns the loop, tool dispatch, context updates, and stopping condition.

## Architecture

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

## What To Notice

First, the model does not execute tools directly. It only returns a structured intent, such as calling `calculator` with an expression.

Second, the Harness executes tools. `run_agent` checks whether the tool exists, calls the matching function, and appends the result to context as a `tool` message.

Third, observations affect the next model output. After the first calculation returns `84`, the model sees that tool observation and then requests `84 + 6`.

Fourth, the loop needs a stopping condition. This example uses both `FinalAnswer` and `max_steps` to avoid infinite loops.

## Production Mapping

A real agent system usually replaces `ScriptedModel` with an LLM API, expands `calculator` into multiple tools, and connects `messages` to context management and tracing. The core control flow is still similar:

1. Prepare context.
2. Call the model.
3. If the model returns a final answer, stop.
4. If the model requests a tool, execute the tool.
5. Write the tool result back into context.
6. Return to the model and continue generation.

## Next Step

The next chapter upgrades hard-coded tool calls into a more general tool-calling protocol, including tool schemas, typed arguments, a tool registry, argument validation, and clearer error handling.
