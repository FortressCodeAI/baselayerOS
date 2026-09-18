use crate::canonical::CanonicalEnvelope;
use crate::state::SubstrateState;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Attestation {
    pub envelope_digest: String,
    pub state_version: u64,
    pub attestation_digest: String,
}

#[derive(Debug, Error)]
pub enum AttestationError {
    #[error("Failed to serialize attestation: {0}")]
    SerializationError(String),
}

pub fn attest_envelope(
    envelope: &CanonicalEnvelope,
    state: &SubstrateState,
) -> Result<Attestation, AttestationError> {
    let mut hasher = Sha256::new();

    hasher.update(envelope.digest.as_bytes());
    hasher.update(state.version.to_string().as_bytes());

    let digest = hex::encode(hasher.finalize());

    Ok(Attestation {
        envelope_digest: envelope.digest.clone(),
        state_version: state.version,
        attestation_digest: digest,
    })
}
