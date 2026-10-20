use crate::envelopes::execution_envelope::ExecutionEnvelope;
use crate::state_machine::substrate_state::SubstrateState;
use crate::state_machine::snapshot::StateSnapshot;
use crate::execution::execution_adapter::execute_envelope;
use crate::execution::replay_engine::{ReplayEngine, ReplayResult};
use crate::execution::invariant_engine::DefaultInvariantEngine;
use crate::config::packs::DummyPack;
use crate::audit::writer::write_audit_event;
use crate::audit::replay::load_events_for_envelope;
use crate::audit::event::AuditEvent;
use crate::errors::substrate_error::SubstrateError;

use serde::Serialize;

#[derive(Debug, Clone, Serialize)]
pub struct WorkflowResult {
    pub envelope_id: String,
    pub execution_ok: bool,
    pub replay: crate::execution::replay_engine::ReplayResult,
}

pub fn run_replay_workflow(
    audit_path: &str,
    envelope: ExecutionEnvelope,
) -> Result<WorkflowResult, SubstrateError> {
    let mut state = SubstrateState::new();
    let exec_result = execute_envelope(&mut state, envelope.clone())?;

    let event = AuditEvent {
        envelope_id: envelope.id.clone(),
        snapshot_before_hash: "before".into(),
        snapshot_after_hash: "after".into(),
        decision: "Allow".into(),
    };

    write_audit_event(audit_path, &event)?;

    let invariants = Box::new(DefaultInvariantEngine::new());
    let pack = Box::new(DummyPack);
    let engine = ReplayEngine::new(invariants, pack);

    let replay_result = engine.replay(audit_path, &envelope)?;

    Ok(WorkflowResult {
        envelope_id: envelope.id.clone(),
        execution_ok: exec_result.allowed,
        replay: replay_result,
    })
}
