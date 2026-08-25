use anyhow::Result;
use serde_json::json;
use std::fs;

fn main() -> Result<()> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 3 {
        println!("Usage: module-scaffolder <module-name> <output.json>");
        return Ok(());
    }

    let module_name = &args[1];

    let module = json!({
        "module_name": module_name,
        "description": format!("Deterministic module '{}'.", module_name),
        "invariants": [],
        "governance": {
            "scopes": [],
            "permissions": []
        },
        "interfaces": {},
        "replay": {
            "paths": []
        }
    });

    fs::write(&args[2], serde_json::to_string_pretty(&module)?)?;
    println!("Module scaffold created.");

    Ok(())
}
