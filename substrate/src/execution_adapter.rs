use crate::canonical::{canonicalize_envelope, CanonicalEnvelope};
use crate::envelope::{Envelope, validate_envelope};
use crate::invariants::check_invariants;
use crate::state::{SubstrateState, apply_state_transition};
use crate::trace::{ExecutionTrace, record_trace};
use crate::audit_chain::{AuditChainBackend, build_audit_entry};
use crate::refusal_commit::{apply_refusal_or_commit, CommitOutcome};
use crate::attestation::attest_envelope;
use crate::governance_engines::kali::KaliGovernanceEngine;
use crate::governance_engines::cage::CageGovernanceEngine;
use crate::governance_engines::rego::RegoGovernanceAdapter;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ExecutionAdapterError {
    #[error("Envelope validation failed: {0}")]
    ValidationError(String),

    #[error("Canonicalization failed: {0}")]
    CanonicalizationError(String),

    #[error("Governance evaluation failed: {0}")]
    GovernanceError(String),

    #[error("Invariant check failed")]
    InvariantViolation,

    #[error("State transition failed: {0}")]
    StateError(String),

    #[error("Audit chain error: {0}")]
    AuditError(String),

    #[error("Attestation error: {0}")]
    AttestationError(String),
}

pub struct ExecutionAdapter {
    kali: KaliGovernanceEngine,
    cage: CageGovernanceEngine,
    rego: RegoGovernanceAdapter,
}

impl ExecutionAdapter {
    pub fn new() -> Self {
        Self {
            kali: KaliGovernanceEngine::new(),
            cage: CageGovernanceEngine::new(),
            rego: RegoGovernanceAdapter::new(),
        }
    }

    pub fn execute(
        &self,
        envelope: &Envelope,
        state: &mut SubstrateState,
        audit_chain: &mut dyn AuditChainBackend,
        required_tags: &[&str],
    ) -> Result<CommitOutcome, ExecutionAdapterError> {
        validate_envelope(envelope, required_tags)
            .map_err(|e| ExecutionAdapterError::ValidationError(e.to_string()))?;

        let canonical: CanonicalEnvelope = canonicalize_envelope(envelope)
            .map_err(|e| ExecutionAdapterError::CanonicalizationError(e.to_string()))?;

        let governance_allows = self.evaluate_governance(&canonical)
            .map_err(|e| ExecutionAdapterError::GovernanceError(e))?;

        let invariants_hold = check_invariants(state, &canonical);
        if !invariants_hold {
            return Err(ExecutionAdapterError::InvariantViolation);
        }

        let outcome = apply_refusal_or_commit(
            &canonical,
            governance_allows,
            invariants_hold,
            state.version,
        ).map_err(|e| ExecutionAdapterError::GovernanceError(e.to_string()))?;

        let mut trace = ExecutionTrace::new(envelope.id.0.clone());
        match &outcome {
            CommitOutcome::Committed { .. } => {
                apply_state_transition(state, &canonical)
                    .map_err(|e| ExecutionAdapterError::StateError(e.to_string()))?;
                record_trace(&mut trace, "Committed envelope and updated state");
            }
            CommitOutcome::Refused { reason, .. } => {
                record_trace(&mut trace, &format!("Refused envelope: {:?}", reason));
            }
        }

        let _attestation = attest_envelope(&canonical, state)
            .map_err(|e| ExecutionAdapterError::AttestationError(e.to_string()))?;

        let sequence = audit_chain.current_sequence()
            .map_err(|e| ExecutionAdapterError::AuditError(e.to_string()))? + 1;

        let entry = build_audit_entry(sequence, canonical, Some(trace));
        audit_chain.append_entry(entry)
            .map_err(|e| ExecutionAdapterError::AuditError(e.to_string()))?;

        Ok(outcome)
    }

    fn evaluate_governance(
        &self,
        canonical: &CanonicalEnvelope,
    ) -> Result<bool, String> {
        let kali_decision = self.kali.evaluate(canonical)
            .map_err(|e| e.to_string())?;

        let cage_decision = self.cage.evaluate(canonical)
            .map_err(|e| e.to_string())?;

        let rego_decision = self.rego.evaluate(canonical)
            .map_err(|e| e.to_string())?;

        if matches!(kali_decision, crate::governance_engines::kali::KaliGovernanceDecision::Deny) {
            return Ok(false);
        }
        if matches!(cage_decision, crate::governance_engines::cage::CageDecision::Deny) {
            return Ok(false);
        }
        if matches!(rego_decision, crate::governance_engines::rego::RegoDecision::Deny) {
            return Ok(false);
        }

        if matches!(kali_decision, crate::governance_engines::kali::KaliGovernanceDecision::Escalate) {
            return Ok(false);
        }
        if matches!(cage_decision, crate::governance_engines::cage::CageDecision::Escalate) {
            return Ok(false);
        }

        Ok(true)
    }
}
