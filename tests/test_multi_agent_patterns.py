import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "multi-agent" / "patterns.py"
SPEC = importlib.util.spec_from_file_location("multi_agent_patterns", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class MultiAgentPatternTests(unittest.TestCase):
    def setUp(self):
        self.packet = module.Packet("refund request", {"order": "A-1"})

    def test_manager_retains_answer_ownership(self):
        result, trace = module.manager(self.packet)
        self.assertEqual("manager", result.agent)
        self.assertEqual("manager", trace.final_owner)

    def test_handoff_transfers_answer_ownership(self):
        result, trace = module.run_handoff(self.packet)
        self.assertEqual("refund", trace.active_agent)
        self.assertEqual("refund", trace.final_owner)
        self.assertIn("handoff:triage->refund", trace.events)

    def test_group_chat_has_bounded_termination(self):
        result, trace = module.group_chat(self.packet, max_rounds=3)
        self.assertEqual("finalizer", trace.final_owner)
        self.assertTrue(any(event.startswith("stop:") for event in trace.events))
        self.assertLessEqual(
            len([e for e in trace.events if e.startswith("speak:")]), 3
        )

    def test_parallel_pattern_has_explicit_join(self):
        _, trace = module.parallel_specialists(self.packet)
        self.assertIn("join:all", trace.events)

    def test_hybrid_has_single_final_owner(self):
        result, trace = module.hybrid(self.packet)
        self.assertEqual("refund", result.agent)
        self.assertEqual("refund", trace.final_owner)
        self.assertIn("call:policy", trace.events)


if __name__ == "__main__":
    unittest.main()
