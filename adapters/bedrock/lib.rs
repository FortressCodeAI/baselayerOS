use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

use crate::substrate::envelope::{Envelope, EnvelopeId, EnvelopeKind};
use sha2::{Digest, Sha256};
use hex;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BedrockContentBlock {
    pub text: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BedrockResponse {
    pub model: String,
    pub output: Vec<BedrockContentBlock>,
    pub raw: Value,
}

pub struct BedrockAdapter;

impl BedrockAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn to_envelope(&self, response: BedrockResponse) -> Envelope {
        let first_text = response
            .output
            .iter()
            .find_map(|b| b.text.clone())
            .unwrap_or_default();

        let mut hasher = Sha256::new();
        hasher.update(first_text.as_bytes());
        let digest = hex::encode(hasher.finalize());

        let id = EnvelopeId(digest);

        let timestamp = chrono::Utc::now().to_rfc3339();

        let mut tags = HashMap::new();
        tags.insert("provider".to_string(), "bedrock".to_string());
        tags.insert("model".to_string(), response.model.clone());

        let payload = serde_json::json!({
            "bedrock_text": first_text,
            "raw": response.raw,
        });

        Envelope {
            id,
            kind: EnvelopeKind::Intent,
            source: "bedrock".to_string(),
            correlation_id: None,
            timestamp,
            payload,
            tags,
        }
    }
}
