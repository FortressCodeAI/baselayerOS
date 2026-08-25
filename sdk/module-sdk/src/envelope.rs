use serde::{Deserialize, Serialize};
use serde_json::Value;
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum EnvelopeSafetyClass {
    Low,
    Medium,
    High,
    #[serde(rename = "high-risk")]
    HighRisk,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum EnvelopeDomain {
    Public,
    Internal,
    Restricted,
    Forbidden,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EnvelopeMetadata {
    pub timestamp: DateTime<Utc>,
    pub version: String,
    pub trace_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EnvelopeInput {
    pub data: Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExecutionEnvelope {
    pub actor: String,
    pub intent: String,
    pub domain: EnvelopeDomain,
    pub safety_class: EnvelopeSafetyClass,
    pub input: EnvelopeInput,
    pub metadata: EnvelopeMetadata,
}

impl ExecutionEnvelope {
    pub fn new(
        actor: String,
        intent: String,
        domain: EnvelopeDomain,
        safety_class: EnvelopeSafetyClass,
        input: Value,
        trace_id: String,
    ) -> Self {
        Self {
            actor,
            intent,
            domain,
            safety_class,
            input: EnvelopeInput { data: input },
            metadata: EnvelopeMetadata {
                timestamp: Utc::now(),
                version: "1.0.0".into(),
                trace_id,
            },
        }
    }

    pub fn input(&self) -> &Value {
        &self.input.data
    }

    pub fn summary(&self) -> String {
        format!(
            "actor={} intent={} domain={:?} safety={:?} trace={}",
            self.actor,
            self.intent,
            self.domain,
            self.safety_class,
            self.metadata.trace_id
        )
    }
}

pub struct EnvelopeBuilder {
    actor: Option<String>,
    intent: Option<String>,
    domain: Option<EnvelopeDomain>,
    safety_class: Option<EnvelopeSafetyClass>,
    input: Option<Value>,
    trace_id: Option<String>,
}

impl EnvelopeBuilder {
    pub fn new() -> Self {
        Self {
            actor: None,
            intent: None,
            domain: None,
            safety_class: None,
            input: None,
            trace_id: None,
        }
    }

    pub fn actor(mut self, actor: impl Into<String>) -> Self {
        self.actor = Some(actor.into());
        self
    }

    pub fn intent(mut self, intent: impl Into<String>) -> Self {
        self.intent = Some(intent.into());
        self
    }

    pub fn domain(mut self, domain: EnvelopeDomain) -> Self {
        self.domain = Some(domain);
        self
    }

    pub fn safety_class(mut self, class: EnvelopeSafetyClass) -> Self {
        self.safety_class = Some(class);
        self
    }

    pub fn input(mut self, value: Value) -> Self {
        self.input = Some(value);
        self
    }

    pub fn trace_id(mut self, id: impl Into<String>) -> Self {
        self.trace_id = Some(id.into());
        self
    }

    pub fn build(self) -> ExecutionEnvelope {
        ExecutionEnvelope::new(
            self.actor.expect("actor required"),
            self.intent.expect("intent required"),
            self.domain.expect("domain required"),
            self.safety_class.expect("safety_class required"),
            self.input.expect("input required"),
            self.trace_id.expect("trace_id required"),
        )
    }
}
