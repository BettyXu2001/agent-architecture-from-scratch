# 01 - Basic Agent Loop

中文教程：`docs/zh/01-basic-agent-loop.md`

English tutorial: `docs/en/01-basic-agent-loop.md`

This example implements the smallest useful agent harness:

```text
model -> tool call -> tool result -> updated context -> model -> final answer
```

There is no LLM API dependency in this demo. The `ScriptedModel` behaves like a tiny deterministic model so you can focus on the architecture instead of credentials, latency, or model variance.

## Run

```bash
python examples/01-basic-agent-loop/basic_agent_loop.py
```

## What To Notice

- The model does not execute tools.
- The harness executes tools.
- Tool results are appended back into context as observations.
- The loop stops only when the model returns a final answer.

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

## Next Step

The next chapter should replace the hard-coded script with a more general tool-calling contract:

- tool schemas
- typed arguments
- tool registry
- validation
- better error handling
