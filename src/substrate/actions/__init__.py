# src/substrate/actions/__init__.py

from .base_action import BaseAction, ActionMetadata  # noqa: F401
from .registry import registry  # noqa: F401

# Register builtin actions
from .builtin.echo import EchoAction  # noqa: F401

# Perform registration at import time
registry.register(EchoAction)
registry.freeze()
