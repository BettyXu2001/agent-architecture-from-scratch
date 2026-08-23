from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum


class Control(str, Enum):
    CODE = "code"
    LLM = "llm"
    HYBRID = "hybrid"


class Topology(str, Enum):
    WORKFLOW = "workflow"
    SINGLE_AGENT = "single-agent"
    SUPERVISOR = "supervisor"
    HANDOFF = "handoff"
    HIERARCHICAL = "hierarchical"
    DISTRIBUTED = "distributed"


class Runtime(str, Enum):
    REQUEST_RESPONSE = "request-response"
    ASYNC = "async"
    DURABLE = "durable"
    DISTRIBUTED = "distributed"


@dataclass(frozen=True)
class ArchitectureCard:
    name: str
    control: Control
    reasoning: str
    topology: Topology
    context: str
    memory: str
    communication: str
    orchestration: str
    runtime: Runtime


def describe(card: ArchitectureCard) -> str:
    lines = [card.name]
    for field in fields(card):
        if field.name == "name":
            continue
        value = getattr(card, field.name)
        rendered = value.value if isinstance(value, Enum) else value
        lines.append(f"  {field.name}: {rendered}")
    return "\n".join(lines)


def compare(before: ArchitectureCard, after: ArchitectureCard) -> tuple[str, ...]:
    changes: list[str] = []
    for field in fields(before):
        if field.name == "name":
            continue
        old = getattr(before, field.name)
        new = getattr(after, field.name)
        if old != new:
            old_value = old.value if isinstance(old, Enum) else old
            new_value = new.value if isinstance(new, Enum) else new
            changes.append(f"{field.name}: {old_value} -> {new_value}")
    return tuple(changes)


def demo() -> None:
    workflow = ArchitectureCard(
        name="Content workflow",
        control=Control.CODE,
        reasoning="direct generation",
        topology=Topology.WORKFLOW,
        context="shared request context",
        memory="none",
        communication="typed step outputs",
        orchestration="sequential",
        runtime=Runtime.REQUEST_RESPONSE,
    )
    research_system = ArchitectureCard(
        name="Research agent system",
        control=Control.HYBRID,
        reasoning="planner-executor-replanner",
        topology=Topology.SUPERVISOR,
        context="isolated specialists + context packets",
        memory="private working memory + shared artifacts",
        communication="agent-as-tool results + artifacts",
        orchestration="graph with parallel fan-out and evaluator loop",
        runtime=Runtime.DURABLE,
    )

    print(describe(workflow))
    print()
    print(describe(research_system))
    print("\nChanged dimensions")
    for change in compare(workflow, research_system):
        print(f"  {change}")


if __name__ == "__main__":
    demo()
