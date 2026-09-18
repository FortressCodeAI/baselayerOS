use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

use baselayeros_substrate::envelope::{Envelope, EnvelopeId, EnvelopeKind};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LangChainMessage {
    pub role: String,
    pub content: Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LangChainRun {
    pub id: String,
    pub model: Option<String>,
    pub output: Option<LangChainMessage>,
}

pub struct LangChainAdapter;

impl LangChainAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn to_envelope(&self, run: LangChainRun) -> Envelope {
        let id = EnvelopeId(run.id.clone());
        let timestamp = chrono::Utc::now().to_rfc3339();

        let mut tags = HashMap::new();
        tags.insert("provider".to_string(), "langchain".to_string());
        if let Some(model) = &run.model {
            tags.insert("model".to_string(), model.clone());
        }

        let content = run
            .output
            .as_ref()
            .map(|m| m.content.clone())
            .unwrap_or(Value::Null);

        let payload = serde_json::json!({
            "langchain_output": content,
            "raw": run,
        });

        Envelope {
            id,
            kind: EnvelopeKind::Intent,
            source: "langchain".to_string(),
            correlation_id: None,
            timestamp,
            payload,
            tags,
        }
    }
}
