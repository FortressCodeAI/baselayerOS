use anyhow::Result;
use reqwest::blocking::Client;
use serde::{Deserialize, Serialize};
use serde_json::Value;

use baselayeros_substrate::envelope::Envelope;

#[derive(Debug, Serialize, Deserialize)]
pub struct AzureOpenAIRequest {
    pub messages: Vec<AzureOpenAIMessage>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AzureOpenAIMessage {
    pub role: String,
    pub content: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AzureOpenAIResponse {
    pub id: String,
    pub choices: Vec<AzureOpenAIChoice>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AzureOpenAIChoice {
    pub message: AzureOpenAIMessage,
}

pub struct AzureOpenAIAdapter {
    client: Client,
    endpoint: String,
    api_key: String,
    deployment: String,
}

impl AzureOpenAIAdapter {
    pub fn new(endpoint: String, api_key: String, deployment: String) -> Self {
        Self {
            client: Client::new(),
            endpoint,
            api_key,
            deployment,
        }
    }

    pub fn invoke(&self, prompt: &str) -> Result<Envelope> {
        let req = AzureOpenAIRequest {
            messages: vec![AzureOpenAIMessage {
                role: "user".into(),
                content: prompt.into(),
            }],
        };

        let url = format!(
            "{}/openai/deployments/{}/chat/completions?api-version=2024-02-01",
            self.endpoint, self.deployment
        );

        let raw: Value = self
            .client
            .post(&url)
            .header("api-key", &self.api_key)
            .json(&req)
            .send()?
            .json()?;

        let parsed: AzureOpenAIResponse = serde_json::from_value(raw.clone())?;

        let text = parsed.choices[0].message.content.clone();

        let envelope = Envelope::new(
            "azure-openai",
            &self.deployment,
            text,
            raw,
        );

        Ok(envelope)
    }
}
