use crate::audit_chain::{AuditChainBackend, AuditChainError, build_audit_entry};
use crate::canonical::{CanonicalEnvelope, canonicalize_envelope, CanonicalizationError};
use crate::envelope::{Envelope, validate_envelope, EnvelopeValidationError};
use crate::invariants::check_invariants;
use crate::refusal_commit::{apply_refusal_or_commit, CommitOutcome, RefusalCommitError};
use crate::state::{SubstrateState, apply_state_transition, StateTransitionError};
use crate::trace::{ExecutionTrace, record_trace};
use thiserror::Error;


#[derive(Debug)]
pub struct ExecutionResult {
    pub outcome: CommitOutcome,
    pub trace: ExecutionTrace,
}

#[derive(Debug, Error)]
pub enum ExecutionError {
    #[error("Envelope validation failed: {0}")]
    ValidationError(#[from] EnvelopeValidationError),

    #[error("Canonicalization failed: {0}")]
    CanonicalizationError(#[from] CanonicalizationError),

    #[error("Refusal/commit evaluation failed: {0}")]
    RefusalCommitError(#[from] RefusalCommitError),

    #[error("State transition failed: {0}")]
    StateTransitionError(#[from] StateTransitionError),

    #[error("Audit chain error: {0}")]
    AuditChainError(#[from] AuditChainError),
}

pub fn execute_envelope(
    envelope: &Envelope,
    state: &mut SubstrateState,
    audit_chain: &mut dyn AuditChainBackend,
    required_tags: &[&str],
    governance_allows: bool,
) -> Result<ExecutionResult, ExecutionError> {
    validate_envelope(envelope, required_tags)?;

    let canonical = canonicalize_envelope(envelope)?;

    let invariants_hold = check_invariants(state, &canonical);

    let outcome = apply_refusal_or_commit(
        &canonical,
        governance_allows,
        invariants_hold,
        state.version,
    )?;

    let mut trace = ExecutionTrace::new(envelope.id.0.clone());
    match &outcome {
        CommitOutcome::Committed { .. } => {
            apply_state_transition(state, &canonical)?;
            record_trace(&mut trace, "Committed envelope and updated state");
        }
        CommitOutcome::Refused { reason, .. } => {
            record_trace(&mut trace, format!("Refused envelope: {:?}", reason).as_str());
        }
    }

    let sequence = audit_chain.current_sequence()? + 1;
    let entry = build_audit_entry(sequence, canonical, Some(trace.clone()));
    audit_chain.append_entry(entry)?;

    Ok(ExecutionResult { outcome, trace })
}
