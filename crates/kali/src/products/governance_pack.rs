use crate::registry::product::*;

pub fn governance_pack() -> ProductSpec {
    ProductSpec {
        slug: "governance_pack".into(),
        name: "Governance Pack".into(),
        description: "Deterministic enterprise governance across evidence, policies, controls, audits, exceptions, and reporting.".into(),
        pricing: PricingModel { annual_price_cad: 350_000 },
        modules: vec![
            
            // MODULE 1 — Evidence Management
            ModuleSpec {
                slug: "evidence_management".into(),
                name: "Evidence Management".into(),
                description: "Ingest, normalize, classify, and tag governance evidence.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "evidence_ingest".into(),
                        name: "Evidence Ingest".into(),
                        description: "Ingest governance evidence from logs, configs, screenshots, and reports.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "evidence_operator".into(),
                                config: serde_json::json!({ "source": "multi" }),
                            },
                            OperatorBinding {
                                operator_slug: "classification_operator".into(),
                                config: serde_json::json!({ "mode": "governance" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "evidence_normalization".into(),
                        name: "Evidence Normalization".into(),
                        description: "Normalize evidence into deterministic schema for replay and audit.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "normalization_operator".into(),
                                config: serde_json::json!({ "schema": "kali_evidence_v1" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "evidence_tagging".into(),
                        name: "Evidence Tagging".into(),
                        description: "Tag evidence with controls, policies, risks, and compliance frameworks.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "tagging_operator".into(),
                                config: serde_json::json!({ "mode": "control_mapping" }),
                            },
                        ],
                    },
                ],
            },

            
            // MODULE 2 — Policy Lifecycle
            ModuleSpec {
                slug: "policy_lifecycle".into(),
                name: "Policy Lifecycle".into(),
                description: "Register, evaluate, enforce, and track governance policies.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "policy_registration".into(),
                        name: "Policy Registration".into(),
                        description: "Register new policies with metadata, scope, owners, and control mappings.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "policy_operator".into(),
                                config: serde_json::json!({ "action": "register" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "policy_evaluation".into(),
                        name: "Policy Evaluation".into(),
                        description: "Evaluate policies against evidence, controls, and deterministic invariants.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "policy_operator".into(),
                                config: serde_json::json!({ "action": "evaluate" }),
                            },
                            OperatorBinding {
                                operator_slug: "invariant_operator".into(),
                                config: serde_json::json!({ "mode": "governance_invariants" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "policy_enforcement".into(),
                        name: "Policy Enforcement".into(),
                        description: "Enforce policies deterministically (block, alert, escalate, remediate).".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "enforcement_operator".into(),
                                config: serde_json::json!({ "mode": "deterministic_enforcement" }),
                            },
                        ],
                    },
                ],
            },

            // MODULE 3 — Control Mapping & Compliance
            ModuleSpec {
                slug: "control_mapping".into(),
                name: "Control Mapping & Compliance".into(),
                description: "Map controls to frameworks, execute tests, and aggregate compliance status.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "control_catalog_mapping".into(),
                        name: "Control Catalog Mapping".into(),
                        description: "Map controls to SOC2, ISO27001, HIPAA, PCI-DSS, and other frameworks.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "control_operator".into(),
                                config: serde_json::json!({
                                    "frameworks": ["SOC2", "ISO27001", "HIPAA", "PCI-DSS"]
                                }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "control_test_execution".into(),
                        name: "Control Test Execution".into(),
                        description: "Execute control tests deterministically with full auditability.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "test_operator".into(),
                                config: serde_json::json!({ "mode": "deterministic_control_test" }),
                            },
                            OperatorBinding {
                                operator_slug: "audit_operator".into(),
                                config: serde_json::json!({ "mode": "control_test_audit" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "compliance_status_aggregation".into(),
                        name: "Compliance Status Aggregation".into(),
                        description: "Aggregate compliance status across frameworks and controls.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "aggregation_operator".into(),
                                config: serde_json::json!({ "mode": "framework_aggregation" }),
                            },
                        ],
                    },
                ],
            },

            // MODULE 4 — Audit, Exceptions & Reporting
            ModuleSpec {
                slug: "audit_exceptions_reporting".into(),
                name: "Audit, Exceptions & Reporting".into(),
                description: "Generate audit trails, handle exceptions, and produce governance reports.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "audit_trail_generation".into(),
                        name: "Audit Trail Generation".into(),
                        description: "Generate deterministic audit trails for regulators, auditors, and internal teams.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "audit_operator".into(),
                                config: serde_json::json!({ "mode": "full_audit_trail" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "exception_handling".into(),
                        name: "Exception Handling".into(),
                        description: "Handle exceptions, waivers, and risk acceptances with deterministic traceability.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "exception_operator".into(),
                                config: serde_json::json!({ "mode": "exception_workflow" }),
                            },
                            OperatorBinding {
                                operator_slug: "risk_operator".into(),
                                config: serde_json::json!({ "mode": "risk_acceptance" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "governance_report_generation".into(),
                        name: "Governance Report Generation".into(),
                        description: "Generate governance reports for boards, regulators, and internal stakeholders.".into(),
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
