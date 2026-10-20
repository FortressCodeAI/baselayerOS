use serde_json::Value;

pub fn run(envelope: String) {
    let parsed: Value = serde_json::from_str(&envelope)
        .expect("Invalid JSON envelope");

    println!(
        "{}",
        serde_json::json!({
            "status": "executed",
            "envelope": parsed
        })
    );
}
