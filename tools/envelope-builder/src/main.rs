use anyhow::Result;
use serde_json::{json, Value};
use std::fs;

fn main() -> Result<()> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 3 {
        println!("Usage: envelope-builder <module-spec.json> <output.json>");
        return Ok(());
    }

    let module_spec: Value = serde_json::from_str(&fs::read_to_string(&args[1])?)?;

    let envelope = json!({
        "envelope_id": uuid::Uuid::new_v4().to_string(),
        "state_snapshot": {
            "module": module_spec["module_name"],
            "version": "0.1.0"
        },
        "transition": module_spec["interfaces"],
        "invariants": module_spec["invariants"],
        "governance_boundary": module_spec["governance"],
        "replay_path": module_spec["replay"]["paths"],
        "trace_anchor": {
            "timestamp": chrono::Utc::now().to_rfc3339(),
            "module": module_spec["module_name"]
        }
    });

    fs::write(&args[2], serde_json::to_string_pretty(&envelope)?)?;
    println!("Deterministic envelope generated.");

    Ok(())
}
