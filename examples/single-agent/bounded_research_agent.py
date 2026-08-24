"""A bounded single-agent architecture without an LLM dependency."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Action:
    name: str
    arguments: dict[str, Any]


@dataclass
class AgentState:
    goal: str
    evidence: list[str] = field(default_factory=list)
    trace: list[str] = field(default_factory=list)
    seen_actions: set[str] = field(default_factory=set)
    status: str = "running"
    answer: str = ""


class Policy:
    """Deterministic stand-in for a model that chooses the next action."""

    def decide(self, state: AgentState) -> Action:
        if not state.goal.strip():
            return Action("clarify", {"question": "What should I research?"})
        if not state.evidence:
            return Action("search", {"query": state.goal})
        return Action("finish", {"answer": "Conclusion based on: " + state.evidence[-1]})


class RepeatingPolicy(Policy):
    def decide(self, state: AgentState) -> Action:
        return Action("search", {"query": state.goal})


class ToolRuntime:
    allowed = {"search"}

    def execute(self, action: Action) -> str:
        if action.name not in self.allowed:
            raise PermissionError(f"tool not allowed: {action.name}")
        query = str(action.arguments.get("query", "")).strip()
        if not query:
            raise ValueError("query is required")
        return f"verified evidence for {query}"


def fingerprint(action: Action) -> str:
    return f"{action.name}:{sorted(action.arguments.items())}"


def run_agent(
    goal: str,
    policy: Policy | None = None,
    max_steps: int = 4,
    runtime: ToolRuntime | None = None,
) -> AgentState:
    state = AgentState(goal=goal)
    policy = policy or Policy()
    runtime = runtime or ToolRuntime()

    for step in range(1, max_steps + 1):
        action = policy.decide(state)
        state.trace.append(f"decide:{step}:{action.name}")

        if action.name == "finish":
            state.answer = str(action.arguments["answer"])
            state.status = "completed"
            return state
        if action.name == "clarify":
            state.answer = str(action.arguments["question"])
            state.status = "needs_user"
            return state

        key = fingerprint(action)
        if key in state.seen_actions:
            state.status = "no_progress"
            state.answer = "Stopped with partial evidence."
            return state
        state.seen_actions.add(key)

        try:
            observation = runtime.execute(action)
        except (PermissionError, ValueError) as error:
            state.trace.append(f"tool_error:{type(error).__name__}")
            state.status = "blocked"
            state.answer = str(error)
            return state
        state.evidence.append(observation)
        state.trace.append(f"observe:{step}")

    state.status = "budget_exhausted"
    state.answer = "Budget exhausted; partial evidence: " + "; ".join(state.evidence)
    return state


def reflect(answer: str) -> tuple[bool, list[str]]:
    issues = []
    if "evidence" not in answer.lower():
        issues.append("missing evidence")
    if not answer.strip().endswith("."):
        issues.append("missing terminal punctuation")
    return not issues, issues


def revise(answer: str, issues: list[str]) -> str:
    revised = answer
    if "missing evidence" in issues:
        revised += " Evidence pending"
    if "missing terminal punctuation" in issues:
        revised = revised.rstrip(".") + "."
    return revised


if __name__ == "__main__":
    print("normal", run_agent("agent architecture"))
    print("clarify", run_agent(""))
    print("loop", run_agent("agent architecture", RepeatingPolicy()))
    answer = "Draft"
    ok, feedback = reflect(answer)
    print("critic", ok, feedback, "->", revise(answer, feedback))
