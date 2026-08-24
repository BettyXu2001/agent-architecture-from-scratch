"""Risk policy, tamper-evident approvals, escalation, and audit."""

from dataclasses import dataclass, field
import hashlib
import json
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class Action:
    name: str
    resource: str
    arguments: dict
    risk: str


@dataclass(frozen=True)
class Approval:
    subject: str
    action_hash: str
    expires_at: datetime
    policy_version: str


@dataclass
class Audit:
    events: list[dict] = field(default_factory=list)

    def record(self, kind: str, subject: str, detail: dict):
        self.events.append({"kind": kind, "subject": subject, "detail": detail})


def action_hash(action: Action):
    payload = {
        "name": action.name,
        "resource": action.resource,
        "arguments": action.arguments,
        "risk": action.risk,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


class GovernanceRuntime:
    def __init__(self, policy_version: str = "v1"):
        self.policy_version = policy_version
        self.audit = Audit()

    def decide(self, subject: str, action: Action, permissions: set[str]):
        required = f"{action.name}:{action.resource}"
        if required not in permissions:
            decision = "deny"
        elif action.risk in {"high", "irreversible"}:
            decision = "needs_approval"
        else:
            decision = "allow"
        self.audit.record("policy", subject, {"decision": decision, "action": action_hash(action)})
        return decision

    def approve(self, subject: str, action: Action, minutes: int = 5):
        approval = Approval(
            subject,
            action_hash(action),
            datetime.now(timezone.utc) + timedelta(minutes=minutes),
            self.policy_version,
        )
        self.audit.record("approval", subject, {"action": approval.action_hash})
        return approval

    def execute(self, subject: str, action: Action, permissions: set[str], approval=None):
        decision = self.decide(subject, action, permissions)
        if decision == "deny":
            raise PermissionError("action denied")
        if decision == "needs_approval":
            if approval is None:
                raise PermissionError("approval required")
            if approval.subject != subject:
                raise PermissionError("approval subject mismatch")
            if approval.action_hash != action_hash(action):
                raise PermissionError("approved action changed")
            if approval.expires_at <= datetime.now(timezone.utc):
                raise PermissionError("approval expired")
            if approval.policy_version != self.policy_version:
                raise PermissionError("policy changed")
        self.audit.record("execute", subject, {"action": action_hash(action)})
        return "executed"


def escalation(goal: str, completed: list[str], gaps: list[str], evidence: list[str]):
    return {
        "goal": goal,
        "completed": tuple(completed),
        "gaps": tuple(gaps),
        "evidence": tuple(evidence),
        "requested_decision": "human review",
    }


if __name__ == "__main__":
    runtime = GovernanceRuntime()
    action = Action("send", "email", {"to": "user@example.com", "body": "draft"}, "high")
    permissions = {"send:email"}
    approval = runtime.approve("user-1", action)
    print(runtime.execute("user-1", action, permissions, approval))
    print(runtime.audit.events)
