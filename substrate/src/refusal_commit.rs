use crate::canonical::CanonicalEnvelope;
use serde::{Deserialize, Serialize};
use thiserror::Error;


#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum RefusalReason {
    InvalidEnvelope(String),
    GovernanceRefusal(String),
    InvariantViolation(String),
    IllegalState(String),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum CommitOutcome {
    Committed {
        envelope_digest: String,
        state_version: u64,
    },

    Refused {
        envelope_digest: String,
        reason: RefusalReason,
    },
}

#[derive(Debug, Error)]
pub enum RefusalCommitError {
    #[error("Failed to evaluate refusal/commit outcome: {0}")]
    EvaluationError(String),
}

pub fn apply_refusal_or_commit(
    envelope: &CanonicalEnvelope,
    governance_allows: bool,
    invariants_hold: bool,
    current_state_version: u64,
) -> Result<CommitOutcome, RefusalCommitError> {
    let digest = envelope.digest.clone();

    if !governance_allows {
        return Ok(CommitOutcome::Refused {
            envelope_digest: digest,
            reason: RefusalReason::GovernanceRefusal(
                "Governance engine refused this envelope".to_string(),
            ),
        });
    }

    if !invariants_hold {
        return Ok(CommitOutcome::Refused {
            envelope_digest: digest,
            reason: RefusalReason::InvariantViolation(
                "Applying this envelope would violate invariants".to_string(),
            ),
        });
    }

    Ok(CommitOutcome::Committed {
        envelope_digest: digest,
        state_version: current_state_version + 1,
    })
}
