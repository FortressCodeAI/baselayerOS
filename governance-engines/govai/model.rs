use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovAiDecision {
    pub compliant: bool,
    pub reason: String,
}
