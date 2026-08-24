"""DAG, state-machine, bounded graph, and durable checkpoint primitives."""

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Checkpoint:
    state: dict = field(default_factory=lambda: {"status": "created", "round": 0})
    completed: set[str] = field(default_factory=set)
    effects: dict[str, str] = field(default_factory=dict)
    version: int = 0
    trace: list[str] = field(default_factory=list)


TRANSITIONS = {
    "created": {"running", "cancelled"},
    "running": {"waiting_approval", "completed", "failed", "cancelled"},
    "waiting_approval": {"running", "cancelled"},
}


def transition(checkpoint: Checkpoint, status: str):
    current = checkpoint.state["status"]
    if status not in TRANSITIONS.get(current, set()):
        raise ValueError(f"illegal transition {current}->{status}")
    checkpoint.state["status"] = status
    checkpoint.version += 1
    checkpoint.trace.append(f"state:{current}->{status}")


def validate_dag(dependencies: dict[str, set[str]]):
    visiting, visited = set(), set()

    def visit(node):
        if node in visiting:
            raise ValueError("cycle in DAG")
        if node in visited:
            return
        visiting.add(node)
        for dep in dependencies.get(node, set()):
            if dep not in dependencies:
                raise ValueError("unknown dependency")
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for node in dependencies:
        visit(node)


def run_dag(dependencies, worker: Callable[[str], str]):
    validate_dag(dependencies)
    completed, results = set(), {}
    while len(completed) < len(dependencies):
        ready = [
            node for node, deps in dependencies.items()
            if node not in completed and deps <= completed
        ]
        if not ready:
            raise ValueError("no ready node")
        for node in ready:
            results[node] = worker(node)
            completed.add(node)
    return results


def bounded_cycle(value: str, evaluator: Callable[[str], bool], max_rounds: int = 3):
    seen, best, trace = set(), value, []
    for round_no in range(1, max_rounds + 1):
        digest = hash(value)
        if digest in seen:
            trace.append("stop:no-progress")
            break
        seen.add(digest)
        trace.append(f"evaluate:{round_no}")
        best = value
        if evaluator(value):
            trace.append("stop:passed")
            break
        value += " improved"
    else:
        trace.append("stop:budget")
    return best, trace


def durable_effect(checkpoint: Checkpoint, effect_id: str, execute: Callable[[], str]):
    if effect_id in checkpoint.effects:
        checkpoint.trace.append(f"effect:{effect_id}:reused")
        return checkpoint.effects[effect_id]
    checkpoint.trace.append(f"effect:{effect_id}:intent")
    result = execute()
    checkpoint.effects[effect_id] = result
    checkpoint.version += 1
    checkpoint.trace.append(f"effect:{effect_id}:committed")
    return result


def resume(checkpoint: Checkpoint, nodes: list[str]):
    for node in nodes:
        if node in checkpoint.completed:
            checkpoint.trace.append(f"node:{node}:skipped")
            continue
        checkpoint.trace.append(f"node:{node}:run")
        checkpoint.completed.add(node)
        checkpoint.version += 1
    return checkpoint


if __name__ == "__main__":
    print(run_dag({"a": set(), "b": {"a"}, "c": {"a"}, "d": {"b", "c"}}, lambda n: n))
    cp = Checkpoint()
    transition(cp, "running")
    durable_effect(cp, "send-1", lambda: "sent")
    durable_effect(cp, "send-1", lambda: "sent twice")
    resume(cp, ["research", "write"])
    resume(cp, ["research", "write"])
    print(cp)
