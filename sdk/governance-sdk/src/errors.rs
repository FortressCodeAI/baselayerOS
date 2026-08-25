#[derive(Debug, Clone)]
pub enum GovernanceError {
    UnknownPolicy(String),
    MissingModuleVersion,
    MissingTransitionName,
    MissingInvariantsStrict,
    RulebookViolation(String),
}

impl std::fmt::Display for GovernanceError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            GovernanceError::UnknownPolicy(p) =>
                write!(f, "Unknown governance policy '{}'", p),
            GovernanceError::MissingModuleVersion =>
                write!(f, "Module version MUST be declared"),
            GovernanceError::MissingTransitionName =>
                write!(f, "Transition name MUST be declared"),
            GovernanceError::MissingInvariantsStrict =>
                write!(f, "Strict governance policy requires invariants"),
            GovernanceError::RulebookViolation(msg) =>
                write!(f, "Rulebook violation: {}", msg),
        }
    }
}

impl std::error::Error for GovernanceError {}
