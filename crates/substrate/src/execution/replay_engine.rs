use serde::Serialize;
use crate::audit::event::AuditEvent;
use crate::audit::replay::load_events_for_envelope;
use crate::envelopes::execution_envelope::ExecutionEnvelope;
use crate::state_machine::snapshot::StateSnapshot;
use crate::execution::invariant_engine::InvariantEngine;
use crate::config::packs::GovernancePack;
use crate::errors::substrate_error::SubstrateError;

#[derive(Debug, Clone, Serialize)]
pub struct ReplayResult {
    pub envelope_id: String,
    pub original_decision: String,
    pub replay_decision: String,
    pub decision_match: bool,
    pub snapshot_before_hash: String,
    pub snapshot_after_hash: String,
    pub snapshot_hash_match: bool,
    pub events_count: usize,
}

pub struct ReplayEngine {
    invariants: Box<dyn InvariantEngine>,
    pack: Box<dyn GovernancePack>,
}

impl ReplayEngine {
    pub fn new(
        invariants: Box<dyn InvariantEngine>,
        pack: Box<dyn GovernancePack>,
    ) -> Self {
        Self { invariants, pack }
    }

    pub fn replay(
        &self,
        audit_path: &str,
        envelope: &ExecutionEnvelope,
    ) -> Result<ReplayResult, SubstrateError> {

        let events: Vec<AuditEvent> = load_events_for_envelope(audit_path, &envelope.id)?;
        if events.is_empty() {
            return Err(SubstrateError::Audit(format!(
                "No audit events found for envelope {}", envelope.id
            )));
        }

        let first = events.first().unwrap();
        let last = events.last().unwrap();

        let snapshot_before = StateSnapshot { hash: first.snapshot_before_hash.clone() };
        let snapshot_after = StateSnapshot { hash: last.snapshot_after_hash.clone() };

        self.invariants.check_pre(&snapshot_before, envelope)?;
        let decision = self.pack.evaluate(&snapshot_before, envelope);
        self.invariants.check_post(&snapshot_after, envelope)?;

        Ok(ReplayResult {
            envelope_id: envelope.id.clone(),
            original_decision: last.decision.clone(),
            replay_decision: decision.to_string(),
            decision_match: last.decision == decision.to_string(),
            snapshot_before_hash: snapshot_before.hash.clone(),
            snapshot_after_hash: snapshot_after.hash.clone(),
            snapshot_hash_match: first.snapshot_before_hash == snapshot_before.hash
                && last.snapshot_after_hash == snapshot_after.hash,
            events_count: events.len(),
        })
    }
}
