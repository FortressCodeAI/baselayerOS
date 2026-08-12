use baselayeros::runtime::ExecutionAdapter;
use baselayeros::schemas::ExecutionEnvelope;
use baselayeros::invariants::InvariantEngine;

#[test]
fn adapter_executes_deterministically() {
    let adapter = ExecutionAdapter::new();
    let envelope: ExecutionEnvelope = serde_json::from_str(r#"{
        "envelope_id": "exec-hello-world-001",
        "state_snapshot": { "module": "hello-world", "version": "0.1.0" },
        "transition": {
            "name": "emit_greeting",
            "inputs": { "name": "James" },
            "outputs": { "message": "Hello, James" }
        },
        "invariants": [
            "outputs.message MUST be non-empty",
            "module MUST be 'hello-world'"
        ],
        "governance_bounds": {
            "policy": "baseline",
            "rulebook_version": "1.0.0"
        }
    }"#).unwrap();

    let result = adapter.execute(&envelope).unwrap();
    assert_eq!(result.outputs["message"], "Hello, James");

    let invariants = InvariantEngine::validate(&envelope, &result);
    assert!(invariants.is_ok());
}

#[test]
fn adapter_rejects_non_deterministic_output() {
    let adapter = ExecutionAdapter::new();
    let mut envelope: ExecutionEnvelope = serde_json::from_str(r#"{
        "envelope_id": "exec-hello-world-002",
        "state_snapshot": { "module": "hello-world", "version": "0.1.0" },
        "transition": {
            "name": "emit_greeting",
            "inputs": { "name": "James" },
            "outputs": { "message": "Hello, James" }
        },
        "invariants": [
            "outputs.message MUST equal 'Hello, James'"
        ],
        "governance_bounds": {
            "policy": "baseline",
            "rulebook_version": "1.0.0"
        }
    }"#).unwrap();

    // Introduce nondeterminism
    envelope.transition.outputs["message"] = "Hello, Kris".into();

    let result = adapter.execute(&envelope);
    assert!(result.is_err());
}
