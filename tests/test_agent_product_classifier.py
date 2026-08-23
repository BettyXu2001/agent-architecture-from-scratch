import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "product-decisions" / "agent_product_classifier.py"
SPEC = importlib.util.spec_from_file_location("agent_product_classifier", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AgentProductClassifierTests(unittest.TestCase):
    def test_stable_steps_start_with_workflow(self):
        request = MODULE.ProductRequest(
            "Invoice processing",
            stable_steps=True,
            needs_dynamic_decisions=False,
            high_risk_actions=True,
        )

        result = MODULE.recommend_architecture(request)

        self.assertEqual(result.architecture, MODULE.StartingArchitecture.WORKFLOW)
        self.assertTrue(any("approval" in item for item in result.product_requirements))

    def test_dynamic_task_starts_with_single_agent(self):
        request = MODULE.ProductRequest(
            "Research assistant",
            stable_steps=False,
            needs_dynamic_decisions=True,
            long_running=True,
        )

        result = MODULE.recommend_architecture(request)

        self.assertEqual(result.architecture, MODULE.StartingArchitecture.SINGLE_AGENT)
        self.assertTrue(any("progress" in item for item in result.product_requirements))

    def test_multiple_independent_specialists_only_create_a_candidate(self):
        request = MODULE.ProductRequest(
            "Incident investigation",
            stable_steps=False,
            needs_dynamic_decisions=True,
            independent_specialists=3,
        )

        result = MODULE.recommend_architecture(request)

        self.assertEqual(result.architecture, MODULE.StartingArchitecture.MULTI_AGENT_CANDIDATE)
        self.assertTrue(any("baseline" in item for item in result.product_requirements))


if __name__ == "__main__":
    unittest.main()
