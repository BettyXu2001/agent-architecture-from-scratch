import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = (
    Path(__file__).parents[1]
    / "examples"
    / "overview"
    / "architecture_decision.py"
)
SPEC = importlib.util.spec_from_file_location("architecture_decision", MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class ArchitectureDecisionTests(unittest.TestCase):
    def test_known_path_stays_workflow(self):
        result = module.recommend(module.TaskProfile(path_known=True))
        self.assertEqual("workflow", result.architecture)

    def test_high_risk_dynamic_task_is_hybrid(self):
        result = module.recommend(
            module.TaskProfile(
                path_known=False,
                needs_dynamic_actions=True,
                side_effects=True,
                high_risk=True,
            )
        )
        self.assertEqual("hybrid", result.architecture)
        self.assertIn("use idempotency keys", result.safeguards)

    def test_context_and_duration_add_only_needed_capabilities(self):
        result = module.recommend(
            module.TaskProfile(
                path_known=False,
                needs_dynamic_actions=True,
                context_bottleneck=True,
                long_running=True,
            )
        )
        self.assertEqual("agent+specialists+durable-runtime", result.architecture)


if __name__ == "__main__":
    unittest.main()
