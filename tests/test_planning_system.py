import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "planning" / "planning_system.py"
SPEC = importlib.util.spec_from_file_location("planning_system", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class PlanningSystemTests(unittest.TestCase):
    def test_dependency_cycle_is_rejected(self):
        tasks = [
            module.Task("a", "research a", ("b",)),
            module.Task("b", "write b", ("a",)),
        ]
        with self.assertRaisesRegex(ValueError, "cycle"):
            module.validate(tasks)

    def test_executor_respects_dependencies(self):
        ledger = module.build_ledger("topic")
        module.execute(ledger, lambda task: f"artifact:{task.id}")
        self.assertTrue(all(t.status == "completed" for t in ledger.tasks.values()))
        positions = {event.split(":")[0]: i for i, event in enumerate(ledger.events)}
        self.assertLess(positions["research"], positions["compare"])
        self.assertLess(positions["compare"], positions["write"])

    def test_replanner_preserves_completed_and_retries_failed(self):
        ledger = module.build_ledger("topic")
        module.execute(
            ledger,
            lambda task: f"artifact:{task.id}",
            fail_once={"research"},
        )
        self.assertEqual("failed", ledger.tasks["research"].status)
        module.replan_failed(ledger)
        module.execute(ledger, lambda task: f"artifact:{task.id}")
        self.assertEqual("completed", ledger.tasks["write"].status)
        self.assertIn("using fallback", ledger.tasks["research"].goal)

    def test_illegal_state_transition_is_rejected(self):
        ledger = module.build_ledger("topic")
        with self.assertRaisesRegex(ValueError, "illegal"):
            ledger.transition("research", "completed")


if __name__ == "__main__":
    unittest.main()
