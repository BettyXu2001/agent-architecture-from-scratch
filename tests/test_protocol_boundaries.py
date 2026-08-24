import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "protocols" / "protocol_boundaries.py"
SPEC = importlib.util.spec_from_file_location("protocols", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class ProtocolBoundaryTests(unittest.TestCase):
    def test_mcp_capability_and_arguments_are_validated(self):
        server = module.McpLikeServer()
        token = module.Token("u", "mcp://search", frozenset({"tool:search"}))
        result = server.call("search", {"query": "agents"}, token)
        self.assertEqual("untrusted_content", result["trust"])
        with self.assertRaisesRegex(ValueError, "arguments"):
            server.call("search", {"query": "x", "extra": "y"}, token)

    def test_token_is_bound_to_audience(self):
        server = module.McpLikeServer()
        token = module.Token("u", "https://wrong", frozenset({"tool:search"}))
        with self.assertRaisesRegex(PermissionError, "audience"):
            server.call("search", {"query": "x"}, token)

    def test_a2a_message_is_idempotent_by_message_id(self):
        server = module.A2ALikeServer()
        token = module.Token("u", server.card.auth_audience, frozenset({"task:create"}))
        first = server.send("m1", [{"text": "report"}], token)
        second = server.send("m1", [{"text": "report"}], token)
        self.assertIs(first, second)

    def test_protocol_completed_is_not_product_success_without_artifact(self):
        server = module.A2ALikeServer()
        token = module.Token("u", server.card.auth_audience, frozenset({"task:create"}))
        task = server.send("m2", [{"text": "report"}], token)
        server.complete(task.id, with_artifact=False)
        success, reason = module.validate_product_success(task)
        self.assertFalse(success)
        self.assertIn("no required artifact", reason)

    def test_task_transitions_are_bounded(self):
        task = module.RemoteTask("t")
        with self.assertRaisesRegex(ValueError, "illegal"):
            task.transition("completed")


if __name__ == "__main__":
    unittest.main()
