import importlib.util
from pathlib import Path
import unittest


PATH = (
    Path(__file__).parents[1]
    / "examples"
    / "single-agent"
    / "bounded_research_agent.py"
)
SPEC = importlib.util.spec_from_file_location("bounded_agent", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class BoundedAgentTests(unittest.TestCase):
    def test_normal_run_uses_observation_then_finishes(self):
        state = module.run_agent("architecture")
        self.assertEqual("completed", state.status)
        self.assertEqual(1, len(state.evidence))

    def test_missing_goal_clarifies_before_tool_use(self):
        state = module.run_agent("")
        self.assertEqual("needs_user", state.status)
        self.assertFalse(state.evidence)

    def test_repeated_action_stops_for_no_progress(self):
        state = module.run_agent("architecture", module.RepeatingPolicy())
        self.assertEqual("no_progress", state.status)
        self.assertEqual(1, len(state.evidence))

    def test_tool_boundary_blocks_unregistered_tool(self):
        runtime = module.ToolRuntime()
        with self.assertRaises(PermissionError):
            runtime.execute(module.Action("send_email", {"to": "x"}))

    def test_critic_returns_actionable_issues(self):
        ok, issues = module.reflect("Draft")
        self.assertFalse(ok)
        revised = module.revise("Draft", issues)
        self.assertTrue(revised.endswith("."))
        self.assertIn("Evidence", revised)


if __name__ == "__main__":
    unittest.main()
