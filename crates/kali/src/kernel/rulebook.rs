use anyhow::Result;

use crate::kernel::invariants::KernelInvariant;
use crate::kernel::constraints::KernelConstraint;
use crate::registry::ProductSpec;

/// KernelRulebook is the authoritative governance engine for Kali.
/// It evaluates invariants and constraints for products, workflows,
/// envelopes, and runtime execution.
pub struct KernelRulebook;

impl KernelRulebook {
    pub fn new() -> Self {
        Self
    }

    /// Return all invariants that apply to a given product.
    /// This merges product-level invariants with kernel-level invariants.
    pub fn invariants_for_product(&self, product_id: &str) -> Vec<String> {
        match product_id {
            "governance-pack" => vec![
                KernelInvariant::Replayability.as_str().into(),
                KernelInvariant::DeterministicTransition.as_str().into(),
                KernelInvariant::AuditAnchorDeterminism.as_str().into(),
                KernelInvariant::EnvelopeIdentityConsistency.as_str().into(),
                KernelInvariant::NoHiddenSideEffects.as_str().into(),
                KernelInvariant::MonotonicVersioning.as_str().into(),
            ],

            "execution-pack" => vec![
                KernelInvariant::DeterministicTransition.as_str().into(),
                KernelInvariant::Replayability.as_str().into(),
                KernelInvariant::AuditAnchorDeterminism.as_str().into(),
            ],

            "workflow-pack" => vec![
                KernelInvariant::WorkflowDeterminism.as_str().into(),
                KernelInvariant::StepOrderConsistency.as_str().into(),
            ],

            "artifact-pack" => vec![
                KernelInvariant::ArtifactDeterminism.as_str().into(),
            ],

            "marketing-pack" => vec![
                KernelInvariant::CampaignDeterminism.as_str().into(),
                KernelInvariant::ContentFormatConsistency.as_str().into(),
            ],

            "sales-pack" => vec![
                KernelInvariant::WorkflowDeterminism.as_str().into(),
            ],

            "tenant-runtime-pack" => vec![
                KernelInvariant::EnvelopeIdentityConsistency.as_str().into(),
            ],

            _ => vec![],
        }
    }

    /// Validate constraints for a product + tenant.
    /// This is called by the compiler, runtime, and delivery engine.
    pub fn validate_product_constraints(
        &self,
        product: &ProductSpec,
        tenant_id: &str,
    ) -> Result<()> {
        let mut violations = vec![];

        // Role-based access
        if product.constraints.contains(&KernelConstraint::RoleBasedAccess.as_str().into()) {
            if tenant_id.is_empty() {
                violations.push("RoleBasedAccess");
            }
        }

        // Tenant boundary
        if product.constraints.contains(&KernelConstraint::TenantBoundary.as_str().into()) {
            if tenant_id == "root" {
                violations.push("TenantBoundary");
            }
        }

        // Action authorization
        if product.constraints.contains(&KernelConstraint::ActionAuthorization.as_str().into()) {
            // Placeholder: real logic later
        }

        // Module version lock
        if product.constraints.contains(&KernelConstraint::ModuleVersionLock.as_str().into()) {
            // Placeholder: real logic later
        }

        // State shape consistency
        if product.constraints.contains(&KernelConstraint::StateShapeConsistency.as_str().into()) {
            // Placeholder: real logic later
        }

        // Workflow authorization
        if product.constraints.contains(&KernelConstraint::WorkflowAuthorization.as_str().into()) {
            // Placeholder: real logic later
        }

        // Identity authorization
        if product.constraints.contains(&KernelConstraint::IdentityAuthorization.as_str().into()) {
            // Placeholder: real logic later
        }

        // Artifact format consistency
        if product.constraints.contains(&KernelConstraint::ArtifactFormatConsistency.as_str().into()) {
            // Placeholder: real logic later
        }

        if product.constraints.contains(&KernelConstraint::MarketingAuthorization.as_str().into()) {
            // Placeholder: real logic later
        }

        if product.constraints.contains(&KernelConstraint::SalesAuthorization.as_str().into()) {
            // Placeholder: real logic later
        }

        if violations.is_empty() {
            Ok(())
        } else {
            Err(anyhow::anyhow!("Constraint violations: {:?}", violations))
        }
    }
}
