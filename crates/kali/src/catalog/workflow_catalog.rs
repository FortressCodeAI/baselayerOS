use std::collections::HashMap;
use crate::registry::WorkflowSpec;

pub fn build_workflow_catalog() -> HashMap<String, WorkflowSpec> {
    let mut workflows = HashMap::new();

    macro_rules! workflow {
        ($id:expr, $desc:expr, [$($step:expr),*]) => {{
            workflows.insert($id.to_string(), WorkflowSpec {
                id: $id.to_string(),
                description: $desc.to_string(),
                version: "1.0.0".to_string(),
                steps: vec![$($step.to_string()),*],
            });
        }};
    }

    // Governance
    workflow!("contradiction_checker", "Detect contradictions in governance input", [
        "load_input", "map_clauses", "detect_conflicts", "generate_report"
    ]);

    workflow!("clause_mapper", "Map clauses into structured governance form", [
        "parse_clauses", "normalize", "index", "export"
    ]);

    workflow!("grievance_intake", "Intake workflow for grievances", [
        "validate_identity", "validate_payload", "route_to_governance"
    ]);

    workflow!("arbitration_precheck", "Pre-check workflow for arbitration", [
        "load_case", "validate_roles", "check_constraints", "prepare_artifacts"
    ]);

    // Execution
    workflow!("execution_trace", "Generate execution trace", [
        "load_state", "compute_trace", "export_trace"
    ]);

    workflow!("audit_chain_update", "Update audit chain", [
        "load_anchor", "append_transition", "write_anchor"
    ]);

    // Sales
    workflow!("sales_pipeline", "Deterministic sales pipeline workflow", [
        "generate_leads", "qualify_leads", "score_leads", "followup", "close_deal"
    ]);

    workflow!("lead_qualification", "Lead qualification workflow", [
        "load_lead", "score_lead", "assign_stage"
    ]);

    // Marketing
    workflow!("marketing_campaign", "Marketing campaign workflow", [
        "create_campaign", "generate_content", "deploy_campaign", "analyze_performance"
    ]);

    workflow!("campaign_creation", "Create marketing campaign", [
        "define_goal", "define_audience", "define_channels"
    ]);

    workflow!("campaign_deployment", "Deploy marketing campaign", [
        "schedule_posts", "publish_content", "monitor_engagement"
    ]);

    workflow!("content_generation", "Generate deterministic marketing content", [
        "load_template", "generate_copy", "format_output"
    ]);

    workflow!("marketing_analytics", "Analyze marketing performance", [
        "load_metrics", "compute_kpis", "generate_report"
    ]);

    // Tenant-specific
    workflow!("tenant_onboarding", "Onboard a new tenant", [
        "validate_identity", "assign_roles", "generate_config"
    ]);

    workflow!("tenant_configuration", "Configure tenant runtime", [
        "load_config", "apply_settings", "verify_runtime"
    ]);

    // Artifact
    workflow!("artifact_generation", "Generate artifacts", [
        "load_inputs", "generate_artifact", "export_artifact"
    ]);

    workflows
}
