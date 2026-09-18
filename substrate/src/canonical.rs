use crate::envelope::Envelope;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::BTreeMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CanonicalEnvelope {
    pub id: String,
    pub kind: String,
    pub source: String,
    pub timestamp: String,
    pub payload: serde_json::Value,
    pub tags: BTreeMap<String, String>,
    pub digest: String,
}

#[derive(Debug, thiserror::Error)]
pub enum CanonicalizationError {
    #[error("Payload must be a JSON object for canonicalization")]
    PayloadNotObject,

    #[error("Failed to serialize canonical envelope for digest computation")]
    SerializationError(#[from] serde_json::Error),
}

pub fn canonicalize_envelope(
    envelope: &Envelope,
) -> Result<CanonicalEnvelope, CanonicalizationError> {
    if !envelope.payload.is_object() {
        return Err(CanonicalizationError::PayloadNotObject);
    }

    let mut sorted_payload = BTreeMap::new();
    if let Some(obj) = envelope.payload.as_object() {
        for (k, v) in obj.iter() {
            sorted_payload.insert(k.clone(), v.clone());
        }
    }

    let canonical_payload = serde_json::to_value(sorted_payload)?;

    let mut sorted_tags = BTreeMap::new();
    for (k, v) in envelope.tags.iter() {
        sorted_tags.insert(k.clone(), v.clone());
    }

    let mut canonical = CanonicalEnvelope {
        id: envelope.id.0.clone(),
        kind: format!("{:?}", envelope.kind),
        source: envelope.source.clone(),
        timestamp: envelope.timestamp.clone(),
        payload: canonical_payload,
        tags: sorted_tags,
        digest: String::new(),
    };

    let serialized = serde_json::to_vec(&canonical)?;
    let mut hasher = Sha256::new();
    hasher.update(&serialized);
    let digest_bytes = hasher.finalize();
    let digest_hex = hex::encode(digest_bytes);
    canonical.digest = digest_hex;

    Ok(canonical)
}
