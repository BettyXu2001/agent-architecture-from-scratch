import importlib.util
import sys
import unittest
from pathlib import Path


EXAMPLE_PATH = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "01-basic-agent-loop"
    / "basic_agent_loop.py"
)


def load_example_module():
    spec = importlib.util.spec_from_file_location("basic_agent_loop", EXAMPLE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class BasicAgentLoopTests(unittest.TestCase):
    def test_agent_returns_final_answer_after_tool_observations(self):
        module = load_example_module()

        answer, messages = module.run_agent("What is 12 * 7, then add 6?")

        self.assertEqual(answer, "12 * 7 + 6 = 90.")
        self.assertEqual([message.role for message in messages], ["user", "assistant", "tool", "assistant", "tool", "assistant"])

    def test_calculator_rejects_unsupported_expressions(self):
        module = load_example_module()

        with self.assertRaises(ValueError):
            module.calculator({"expression": "__import__('os').system('echo unsafe')"})


if __name__ == "__main__":
    unittest.main()
