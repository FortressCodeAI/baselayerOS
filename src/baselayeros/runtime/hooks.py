# src/substrate/runtime/hooks.py

from typing import Any, Dict, Protocol


class PreExecuteHook(Protocol):
    """
    Called before an action is executed.

    Must be:
    - deterministic
    - side-effect free (from substrate perspective)
    """

    def __call__(
        self,
        action_name: str,
        version: str,
        params: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Can:
        - validate/normalize context
        - enrich context deterministically

        Must:
        - not mutate params in-place
        - return a (possibly updated) context
        """
        ...


class PostExecuteHook(Protocol):
    """
    Called after an action is executed.

    Must be:
    - deterministic
    - side-effect free (from substrate perspective)
    """

    def __call__(
        self,
        action_name: str,
        version: str,
        result: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Can:
        - enrich context deterministically
        - compute derived metadata

        Must:
        - not mutate result in-place
        - return a (possibly updated) context
        """
        ...


class HookManager:
    """
    Deterministic hook manager.

    - maintains ordered lists of pre/post hooks
    - evaluation order is registration order
    """

    def __init__(self):
        self._pre_hooks: list[PreExecuteHook] = []
        self._post_hooks: list[PostExecuteHook] = []

    def register_pre(self, hook: PreExecuteHook):
        self._pre_hooks.append(hook)

    def register_post(self, hook: PostExecuteHook):
        self._post_hooks.append(hook)

    def run_pre(
        self,
        action_name: str,
        version: str,
        params: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        ctx = dict(context)
        for hook in self._pre_hooks:
            ctx = hook(action_name, version, params, ctx)
        return ctx

    def run_post(
        self,
        action_name: str,
        version: str,
        result: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        ctx = dict(context)
        for hook in self._post_hooks:
            ctx = hook(action_name, version, result, ctx)
        return ctx


# Global hook manager for the substrate
hooks = HookManager()
