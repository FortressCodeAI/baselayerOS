use crate::registry::product::*;

pub fn finance_pack() -> ProductSpec {
    ProductSpec {
        slug: "finance_pack".into(),
        name: "Finance Risk & Controls Pack".into(),
        description: "Deterministic AML/KYC, SOX controls, fraud detection, transaction monitoring, and regulatory reporting.".into(),
        pricing: PricingModel { annual_price_cad: 300_000 },
        modules: vec![

            // ---------------------------------------------------------------------
            // MODULE 1 — Transaction Monitoring & AML
            // ---------------------------------------------------------------------
            ModuleSpec {
                slug: "transaction_monitoring".into(),
                name: "Transaction Monitoring & AML".into(),
                description: "Monitor transactions, detect AML patterns, and classify suspicious activity deterministically.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "transaction_ingest".into(),
                        name: "Transaction Ingest".into(),
                        description: "Ingest financial transactions from core banking, payment rails, and ledger systems.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "transaction_operator".into(),
                                config: serde_json::json!({ "mode": "ingest" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "aml_pattern_detection".into(),
                        name: "AML Pattern Detection".into(),
                        description: "Detect AML patterns such as structuring, layering, and rapid movement of funds.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "aml_operator".into(),
                                config: serde_json::json!({ "mode": "pattern_detection" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "suspicious_activity_classification".into(),
                        name: "Suspicious Activity Classification".into(),
                        description: "Classify suspicious activity deterministically for SAR generation.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "classification_operator".into(),
                                config: serde_json::json!({ "mode": "suspicious_activity" }),
                            },
                        ],
                    },
                ],
            },

            // ---------------------------------------------------------------------
            // MODULE 2 — KYC, Identity & Customer Due Diligence
            // ---------------------------------------------------------------------
            ModuleSpec {
                slug: "kyc_identity".into(),
                name: "KYC, Identity & Customer Due Diligence".into(),
                description: "Verify identity, validate documents, and enforce deterministic KYC rules.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "kyc_verification".into(),
                        name: "KYC Verification".into(),
                        description: "Verify customer identity using deterministic document and biometric checks.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "kyc_operator".into(),
                                config: serde_json::json!({ "mode": "verify" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "document_validation".into(),
                        name: "Document Validation".into(),
                        description: "Validate identity documents (passport, driver’s license, national ID) deterministically.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "validation_operator".into(),
                                config: serde_json::json!({ "mode": "document_validation" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "risk_scoring".into(),
                        name: "Risk Scoring".into(),
                        description: "Generate deterministic customer risk scores using KYC, AML, and behavioral signals.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "risk_operator".into(),
                                config: serde_json::json!({ "mode": "risk_scoring" }),
                            },
                        ],
                    },
                ],
            },

            // ---------------------------------------------------------------------
            // MODULE 3 — SOX Controls & Financial Governance
            // ---------------------------------------------------------------------
            ModuleSpec {
                slug: "sox_controls".into(),
                name: "SOX Controls & Financial Governance".into(),
                description: "Execute SOX controls, validate financial workflows, and enforce deterministic governance.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "sox_control_mapping".into(),
                        name: "SOX Control Mapping".into(),
                        description: "Map financial controls to SOX requirements and internal governance frameworks.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "control_operator".into(),
                                config: serde_json::json!({ "framework": "SOX" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "control_test_execution".into(),
                        name: "Control Test Execution".into(),
                        description: "Execute SOX control tests deterministically with full auditability.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "test_operator".into(),
                                config: serde_json::json!({ "mode": "sox_test" }),
                            },
                            OperatorBinding {
                                operator_slug: "audit_operator".into(),
                                config: serde_json::json!({ "mode": "sox_audit" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "financial_workflow_validation".into(),
                        name: "Financial Workflow Validation".into(),
                        description: "Validate financial workflows (approvals, transfers, reconciliations) deterministically.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "validation_operator".into(),
                                config: serde_json::json!({ "mode": "financial_workflow" }),
                            },
                        ],
                    },
                ],
            },

            // ---------------------------------------------------------------------
            // MODULE 4 — Fraud Detection & Regulatory Reporting
            // ---------------------------------------------------------------------
            ModuleSpec {
                slug: "fraud_reporting".into(),
                name: "Fraud Detection & Regulatory Reporting".into(),
                description: "Detect fraud, escalate incidents, and generate deterministic regulatory reports.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "fraud_detection".into(),
                        name: "Fraud Detection".into(),
                        description: "Detect fraud patterns such as account takeover, synthetic identity, and insider fraud.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "fraud_operator".into(),
                                config: serde_json::json!({ "mode": "fraud_detection" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "fraud_escalation".into(),
                        name: "Fraud Escalation".into(),
                        description: "Escalate fraud incidents deterministically with predefined workflows.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "escalation_operator".into(),
                                config: serde_json::json!({ "mode": "fraud_escalation" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "regulatory_report_generation".into(),
                        name: "Regulatory Report Generation".into(),
                        description: "Generate SARs, STRs, and other regulatory reports deterministically.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "report_operator".into(),
                                config: serde_json::json!({
                                    "formats": ["pdf", "json"],
                                    "reports": ["SAR", "STR"]
                                }),
                            },
                        ],
                    },
                ],
            },
        ],
    }
}
