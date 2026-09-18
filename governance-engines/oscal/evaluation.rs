use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OscalEvaluation {
    pub status: String,
}

impl OscalEvaluation {
    pub fn pass() -> Self {
        Self { status: "pass".into() }
    }

    pub fn fail(reason: &str) -> Self {
        Self { status: format!("fail: {}", reason) }
    }
}
