use crate::module_sdk::ModuleExecutor;
use crate::governance_sdk::GovernanceEngine;
use crate::schemas::{ExecutionEnvelope, ExecutionResult};
use crate::invariants::InvariantEngine;

pub struct ExecutionAdapter {
    module_executor: ModuleExecutor,
    governance: GovernanceEngine,
}

impl ExecutionAdapter {
    pub fn new() -> Self {
        Self {
            module_executor: ModuleExecutor::new(),
            governance: GovernanceEngine::new(),
        }
    }

    pub fn execute(&self, envelope: &ExecutionEnvelope) -> Result<ExecutionResult, String> {
        // 1. Governance check
        self.governance.validate(envelope)?;

        // 2. Deterministic module execution
        let result = self.module_executor.execute(envelope)?;

        // 3. Invariant enforcement
        InvariantEngine::validate(envelope, &result)?;

        Ok(result)
    }
}
