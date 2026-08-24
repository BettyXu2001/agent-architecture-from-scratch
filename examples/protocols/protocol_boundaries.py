"""Protocol-boundary simulation for MCP-like capabilities and A2A-like tasks."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Capability:
    name: str
    kind: str
    input_fields: frozenset[str]


@dataclass(frozen=True)
class AgentCard:
    name: str
    endpoint: str
    versions: tuple[str, ...]
    skills: tuple[str, ...]
    auth_audience: str


@dataclass(frozen=True)
class Token:
    subject: str
    audience: str
    scopes: frozenset[str]


def authorize(token: Token, audience: str, scope: str):
    if token.audience != audience:
        raise PermissionError("invalid token audience")
    if scope not in token.scopes:
        raise PermissionError("insufficient scope")


class McpLikeServer:
    def __init__(self):
        self.capabilities = {
            "search": Capability("search", "tool", frozenset({"query"}))
        }

    def discover(self):
        return tuple(self.capabilities.values())

    def call(self, name: str, arguments: dict[str, Any], token: Token):
        authorize(token, "mcp://search", f"tool:{name}")
        capability = self.capabilities.get(name)
        if capability is None:
            raise ValueError("unknown capability")
        if set(arguments) != set(capability.input_fields):
            raise ValueError("invalid tool arguments")
        return {"content": f"result:{arguments['query']}", "trust": "untrusted_content"}


@dataclass
class RemoteTask:
    id: str
    status: str = "submitted"
    messages: list[dict] = field(default_factory=list)
    artifacts: list[dict] = field(default_factory=list)
    version: int = 0

    def transition(self, status: str):
        allowed = {
            "submitted": {"working", "cancelled"},
            "working": {"input_required", "completed", "failed", "cancelled"},
            "input_required": {"working", "cancelled"},
        }
        if status not in allowed.get(self.status, set()):
            raise ValueError(f"illegal task transition {self.status}->{status}")
        self.status = status
        self.version += 1

    def add_artifact(self, artifact_id: str, media_type: str, data: Any):
        self.artifacts.append(
            {"artifactId": artifact_id, "parts": [{"mediaType": media_type, "data": data}]}
        )


class A2ALikeServer:
    card = AgentCard(
        "report-agent",
        "https://agent.example/a2a",
        ("1.0",),
        ("report",),
        "https://agent.example/a2a",
    )

    def __init__(self):
        self.tasks = {}

    def send(self, message_id: str, parts: list[dict], token: Token):
        authorize(token, self.card.auth_audience, "task:create")
        if not message_id or not parts:
            raise ValueError("invalid message")
        task_id = f"task-{message_id}"
        if task_id in self.tasks:
            return self.tasks[task_id]
        task = RemoteTask(task_id, messages=[{"messageId": message_id, "parts": parts}])
        self.tasks[task_id] = task
        return task

    def get(self, task_id: str):
        return self.tasks[task_id]

    def complete(self, task_id: str, with_artifact: bool = True):
        task = self.tasks[task_id]
        task.transition("working")
        if with_artifact:
            task.add_artifact("report-1", "application/json", {"answer": "done"})
        task.transition("completed")
        return task


def validate_product_success(task: RemoteTask):
    if task.status != "completed":
        return False, "not terminal success"
    if not task.artifacts:
        return False, "completed task has no required artifact"
    return True, "ok"


if __name__ == "__main__":
    mcp = McpLikeServer()
    print(mcp.discover())
    print(mcp.call("search", {"query": "agents"}, Token("u", "mcp://search", frozenset({"tool:search"}))))
    a2a = A2ALikeServer()
    token = Token("u", a2a.card.auth_audience, frozenset({"task:create"}))
    task = a2a.send("m1", [{"text": "build report"}], token)
    print(a2a.complete(task.id), validate_product_success(task))
