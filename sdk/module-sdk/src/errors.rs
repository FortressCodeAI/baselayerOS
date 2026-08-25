use std::fmt;

#[derive(Debug, Clone)]
pub enum ModuleError {
    UnknownModule(String),
    MissingInput(String),
    ExecutionFailure(String),
    DeterminismViolation(String),
    Validation(ValidationError),
    Refusal(RefusalError),
}

pub enum Refusal {
}

impl std::fmt::Display for ModuleError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ModuleError::UnknownModule(m) =>
                write!(f, "Unknown module '{}'", m),
            ModuleError::MissingInput(i) =>
                write!(f, "Required input '{}' missing", i),
            ModuleError::ExecutionFailure(msg) =>
                write!(f, "Module execution failure: {}", msg),
            ModuleError::DeterminismViolation(msg) =>
                write!(f, "Determinism violation: {}", msg),
        }
    }
}

impl std::error::Error for ModuleError {}
