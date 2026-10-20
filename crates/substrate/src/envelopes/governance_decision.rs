use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum GovernanceDecision {
    Allow,
    Deny,
}

impl ToString for GovernanceDecision {
    fn to_string(&self) -> String {
        match self {
            GovernanceDecision::Allow => "Allow".into(),
            GovernanceDecision::Deny => "Deny".into(),
        }
    }
}
