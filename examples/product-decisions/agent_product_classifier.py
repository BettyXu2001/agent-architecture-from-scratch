from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StartingArchitecture(str, Enum):
    AI_FEATURE = "regular AI feature"
    WORKFLOW = "deterministic workflow"
    SINGLE_AGENT = "single agent"
    MULTI_AGENT_CANDIDATE = "multi-agent candidate"


@dataclass(frozen=True)
class ProductRequest:
    name: str
    stable_steps: bool
    needs_dynamic_decisions: bool
    independent_specialists: int = 0
    high_risk_actions: bool = False
    long_running: bool = False


@dataclass(frozen=True)
class Recommendation:
    architecture: StartingArchitecture
    reasons: tuple[str, ...]
    product_requirements: tuple[str, ...]


def recommend_architecture(request: ProductRequest) -> Recommendation:
    reasons: list[str] = []
    requirements: list[str] = []

    if request.needs_dynamic_decisions and request.independent_specialists >= 2:
        architecture = StartingArchitecture.MULTI_AGENT_CANDIDATE
        reasons.append("multiple independent specialties may benefit from isolation or parallel work")
        requirements.append("compare against a single-agent baseline before adopting multi-agent")
    elif request.needs_dynamic_decisions:
        architecture = StartingArchitecture.SINGLE_AGENT
        reasons.append("the next step depends on observations produced during the task")
    elif request.stable_steps:
        architecture = StartingArchitecture.WORKFLOW
        reasons.append("the execution path can be defined and tested in code")
    else:
        architecture = StartingArchitecture.AI_FEATURE
        reasons.append("start with a bounded input-to-output experience")

    if request.high_risk_actions:
        requirements.append("add an approval gate and idempotency protection for risky actions")
    if request.long_running:
        requirements.append("show progress and support cancel, retry, and resume")
    if architecture in {
        StartingArchitecture.SINGLE_AGENT,
        StartingArchitecture.MULTI_AGENT_CANDIDATE,
    }:
        requirements.append("define a step budget, stop conditions, and a partial-result fallback")

    return Recommendation(architecture, tuple(reasons), tuple(requirements))


def demo() -> None:
    requests = [
        ProductRequest("Meeting summary", stable_steps=False, needs_dynamic_decisions=False),
        ProductRequest(
            "Invoice processing",
            stable_steps=True,
            needs_dynamic_decisions=False,
            high_risk_actions=True,
        ),
        ProductRequest(
            "Research assistant",
            stable_steps=False,
            needs_dynamic_decisions=True,
            long_running=True,
        ),
        ProductRequest(
            "Incident investigation",
            stable_steps=False,
            needs_dynamic_decisions=True,
            independent_specialists=3,
            long_running=True,
        ),
    ]

    for request in requests:
        recommendation = recommend_architecture(request)
        print(f"{request.name}: {recommendation.architecture.value}")
        for reason in recommendation.reasons:
            print(f"  why: {reason}")
        for requirement in recommendation.product_requirements:
            print(f"  product: {requirement}")


if __name__ == "__main__":
    demo()
