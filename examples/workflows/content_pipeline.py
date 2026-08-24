"""Minimal workflow patterns with deterministic, inspectable behavior."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Run:
    state: dict = field(default_factory=dict)
    trace: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def sequential(topic: str) -> Run:
    run = Run({"topic": topic})
    run.state["outline"] = [f"Why {topic}", "Evidence", "Risks"]
    run.trace.append("outline:ok")
    run.state["draft"] = " | ".join(run.state["outline"])
    run.trace.append("draft:ok")
    if "Risks" not in run.state["draft"]:
        raise ValueError("quality gate: missing risks")
    run.trace.append("fact_check:ok")
    return run


def route(text: str) -> str:
    lowered = text.lower()
    if "refund" in lowered or "退款" in lowered:
        return "support"
    if "price" in lowered or "价格" in lowered:
        return "sales"
    return "clarify"


def parallel_checks(draft: str, fail: str | None = None) -> Run:
    checks: dict[str, Callable[[str], str]] = {
        "facts": lambda value: "facts:ok" if value else "facts:empty",
        "audience": lambda value: "audience:ok",
        "policy": lambda value: "policy:ok",
    }

    def execute(item: tuple[str, Callable[[str], str]]) -> tuple[str, str]:
        name, check = item
        if name == fail:
            raise TimeoutError(name)
        return name, check(draft)

    run = Run({"draft": draft, "checks": {}})
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(execute, item): item[0] for item in checks.items()}
        for future, name in futures.items():
            try:
                key, result = future.result()
                run.state["checks"][key] = result
                run.trace.append(f"{key}:ok")
            except TimeoutError:
                run.warnings.append(f"{name}:timeout")
    return run


def evaluator_optimizer(draft: str, max_rounds: int = 2) -> Run:
    run = Run({"candidate": draft, "score": 0})
    best = draft
    best_score = -1
    for round_no in range(1, max_rounds + 1):
        candidate = run.state["candidate"]
        score = int("Evidence" in candidate) + int("Risks" in candidate)
        run.trace.append(f"evaluate:{round_no}:{score}")
        if score > best_score:
            best, best_score = candidate, score
        if score == 2:
            run.state.update(candidate=candidate, score=score, status="passed")
            return run
        missing = [x for x in ("Evidence", "Risks") if x not in candidate]
        run.state["candidate"] = candidate + " | " + " | ".join(missing)
        run.trace.append(f"revise:{round_no}")
    run.state.update(candidate=best, score=best_score, status="budget_exhausted")
    return run


def composed(topic: str, fail_check: str | None = None) -> Run:
    run = sequential(topic)
    run.state["route"] = route(topic)
    checked = parallel_checks(run.state["draft"], fail=fail_check)
    run.state["checks"] = checked.state["checks"]
    run.trace.extend(checked.trace)
    run.warnings.extend(checked.warnings)
    if "facts:timeout" in run.warnings:
        run.state["fallback"] = "cached_sources"
    optimized = evaluator_optimizer(run.state["draft"])
    run.state["result"] = optimized.state["candidate"]
    run.state["status"] = optimized.state["status"]
    run.trace.extend(optimized.trace)
    return run


if __name__ == "__main__":
    print("sequential", sequential("Agent products"))
    print("routing", route("I need a refund"))
    print("parallel", parallel_checks("Evidence | Risks"))
    print("evaluator", evaluator_optimizer("Draft"))
    print("composition", composed("Agent products", fail_check="facts"))
