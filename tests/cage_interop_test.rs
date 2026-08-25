use baselayeros::substrate::Substrate;
use baselayeros::substrate::execution::{
    ExecutionAdapter,
    module_executor::ModuleExecutor,
    governance_engine::GovernanceEngine,
    invariant_engine::InvariantEngine,
    refusal_engine::ExecutionResult,
};
use envelopes::{ExecutionEnvelope, GovernanceEnvelope, GovernanceDecision, StateSnapshot};
use baselayeros::substrate::execution::routing_seal::{RoutingSealConfig, compute_record_hash_hex, compute_routing_seal};

#[test]
fn cage_interop_demo() {
    let mut substrate = Substrate::new();

    let snapshot = StateSnapshot {
        state_version: substrate.state().state_version,
        last_transition_hash: substrate.state().last_transition_hash.clone(),
        audit_anchor: substrate.state().audit_anchor.clone(),
        envelope_id: "env1".into(),
        actor_id: "actor1".into(),
        extractive_action: false,
        consent_granted: false,
    };

    let record_bytes = serde_json::to_vec(&snapshot).unwrap();
    let record_hash_hex = compute_record_hash_hex(&record_bytes);
    let timestamp_ms_hex = format!("{:x}", 1724170000000u64);
    let action_slug = "test_action";

    let routing_cfg = RoutingSealConfig {
        hmac_key: b"test-hmac-key".to_vec(),
    };

    let routing_seal = compute_routing_seal(
        &routing_cfg,
        &timestamp_ms_hex,
        action_slug,
        &record_hash_hex,
    );

    let exec_env = ExecutionEnvelope {
        envelope_id: snapshot.envelope_id.clone(),
        actor_id: snapshot.actor_id.clone(),
        action_slug: action_slug.into(),
        timestamp_ms_hex: timestamp_ms_hex.clone(),
        state_snapshot: snapshot,
        invariant_assertions: vec!["NonExtraction".into(), "Replayability".into()],
        trace_anchors: vec![],
        record_hash_hex: record_hash_hex.clone(),
        routing_seal: routing_seal.clone(),
    };

    let gov_env = GovernanceEnvelope {
        policy_id: "system_authz.rego".into(),
        policy_version: "v1".into(),
        decision: GovernanceDecision::Allow, // flip to Refuse to test refusal
        reason: Some("Test allow decision".into()),
        actor_id: exec_env.actor_id.clone(),
        envelope_id: exec_env.envelope_id.clone(),
        invariants: vec!["NonExtraction".into(), "Replayability".into()],
        timestamp_ms_hex,
        action_slug: exec_env.action_slug.clone(),
        record_hash_hex,
        routing_seal,
    };

    let module_executor = ModuleExecutor::new(substrate.state().clone());
    let governance_engine = GovernanceEngine::new(routing_cfg);
    let invariant_engine = InvariantEngine::new();

    let adapter = ExecutionAdapter::new(
        module_executor,
        governance_engine,
        invariant_engine,
    );

    let result = adapter.execute(exec_env, gov_env);

    match result {
        ExecutionResult::Committed { state_commit_id, trace_anchor } => {
            println!("Committed:");
            println!("  state_commit_id = {}", state_commit_id);
            println!("  trace_anchor     = {}", trace_anchor);
        }
        ExecutionResult::Refused(reason) => {
            println!("Refused:");
            println!("  code   = {:?}", reason.code);
            println!("  msg    = {}", reason.message);
            println!("  invs   = {:?}", reason.violated_invariants);
        }
    }
}
