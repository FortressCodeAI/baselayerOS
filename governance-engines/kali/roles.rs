// governance-engines/kali/roles.rs

use serde::{Deserialize, Serialize};

/// Canonical governance roles for Kali.
/// These are substrate-wide and should remain stable over time.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub enum KaliRole {
    Operator,
    Reviewer,
    Approver,
    Auditor,
    Admin,
}

impl KaliRole {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "operator" => Some(KaliRole::Operator),
            "reviewer" => Some(KaliRole::Reviewer),
            "approver" => Some(KaliRole::Approver),
            "auditor" => Some(KaliRole::Auditor),
            "admin" => Some(KaliRole::Admin),
            _ => None,
        }
    }

    pub fn as_str(&self) -> &'static str {
        match self {
            KaliRole::Operator => "operator",
            KaliRole::Reviewer => "reviewer",
            KaliRole::Approver => "approver",
            KaliRole::Auditor => "auditor",
            KaliRole::Admin => "admin",
        }
    }
}
