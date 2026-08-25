use crate::constraints::ConstraintViolation;


pub fn qc_invariants(invariants: &[String]) -> Result<(), Vec<ConstraintViolation>> {
    if invariants.is_empty() {
        return Err(vec![ConstraintViolation {
            field: "invariants".into(),
            message: "Invariant set must not be empty".into(),
        }]);
    }

    Ok(())
}
