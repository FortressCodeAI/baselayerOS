use serde_json::Value;
use crate::constraints::ConstraintViolation;

/// Simple safety checks Kali can run before building envelopes.
pub fn ensure_safe_payload(payload: &Value) -> Result<(), Vec<ConstraintViolation>> {
    let mut violations = Vec::new();

    // Example: payload must not be null
    if payload.is_null() {
        violations.push(ConstraintViolation {
            field: "payload".into(),
            message: "Payload must not be null".into(),
        });
    }

    if violations.is_empty() {
        Ok(())
    } else {
        Err(violations)
    }
}
