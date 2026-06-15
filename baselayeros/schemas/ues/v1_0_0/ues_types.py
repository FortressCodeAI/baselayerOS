from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal


# -----------------------------
# Intent
# -----------------------------
@dataclass
class Intent:
    name: str
    description: str
    domain: str
    priority: Literal["low", "normal", "high"]


# -----------------------------
# Inputs
# -----------------------------
@dataclass
class Inputs:
    raw: str
    structured: Dict


# -----------------------------
# Capabilities
# -----------------------------
@dataclass
class Capability:
    id: str
    name: str
    version: str
    provider: Literal["agent", "module", "workflow"]
    preconditions: List[str]
    postconditions: List[str]
    scopes: List[Literal["read", "write", "execute"]]


# -----------------------------
# Plan → Tasks
# -----------------------------
@dataclass
class Task:
    id: str
    description: str
    capability: str
    inputs: Dict
    outputs: Dict
    dependencies: List[str]
    preconditions: List[str]
    postconditions: List[str]


@dataclass
class Phase:
    id: str
    name: str
    tasks: List[Task]


@dataclass
class PlanGraphEdge:
    from_task: str
    to_task: str


@dataclass
class PlanGraph:
    nodes: List[str]
    edges: List[PlanGraphEdge]


@dataclass
class Plan:
    phases: List[Phase]
    graph: PlanGraph


# -----------------------------
# Constraints
# -----------------------------
@dataclass
class Constraints:
    hard: List[str]
    soft: List[str]
    max_cost_giu: float
    max_latency_ms: float
    safety_level: Literal["standard", "strict"]
    compliance_targets: List[str]


# -----------------------------
# Global Conditions
# -----------------------------
@dataclass
class Conditions:
    pre: List[str]
    post: List[str]


# -----------------------------
# Scores
# -----------------------------
@dataclass
class Scores:
    cost: float
    risk: float
    time: float


# -----------------------------
# State
# -----------------------------
@dataclass
class State:
    status: Literal[
        "DRAFTED",
        "OPTIMIZED",
        "RISK_REVIEWED",
        "APPROVED",
        "COMPILED",
        "EXECUTED",
        "REJECTED"
    ]
    last_transition_at: str
    last_transition_by: str


# -----------------------------
# Authority
# -----------------------------
@dataclass
class Authority:
    subject_id: str
    roles: List[str]
    scopes: List[str]
    top_authority_required: bool


# -----------------------------
# Approvals
# -----------------------------
@dataclass
class Approvals:
    requester_signature: Optional[str]
    top_authority_signature: Optional[str]


# -----------------------------
# Audit
# -----------------------------
@dataclass
class AuditActor:
    id: str
    org: str
    roles: List[str]


@dataclass
class Audit:
    event_chain_head: str
    events: List[str]
    request_id: str
    proposal_id: str
    timestamp: str
    actor: AuditActor
    policy_versions: List[str]
    capability_versions: List[str]


# -----------------------------
# Universal Execution Schema (UES)
# -----------------------------
@dataclass
class UES:
    ues_version: str
    intent: Intent
    inputs: Inputs
    capabilities: List[Capability]
    plan: Plan
    constraints: Constraints
    conditions: Conditions
    scores: Scores
    state: State
    authority: Authority
    approvals: Approvals
    audit: Audit
