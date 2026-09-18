use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovAiEvaluation {
    pub status: String,
}

impl GovAiEvaluation {
    pub fn compliant() -> Self {
        Self { status: "compliant".into() }
    }

    pub fn non_compliant(reason: &str) -> Self {
        Self { status: format!("non-compliant: {}", reason) }
    }
}
