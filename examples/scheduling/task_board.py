"""A bounded multi-agent task board with scheduling and cancellation."""

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class Task:
    id: str
    requirements: frozenset[str]
    dependencies: frozenset[str] = frozenset()
    priority: int = 0
    age: int = 0
    status: str = "pending"
    assignee: str | None = None
    result: str | None = None


@dataclass(frozen=True)
class Agent:
    id: str
    capabilities: frozenset[str]
    allowed_data: frozenset[str]
    cost: int = 1


class TaskBoard:
    def __init__(self, capacity: int = 10, concurrency: int = 2):
        self.tasks: dict[str, Task] = {}
        self.capacity = capacity
        self.concurrency = concurrency

    def submit(self, task: Task):
        if len([t for t in self.tasks.values() if t.status not in {"completed", "cancelled"}]) >= self.capacity:
            raise ValueError("backpressure: queue full")
        if task.id in self.tasks:
            raise ValueError("duplicate task")
        self.tasks[task.id] = task

    def refresh(self):
        for task in self.tasks.values():
            if task.status != "pending":
                continue
            deps = [self.tasks[d].status for d in task.dependencies]
            if any(status in {"failed", "blocked", "cancelled"} for status in deps):
                task.status = "blocked"
            elif all(status == "completed" for status in deps):
                task.status = "ready"

    def ready(self):
        self.refresh()
        items = [task for task in self.tasks.values() if task.status == "ready"]
        return sorted(items, key=lambda t: (-(t.priority + t.age), t.id))

    def allocate(self, task: Task, agents: Iterable[Agent]):
        feasible = [
            agent for agent in agents
            if task.requirements <= agent.capabilities
        ]
        if not feasible:
            raise ValueError("unassigned: no capable agent")
        chosen = min(feasible, key=lambda a: (a.cost, a.id))
        task.assignee = chosen.id
        return chosen

    def lease(self, agents: Iterable[Agent]):
        running = sum(task.status == "running" for task in self.tasks.values())
        slots = max(0, self.concurrency - running)
        leased = []
        for task in self.ready()[:slots]:
            self.allocate(task, agents)
            task.status = "running"
            leased.append(task)
        for task in self.tasks.values():
            if task.status == "ready" and task not in leased:
                task.age += 1
        return leased

    def complete(self, task_id: str, result: str):
        task = self.tasks[task_id]
        if task.status != "running":
            raise ValueError("task is not running")
        task.status, task.result = "completed", result

    def cancel(self, task_id: str):
        descendants = {task_id}
        changed = True
        while changed:
            changed = False
            for task in self.tasks.values():
                if task.dependencies & descendants and task.id not in descendants:
                    descendants.add(task.id)
                    changed = True
        for item in descendants:
            task = self.tasks[item]
            if task.status != "completed":
                task.status = "cancelled"


def resolve(candidates: list[tuple[str, str, bool]]):
    # candidate = (answer, evidence_id, independent)
    independent = [item for item in candidates if item[2]]
    evidence = {item[1] for item in independent}
    if len(evidence) < 2:
        return "needs_external_validation"
    counts = {}
    for answer, _, _ in independent:
        counts[answer] = counts.get(answer, 0) + 1
    return max(counts, key=counts.get)


if __name__ == "__main__":
    board = TaskBoard(capacity=3, concurrency=1)
    board.submit(Task("research", frozenset({"research"}), priority=1))
    board.submit(Task("write", frozenset({"write"}), frozenset({"research"})))
    agents = [
        Agent("cheap-researcher", frozenset({"research"}), frozenset({"public"}), 1),
        Agent("writer", frozenset({"write"}), frozenset({"public"}), 1),
    ]
    print(board.lease(agents))
