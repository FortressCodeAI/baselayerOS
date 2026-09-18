use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OscalControlResult {
    pub control_id: String,
    pub passed: bool,
    pub reason: String,
}
