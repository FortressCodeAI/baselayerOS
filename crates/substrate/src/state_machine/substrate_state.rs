use crate::state_machine::snapshot::StateSnapshot;

#[derive(Debug, Clone)]
pub struct SubstrateState;

impl SubstrateState {
    pub fn new() -> Self {
        Self
    }

    pub fn snapshot(&self) -> StateSnapshot {
        StateSnapshot {
            hash: "state-hash".into(),
        }
    }
}
