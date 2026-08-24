"""Compare single, modular-single, and multi-agent boundaries."""

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class Result:
    owner: str
    content: str
    evidence: tuple[str, ...] = ()
    error: str | None = None


@dataclass
class Metrics:
    calls: int = 0
    messages: int = 0
    visible_fields: dict[str, set[str]] = field(default_factory=dict)


def research(topic: str) -> Result:
    return Result("researcher", f"research:{topic}", ("source:research",))


def risk(topic: str) -> Result:
    if topic == "fail-risk":
        return Result("risk", "", error="risk source unavailable")
    return Result("risk", f"risk:{topic}", ("source:risk",))


def single_agent(topic: str, metrics: Metrics) -> Result:
    metrics.calls += 1
    metrics.visible_fields["single"] = {"goal", "research_data", "risk_data", "user_profile"}
    return Result(
        "single",
        f"{research(topic).content}; {risk(topic).content}",
        ("source:research", "source:risk"),
    )


def modular_single(topic: str, metrics: Metrics) -> Result:
    metrics.calls += 1
    metrics.visible_fields["controller"] = {"goal", "user_profile"}
    parts = [research(topic), risk(topic)]
    return synthesize("controller", parts, metrics)


def specialist(
    name: str,
    topic: str,
    allowed_fields: set[str],
    worker: Callable[[str], Result],
    metrics: Metrics,
) -> Result:
    metrics.calls += 1
    metrics.visible_fields[name] = allowed_fields
    return worker(topic)


def synthesize(owner: str, parts: list[Result], metrics: Metrics) -> Result:
    metrics.messages += len(parts)
    good = [part for part in parts if not part.error]
    gaps = [part.error for part in parts if part.error]
    content = "; ".join(part.content for part in good)
    if gaps:
        content += "; gaps=" + ",".join(gaps)
    evidence = tuple(item for part in good for item in part.evidence)
    return Result(owner, content, evidence)


def multi_agent(topic: str, metrics: Metrics) -> Result:
    parts = [
        specialist("researcher", topic, {"goal", "public_sources"}, research, metrics),
        specialist("risk", topic, {"goal", "risk_sources"}, risk, metrics),
    ]
    return synthesize("manager", parts, metrics)


if __name__ == "__main__":
    for architecture in (single_agent, modular_single, multi_agent):
        metrics = Metrics()
        print(architecture.__name__, architecture("agents", metrics), metrics)
    metrics = Metrics()
    print("partial failure", multi_agent("fail-risk", metrics))
