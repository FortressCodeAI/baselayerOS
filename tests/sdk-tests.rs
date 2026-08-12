use baselayeros::sdk::{DeterministicExecutor, ReplayEngine};
use baselayeros::schemas::ExecutionEnvelope;

#[test]
fn sdk_executes_module_deterministically() {
    let executor = DeterministicExecutor::new();

    let envelope: ExecutionEnvelope = serde_json::from_str(r#"{
        "envelope_id": "exec-hello-world-003",
        "state_snapshot": { "module": "hello-world", "version": "0.1.0" },
        "transition": {
            "name": "emit_greeting",
            "inputs": { "name": "James" },
            "outputs": { "message": "Hello, James" }
        },
        "invariants": [
            "outputs.message MUST be non-empty"
        ],
        "governance_bounds": {
            "policy": "baseline",
            "rulebook_version": "1.0.0"
        }
    }"#).unwrap();

    let result = executor.execute(&envelope).unwrap();
    assert_eq!(result.outputs["message"], "Hello, James");
}

#[test]
fn sdk_replay_produces_identical_output() {
    let executor = DeterministicExecutor::new();
    let replay = ReplayEngine::new();

    let envelope: ExecutionEnvelope = serde_json::from_str(r#"{
        "envelope_id": "exec-hello-world-004",
        "state_snapshot": { "module": "hello-world", "version": "0.1.0" },
        "transition": {
            "name": "emit_greeting",
            "inputs": { "name": "James" },
            "outputs": { "message": "Hello, James" }
        },
        "invariants": [
            "outputs.message MUST be non-empty"
        ],
        "governance_bounds": {
            "policy": "baseline",
            "rulebook_version": "1.0.0"
        }
    }"#).unwrap();

    let first = executor.execute(&envelope).unwrap();
    let second = replay.replay(&envelope).unwrap();

    assert_eq!(first.outputs, second.outputs);
}
