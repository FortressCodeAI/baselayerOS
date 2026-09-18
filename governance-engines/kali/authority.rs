use super::roles::KaliRole;
use serde::{Deserialize, Serialize};


#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub enum KaliCapability {
    RunWorkflow,
    ViewEvidence,
    ApproveModel,
    ConfigureGovernance,
    ViewAuditChain,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KaliAuthority {
    pub role: KaliRole,
    pub capabilities: Vec<KaliCapability>,
}

impl KaliAuthority {
    pub fn for_role(role: KaliRole) -> Self {
        let capabilities = match role {
            KaliRole::Operator => vec![
                KaliCapability::RunWorkflow,
            ],
            KaliRole::Reviewer => vec![
                KaliCapability::RunWorkflow,
                KaliCapability::ViewEvidence,
            ],
            KaliRole::Approver => vec![
                KaliCapability::RunWorkflow,
                KaliCapability::ViewEvidence,
                KaliCapability::ApproveModel,
            ],
            KaliRole::Auditor => vec![
                KaliCapability::ViewEvidence,
                KaliCapability::ViewAuditChain,
            ],
            KaliRole::Admin => vec![
                KaliCapability::RunWorkflow,
                KaliCapability::ViewEvidence,
                KaliCapability::ApproveModel,
                KaliCapability::ConfigureGovernance,
                KaliCapability::ViewAuditChain,
            ],
        };

        Self { role, capabilities }
    }

    pub fn can(&self, capability: KaliCapability) -> bool {
        self.capabilities.contains(&capability)
    }
}
