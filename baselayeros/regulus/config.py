# baselayeros/regulus/config.py

from dataclasses import dataclass
from typing import Literal


RiskMode = Literal["strict", "permissive"]


@dataclass
class RegulusConfig:
    """
    Configuration for Regulus behavior.
    """

    risk_mode: RiskMode = "strict"
    max_autonomous_risk_tier: int = 3  # 0–3 allowed, 4+ escalate
