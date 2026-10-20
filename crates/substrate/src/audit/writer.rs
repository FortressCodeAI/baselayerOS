use crate::audit::event::AuditEvent;
use crate::errors::substrate_error::SubstrateError;

pub fn write_audit_event(path: &str, event: &AuditEvent) -> Result<(), SubstrateError> {
    let line = serde_json::to_string(event).unwrap() + "\n";
    std::fs::write(path, line).map_err(|e| SubstrateError::Audit(e.to_string()))
}
