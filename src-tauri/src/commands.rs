use tauri::AppHandle;
use baselayeros::substrate::Substrate;
use baselayeros::envelopes::Envelope;

#[tauri::command]
pub fn get_state(app: AppHandle) -> Result<serde_json::Value, String> {
    let substrate = app.state::<Substrate>();
    serde_json::to_value(substrate.state()).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn get_audit(app: AppHandle) -> Result<serde_json::Value, String> {
    let substrate = app.state::<Substrate>();
    serde_json::to_value(substrate.audit()).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn get_invariants(app: AppHandle) -> Result<serde_json::Value, String> {
    let substrate = app.state::<Substrate>();
    serde_json::to_value(substrate.invariants()).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn get_modules(app: AppHandle) -> Result<serde_json::Value, String> {
    let substrate = app.state::<Substrate>();
    serde_json::to_value(substrate.modules()).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn validate_envelope(app: AppHandle, env: serde_json::Value) -> Result<serde_json::Value, String> {
    let mut substrate = app.state::<Substrate>();
    let envelope: Envelope = serde_json::from_value(env).map_err(|e| e.to_string())?;
    let result = substrate.validate_envelope(&envelope);
    serde_json::to_value(result).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn run_demo(app: AppHandle, env: serde_json::Value) -> Result<serde_json::Value, String> {
    let mut substrate = app.state::<Substrate>();
    let envelope: Envelope = serde_json::from_value(env).map_err(|e| e.to_string())?;
    let demo_result = substrate.run_demo_flow(envelope); // execute module, produce audit + evidence
    serde_json::to_value(demo_result).map_err(|e| e.to_string())
}

#[tauri::command]
pub fn get_summary(app: AppHandle) -> Result<serde_json::Value, String> {
    let mut substrate = app.state::<Substrate>();
    let artifact = substrate.generate_global_summary();
    serde_json::to_value(artifact).map_err(|e| e.to_string())
}
