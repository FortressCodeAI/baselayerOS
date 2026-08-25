use serde_json::Value;

use crate::identity::ActorIdentity;
use crate::envelopes::{ExecutionEnvelope, GovernanceEnvelope};
use crate::proposal::GovernedProposal;
use crate::invariants::{KernelInvariantSource, select_invariants};
use crate::constraints::{KernelConstraintSource, ConstraintViolation};
use crate::safety::ensure_safe_payload;
use crate::qc::qc_invariants;

pub struct KaliGovernance<'a> {
    invariants: &'a dyn KernelInvariantSource,
    constraints: &'a dyn KernelConstraintSource,
}

impl<'a> KaliGovernance<'a> {
    pub fn new(
        invariants: &'a dyn KernelInvariantSource,
        constraints: &'a dyn KernelConstraintSource,
    ) -> Self {
        Self { invariants, constraints }
    }

    #[allow(clippy::too_many_arguments)]
    pub fn build(
        &self,
        identity: &ActorIdentity,
        module_id: &str,
        version: &str,
        envelope_id: &str,
        action_slug: &str,
        timestamp_ms_hex: &str,
        record_hash_hex: &str,
        routing_seal: &str,
        payload: Value,
        trace_id: &str,
        state_snapshot: Value,
    ) -> Result<(ExecutionEnvelope, GovernanceEnvelope, GovernedProposal), Vec<ConstraintViolation>> {

        // 1. Kernel constraints (roles, action, etc.)
        self.constraints
            .validate_action(action_slug, &identity.roles)?;

        // 2. Safety checks on payload
        ensure_safe_payload(&payload)?;

        // 3. Invariants from Kernel
        let invariants = select_invariants(self.invariants, action_slug);

        // 4. QC on invariants
        qc_invariants(&invariants)?;

        // 5. Build execution envelope for substrate
        let exec_env = ExecutionEnvelope::new(
            envelope_id,
            identity,
            action_slug,
            timestamp_ms_hex,
            record_hash_hex,
            state_snapshot,
        );

        // 6. Build governance envelope for MayIAI / CAGE / substrate governance engine
        let gov_env = GovernanceEnvelope::new(
            envelope_id,
            identity,
            action_slug,
            timestamp_ms_hex,
            record_hash_hex,
            routing_seal,
            invariants,
        );

        // 7. Build governed proposal for substrate integration layer
        let proposal = GovernedProposal::new(
            module_id.to_string(),
            version.to_string(),
            envelope_id.to_string(),
            payload,
            identity,
            trace_id.to_string(),
            timestamp_ms_hex.to_string(),
        );

        Ok((exec_env, gov_env, proposal))
    }
}
