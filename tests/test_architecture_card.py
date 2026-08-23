import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "architecture-map" / "architecture_card.py"
SPEC = importlib.util.spec_from_file_location("architecture_card", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ArchitectureCardTests(unittest.TestCase):
    def make_workflow(self):
        return MODULE.ArchitectureCard(
            name="Workflow",
            control=MODULE.Control.CODE,
            reasoning="direct",
            topology=MODULE.Topology.WORKFLOW,
            context="shared",
            memory="none",
            communication="typed outputs",
            orchestration="sequential",
            runtime=MODULE.Runtime.REQUEST_RESPONSE,
        )

    def test_describe_includes_every_architecture_dimension(self):
        text = MODULE.describe(self.make_workflow())

        for dimension in (
            "control",
            "reasoning",
            "topology",
            "context",
            "memory",
            "communication",
            "orchestration",
            "runtime",
        ):
            self.assertIn(f"{dimension}:", text)

    def test_compare_reports_only_changed_dimensions(self):
        before = self.make_workflow()
        after = MODULE.ArchitectureCard(
            name="Agent",
            control=MODULE.Control.HYBRID,
            reasoning="react",
            topology=MODULE.Topology.SINGLE_AGENT,
            context="shared",
            memory="none",
            communication="typed outputs",
            orchestration="sequential",
            runtime=MODULE.Runtime.REQUEST_RESPONSE,
        )

        changes = MODULE.compare(before, after)

        self.assertEqual(
            changes,
            (
                "control: code -> hybrid",
                "reasoning: direct -> react",
                "topology: workflow -> single-agent",
            ),
        )


if __name__ == "__main__":
    unittest.main()
