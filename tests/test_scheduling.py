import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).parents[1] / "examples" / "scheduling" / "task_board.py"
SPEC = importlib.util.spec_from_file_location("task_board", PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


class SchedulingTests(unittest.TestCase):
    def test_backpressure_rejects_excess_work(self):
        board = module.TaskBoard(capacity=1)
        board.submit(module.Task("a", frozenset()))
        with self.assertRaisesRegex(ValueError, "backpressure"):
            board.submit(module.Task("b", frozenset()))

    def test_capability_matching_rejects_invalid_assignment(self):
        board = module.TaskBoard()
        task = module.Task("a", frozenset({"legal"}))
        with self.assertRaisesRegex(ValueError, "no capable"):
            board.allocate(task, [module.Agent("x", frozenset({"write"}), frozenset())])

    def test_concurrency_limit_and_priority(self):
        board = module.TaskBoard(concurrency=1)
        board.submit(module.Task("low", frozenset({"work"}), priority=1))
        board.submit(module.Task("high", frozenset({"work"}), priority=5))
        agent = module.Agent("worker", frozenset({"work"}), frozenset())
        leased = board.lease([agent])
        self.assertEqual(["high"], [task.id for task in leased])
        self.assertEqual(1, board.tasks["low"].age)

    def test_dependency_and_cancellation_propagate(self):
        board = module.TaskBoard()
        board.submit(module.Task("a", frozenset()))
        board.submit(module.Task("b", frozenset(), frozenset({"a"})))
        board.submit(module.Task("c", frozenset(), frozenset({"b"})))
        board.cancel("a")
        self.assertTrue(all(board.tasks[x].status == "cancelled" for x in ("a", "b", "c")))

    def test_consensus_requires_independent_evidence(self):
        candidates = [("yes", "same", True), ("yes", "same", True), ("yes", "x", False)]
        self.assertEqual("needs_external_validation", module.resolve(candidates))


if __name__ == "__main__":
    unittest.main()
