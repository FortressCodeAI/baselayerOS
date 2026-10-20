"""
Kali v1.0.0 — Configuration module.

Centralized configuration for:
- risk tiers
- Kali Standard levels
- capability scopes
- HITL thresholds
- neural sandbox settings
- substrate integration
"""

from __future__ import annotations

import os
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


DEFAULT_CONFIG_PATH = os.environ.get("KALI_CONFIG_PATH", "config/kali.config.json")


@dataclass
class RiskTierConfig:
    name: str
    level: int
    description: str
    requires_hitl: bool
    councils: List[str]


@dataclass
class CapabilityScopeConfig:
    name: str
    description: str
    allowed_actions: List[str]


@dataclass
class NeuralConfig:
    model_name: str
    max_tokens: int
    temperature: float
    enable_cache: bool
    sandbox_enabled: bool


@dataclass
class SubstrateConfig:
    enabled: bool
    endpoint: Optional[str] = None
    api_key: Optional[str] = None


@dataclass
class KaliConfig:
    """
    Top-level configuration object for Kali.
    """

    environment: str = "local"
    risk_tiers: Dict[str, RiskTierConfig] = field(default_factory=dict)
    capability_scopes: Dict[str, CapabilityScopeConfig] = field(default_factory=dict)
    neural: NeuralConfig = field(
        default_factory=lambda: NeuralConfig(
            model_name="deepseek-coder-6b",
            max_tokens=1024,
            temperature=0.2,
            enable_cache=True,
            sandbox_enabled=True,
        )
    )
    substrate: SubstrateConfig = field(
        default_factory=lambda: SubstrateConfig(enabled=False)
    )
    hitl_threshold_level: int = 4  # Level 4+ requires HITL by default

    @classmethod
    def load(cls, path: str = DEFAULT_CONFIG_PATH) -> "KaliConfig":
        """
        Load configuration from JSON file, or fall back to sane defaults.
        """
        if not os.path.exists(path):
            return cls._default()

        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        return cls._from_dict(raw)

    @classmethod
    def _default(cls) -> "KaliConfig":
        """
        Default configuration suitable for local testing.
        """
        # Minimal risk tiers for v1.0.0
        low = RiskTierConfig(
            name="low",
            level=1,
            description="Read-only, non-sensitive, reversible actions.",
            requires_hitl=False,
            councils=["determinism", "capability"],
        )
        medium = RiskTierConfig(
            name="medium",
            level=2,
            description="Workflow-level decisions with limited write scope.",
            requires_hitl=False,
            councils=["determinism", "capability", "safety"],
        )
        high = RiskTierConfig(
            name="high",
            level=3,
            description="Write operations, external API calls, moderate impact.",
            requires_hitl=True,
            councils=["determinism", "capability", "safety", "compliance"],
        )
        critical = RiskTierConfig(
            name="critical",
            level=4,
            description="Financial, medical, or irreversible actions.",
            requires_hitl=True,
            councils=[
                "determinism",
                "capability",
                "safety",
                "compliance",
                "redteam",
            ],
        )

        # Minimal capability scopes
        read_only = CapabilityScopeConfig(
            name="read_only",
            description="Read-only access to governed resources.",
            allowed_actions=["read"],
        )
        workflow = CapabilityScopeConfig(
            name="workflow",
            description="Start, inspect, and replay workflows.",
            allowed_actions=["read", "start_workflow", "inspect_workflow", "replay"],
        )
        write_limited = CapabilityScopeConfig(
            name="write_limited",
            description="Limited write access under governance.",
            allowed_actions=["read", "write_limited"],
        )

        return cls(
            environment="local",
            risk_tiers={
                "low": low,
                "medium": medium,
                "high": high,
                "critical": critical,
            },
            capability_scopes={
                "read_only": read_only,
                "workflow": workflow,
                "write_limited": write_limited,
            },
        )

    @classmethod
    def _from_dict(cls, raw: Dict[str, Any]) -> "KaliConfig":
        """
        Construct KaliConfig from a raw dict (JSON).
        """
        risk_tiers = {}
        for name, cfg in raw.get("risk_tiers", {}).items():
            risk_tiers[name] = RiskTierConfig(
                name=cfg["name"],
                level=cfg["level"],
                description=cfg["description"],
                requires_hitl=cfg["requires_hitl"],
                councils=cfg["councils"],
            )

        capability_scopes = {}
        for name, cfg in raw.get("capability_scopes", {}).items():
            capability_scopes[name] = CapabilityScopeConfig(
                name=cfg["name"],
                description=cfg["description"],
                allowed_actions=cfg["allowed_actions"],
            )

        neural_raw = raw.get("neural", {})
        neural = NeuralConfig(
            model_name=neural_raw.get("model_name", "deepseek-coder-6b"),
            max_tokens=neural_raw.get("max_tokens", 1024),
            temperature=neural_raw.get("temperature", 0.2),
            enable_cache=neural_raw.get("enable_cache", True),
            sandbox_enabled=neural_raw.get("sandbox_enabled", True),
        )

        substrate_raw = raw.get("substrate", {})
        substrate = SubstrateConfig(
            enabled=substrate_raw.get("enabled", False),
            endpoint=substrate_raw.get("endpoint"),
            api_key=substrate_raw.get("api_key"),
        )

        return cls(
            environment=raw.get("environment", "local"),
            risk_tiers=risk_tiers,
            capability_scopes=capability_scopes,
            neural=neural,
            substrate=substrate,
            hitl_threshold_level=raw.get("hitl_threshold_level", 4),
        )
