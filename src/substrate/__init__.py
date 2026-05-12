# src/substrate/__init__.py

from .actions import registry as actions_registry  # noqa: F401
from .runtime.executor import Executor  # noqa: F401
from .runtime.dispatcher import Dispatcher  # noqa: F401
from .runtime.replay import replay_engine  # noqa: F401
from .credits.burn import burner, ledger  # noqa: F401
from .invariants.verifier import verifier  # noqa: F401
from .actions.base_action import BaseAction, ActionMetadata  # noqa: F401
from .actions.registry import registry  # noqa: F401
from .actions.builtin.echo import EchoAction  # noqa: F401


registry.register(EchoAction)
registry.freeze()
