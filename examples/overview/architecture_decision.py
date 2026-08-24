"""Framework-free architecture decision helper for the overview module."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskProfile:
    path_known: bool
    needs_dynamic_actions: bool = False
    side_effects: bool = False
    high_risk: bool = False
    long_running: bool = False
    context_bottleneck: bool = False


@dataclass(frozen=True)
class Decision:
    architecture: str
    reasons: tuple[str, ...]
    safeguards: tuple[str, ...]


def recommend(profile: TaskProfile) -> Decision:
    reasons: list[str] = []
    safeguards: list[str] = []

    if profile.path_known and not profile.needs_dynamic_actions:
        architecture = "workflow"
        reasons.append("the execution path can be enumerated")
    elif profile.high_risk:
        architecture = "hybrid"
        reasons.append("dynamic decisions need coded risk boundaries")
    else:
        architecture = "agent"
        reasons.append("the next action depends on intermediate observations")

    if profile.context_bottleneck:
        architecture += "+specialists"
        reasons.append("isolated contexts address a demonstrated bottleneck")
    if profile.long_running:
        architecture += "+durable-runtime"
        safeguards.append("checkpoint plan, artifacts, and side-effect results")
    if profile.side_effects:
        safeguards.extend(
            ("use idempotency keys", "preview or approve consequential actions")
        )
    if architecture.startswith(("agent", "hybrid")):
        safeguards.extend(
            ("set a step budget", "define stop and clarification conditions")
        )

    return Decision(architecture, tuple(reasons), tuple(safeguards))


if __name__ == "__main__":
    cases = {
        "contract extraction": TaskProfile(path_known=True),
        "open-ended research": TaskProfile(
            path_known=False, needs_dynamic_actions=True, long_running=True
        ),
        "purchase submission": TaskProfile(
            path_known=False,
            needs_dynamic_actions=True,
            side_effects=True,
            high_risk=True,
        ),
    }
    for name, profile in cases.items():
        print(name, "->", recommend(profile))
