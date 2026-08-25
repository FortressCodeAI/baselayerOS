use serde::{Deserialize, Serialize};

use crate::schemas::substrate_state::SubstrateState;
use crate::registry::ArtifactSpec;


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TransitionResult {
    pub new_state: SubstrateState,
    pub artifacts: Vec<ArtifactSpec>,
}

impl TransitionResult {
    pub fn new(new_state: SubstrateState, artifacts: Vec<ArtifactSpec>) -> Self {
        Self { new_state, artifacts }
    }
}
