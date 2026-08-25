use crate::schemas::{ExecutionEnvelope, ExecutionResult};

pub struct LulaAdapter;

impl LulaAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn emit_log(&self, envelope: &ExecutionEnvelope, result: &ExecutionResult)
        -> String
    {
        format!(
            "[LULA] module={} transition={} inputs={:?} outputs={:?}",
            envelope.state_snapshot.module,
            envelope.transition.name,
            envelope.transition.inputs,
            result.outputs
        )
    }
}
