import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "workflows" / "content_pipeline.py"
SPEC = importlib.util.spec_from_file_location("content_pipeline", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class WorkflowPatternTests(unittest.TestCase):
    def test_sequential_has_ordered_trace(self):
        self.assertEqual(
            ["outline:ok", "draft:ok", "fact_check:ok"],
            module.sequential("test").trace,
        )

    def test_router_has_safe_fallback(self):
        self.assertEqual("support", module.route("退款"))
        self.assertEqual("clarify", module.route("ambiguous request"))

    def test_parallel_keeps_partial_results(self):
        run = module.parallel_checks("draft", fail="facts")
        self.assertEqual(2, len(run.state["checks"]))
        self.assertIn("facts:timeout", run.warnings)

    def test_evaluator_is_bounded(self):
        run = module.evaluator_optimizer("Draft", max_rounds=1)
        self.assertEqual("budget_exhausted", run.state["status"])
        self.assertEqual(1, len([x for x in run.trace if x.startswith("evaluate")]))

    def test_composition_uses_explicit_fallback(self):
        run = module.composed("Agent products", fail_check="facts")
        self.assertEqual("cached_sources", run.state["fallback"])


if __name__ == "__main__":
    unittest.main()
