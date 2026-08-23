from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ExecutionMode(str, Enum):
    AI_FEATURE = "regular AI feature"
    WORKFLOW = "workflow"
    AGENT = "agent"


class InterfaceMode(str, Enum):
    INLINE_OR_FORM = "inline or form"
    CHAT = "chat"
    TASK_WORKSPACE = "task workspace"
    BACKGROUND_NOTIFICATION = "background task and notification"


@dataclass(frozen=True)
class ProductScenario:
    name: str
    stable_steps: bool
    needs_dynamic_replanning: bool
    needs_conversational_clarification: bool = False
    long_running: bool = False
    user_starts_each_task: bool = True
    high_risk_actions: bool = False


@dataclass(frozen=True)
class ProductShape:
    execution_mode: ExecutionMode
    interface_mode: InterfaceMode
    required_controls: tuple[str, ...]


def advise_product_shape(scenario: ProductScenario) -> ProductShape:
    if scenario.needs_dynamic_replanning:
        execution = ExecutionMode.AGENT
    elif scenario.stable_steps:
        execution = ExecutionMode.WORKFLOW
    else:
        execution = ExecutionMode.AI_FEATURE

    if not scenario.user_starts_each_task:
        interface = InterfaceMode.BACKGROUND_NOTIFICATION
    elif scenario.long_running:
        interface = InterfaceMode.TASK_WORKSPACE
    elif scenario.needs_conversational_clarification:
        interface = InterfaceMode.CHAT
    else:
        interface = InterfaceMode.INLINE_OR_FORM

    controls: list[str] = []
    if scenario.long_running:
        controls.extend(["progress", "cancel", "retry", "resume"])
    if scenario.high_risk_actions:
        controls.extend(["action preview", "approval", "audit record"])
    if scenario.needs_conversational_clarification:
        controls.append("structured clarification state")
    if execution is ExecutionMode.AGENT:
        controls.extend(["step budget", "stop condition", "partial result"])

    return ProductShape(execution, interface, tuple(dict.fromkeys(controls)))


def demo() -> None:
    scenarios = [
        ProductScenario("Rewrite selection", False, False),
        ProductScenario("Expense reimbursement", True, False, high_risk_actions=True),
        ProductScenario("Customer support", False, True, True),
        ProductScenario("Deep research", False, True, True, long_running=True),
        ProductScenario(
            "Competitor monitoring",
            False,
            True,
            long_running=True,
            user_starts_each_task=False,
        ),
    ]

    for scenario in scenarios:
        shape = advise_product_shape(scenario)
        print(f"{scenario.name}")
        print(f"  execution: {shape.execution_mode.value}")
        print(f"  interface: {shape.interface_mode.value}")
        if shape.required_controls:
            print(f"  controls: {', '.join(shape.required_controls)}")


if __name__ == "__main__":
    demo()
