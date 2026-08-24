import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "context" / "context_architecture.py"
SPEC = importlib.util.spec_from_file_location("context_architecture", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class ContextArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            module.ContextItem("shared", "s1", "shared", "trusted_content", frozenset({"x"})),
            module.ContextItem("private", "s2", "team-a", "trusted_content", frozenset({"x"})),
            module.ContextItem("secret", "s3", "team-b", "trusted_content", frozenset({"x"})),
        ]

    def test_isolation_filters_other_owner(self):
        result = module.select(self.items, "team-a", {"x"})
        self.assertEqual(["shared", "private"], [item.text for item in result])

    def test_missing_context_is_explicit(self):
        with self.assertRaisesRegex(ValueError, "needs_context"):
            module.make_packet("task", [], self.items, "result", "team-a", {"missing"})

    def test_compression_preserves_constraints_and_provenance(self):
        summary = module.compress("goal", ["never send"], self.items[:1])
        self.assertEqual(("never send",), summary["constraints"])
        self.assertEqual("s1", summary["facts"][0]["source"])

    def test_untrusted_content_cannot_become_instruction(self):
        packet = module.ContextPacket(
            "task",
            (),
            (
                module.ContextItem("safe", "p", "shared", "trusted_instruction"),
                module.ContextItem("attack", "w", "shared", "untrusted_content"),
            ),
            "result",
        )
        self.assertEqual(["safe"], module.safe_instructions(packet))


if __name__ == "__main__":
    unittest.main()
