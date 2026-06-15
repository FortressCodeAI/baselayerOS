# baselayeros/kali/config.py

"""
Central configuration for Kali Enforcement Boundary.

This file defines:
- GIU burn costs for each event type
- audit chain behavior
- deterministic execution flags
- operator contract defaults
"""

# -----------------------------
# GIU COSTS
# -----------------------------

# Cost for a deterministic refusal
REFUSAL_GIU_COST = 5

# Cost for a deterministic commit
COMMIT_GIU_COST = 10

# Cost for a human‑in‑the‑loop authority gate event
AUTHORITY_GATE_GIU_COST = 3


# -----------------------------
# AUDIT CHAIN SETTINGS
# -----------------------------

# Whether to hash‑link audit events
AUDIT_CHAIN_ENABLED = True

# Whether to export audit chain automatically after each run
AUTO_EXPORT_AUDIT_CHAIN = False

# Path for audit chain export (if enabled)
AUDIT_CHAIN_EXPORT_PATH = "data/audit_chain.json"


# -----------------------------
# DETERMINISM FLAGS
# -----------------------------

# Enforce deterministic ordering of payload keys
DETERMINISTIC_SERIALIZATION = True

# Enforce deterministic node execution order (ActionGraph already does this)
DETERMINISTIC_NODE_ORDER = True


# -----------------------------
# OPERATOR CONTRACT DEFAULTS
# -----------------------------

# Default path for operator contract JSON
DEFAULT_OPERATOR_CONTRACT_PATH = "config/operator_contract.json"
