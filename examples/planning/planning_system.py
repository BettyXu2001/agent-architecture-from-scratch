"""Planning, dependency validation, execution, ledger, and replanning."""

from dataclasses import dataclass, field, replace
from typing import Callable


TERMINAL = {"completed", "failed", "blocked", "cancelled"}


@dataclass(frozen=True)
class Task:
    id: str
    goal: str
    dependencies: tuple[str, ...] = ()
    status: str = "pending"
    artifact: str | None = None
    attempts: int = 0


@dataclass
class Ledger:
    version: int
    tasks: dict[str, Task]
    events: list[str] = field(default_factory=list)
    budget: int = 10

    def transition(self, task_id: str, status: str, artifact: str | None = None):
        task = self.tasks[task_id]
        allowed = {
            "pending": {"ready", "blocked", "cancelled"},
            "ready": {"running", "cancelled"},
            "running": {"completed", "failed"},
            "failed": {"ready", "blocked"},
        }
        if status not in allowed.get(task.status, set()):
            raise ValueError(f"illegal transition {task.status}->{status}")
        self.tasks[task_id] = replace(
            task,
            status=status,
            artifact=artifact if artifact is not None else task.artifact,
            attempts=task.attempts + (status == "running"),
        )
        self.version += 1
        self.events.append(f"{task_id}:{task.status}->{status}")


def static_plan(goal: str) -> list[Task]:
    return [
        Task("research", f"research {goal}"),
        Task("compare", "compare evidence", ("research",)),
        Task("write", "write report", ("compare",)),
    ]


def validate(tasks: list[Task], capabilities: set[str] | None = None) -> None:
    ids = {task.id for task in tasks}
    if len(ids) != len(tasks):
        raise ValueError("duplicate task id")
    for task in tasks:
        if not set(task.dependencies) <= ids:
            raise ValueError(f"unknown dependency for {task.id}")
        if capabilities is not None and task.goal.split()[0] not in capabilities:
            raise ValueError(f"capability missing for {task.id}")

    visiting: set[str] = set()
    visited: set[str] = set()
    graph = {task.id: task.dependencies for task in tasks}

    def visit(node: str):
        if node in visiting:
            raise ValueError("dependency cycle")
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph[node]:
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)


def refresh_ready(ledger: Ledger) -> None:
    for task in list(ledger.tasks.values()):
        if task.status != "pending":
            continue
        dependencies = [ledger.tasks[item].status for item in task.dependencies]
        if any(status in {"failed", "blocked", "cancelled"} for status in dependencies):
            ledger.transition(task.id, "blocked")
        elif all(status == "completed" for status in dependencies):
            ledger.transition(task.id, "ready")


def execute(
    ledger: Ledger,
    worker: Callable[[Task], str],
    fail_once: set[str] | None = None,
) -> Ledger:
    fail_once = fail_once or set()
    while ledger.budget > 0:
        refresh_ready(ledger)
        ready = [task for task in ledger.tasks.values() if task.status == "ready"]
        if not ready:
            break
        task = ready[0]
        ledger.transition(task.id, "running")
        ledger.budget -= 1
        if task.id in fail_once and task.attempts == 0:
            ledger.transition(task.id, "failed")
            continue
        ledger.transition(task.id, "completed", worker(task))
    return ledger


def replan_failed(ledger: Ledger) -> None:
    failed_ids = {task.id for task in ledger.tasks.values() if task.status == "failed"}
    for task_id in failed_ids:
        task = ledger.tasks[task_id]
        replacement = replace(task, goal=task.goal + " using fallback")
        ledger.tasks[task_id] = replacement
        ledger.transition(task_id, "ready")
        ledger.events.append(f"replan:{task_id}:fallback")

    # Blocking is derived from dependencies. Re-open unfinished descendants
    # so refresh_ready can recompute them from the repaired dependency chain.
    for task in list(ledger.tasks.values()):
        if task.status == "blocked":
            ledger.tasks[task.id] = replace(task, status="pending")
            ledger.version += 1
            ledger.events.append(f"replan:{task.id}:pending")


def build_ledger(goal: str) -> Ledger:
    tasks = static_plan(goal)
    validate(tasks)
    return Ledger(version=1, tasks={task.id: task for task in tasks})


if __name__ == "__main__":
    ledger = build_ledger("agent architecture")
    execute(ledger, lambda task: f"artifact:{task.id}", fail_once={"research"})
    replan_failed(ledger)
    execute(ledger, lambda task: f"artifact:{task.id}")
    print(ledger)
