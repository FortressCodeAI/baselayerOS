"""
Kali v1.0.0 — Core Constants

Central place for:
- Kali Standard levels
- default council names
- risk tier labels
- capability scope names
"""

KALI_VERSION = "1.0.0"

# Kali Standard Levels
KALI_STANDARD_LV1 = "kali_standard_lv1"
KALI_STANDARD_LV2 = "kali_standard_lv2"
KALI_STANDARD_LV3 = "kali_standard_lv3"

# Default councils
COUNCIL_DETERMINISM = "determinism"
COUNCIL_CAPABILITY = "capability"
COUNCIL_SAFETY = "safety"
COUNCIL_COMPLIANCE = "compliance"
COUNCIL_REDTEAM = "redteam"

DEFAULT_COUNCILS = [
    COUNCIL_DETERMINISM,
    COUNCIL_CAPABILITY,
    COUNCIL_SAFETY,
    COUNCIL_COMPLIANCE,
]

# Risk tiers
RISK_TIER_LOW = "low"
RISK_TIER_MEDIUM = "medium"
RISK_TIER_HIGH = "high"
RISK_TIER_CRITICAL = "critical"

# Capability scopes
CAP_SCOPE_READ_ONLY = "read_only"
CAP_SCOPE_WORKFLOW = "workflow"
CAP_SCOPE_WRITE_LIMITED = "write_limited"
