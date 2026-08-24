import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "hierarchical" / "hierarchical_system.py"
SPEC = importlib.util.spec_from_file_location("hierarchy", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class HierarchicalSystemTests(unittest.TestCase):
    def test_hierarchy_has_single_final_owner(self):
        final, runtime = module.coordinator("topic")
        self.assertEqual("coordinator", final["owner"])
        self.assertEqual(2, len(final["artifacts"]))
        self.assertEqual(5, len(runtime.seen))

    def test_team_failure_is_isolated_and_visible(self):
        final, _ = module.coordinator("topic", fail_team="risk")
        self.assertEqual(1, len(final["artifacts"]))
        self.assertEqual(["worker failed"], final["gaps"])

    def test_depth_is_bounded(self):
        runtime = module.Runtime(max_depth=1)
        with self.assertRaisesRegex(ValueError, "depth"):
            runtime.claim(module.Task("deep", "x", "p", 2, 1))

    def test_duplicate_delegation_is_rejected(self):
        runtime = module.Runtime()
        task = module.Task("same", "x", None, 0, 1)
        runtime.claim(task)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            runtime.claim(task)

    def test_global_budget_is_conserved(self):
        runtime = module.Runtime(global_budget=1)
        runtime.claim(module.Task("one", "x", None, 0, 1))
        with self.assertRaisesRegex(ValueError, "budget"):
            runtime.claim(module.Task("two", "x", None, 0, 1))


if __name__ == "__main__":
    unittest.main()
