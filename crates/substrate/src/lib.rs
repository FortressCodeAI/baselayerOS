pub mod execution;
pub mod config;
pub mod envelopes;
pub mod errors;
pub mod state_machine;
pub mod audit;
pub mod evidence;
pub mod wasm;


pub use execution::replay_engine::ReplayEngine;
pub use execution::invariant_engine::DefaultInvariantEngine;
pub use execution::refusal_engine::ExecutionResult;

pub use config::packs::DummyPack;

pub use envelopes::execution_envelope::ExecutionEnvelope;

pub use errors::substrate_error::SubstrateError;

pub fn replay_envelope(
    audit_path: &str,
    envelope: ExecutionEnvelope,
) -> Result<execution::replay_engine::ReplayResult, SubstrateError> {
    let invariants = Box::new(DefaultInvariantEngine::new());
    let pack = Box::new(DummyPack);

    let engine = ReplayEngine::new(invariants, pack);
    engine.replay(audit_path, &envelope)
}
