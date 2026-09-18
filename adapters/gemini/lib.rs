use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

use baselayeros_substrate::envelope::{Envelope, EnvelopeId, EnvelopeKind};
use sha2::{Digest, Sha256};
use hex;


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeminiCandidate {
    pub content: Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeminiResponse {
    pub candidates: Vec<GeminiCandidate>,
    pub model: Option<String>,
    pub create_time: Option<String>,
}

pub struct GeminiAdapter;

impl GeminiAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn to_envelope(&self, response: GeminiResponse) -> Envelope {
        let first_content = response
            .candidates
            .get(0)
            .map(|c| c.content.clone())
            .unwrap_or(Value::Null);

        let serialized = serde_json::to_vec(&first_content).unwrap_or_default();
        let mut hasher = Sha256::new();
        hasher.update(&serialized);
        let digest = hex::encode(hasher.finalize());

        let id = EnvelopeId(digest);

        let timestamp = response
            .create_time
            .clone()
            .unwrap_or_else(|| "1970-01-01T00:00:00Z".to_string());

        let mut tags = HashMap::new();
        tags.insert("provider".to_string(), "gemini".to_string());
        if let Some(model) = &response.model {
            tags.insert("model".to_string(), model.clone());
        }

        let payload = serde_json::json!({
            "gemini_content": first_content,
            "raw": response,
        });

        Envelope {
            id,
            kind: EnvelopeKind::Intent,
            source: "gemini".to_string(),
            correlation_id: None,
            timestamp,
            payload,
            tags,
        }
    }
}
