use serde::{Serialize, Deserialize};
use substrate::envelope::Envelope;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AaifEvaluation {
    pub decision: String,
    pub score: u8,
}

impl AaifEvaluation {
    pub fn pass() -> Self {
        Self { decision: "pass".into(), score: 100 }
    }

    pub fn fail(reason: &str) -> Self {
        Self { decision: format!("fail: {}", reason), score: 0 }
    }
}
