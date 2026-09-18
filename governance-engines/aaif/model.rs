use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AaifDecision {
    pub passed: bool,
    pub reason: String,
    pub score: u8,
}
