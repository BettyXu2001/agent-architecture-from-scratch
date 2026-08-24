"""Framework-free implementations of common multi-agent patterns."""

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class Packet:
    task: str
    fields: dict[str, str]


@dataclass(frozen=True)
class AgentResult:
    agent: str
    content: str
    handoff_to: str | None = None


@dataclass
class Trace:
    events: list[str] = field(default_factory=list)
    active_agent: str = "triage"
    final_owner: str | None = None


def policy_agent(packet: Packet) -> AgentResult:
    return AgentResult("policy", f"eligible:{packet.fields.get('order', 'unknown')}")


def risk_agent(packet: Packet) -> AgentResult:
    return AgentResult("risk", "risk:low")


def manager(packet: Packet, workers=None) -> tuple[AgentResult, Trace]:
    workers = workers or (policy_agent, risk_agent)
    trace = Trace(active_agent="manager")
    parts = []
    for worker in workers:
        result = worker(packet)
        trace.events.append(f"call:{result.agent}")
        parts.append(result.content)
    trace.final_owner = "manager"
    return AgentResult("manager", "; ".join(parts)), trace


def parallel_specialists(packet: Packet) -> tuple[AgentResult, Trace]:
    # The deterministic example records fan-out; production may run concurrently.
    result, trace = manager(packet)
    trace.events.insert(0, "fan-out:policy,risk")
    trace.events.append("join:all")
    return result, trace


def triage(packet: Packet) -> AgentResult:
    if "refund" in packet.task.lower():
        return AgentResult("triage", "transfer", "refund")
    return AgentResult("triage", "transfer", "general")


def refund(packet: Packet) -> AgentResult:
    return AgentResult("refund", f"refund help for {packet.fields.get('order', 'unknown')}")


def general(packet: Packet) -> AgentResult:
    return AgentResult("general", "general help")


def run_handoff(packet: Packet, max_handoffs: int = 2) -> tuple[AgentResult, Trace]:
    agents: dict[str, Callable[[Packet], AgentResult]] = {
        "triage": triage, "refund": refund, "general": general
    }
    trace = Trace()
    visited = set()
    for _ in range(max_handoffs + 1):
        if trace.active_agent in visited:
            return AgentResult(trace.active_agent, "handoff loop"), trace
        visited.add(trace.active_agent)
        result = agents[trace.active_agent](packet)
        trace.events.append(f"run:{trace.active_agent}")
        if result.handoff_to is None:
            trace.final_owner = result.agent
            return result, trace
        trace.events.append(f"handoff:{result.agent}->{result.handoff_to}")
        trace.active_agent = result.handoff_to
    return AgentResult(trace.active_agent, "handoff budget exhausted"), trace


def group_chat(packet: Packet, max_rounds: int = 3) -> tuple[AgentResult, Trace]:
    speakers = ("writer", "reviewer")
    trace = Trace(active_agent=speakers[0])
    draft = packet.task
    previous = None
    for round_no in range(max_rounds):
        speaker = speakers[round_no % len(speakers)]
        trace.events.append(f"speak:{speaker}")
        current = draft if speaker == "writer" else draft + " [reviewed]"
        if current == previous:
            trace.events.append("stop:no-progress")
            break
        previous, draft = current, current
        if "[reviewed]" in draft:
            trace.events.append("stop:approved")
            break
    trace.final_owner = "finalizer"
    return AgentResult("finalizer", draft), trace


def hybrid(packet: Packet) -> tuple[AgentResult, Trace]:
    handoff_result, trace = run_handoff(packet)
    if handoff_result.agent == "refund":
        checks, check_trace = manager(packet)
        trace.events.extend(check_trace.events)
        trace.final_owner = "refund"
        return AgentResult("refund", handoff_result.content + "; " + checks.content), trace
    trace.final_owner = handoff_result.agent
    return handoff_result, trace


if __name__ == "__main__":
    request = Packet("refund request", {"order": "A-1"})
    for pattern in (manager, parallel_specialists, run_handoff, group_chat, hybrid):
        print(pattern.__name__, pattern(request))
