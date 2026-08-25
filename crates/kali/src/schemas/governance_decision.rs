use serde::{Deserialize, Serialize};


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovernanceDecision {
    pub decision: String,
    pub reason: String,
    pub violated_invariants: Vec<String>,
    pub violated_constraints: Vec<String>,
}

impl GovernanceDecision {
    pub fn allow() -> Self {
        Self {
            decision: "Allow".into(),
            reason: "All invariants and constraints satisfied".into(),
            violated_invariants: vec![],
            violated_constraints: vec![],
        }
    }

    pub fn refuse(reason: impl Into<String>, inv: Vec<String>, cons: Vec<String>) -> Self {
        Self {
            decision: "Refuse".into(),
            reason: reason.into(),
            violated_invariants: inv,
            violated_constraints: cons,
        }
    }
}
