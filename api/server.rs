use axum::{
    routing::{get, post},
    Json, Router,
};
use std::sync::{Arc, Mutex};
use std::path::PathBuf;

use crate::substrate::{
    envelope::Envelope,
    state::SubstrateState,
    audit_chain_local::LocalAuditChain,
    execution_adapter::ExecutionAdapter,
};

#[derive(Clone)]
pub struct ConsoleContext {
    pub state: Arc<Mutex<SubstrateState>>,
    pub audit: Arc<Mutex<LocalAuditChain>>,
    pub adapter: Arc<ExecutionAdapter>,
}

impl ConsoleContext {
    pub fn new() -> Self {
        let state = Arc::new(Mutex::new(SubstrateState::new()));

        let audit_path = PathBuf::from("data/audit_chain.jsonl");
        let audit = Arc::new(Mutex::new(
            LocalAuditChain::new(audit_path).expect("audit chain")
        ));

        let adapter = Arc::new(ExecutionAdapter::new());

        Self { state, audit, adapter }
    }
}

async fn get_state(ctx: Arc<ConsoleContext>) -> Json<serde_json::Value> {
    let state = ctx.state.lock().unwrap();
    Json(state.to_json())
}

async fn get_envelopes(ctx: Arc<ConsoleContext>) -> Json<serde_json::Value> {
    let audit = ctx.audit.lock().unwrap();
    let entries = audit.read_all().expect("audit read");
    Json(serde_json::json!(entries))
}

async fn get_audit_chain(ctx: Arc<ConsoleContext>) -> Json<serde_json::Value> {
    let audit = ctx.audit.lock().unwrap();
    let entries = audit.read_all().expect("audit read");
    Json(serde_json::json!(entries))
}

async fn post_envelope(
    ctx: Arc<ConsoleContext>,
    Json(envelope): Json<Envelope>,
) -> Json<serde_json::Value> {
    let mut state = ctx.state.lock().unwrap();
    let mut audit = ctx.audit.lock().unwrap();

    let required_tags: [&str; 0] = [];

    let outcome = ctx
        .adapter
        .execute(&envelope, &mut state, &mut audit, &required_tags)
        .expect("execution");

    Json(serde_json::json!({
        "outcome": format!("{:?}", outcome),
        "state": state.to_json()
    }))
}

pub async fn start_console_server() {
    let ctx = Arc::new(ConsoleContext::new());

    let app = Router::new()
        .route("/api/state", get({
            let ctx = ctx.clone();
            move || get_state(ctx.clone())
        }))
        .route("/api/envelopes", get({
            let ctx = ctx.clone();
            move || get_envelopes(ctx.clone())
        }))
        .route("/api/audit-chain", get({
            let ctx = ctx.clone();
            move || get_audit_chain(ctx.clone())
        }))
        .route("/api/envelope", post({
            let ctx = ctx.clone();
            move |body| post_envelope(ctx.clone(), body)
        }));

    println!("Console running on http://localhost:3000");
    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
