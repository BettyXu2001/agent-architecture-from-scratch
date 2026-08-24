import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "multi-agent" / "single_vs_multi.py"
SPEC = importlib.util.spec_from_file_location("single_vs_multi", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class MultiAgentFundamentalsTests(unittest.TestCase):
    def test_manager_owns_final_answer(self):
        metrics = module.Metrics()
        result = module.multi_agent("agents", metrics)
        self.assertEqual("manager", result.owner)
        self.assertEqual(2, metrics.calls)

    def test_specialist_contexts_are_isolated(self):
        metrics = module.Metrics()
        module.multi_agent("agents", metrics)
        self.assertNotIn("risk_sources", metrics.visible_fields["researcher"])
        self.assertNotIn("public_sources", metrics.visible_fields["risk"])

    def test_partial_failure_is_visible(self):
        metrics = module.Metrics()
        result = module.multi_agent("fail-risk", metrics)
        self.assertIn("gaps=risk source unavailable", result.content)
        self.assertIn("source:research", result.evidence)

    def test_modular_single_keeps_one_decision_call(self):
        metrics = module.Metrics()
        result = module.modular_single("agents", metrics)
        self.assertEqual("controller", result.owner)
        self.assertEqual(1, metrics.calls)


if __name__ == "__main__":
    unittest.main()
