use serde::Serialize;

#[derive(Debug, Clone, Serialize)]
pub struct ExecutionResult {
    pub allowed: bool,
    pub message: String,
}

impl ExecutionResult {
    pub fn allow(msg: impl Into<String>) -> Self {
        Self { allowed: true, message: msg.into() }
    }

    pub fn deny(msg: impl Into<String>) -> Self {
        Self { allowed: false, message: msg.into() }
    }
}
