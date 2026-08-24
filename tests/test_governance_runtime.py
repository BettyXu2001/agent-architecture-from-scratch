import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "governance" / "governance_runtime.py"
SPEC = importlib.util.spec_from_file_location("governance", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.runtime = module.GovernanceRuntime()
        self.action = module.Action("send", "email", {"to": "a", "body": "x"}, "high")
        self.permissions = {"send:email"}

    def test_high_risk_action_requires_approval(self):
        with self.assertRaisesRegex(PermissionError, "approval required"):
            self.runtime.execute("u", self.action, self.permissions)

    def test_approval_is_bound_to_exact_action(self):
        approval = self.runtime.approve("u", self.action)
        changed = module.Action("send", "email", {"to": "b", "body": "x"}, "high")
        with self.assertRaisesRegex(PermissionError, "changed"):
            self.runtime.execute("u", changed, self.permissions, approval)

    def test_expired_approval_is_rejected(self):
        approval = module.Approval(
            "u",
            module.action_hash(self.action),
            datetime.now(timezone.utc) - timedelta(seconds=1),
            "v1",
        )
        with self.assertRaisesRegex(PermissionError, "expired"):
            self.runtime.execute("u", self.action, self.permissions, approval)

    def test_policy_change_invalidates_approval(self):
        approval = self.runtime.approve("u", self.action)
        self.runtime.policy_version = "v2"
        with self.assertRaisesRegex(PermissionError, "policy changed"):
            self.runtime.execute("u", self.action, self.permissions, approval)

    def test_missing_permission_is_denied_before_execution(self):
        low = module.Action("read", "account", {}, "low")
        with self.assertRaisesRegex(PermissionError, "denied"):
            self.runtime.execute("u", low, set())

    def test_escalation_carries_progress_and_gap(self):
        package = module.escalation("goal", ["research"], ["approval"], ["source:1"])
        self.assertEqual(("research",), package["completed"])
        self.assertEqual(("approval",), package["gaps"])


if __name__ == "__main__":
    unittest.main()
