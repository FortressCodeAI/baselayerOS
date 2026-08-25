use crate::registry::product::*;

pub fn onboarding_pack() -> ProductSpec {
    ProductSpec {
        slug: "onboarding_pack".into(),
        name: "Enterprise Onboarding & Automation Pack".into(),
        description: "Deterministic employee onboarding, identity verification, access provisioning, compliance training, and offboarding workflows.".into(),
        pricing: PricingModel { annual_price_cad: 75_000 },
        modules: vec![

            ModuleSpec {
                slug: "intake_identity".into(),
                name: "Intake & Identity".into(),
                description: "Collect employee data, verify identity, and establish deterministic onboarding baselines.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "employee_intake".into(),
                        name: "Employee Intake".into(),
                        description: "Collect employee data, role, department, and onboarding requirements.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "intake_operator".into(),
                                config: serde_json::json!({ "mode": "employee_intake" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "identity_verification".into(),
                        name: "Identity Verification".into(),
                        description: "Verify identity documents and validate employee identity deterministically.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "validation_operator".into(),
                                config: serde_json::json!({ "mode": "identity_verification" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "role_assignment".into(),
                        name: "Role Assignment".into(),
                        description: "Assign roles and responsibilities deterministically based on intake data.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "hr_operator".into(),
                                config: serde_json::json!({ "mode": "role_assignment" }),
                            },
                        ],
                    },
                ],
            },

            ModuleSpec {
                slug: "access_provisioning".into(),
                name: "Access Provisioning".into(),
                description: "Provision accounts, access rights, and system permissions deterministically.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "account_creation".into(),
                        name: "Account Creation".into(),
                        description: "Create accounts across identity providers and enterprise systems.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "provision_operator".into(),
                                config: serde_json::json!({ "mode": "account_creation" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "access_rights_assignment".into(),
                        name: "Access Rights Assignment".into(),
                        description: "Assign access rights based on role, department, and compliance requirements.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "governance_operator".into(),
                                config: serde_json::json!({ "mode": "access_rights" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "system_provisioning".into(),
                        name: "System Provisioning".into(),
                        description: "Provision access to enterprise systems deterministically with audit anchors.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "enforcement_operator".into(),
                                config: serde_json::json!({ "mode": "system_provisioning" }),
                            },
                        ],
                    },
                ],
            },

            ModuleSpec {
                slug: "compliance_training".into(),
                name: "Compliance & Training".into(),
                description: "Deliver compliance training, track completion, and enforce policy acknowledgements.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "policy_acknowledgement".into(),
                        name: "Policy Acknowledgement".into(),
                        description: "Require employees to acknowledge policies deterministically.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "policy_operator".into(),
                                config: serde_json::json!({ "mode": "acknowledgement" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "training_assignment".into(),
                        name: "Training Assignment".into(),
                        description: "Assign compliance training modules based on role and jurisdiction.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "training_operator".into(),
                                config: serde_json::json!({ "mode": "assign_training" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "training_completion_validation".into(),
                        name: "Training Completion Validation".into(),
                        description: "Validate training completion deterministically and enforce follow‑ups.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "validation_operator".into(),
                                config: serde_json::json!({ "mode": "training_completion" }),
                            },
                        ],
                    },
                ],
            },

            ModuleSpec {
                slug: "offboarding".into(),
                name: "Offboarding & Access Revocation".into(),
                description: "Revoke access, collect assets, and generate deterministic exit audits.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "access_revocation".into(),
                        name: "Access Revocation".into(),
                        description: "Revoke all access rights deterministically with audit anchors.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "enforcement_operator".into(),
                                config: serde_json::json!({ "mode": "access_revocation" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "asset_collection".into(),
                        name: "Asset Collection".into(),
                        description: "Collect physical and digital assets deterministically during offboarding.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "hr_operator".into(),
                                config: serde_json::json!({ "mode": "asset_collection" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "exit_audit".into(),
                        name: "Exit Audit".into(),
                        description: "Generate deterministic exit audit reports for compliance and governance.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "audit_operator".into(),
                                config: serde_json::json!({ "mode": "exit_audit" }),
                            },
                        ],
                    },
                ],
            },
        ],
    }
}
