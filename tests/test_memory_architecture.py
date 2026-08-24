import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "memory" / "memory_architecture.py"
SPEC = importlib.util.spec_from_file_location("memory_architecture", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class MemoryArchitectureTests(unittest.TestCase):
    def test_long_term_fact_requires_verification(self):
        store = module.MemoryStore()
        item = module.Memory("tone", "concise", "semantic", "u", "model")
        with self.assertRaisesRegex(ValueError, "verification"):
            store.write(item)

    def test_private_and_shared_memory_are_separated(self):
        store = module.MemoryStore()
        store.write(module.working("plan", "secret", "a"))
        store.write(module.artifact("report", "artifact://v1", "a", shared=True))
        self.assertEqual(["report"], [x.key for x in store.retrieve("b")])

    def test_expired_memory_is_not_retrieved(self):
        store = module.MemoryStore()
        expired = module.Memory(
            "old", "x", "working", "a", "run",
            datetime.now(timezone.utc) - timedelta(seconds=1)
        )
        store.write(expired)
        self.assertEqual([], store.retrieve("a"))

    def test_forgetting_is_effective(self):
        store = module.MemoryStore()
        store.write(module.working("plan", "x", "a"))
        store.forget("a", "plan")
        self.assertEqual([], store.retrieve("a"))


if __name__ == "__main__":
    unittest.main()
