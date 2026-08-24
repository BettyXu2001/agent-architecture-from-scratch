import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "communication" / "communication_patterns.py"
SPEC = importlib.util.spec_from_file_location("communication", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class CommunicationPatternTests(unittest.TestCase):
    def test_direct_message_is_idempotent(self):
        bus = module.DirectBus()
        msg = module.Message("m1", "a", "b", "t", "request", {})
        self.assertTrue(bus.send(msg))
        self.assertFalse(bus.send(msg))
        self.assertEqual(1, len(bus.inboxes["b"]))

    def test_shared_state_detects_conflict(self):
        state = module.SharedState()
        state.update(0, {"status": "running"})
        with self.assertRaisesRegex(ValueError, "conflict"):
            state.update(0, {"status": "done"})

    def test_blackboard_deduplicates_entries(self):
        board = module.Blackboard()
        entry = module.Entry("e1", "a", "evidence", "source")
        self.assertTrue(board.post(entry))
        self.assertFalse(board.post(entry))

    def test_event_subscriber_is_idempotent(self):
        calls = []
        bus = module.EventBus()
        bus.subscribe("done", "ui", calls.append)
        bus.publish("event-1", "done", {"x": 1})
        bus.publish("event-1", "done", {"x": 1})
        self.assertEqual([{"x": 1}], calls)

    def test_artifact_is_immutable_and_missing_is_explicit(self):
        store = module.ArtifactStore()
        store.put("a1", "v1")
        with self.assertRaisesRegex(ValueError, "already exists"):
            store.put("a1", "v2")
        with self.assertRaisesRegex(ValueError, "missing"):
            store.get("unknown")


if __name__ == "__main__":
    unittest.main()
