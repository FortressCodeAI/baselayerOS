# tests/test_replay.py

from substrate.runtime.replay import replay_engine


def test_replay_simple_sequence():
    initial_state = {"value": 0}

    events = [
        {
            "action": "echo:1.0",
            "params": {"value": 10}
        }
    ]

    context = {}

    result = replay_engine.replay(initial_state, events, context)

    assert result["final_state"]["value"] == 10
    assert len(result["trace"]) == 1
    assert result["state_hash"] is not None
