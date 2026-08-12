use anyhow::{Result, anyhow};
use std::fs;

pub fn load_json(path: &str) -> Result<serde_json::Value> {
    let data = fs::read_to_string(path)
        .map_err(|e| anyhow!("Failed to read file {}: {}", path, e))?;
    let json: serde_json::Value = serde_json::from_str(&data)
        .map_err(|e| anyhow!("Invalid JSON in {}: {}", path, e))?;
    Ok(json)
}
