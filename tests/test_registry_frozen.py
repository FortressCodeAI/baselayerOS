# tests/test_registry_frozen.py

import pytest # type: ignore

from substrate.actions.registry import registry
from substrate.actions.base_action import BaseAction, ActionMetadata


class DummyAction(BaseAction):
    metadata = ActionMetadata(name="dummy", version="1.0", giu_cost=1)

    def validate(self, params): return params
    def run(self, params, state): return state


def test_registry_is_frozen():
    assert registry.frozen is True
    with pytest.raises(RuntimeError):
        registry.register(DummyAction)
