use thiserror::Error;

#[derive(Debug, Error)]
pub enum SubstrateError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),

    #[error("Invariant error: {0}")]
    Invariant(String),

    #[error("Execution error: {0}")]
    Execution(String),

    #[error("Audit error: {0}")]
    Audit(String),
}
