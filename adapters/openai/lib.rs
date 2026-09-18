use anyhow::Result;
use reqwest::blocking::Client;
use serde::{Deserialize, Serialize};
use serde_json::Value;

use baselayeros_substrate::envelope::Envelope;

#[derive(Debug, Serialize, Deserialize)]
pub struct OpenAIRequest {
    pub model: String,
    pub messages: Vec<OpenAIMessage>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct OpenAIMessage {
    pub role: String,
    pub content: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct OpenAIResponse {
    pub id: String,
    pub choices: Vec<OpenAIChoice>,
    pub model: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct OpenAIChoice {
    pub message: OpenAIMessage,
}

pub struct OpenAIAdapter {
    client: Client,
    api_key: String,
}

impl OpenAIAdapter {
    pub fn new(api_key: String) -> Self {
        Self {
            client: Client::new(),
            api_key,
        }
    }

    pub fn invoke(&self, model: &str, prompt: &str) -> Result<Envelope> {
        let req = OpenAIRequest {
            model: model.to_string(),
            messages: vec![OpenAIMessage {
                role: "user".into(),
                content: prompt.into(),
            }],
        };

        let raw: Value = self
            .client
            .post("https://api.openai.com/v1/chat/completions")
            .header("Authorization", format!("Bearer {}", self.api_key))
            .json(&req)
            .send()?
            .json()?;

        let parsed: OpenAIResponse = serde_json::from_value(raw.clone())?;

        let text = parsed.choices[0].message.content.clone();

        let envelope = Envelope::new(
            "openai",
            &parsed.model,
            text,
            raw,
        );

        Ok(envelope)
    }
}
