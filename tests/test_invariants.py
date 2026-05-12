# tests/test_invariants.py

from substrate.invariants.verifier import verifier


def test_invariant_non_negative_counters():
    prev = {"task_count": 1}
    next_state = {"task_count": 2}
    context = {}

    violations = verifier.verify(prev, next_state, context)
    assert len(violations) == 0


def test_invariant_negative_counter_fails():
    prev = {"task_count": 1}
    next_state = {"task_count": -1}
    context = {}

    violations = verifier.verify(prev, next_state, context)
    assert len(violations) == 1
    assert violations[0].name == "non_negative_counters"
