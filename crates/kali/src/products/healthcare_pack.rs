use crate::registry::product::*;

pub fn healthcare_pack() -> ProductSpec {
    ProductSpec {
        slug: "healthcare_pack".into(),
        name: "Healthcare Compliance Pack".into(),
        description: "Deterministic HIPAA/PHIPA/FHIR/HL7 compliance, PHI detection, access control, clinical audit, and regulatory reporting.".into(),
        pricing: PricingModel { annual_price_cad: 250_000 },
        modules: vec![

            // ---------------------------------------------------------------------
            // MODULE 1 — PHI Detection & Data Governance
            // ---------------------------------------------------------------------
            ModuleSpec {
                slug: "phi_detection".into(),
                name: "PHI Detection & Data Governance".into(),
                description: "Detect, classify, and govern PHI across documents, messages, and clinical data.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "phi_scan".into(),
                        name: "PHI Scan".into(),
                        description: "Scan documents, messages, and structured data for PHI using deterministic classifiers.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "phi_operator".into(),
                                config: serde_json::json!({ "mode": "scan" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "phi_classification".into(),
                        name: "PHI Classification".into(),
                        description: "Classify detected PHI into categories (identifiers, clinical data, financial data).".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "classification_operator".into(),
                                config: serde_json::json!({ "mode": "phi_classification" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "phi_redaction".into(),
                        name: "PHI Redaction".into(),
                        description: "Deterministically redact PHI from documents and messages.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "redaction_operator".into(),
                                config: serde_json::json!({ "mode": "deterministic_redaction" }),
                            },
                        ],
                    },
                ],
            },

            // ---------------------------------------------------------------------
            // MODULE 2 — Consent, Access & Authorization
            // ---------------------------------------------------------------------
            ModuleSpec {
                slug: "consent_access".into(),
                name: "Consent, Access & Authorization".into(),
                description: "Evaluate consent, authorize access, and enforce deterministic access controls.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "consent_validation".into(),
                        name: "Consent Validation".into(),
                        description: "Validate patient consent against PHIPA/HIPAA rules and clinical context.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "consent_operator".into(),
                                config: serde_json::json!({ "mode": "validate" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "access_request_evaluation".into(),
                        name: "Access Request Evaluation".into(),
                        description: "Evaluate access requests deterministically based on role, consent, and PHI sensitivity.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "access_operator".into(),
                                config: serde_json::json!({ "mode": "evaluate_request" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "access_enforcement".into(),
                        name: "Access Enforcement".into(),
                        description: "Enforce access decisions deterministically with audit anchors.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "enforcement_operator".into(),
                                config: serde_json::json!({ "mode": "access_enforcement" }),
                            },
                        ],
                    },
                ],
            },

            // ---------------------------------------------------------------------
            // MODULE 3 — Clinical Workflow Audit
            // ---------------------------------------------------------------------
            ModuleSpec {
                slug: "clinical_audit".into(),
                name: "Clinical Workflow Audit".into(),
                description: "Audit clinical workflows for compliance with HIPAA, PHIPA, FHIR, and HL7.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "clinical_event_audit".into(),
                        name: "Clinical Event Audit".into(),
                        description: "Audit clinical events (orders, notes, labs) for compliance and traceability.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "audit_operator".into(),
                                config: serde_json::json!({ "mode": "clinical_event" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "clinical_data_validation".into(),
                        name: "Clinical Data Validation".into(),
                        description: "Validate clinical data against FHIR/HL7 schemas deterministically.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "validation_operator".into(),
                                config: serde_json::json!({ "schema": "FHIR_R4" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "clinical_workflow_compliance".into(),
                        name: "Clinical Workflow Compliance".into(),
                        description: "Check clinical workflows for compliance violations and generate deterministic findings.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "compliance_operator".into(),
                                config: serde_json::json!({ "mode": "clinical_compliance" }),
                            },
                        ],
                    },
                ],
            },

            // ---------------------------------------------------------------------
            // MODULE 4 — Regulatory Reporting & Audit Trails
            // ---------------------------------------------------------------------
            ModuleSpec {
                slug: "regulatory_reporting".into(),
                name: "Regulatory Reporting & Audit Trails".into(),
                description: "Generate deterministic audit trails and regulatory reports for HIPAA/PHIPA.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "hipaa_audit_trail".into(),
                        name: "HIPAA Audit Trail".into(),
                        description: "Generate deterministic HIPAA audit trails for all PHI access and modifications.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "audit_operator".into(),
                                config: serde_json::json!({ "mode": "hipaa_audit" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "phipa_audit_trail".into(),
                        name: "PHIPA Audit Trail".into(),
                        description: "Generate deterministic PHIPA audit trails for Ontario healthcare compliance.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "audit_operator".into(),
                                config: serde_json::json!({ "mode": "phipa_audit" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "regulatory_report_generation".into(),
                        name: "Regulatory Report Generation".into(),
                        description: "Generate compliance reports for regulators, auditors, and internal governance teams.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "report_operator".into(),
                                config: serde_json::json!({ "formats": ["pdf", "json"] }),
                            },
                        ],
                    },
                ],
            },
        ],
    }
}
