use baselayeros::schemas::{
    ExecutionEnvelopeSchema,
    GovernanceEnvelopeSchema,
    ModuleSpecSchema,
    PolicySpecSchema,
    RulebookSchema,
    SeaArtifactSchema
};

use jsonschema::JSONSchema;
use serde_json::json;

fn validate(schema: &serde_json::Value, instance: &serde_json::Value) {
    let compiled = JSONSchema::compile(schema).unwrap();
    let result = compiled.validate(instance);
    assert!(result.is_ok(), "Schema validation failed");
}

#[test]
fn execution_envelope_schema_validates_example() {
    let schema = ExecutionEnvelopeSchema::as_json();
    let example = json!({
        "envelope_id": "exec-hello-world-001",
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
    });

    validate(&schema, &example);
}

#[test]
fn rulebook_schema_validates_minimal_rulebook() {
    let schema = RulebookSchema::as_json();
    let example = json!({
        "rulebook_id": "baseline-1.0.0",
        "rules": [
            { "id": "R001", "description": "Outputs MUST be deterministic" },
            { "id": "R002", "description": "Modules MUST declare all transitions" }
        ]
    });

    validate(&schema, &example);
}
