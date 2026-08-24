"""Fault injection for retries, loops, partial failure, and recovery."""

from dataclasses import dataclass, field
from typing import Callable


class TransientError(RuntimeError):
    pass


class PermanentError(RuntimeError):
    pass


@dataclass
class EffectStore:
    results: dict[str, str] = field(default_factory=dict)

    def execute_once(self, key: str, action: Callable[[], str]):
        if key in self.results:
            return self.results[key]
        result = action()
        self.results[key] = result
        return result


def retry(operation: Callable[[], str], max_attempts: int = 3):
    errors = []
    for attempt in range(1, max_attempts + 1):
        try:
            return operation(), attempt
        except TransientError as error:
            errors.append(str(error))
        except PermanentError:
            raise
    raise TransientError(f"retry exhausted: {errors}")


def detect_loop(actions: list[str], evidence_counts: list[int]):
    if len(actions) >= 2 and actions[-1] == actions[-2]:
        return "repeated_action"
    if len(evidence_counts) >= 3 and len(set(evidence_counts[-3:])) == 1:
        return "no_progress"
    return None


def run_parallel(workers: dict[str, Callable[[], str]]):
    results, failures = {}, {}
    for name, worker in workers.items():
        try:
            results[name] = worker()
        except Exception as error:
            failures[name] = f"{type(error).__name__}:{error}"
    return {"results": results, "failures": failures, "status": "partial" if failures else "completed"}


@dataclass
class Checkpoint:
    completed: dict[str, str] = field(default_factory=dict)
    uncertain_effects: set[str] = field(default_factory=set)


def resume(checkpoint: Checkpoint, steps: list[tuple[str, Callable[[], str]]]):
    for step_id, step in steps:
        if step_id in checkpoint.completed:
            continue
        if step_id in checkpoint.uncertain_effects:
            raise RuntimeError(f"reconciliation required: {step_id}")
        checkpoint.completed[step_id] = step()
    return checkpoint


def handoff_path(path: list[str], target: str, max_handoffs: int = 3):
    if len(path) >= max_handoffs:
        return False, "handoff budget"
    if target in path:
        return False, "handoff loop"
    path.append(target)
    return True, "ok"


if __name__ == "__main__":
    attempts = {"n": 0}
    def flaky():
        attempts["n"] += 1
        if attempts["n"] < 2:
            raise TransientError("timeout")
        return "ok"
    print(retry(flaky))
    print(run_parallel({"good": lambda: "artifact", "bad": lambda: (_ for _ in ()).throw(PermanentError("bad"))}))
