use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use crate::errors::{GovernanceError, ValidationError};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovernedSchema {
    pub name: String,
    pub schema: Value,
}

pub struct SchemaValidator {
    schemas: Vec<GovernedSchema>,
}

impl SchemaValidator {
    pub fn new() -> Self {
        Self { schemas: Vec::new() }
    }

    pub fn register(&mut self, schema: GovernedSchema) {
        self.schemas.push(schema);
    }

    pub fn validate(&self, name: &str, value: &Value) -> Result<(), GovernanceError> {
        let schema = self
            .schemas
            .iter()
            .find(|s| s.name == name)
            .ok_or_else(|| GovernanceError::Validation(ValidationError {
                field: "schema".into(),
                reason: format!("Schema '{}' not found", name),
            }))?;

        // Minimal deterministic validation (no external libs)
        if !value.is_object() {
            return Err(GovernanceError::Validation(ValidationError {
                field: name.into(),
                reason: "Value must be an object".into(),
            }));
        }

        let required = schema.schema["required"].as_array().unwrap_or(&vec![]);
        for field in required {
            let field_name = field.as_str().unwrap_or("");
            if !value.get(field_name).is_some() {
                return Err(GovernanceError::Validation(ValidationError {
                    field: field_name.into(),
                    reason: "Missing required field".into(),
                }));
            }
        }

        Ok(())
    }
}

pub fn envelope_schema() -> GovernedSchema {
    GovernedSchema {
        name: "envelope".into(),
        schema: json!({
            "required": [
                "actor",
                "intent",
                "input",
                "domain",
                "safety_class"
            ]
        }),
    }
}

pub fn default_schemas() -> SchemaValidator {
    let mut validator = SchemaValidator::new();
    validator.register(envelope_schema());
    validator
}
