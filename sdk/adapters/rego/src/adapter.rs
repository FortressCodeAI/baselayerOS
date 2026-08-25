use crate::schemas::ExecutionEnvelope;

pub struct RegoAdapter;

impl RegoAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn evaluate(&self, envelope: &ExecutionEnvelope) -> Result<(), String> {
        let module = &envelope.state_snapshot.module;

        match module.as_str() {
            "hello-world" => Ok(()),
            "data-cleaner" => Ok(()),
            "pii-scrubber" => Ok(()),
            _ => Err(format!("Rego policy denies module '{}'", module)),
        }
    }
}
