"""A two-level hierarchy with bounded recursive delegation."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Task:
    id: str
    goal: str
    parent_id: str | None
    depth: int
    budget: int


@dataclass(frozen=True)
class Result:
    task_id: str
    owner: str
    artifact: str
    evidence: tuple[str, ...] = ()
    error: str | None = None


@dataclass
class Runtime:
    max_depth: int = 2
    global_budget: int = 8
    seen: set[str] = field(default_factory=set)
    trace: list[str] = field(default_factory=list)

    def claim(self, task: Task):
        if task.depth > self.max_depth:
            raise ValueError("delegation depth exceeded")
        if self.global_budget <= 0 or task.budget <= 0:
            raise ValueError("delegation budget exhausted")
        if task.id in self.seen:
            raise ValueError("duplicate task")
        self.seen.add(task.id)
        self.global_budget -= 1
        self.trace.append(f"claim:{task.id}:depth={task.depth}")


def worker(task: Task, fail: bool = False) -> Result:
    if fail:
        return Result(task.id, "worker", "", error="worker failed")
    return Result(task.id, "worker", f"artifact:{task.id}", (f"source:{task.id}",))


def team_lead(task: Task, runtime: Runtime, fail_worker: bool = False) -> Result:
    runtime.claim(task)
    child = Task(
        id=f"{task.id}.worker",
        goal=f"execute {task.goal}",
        parent_id=task.id,
        depth=task.depth + 1,
        budget=task.budget - 1,
    )
    runtime.claim(child)
    result = worker(child, fail_worker)
    if result.error:
        return Result(task.id, "team-lead", "", error=result.error)
    return Result(task.id, "team-lead", result.artifact, result.evidence)


def coordinator(goal: str, fail_team: str | None = None):
    runtime = Runtime()
    root = Task("root", goal, None, 0, runtime.global_budget)
    runtime.claim(root)
    results = []
    for name in ("research", "risk"):
        task = Task(name, f"{name} {goal}", root.id, 1, 3)
        results.append(team_lead(task, runtime, fail_worker=name == fail_team))
    successful = [item for item in results if not item.error]
    gaps = [item.error for item in results if item.error]
    final = {
        "owner": "coordinator",
        "artifacts": [item.artifact for item in successful],
        "evidence": [e for item in successful for e in item.evidence],
        "gaps": gaps,
    }
    return final, runtime


if __name__ == "__main__":
    print(coordinator("agent architecture"))
    print(coordinator("agent architecture", fail_team="risk"))
