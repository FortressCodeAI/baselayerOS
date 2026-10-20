use crate::audit::event::AuditEvent;
use crate::errors::substrate_error::SubstrateError;

pub fn load_events_for_envelope(path: &str, envelope_id: &str) -> Result<Vec<AuditEvent>, SubstrateError> {
    let content = std::fs::read_to_string(path).map_err(|e| SubstrateError::Audit(e.to_string()))?;
    let mut events = Vec::new();

    for line in content.lines() {
        if let Ok(event) = serde_json::from_str::<AuditEvent>(line) {
            if event.envelope_id == envelope_id {
                events.push(event);
            }
        }
    }

    Ok(events)
}
