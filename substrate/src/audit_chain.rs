use crate::canonical::CanonicalEnvelope;
use crate::trace::ExecutionTrace;
use serde::{Deserialize, Serialize};
use std::time::SystemTime;
use thiserror::Error;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditEntry {
    pub sequence: u64,
    pub envelope: CanonicalEnvelope,
    pub trace: Option<ExecutionTrace>,
    pub appended_at: String,
}

#[derive(Debug, Error)]
pub enum AuditChainError {
    #[error("Failed to append to audit chain: {0}")]
    AppendError(String),

    #[error("Failed to load audit chain: {0}")]
    LoadError(String),

    #[error("Failed to seal audit chain: {0}")]
    SealError(String),
}

pub trait AuditChainBackend: Send + Sync {
    fn append_entry(&mut self, entry: AuditEntry) -> Result<(), AuditChainError>;
    fn current_sequence(&self) -> Result<u64, AuditChainError>;
    fn seal_chain(&mut self) -> Result<(), AuditChainError>;
}

pub fn build_audit_entry(
    sequence: u64,
    envelope: CanonicalEnvelope,
    trace: Option<ExecutionTrace>,
) -> AuditEntry {
    let appended_at = iso8601_now();

    AuditEntry {
        sequence,
        envelope,
        trace,
        appended_at,
    }
}

fn iso8601_now() -> String {
    let now = SystemTime::now();
    let datetime: chrono::DateTime<chrono::Utc> = now.into();
    datetime.to_rfc3339()
}
