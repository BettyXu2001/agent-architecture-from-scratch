import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "product-decisions" / "product_shape_advisor.py"
SPEC = importlib.util.spec_from_file_location("product_shape_advisor", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ProductShapeAdvisorTests(unittest.TestCase):
    def test_stable_process_uses_workflow_without_forcing_chat(self):
        scenario = MODULE.ProductScenario(
            "Expense reimbursement",
            stable_steps=True,
            needs_dynamic_replanning=False,
            high_risk_actions=True,
        )

        result = MODULE.advise_product_shape(scenario)

        self.assertEqual(result.execution_mode, MODULE.ExecutionMode.WORKFLOW)
        self.assertEqual(result.interface_mode, MODULE.InterfaceMode.INLINE_OR_FORM)
        self.assertIn("approval", result.required_controls)

    def test_long_running_agent_uses_task_workspace(self):
        scenario = MODULE.ProductScenario(
            "Deep research",
            stable_steps=False,
            needs_dynamic_replanning=True,
            needs_conversational_clarification=True,
            long_running=True,
        )

        result = MODULE.advise_product_shape(scenario)

        self.assertEqual(result.execution_mode, MODULE.ExecutionMode.AGENT)
        self.assertEqual(result.interface_mode, MODULE.InterfaceMode.TASK_WORKSPACE)
        self.assertIn("resume", result.required_controls)
        self.assertIn("partial result", result.required_controls)

    def test_proactive_agent_uses_background_notification(self):
        scenario = MODULE.ProductScenario(
            "Competitor monitoring",
            stable_steps=False,
            needs_dynamic_replanning=True,
            long_running=True,
            user_starts_each_task=False,
        )

        result = MODULE.advise_product_shape(scenario)

        self.assertEqual(result.interface_mode, MODULE.InterfaceMode.BACKGROUND_NOTIFICATION)


if __name__ == "__main__":
    unittest.main()
