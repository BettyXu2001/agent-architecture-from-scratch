import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "reliability" / "fault_injection.py"
SPEC = importlib.util.spec_from_file_location("reliability", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class ReliabilityTests(unittest.TestCase):
    def test_transient_error_retries_but_permanent_does_not(self):
        calls = []
        def flaky():
            calls.append(1)
            if len(calls) == 1:
                raise module.TransientError("timeout")
            return "ok"
        result, attempts = module.retry(flaky)
        self.assertEqual(("ok", 2), (result, attempts))
        with self.assertRaises(module.PermanentError):
            module.retry(lambda: (_ for _ in ()).throw(module.PermanentError("auth")))

    def test_effect_is_idempotent(self):
        store = module.EffectStore()
        calls = []
        first = store.execute_once("pay-1", lambda: calls.append(1) or "paid")
        second = store.execute_once("pay-1", lambda: calls.append(2) or "paid-again")
        self.assertEqual(first, second)
        self.assertEqual([1], calls)

    def test_loop_detection_uses_action_and_progress(self):
        self.assertEqual("repeated_action", module.detect_loop(["a", "a"], [0, 1]))
        self.assertEqual("no_progress", module.detect_loop(["a", "b", "c"], [1, 1, 1]))

    def test_partial_failure_preserves_success(self):
        outcome = module.run_parallel({
            "good": lambda: "artifact",
            "bad": lambda: (_ for _ in ()).throw(module.PermanentError("bad")),
        })
        self.assertEqual("partial", outcome["status"])
        self.assertEqual("artifact", outcome["results"]["good"])
        self.assertIn("bad", outcome["failures"])

    def test_uncertain_effect_requires_reconciliation(self):
        checkpoint = module.Checkpoint(uncertain_effects={"send"})
        with self.assertRaisesRegex(RuntimeError, "reconciliation"):
            module.resume(checkpoint, [("send", lambda: "sent")])

    def test_handoff_loop_is_stopped(self):
        path = ["triage", "refund"]
        ok, reason = module.handoff_path(path, "triage")
        self.assertFalse(ok)
        self.assertEqual("handoff loop", reason)


if __name__ == "__main__":
    unittest.main()
