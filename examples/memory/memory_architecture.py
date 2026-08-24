"""Typed memory with explicit write, read, sharing, and forgetting policies."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class Memory:
    key: str
    value: str
    kind: str
    owner: str
    source: str
    expires_at: datetime | None = None
    shared: bool = False


class MemoryStore:
    def __init__(self):
        self.records = {}

    def write(self, memory: Memory, verified: bool = False):
        if memory.kind in {"semantic", "procedural"} and not verified:
            raise ValueError("verification required")
        self.records[(memory.owner, memory.key)] = memory

    def retrieve(self, owner: str, kind: str | None = None):
        now = datetime.now(timezone.utc)
        return [
            item for item in self.records.values()
            if (item.owner == owner or item.shared)
            and (kind is None or item.kind == kind)
            and (item.expires_at is None or item.expires_at > now)
        ]

    def forget(self, owner: str, key: str):
        self.records.pop((owner, key), None)


def working(key: str, value: str, owner: str):
    return Memory(
        key, value, "working", owner, "current-run",
        datetime.now(timezone.utc) + timedelta(hours=1)
    )


def artifact(key: str, reference: str, owner: str, shared: bool = False):
    return Memory(key, reference, "artifact", owner, "artifact-store", shared=shared)


if __name__ == "__main__":
    store = MemoryStore()
    store.write(working("plan", "research -> write", "agent-a"))
    store.write(Memory("tone", "concise", "semantic", "user-1", "user-confirmed"), verified=True)
    store.write(artifact("report", "artifact://report/v1", "agent-a", shared=True))
    print(store.retrieve("agent-a"))
    print(store.retrieve("agent-b"))
