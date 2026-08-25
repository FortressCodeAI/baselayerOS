use serde::{Deserialize, Serialize};


#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum KernelInvariant {
    Replayability,
    DeterministicTransition,
    AuditAnchorDeterminism,
    EnvelopeIdentityConsistency,
    NoHiddenSideEffects,
    MonotonicVersioning,
    WorkflowDeterminism,
    StepOrderConsistency,
    ArtifactDeterminism,
    ContentFormatConsistency,
    CampaignDeterminism,
}

impl KernelInvariant {
    pub fn as_str(&self) -> &'static str {
        match self {
            KernelInvariant::Replayability => "Replayability",
            KernelInvariant::DeterministicTransition => "DeterministicTransition",
            KernelInvariant::AuditAnchorDeterminism => "AuditAnchorDeterminism",
            KernelInvariant::EnvelopeIdentityConsistency => "EnvelopeIdentityConsistency",
            KernelInvariant::NoHiddenSideEffects => "NoHiddenSideEffects",
            KernelInvariant::MonotonicVersioning => "MonotonicVersioning",
            KernelInvariant::WorkflowDeterminism => "WorkflowDeterminism",
            KernelInvariant::StepOrderConsistency => "StepOrderConsistency",
            KernelInvariant::ArtifactDeterminism => "ArtifactDeterminism",
            KernelInvariant::ContentFormatConsistency => "ContentFormatConsistency",
            KernelInvariant::CampaignDeterminism => "CampaignDeterminism",
        }
    }
}
