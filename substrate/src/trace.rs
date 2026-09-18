use serde::{Deserialize, Serialize};


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TraceEvent {
    pub message: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExecutionTrace {
    pub envelope_id: String,
    pub events: Vec<TraceEvent>,
}

impl ExecutionTrace {
    pub fn new(envelope_id: String) -> Self {
        Self {
            envelope_id,
            events: Vec::new(),
        }
    }
}

pub fn record_trace(trace: &mut ExecutionTrace, message: &str) {
    trace.events.push(TraceEvent {
        message: message.to_string(),
    });
}
