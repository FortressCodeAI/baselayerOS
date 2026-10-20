use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditEvent {
    pub envelope_id: String,
    pub snapshot_before_hash: String,
    pub snapshot_after_hash: String,
    pub decision: String,
}
