"""Communication primitives with explicit identity, versions, and artifacts."""

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class Message:
    id: str
    sender: str
    recipient: str
    task_id: str
    kind: str
    payload: dict


class DirectBus:
    def __init__(self):
        self.seen = set()
        self.inboxes = {}

    def send(self, message: Message):
        if message.id in self.seen:
            return False
        self.seen.add(message.id)
        self.inboxes.setdefault(message.recipient, []).append(message)
        return True


@dataclass
class SharedState:
    value: dict = field(default_factory=dict)
    version: int = 0

    def update(self, expected_version: int, changes: dict):
        if expected_version != self.version:
            raise ValueError("version conflict")
        self.value.update(changes)
        self.version += 1
        return self.version


@dataclass(frozen=True)
class Entry:
    id: str
    owner: str
    kind: str
    content: str
    status: str = "open"


class Blackboard:
    def __init__(self):
        self.entries = {}

    def post(self, entry: Entry):
        if entry.id in self.entries:
            return False
        self.entries[entry.id] = entry
        return True

    def query(self, kind: str):
        return [entry for entry in self.entries.values() if entry.kind == kind]


class EventBus:
    def __init__(self):
        self.subscribers: dict[str, list[Callable]] = {}
        self.processed: set[tuple[str, str]] = set()

    def subscribe(self, kind: str, name: str, handler: Callable):
        self.subscribers.setdefault(kind, []).append((name, handler))

    def publish(self, event_id: str, kind: str, payload: dict):
        for name, handler in self.subscribers.get(kind, []):
            key = (name, event_id)
            if key in self.processed:
                continue
            handler(payload)
            self.processed.add(key)


class ArtifactStore:
    def __init__(self):
        self.data = {}

    def put(self, artifact_id: str, content: str):
        if artifact_id in self.data:
            raise ValueError("immutable artifact already exists")
        self.data[artifact_id] = content

    def get(self, artifact_id: str):
        if artifact_id not in self.data:
            raise ValueError("artifact missing")
        return self.data[artifact_id]


if __name__ == "__main__":
    bus = DirectBus()
    print(bus.send(Message("m1", "a", "b", "t1", "request", {"goal": "research"})))
    state = SharedState()
    state.update(0, {"status": "running"})
    board = Blackboard()
    board.post(Entry("e1", "a", "evidence", "source:1"))
    events = EventBus()
    events.subscribe("done", "ui", print)
    events.publish("v1", "done", {"task": "t1"})
