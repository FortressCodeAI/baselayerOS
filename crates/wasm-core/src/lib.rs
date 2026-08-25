use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};
use serde_wasm_bindgen::{from_value, to_value};

#[derive(Serialize, Deserialize)]
pub struct Context {
    pub tenant_id: String,
    pub actor_id: String,
    pub trace_id: String,
}

#[derive(Serialize, Deserialize)]
pub struct Payload {
    pub data: serde_json::Value,
    pub params: serde_json::Value,
}

#[derive(Serialize, Deserialize)]
pub struct ExecutionInput {
    pub module_id: String,
    pub version: String,
    pub context: Context,
    pub payload: Payload,
}

#[derive(Serialize, Deserialize)]
pub struct ErrorInfo {
    pub code: String,
    pub message: String,
}

#[derive(Serialize, Deserialize)]
pub struct AuditInfo {
    pub invariants_passed: bool,
    pub messages: Vec<String>,
}

#[derive(Serialize, Deserialize)]
pub struct ExecutionOutput {
    pub module_id: String,
    pub version: String,
    pub status: String, // "ok" | "error"
    pub result: Option<serde_json::Value>,
    pub audit: AuditInfo,
    pub error: Option<ErrorInfo>,
}

#[wasm_bindgen]
pub fn execute(input: JsValue) -> JsValue {
    let parsed: ExecutionInput = from_value(input).unwrap();

    // TODO: module-specific logic here
    let result = serde_json::json!({ "example": true });

    let out = ExecutionOutput {
        module_id: parsed.module_id,
        version: parsed.version,
        status: "ok".to_string(),
        result: Some(result),
        audit: AuditInfo {
            invariants_passed: true,
            messages: vec![],
        },
        error: None,
    };

    to_value(&out).unwrap()
}
