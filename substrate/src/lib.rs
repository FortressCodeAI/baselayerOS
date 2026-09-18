// src/lib.rs

pub mod envelope;
pub mod canonical;
pub mod execution;
pub mod refusal_commit;
pub mod replay;
pub mod attestation;
pub mod state;
pub mod trace;
pub mod invariants;

pub use envelope::{
    Envelope,
    EnvelopeId,
    EnvelopeKind,
    EnvelopeValidationError,
    validate_envelope,
};

pub use canonical::{
    CanonicalEnvelope,
    canonicalize_envelope,
};

pub use execution::{
    ExecutionResult,
    execute_envelope,
};

pub use refusal_commit::{
    RefusalReason,
    CommitOutcome,
    apply_refusal_or_commit,
};

pub use replay::{
    ReplayResult,
    replay_envelope,
};

pub use attestation::{
    Attestation,
    AttestationError,
    attest_envelope,
};

pub use state::{
    SubstrateState,
    StateTransitionError,
    apply_state_transition,
};

pub use trace::{
    ExecutionTrace,
    TraceEvent,
    record_trace,
};

pub use invariants::{
    InvariantViolation,
    check_invariants,
};
