# tests/test_actions.py

from substrate.actions.registry import registry
from substrate.actions.builtin.echo import EchoAction  # noqa: F401


def test_echo_action_registration():
    # Ensure echo is registered
    key = "echo:1.0"
    assert key in registry.list_actions()


def test_echo_action_execution():
    action_cls = registry.get("echo", "1.0")
    action = action_cls()

    params = {"x": 1, "y": "test"}
    validated = action.validate(params)
    result = action.run(validated, {})

    assert validated == params
    assert result == params
