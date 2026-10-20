use wasm_bindgen::prelude::*;
use crate::envelopes::execution_envelope::ExecutionEnvelope;
use crate::execution::execution_adapter::execute_envelope;
use crate::execution::workflow::run_replay_workflow;
use crate::audit::replay::load_events_for_envelope;
use crate::state_machine::snapshot::StateSnapshot;
use crate::audit::chain_seal::generate_chain_seal;
use crate::evidence::package::generate_evidence_package;
use crate::state_machine::substrate_state::SubstrateState;

#[wasm_bindgen]
pub fn exec(json: &str) -> String {
    let envelope: ExecutionEnvelope = serde_json::from_str(json).unwrap();
    let mut state = SubstrateState::new();
    let result = execute_envelope(&mut state, envelope).unwrap();
    serde_json::to_string(&result).unwrap()
}

#[wasm_bindgen]
pub fn replay(json: &str) -> String {
    let envelope: ExecutionEnvelope = serde_json::from_str(json).unwrap();
    let result = run_replay_workflow("audit-chain/events.jsonl", envelope).unwrap();
    serde_json::to_string(&result).unwrap()
}

#[wasm_bindgen]
pub fn evidence(json: &str) -> String {
    let envelope: ExecutionEnvelope = serde_json::from_str(json).unwrap();
    let workflow = run_replay_workflow("audit-chain/events.jsonl", envelope.clone()).unwrap();

    let events = load_events_for_envelope("audit-chain/events.jsonl", &envelope.id).unwrap();
    let first = events.first().unwrap();
    let last = events.last().unwrap();

    let snapshot_before = StateSnapshot { hash: first.snapshot_before_hash.clone() };
    let snapshot_after = StateSnapshot { hash: last.snapshot_after_hash.clone() };

    let chain_seal = generate_chain_seal("audit-chain/events.jsonl").unwrap();

    let path = generate_evidence_package(
        "evidence",
        &format!("evidence_{}", envelope.id),
        &envelope,
        &snapshot_before,
        &snapshot_after,
        &events,
        &workflow,
        &chain_seal,
    ).unwrap();

    path
}
