use crate::module_sdk::errors::ModuleError;
use std::collections::HashMap;

/// The execution perimeter defines what a module is allowed to do.
/// No filesystem, no network, no randomness, no external state.
pub struct ExecutionPerimeter;

impl ExecutionPerimeter {
    pub fn new() -> Self {
        Self
    }

    /// Reject any attempt to access the filesystem.
    pub fn deny_filesystem(&self, path: &str) -> Result<(), ModuleError> {
        Err(ModuleError::ExecutionFailure(format!(
            "Filesystem access denied: {}", path
        )))
    }

    /// Reject any attempt to perform network calls.
    pub fn deny_network(&self, url: &str) -> Result<(), ModuleError> {
        Err(ModuleError::ExecutionFailure(format!(
            "Network access denied: {}", url
        )))
    }

    /// Reject any attempt to use randomness.
    pub fn deny_random(&self) -> Result<(), ModuleError> {
        Err(ModuleError::DeterminismViolation(
            "Randomness is forbidden in deterministic execution".into()
        ))
    }

    /// Validate that outputs are deterministic.
    pub fn enforce_deterministic_outputs(
        &self,
        outputs: &HashMap<String, String>
    ) -> Result<(), ModuleError> {
        for (k, v) in outputs {
            if v.contains("RANDOM") || v.contains("NONDETERMINISTIC") {
                return Err(ModuleError::DeterminismViolation(format!(
                    "Output '{}' contains nondeterministic content", k
                )));
            }
        }
        Ok(())
    }
}
