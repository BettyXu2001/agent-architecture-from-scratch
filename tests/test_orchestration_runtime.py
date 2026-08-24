import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "orchestration" / "orchestration_runtime.py"
SPEC = importlib.util.spec_from_file_location("orchestration", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class OrchestrationTests(unittest.TestCase):
    def test_dag_runs_dependencies_before_join(self):
        order = []
        module.run_dag(
            {"a": set(), "b": {"a"}, "c": {"a"}, "d": {"b", "c"}},
            lambda node: order.append(node),
        )
        self.assertLess(order.index("a"), order.index("b"))
        self.assertGreater(order.index("d"), order.index("c"))

    def test_dag_rejects_cycle(self):
        with self.assertRaisesRegex(ValueError, "cycle"):
            module.validate_dag({"a": {"b"}, "b": {"a"}})

    def test_state_machine_rejects_illegal_transition(self):
        checkpoint = module.Checkpoint()
        with self.assertRaisesRegex(ValueError, "illegal"):
            module.transition(checkpoint, "completed")

    def test_cycle_is_bounded(self):
        _, trace = module.bounded_cycle("x", lambda _: False, max_rounds=2)
        self.assertEqual("stop:budget", trace[-1])

    def test_durable_effect_is_not_repeated(self):
        checkpoint = module.Checkpoint()
        calls = []
        first = module.durable_effect(checkpoint, "send", lambda: calls.append(1) or "ok")
        second = module.durable_effect(checkpoint, "send", lambda: calls.append(2) or "bad")
        self.assertEqual(first, second)
        self.assertEqual([1], calls)

    def test_resume_skips_completed_nodes(self):
        checkpoint = module.Checkpoint()
        module.resume(checkpoint, ["a", "b"])
        module.resume(checkpoint, ["a", "b", "c"])
        runs = [x for x in checkpoint.trace if x.endswith(":run")]
        self.assertEqual(["node:a:run", "node:b:run", "node:c:run"], runs)


if __name__ == "__main__":
    unittest.main()
