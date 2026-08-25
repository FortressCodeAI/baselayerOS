use serde::{Deserialize, Serialize};


#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum KernelConstraint {
    RoleBasedAccess,
    TenantBoundary,
    ActionAuthorization,
    ModuleVersionLock,
    StateShapeConsistency,
    WorkflowAuthorization,
    IdentityAuthorization,
    ArtifactFormatConsistency,
    MarketingAuthorization,
    SalesAuthorization,
}

impl KernelConstraint {
    pub fn as_str(&self) -> &'static str {
        match self {
            KernelConstraint::RoleBasedAccess => "RoleBasedAccess",
            KernelConstraint::TenantBoundary => "TenantBoundary",
            KernelConstraint::ActionAuthorization => "ActionAuthorization",
            KernelConstraint::ModuleVersionLock => "ModuleVersionLock",
            KernelConstraint::StateShapeConsistency => "StateShapeConsistency",
            KernelConstraint::WorkflowAuthorization => "WorkflowAuthorization",
            KernelConstraint::IdentityAuthorization => "IdentityAuthorization",
            KernelConstraint::ArtifactFormatConsistency => "ArtifactFormatConsistency",
            KernelConstraint::MarketingAuthorization => "MarketingAuthorization",
            KernelConstraint::SalesAuthorization => "SalesAuthorization",
        }
    }
}
