"""Small evaluation harness for outcomes, trajectories, and attribution."""

from dataclasses import dataclass, field
from time import perf_counter
from typing import Callable


@dataclass(frozen=True)
class Span:
    name: str
    kind: str
    parent: str | None
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0
    latency_ms: float = 0.0
    data: dict = field(default_factory=dict)


@dataclass
class Trace:
    id: str
    spans: list[Span] = field(default_factory=list)
    outcome: dict = field(default_factory=dict)

    def add(self, span: Span):
        self.spans.append(span)


@dataclass(frozen=True)
class Scenario:
    id: str
    prompt: str
    required_artifacts: frozenset[str]
    required_tools: frozenset[str] = frozenset()
    forbidden_tools: frozenset[str] = frozenset()


def run_scenario(scenario: Scenario, use_specialist: bool = True):
    trace = Trace(scenario.id)
    start = perf_counter()
    tools = ["search"]
    trace.add(Span("search", "tool", "agent", 0, 0, 0.01, 5, {"tool": "search"}))
    if use_specialist:
        trace.add(Span("risk", "agent", "agent", 100, 30, 0.02, 8, {"contribution": "risk"}))
    artifacts = {"report"}
    trace.add(Span("agent", "agent", None, 200, 80, 0.05, (perf_counter() - start) * 1000))
    trace.outcome = {"artifacts": artifacts, "tools": tools, "answer": "report with evidence"}
    return trace


def task_grade(trace: Trace, scenario: Scenario):
    missing = scenario.required_artifacts - set(trace.outcome.get("artifacts", set()))
    return {"pass": not missing, "missing_artifacts": sorted(missing)}


def trajectory_grade(trace: Trace, scenario: Scenario):
    called = {span.data.get("tool") for span in trace.spans if span.kind == "tool"}
    called.discard(None)
    return {
        "required_tools_present": scenario.required_tools <= called,
        "forbidden_tools_absent": not bool(scenario.forbidden_tools & called),
        "called": sorted(called),
    }


def attribution(trace: Trace):
    total_cost = sum(span.cost for span in trace.spans)
    total_tokens = sum(span.input_tokens + span.output_tokens for span in trace.spans)
    by_kind = {}
    for span in trace.spans:
        by_kind[span.kind] = by_kind.get(span.kind, 0.0) + span.cost
    return {"total_cost": total_cost, "total_tokens": total_tokens, "cost_by_kind": by_kind}


def evaluate(dataset: list[Scenario], runner: Callable[[Scenario], Trace]):
    rows = []
    for scenario in dataset:
        trace = runner(scenario)
        rows.append({
            "scenario": scenario.id,
            "task": task_grade(trace, scenario),
            "trajectory": trajectory_grade(trace, scenario),
            "usage": attribution(trace),
        })
    successes = sum(row["task"]["pass"] for row in rows)
    cost = sum(row["usage"]["total_cost"] for row in rows)
    return {"rows": rows, "success_rate": successes / len(rows), "cost_per_success": cost / max(successes, 1)}


if __name__ == "__main__":
    golden = [Scenario("research-1", "research agents", frozenset({"report"}), frozenset({"search"}), frozenset({"send"}))]
    print(evaluate(golden, run_scenario))
    print("ablation", evaluate(golden, lambda s: run_scenario(s, use_specialist=False)))
