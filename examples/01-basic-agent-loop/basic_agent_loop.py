from __future__ import annotations

import ast
import operator
from dataclasses import dataclass
from typing import Callable, Union


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, str]


@dataclass(frozen=True)
class FinalAnswer:
    content: str


ModelOutput = Union[ToolCall, FinalAnswer]
Tool = Callable[[dict[str, str]], str]


class ScriptedModel:
    """A deterministic stand-in for an LLM so the loop stays easy to inspect."""

    def generate(self, messages: list[Message]) -> ModelOutput:
        observations = [m.content for m in messages if m.role == "tool"]

        if not observations:
            return ToolCall(name="calculator", arguments={"expression": "12 * 7"})

        if observations[-1] == "84":
            return ToolCall(name="calculator", arguments={"expression": "84 + 6"})

        return FinalAnswer(content=f"12 * 7 + 6 = {observations[-1]}.")


def calculator(arguments: dict[str, str]) -> str:
    expression = arguments["expression"]
    tree = ast.parse(expression, mode="eval")
    result = _eval_arithmetic(tree.body)
    return str(result)


def _eval_arithmetic(node: ast.AST) -> int:
    operators: dict[type[ast.operator], Callable[[int, int], int]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.FloorDiv: operator.floordiv,
    }

    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in operators:
        left = _eval_arithmetic(node.left)
        right = _eval_arithmetic(node.right)
        return operators[type(node.op)](left, right)

    raise ValueError(f"Unsupported expression: {ast.unparse(node)}")


def run_agent(
    user_input: str,
    model: ScriptedModel | None = None,
    tools: dict[str, Tool] | None = None,
    max_steps: int = 10,
) -> tuple[str, list[Message]]:
    model = model or ScriptedModel()
    tools = tools or {"calculator": calculator}
    messages = [Message(role="user", content=user_input)]

    for _ in range(max_steps):
        output = model.generate(messages)

        if isinstance(output, FinalAnswer):
            messages.append(Message(role="assistant", content=output.content))
            return output.content, messages

        if output.name not in tools:
            raise ValueError(f"Unknown tool: {output.name}")

        tool_result = tools[output.name](output.arguments)
        messages.append(Message(role="assistant", content=f"ToolCall({output.name})"))
        messages.append(Message(role="tool", content=tool_result))

    raise RuntimeError("Agent stopped because max_steps was reached.")


def main() -> None:
    user_input = "What is 12 * 7, then add 6?"
    answer, messages = run_agent(user_input)

    print(f"User: {user_input}")
    for index, message in enumerate(messages):
        if message.role == "assistant" and message.content.startswith("ToolCall("):
            tool_result = messages[index + 1].content
            tool_name = message.content.removeprefix("ToolCall(").removesuffix(")")
            print(f"Assistant requested tool: {tool_name}")
            print(f"Tool result: {tool_result}")

    print(f"Assistant: {answer}")


if __name__ == "__main__":
    main()
