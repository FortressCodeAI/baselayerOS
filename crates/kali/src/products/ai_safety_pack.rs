use crate::registry::product::*;

pub fn ai_safety_pack() -> ProductSpec {
    ProductSpec {
        slug: "ai_safety_pack".into(),
        name: "AI Safety & Determinism Pack".into(),
        description: "Deterministic AI safety envelopes, behavior proofs, red-team testing, and incident response.".into(),
        pricing: PricingModel { annual_price_cad: 450_000 },
        modules: vec![
            ModuleSpec {
                slug: "safety_envelopes".into(),
                name: "Safety Envelope Management".into(),
                description: "Register, validate, and enforce deterministic AI safety envelopes.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "envelope_registration".into(),
                        name: "Envelope Registration".into(),
                        description: "Register deterministic safety envelopes defining allowed inputs, outputs, and transformations.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "safety_operator".into(),
                                config: serde_json::json!({ "action": "register" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "envelope_validation".into(),
                        name: "Envelope Validation".into(),
                        description: "Validate safety envelopes against constraints, forbidden behaviors, and escalation rules.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "constraint_operator".into(),
                                config: serde_json::json!({ "mode": "validate_envelope" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "envelope_enforcement".into(),
                        name: "Envelope Enforcement".into(),
                        description: "Enforce safety envelopes deterministically during AI execution.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "enforcement_operator".into(),
                                config: serde_json::json!({ "mode": "enforce_safety" }),
                            },
                        ],
                    },
                ],
            },

            ModuleSpec {
                slug: "determinism_enforcement".into(),
                name: "Determinism Enforcement".into(),
                description: "Replay AI actions, hash transitions, and verify invariants.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "determinism_replay".into(),
                        name: "Determinism Replay".into(),
                        description: "Replay AI actions deterministically to verify identical outcomes.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "determinism_operator".into(),
                                config: serde_json::json!({ "mode": "replay" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "transition_hashing".into(),
                        name: "Transition Hashing".into(),
                        description: "Hash transitions to ensure deterministic state evolution and auditability.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "hash_operator".into(),
                                config: serde_json::json!({ "mode": "transition_hash" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "invariant_verification".into(),
                        name: "Invariant Verification".into(),
                        description: "Verify deterministic invariants across AI actions and safety envelopes.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "invariant_operator".into(),
                                config: serde_json::json!({ "mode": "ai_safety_invariants" }),
                            },
                        ],
                    },
                ],
            },

            ModuleSpec {
                slug: "redteam_testing".into(),
                name: "Red-Team & Safety Testing".into(),
                description: "Probe unsafe outputs, jailbreak attempts, and safety regressions.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "jailbreak_detection".into(),
                        name: "Jailbreak Detection".into(),
                        description: "Detect jailbreak attempts and unsafe prompt patterns.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "redteam_operator".into(),
                                config: serde_json::json!({ "mode": "jailbreak_probe" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "unsafe_output_simulation".into(),
                        name: "Unsafe Output Simulation".into(),
                        description: "Simulate unsafe outputs to test envelope boundaries and refusal behavior.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "simulation_operator".into(),
                                config: serde_json::json!({ "mode": "unsafe_simulation" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "safety_regression_testing".into(),
                        name: "Safety Regression Testing".into(),
                        description: "Run deterministic regression tests to ensure safety envelopes remain effective.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "regression_operator".into(),
                                config: serde_json::json!({ "mode": "safety_regression" }),
                            },
                        ],
                    },
                ],
            },

            ModuleSpec {
                slug: "incident_response".into(),
                name: "Incident Response & Reporting".into(),
                description: "Detect unsafe events, escalate incidents, and generate deterministic reports.".into(),
                workflows: vec![

                    WorkflowSpec {
                        slug: "safety_incident_detection".into(),
                        name: "Safety Incident Detection".into(),
                        description: "Detect unsafe AI events and violations of safety envelopes.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "incident_operator".into(),
                                config: serde_json::json!({ "mode": "detect" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "incident_escalation".into(),
                        name: "Incident Escalation".into(),
                        description: "Escalate safety incidents deterministically with predefined workflows.".into(),
                        operators: vec![
                            OperatorBinding {
                                operator_slug: "escalation_operator".into(),
                                config: serde_json::json!({ "mode": "escalate" }),
                            },
                        ],
                    },

                    WorkflowSpec {
                        slug: "safety_report_generation".into(),
                        name: "Safety Report Generation".into(),
                        description: "Generate deterministic safety reports for regulators, auditors, and internal teams.".into(),
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
