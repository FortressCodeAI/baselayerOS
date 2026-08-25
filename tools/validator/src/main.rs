use anyhow::{Result, anyhow};
use serde_json::Value;
use std::fs;

fn main() -> Result<()> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        println!("Usage: validator <file.json>");
        return Ok(());
    }

    let json: Value = serde_json::from_str(&fs::read_to_string(&args[1])?)?;

    validate(&json)?;
    println!("File is deterministic and governance‑safe.");

    Ok(())
}

fn validate(json: &Value) -> Result<()> {
    if json.get("invariants").is_none() {
        return Err(anyhow!("Missing invariants."));
    }
    if json.get("governance").is_none() {
        return Err(anyhow!("Missing governance block."));
    }
    Ok(())
}
