import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "evaluation" / "evaluation_harness.py"
SPEC = importlib.util.spec_from_file_location("evaluation", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class EvaluationHarnessTests(unittest.TestCase):
    def setUp(self):
        self.scenario = module.Scenario(
            "s1", "research", frozenset({"report"}),
            frozenset({"search"}), frozenset({"send"})
        )

    def test_task_and_trajectory_are_separate(self):
        trace = module.run_scenario(self.scenario)
        self.assertTrue(module.task_grade(trace, self.scenario)["pass"])
        trajectory = module.trajectory_grade(trace, self.scenario)
        self.assertTrue(trajectory["required_tools_present"])
        self.assertTrue(trajectory["forbidden_tools_absent"])

    def test_missing_artifact_fails_product_outcome(self):
        trace = module.run_scenario(self.scenario)
        trace.outcome["artifacts"] = set()
        grade = module.task_grade(trace, self.scenario)
        self.assertFalse(grade["pass"])
        self.assertEqual(["report"], grade["missing_artifacts"])

    def test_attribution_includes_all_spans(self):
        trace = module.run_scenario(self.scenario)
        usage = module.attribution(trace)
        self.assertAlmostEqual(0.08, usage["total_cost"])
        self.assertEqual(410, usage["total_tokens"])

    def test_cost_per_success_includes_run_cost(self):
        report = module.evaluate([self.scenario], module.run_scenario)
        self.assertEqual(1.0, report["success_rate"])
        self.assertAlmostEqual(0.08, report["cost_per_success"])

    def test_specialist_ablation_changes_cost(self):
        full = module.attribution(module.run_scenario(self.scenario, True))
        ablated = module.attribution(module.run_scenario(self.scenario, False))
        self.assertGreater(full["total_cost"], ablated["total_cost"])


if __name__ == "__main__":
    unittest.main()
