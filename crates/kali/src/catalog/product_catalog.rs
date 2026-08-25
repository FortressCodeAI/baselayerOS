use std::collections::HashMap;

use crate::registry::{
    ProductRegistry, ProductSpec, ModuleSpec, WorkflowSpec,
    ArtifactSpec, DeliverySpec,
};

pub fn build_product_catalog() -> ProductRegistry {

    let mut modules = HashMap::new();

    macro_rules! module {
        ($id:expr, $desc:expr, $path:expr) => {{
            modules.insert($id.to_string(), ModuleSpec {
                id: $id.to_string(),
                description: $desc.to_string(),
                version: "1.0.0".to_string(),
                path: $path.to_string(),
            });
        }};
    }

    module!("governance_engine", "Deterministic governance engine", "modules/governance_engine.wasm");
    module!("invariant_engine", "Execution invariant engine", "modules/invariant_engine.wasm");
    module!("constraint_engine", "Constraint evaluation engine", "modules/constraint_engine.wasm");
    module!("routing_seal_engine", "Routing seal generator", "modules/routing_seal_engine.wasm");

    module!("state_reducer", "Deterministic WASM state reducer", "modules/state_reducer.wasm");
    module!("audit_writer", "Audit chain writer", "modules/audit_writer.wasm");
    module!("artifact_generator", "Artifact generation module", "modules/artifact_generator.wasm");
    module!("domain_logic_core", "Core domain logic module", "modules/domain_logic_core.wasm");

    module!("workflow_engine", "Deterministic workflow engine", "modules/workflow_engine.wasm");

    module!("identity_engine", "Tenant identity engine", "modules/identity_engine.wasm");
    module!("role_engine", "Role enforcement engine", "modules/role_engine.wasm");

    module!("sales_engine", "Deterministic sales automation engine", "modules/sales_engine.wasm");
    module!("lead_scoring_engine", "Deterministic lead scoring engine", "modules/lead_scoring_engine.wasm");

    module!("marketing_engine", "Deterministic marketing automation engine", "modules/marketing_engine.wasm");
    module!("content_generator", "Deterministic content generation engine", "modules/content_generator.wasm");
    module!("analytics_engine", "Marketing analytics engine", "modules/analytics_engine.wasm");

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

    workflow!("execution_trace", "Generate execution trace", [
        "load_state", "compute_trace", "export_trace"
    ]);

    workflow!("audit_chain_update", "Update audit chain", [
        "load_anchor", "append_transition", "write_anchor"
    ]);

    workflow!("sales_pipeline", "Deterministic sales pipeline workflow", [
        "generate_leads", "qualify_leads", "score_leads", "followup", "close_deal"
    ]);

    workflow!("marketing_campaign", "Marketing campaign workflow", [
        "create_campaign", "generate_content", "deploy_campaign", "analyze_performance"
    ]);

    workflow!("lead_qualification", "Lead qualification workflow", [
        "load_lead", "score_lead", "assign_stage"
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

    workflow!("tenant_onboarding", "Onboard a new tenant", [
        "validate_identity", "assign_roles", "generate_config"
    ]);

    workflow!("tenant_configuration", "Configure tenant runtime", [
        "load_config", "apply_settings", "verify_runtime"
    ]);

    workflow!("artifact_generation", "Generate artifacts", [
        "load_inputs", "generate_artifact", "export_artifact"
    ]);

    let mut artifacts = HashMap::new();

    macro_rules! artifact {
        ($id:expr, $desc:expr, $format:expr) => {{
            artifacts.insert($id.to_string(), ArtifactSpec {
                id: $id.to_string(),
                description: $desc.to_string(),
                format: $format.to_string(),
            });
        }};
    }

    artifact!("contradiction_report", "Report of detected contradictions", "json");
    artifact!("clause_map", "Mapped clause structure", "json");
    artifact!("governance_decision_pack", "Governance decision output", "json");
    artifact!("audit_chain", "Full audit chain", "json");
    artifact!("execution_trace_pack", "Execution trace output", "json");
    artifact!("tenant_config_pack", "Tenant configuration bundle", "json");
    artifact!("sales_report", "Sales performance report", "json");
    artifact!("lead_score_pack", "Lead scoring output", "json");
    artifact!("campaign_report", "Marketing campaign performance report", "json");
    artifact!("content_pack", "Generated marketing content", "json");
    artifact!("analytics_pack", "Marketing analytics output", "json");
    artifact!("workflow_report", "Workflow execution report", "json");

    let mut delivery = HashMap::new();

    macro_rules! delivery_rule {
        ($id:expr, $desc:expr, [$($target:expr),*]) => {{
            delivery.insert($id.to_string(), DeliverySpec {
                id: $id.to_string(),
                description: $desc.to_string(),
                targets: vec![$($target.to_string()),*],
            });
        }};
    }

    delivery_rule!("substrate", "Deliver to substrate runtime", ["substrate"]);
    delivery_rule!("supabase", "Deliver to Supabase storage", ["supabase"]);
    delivery_rule!("tenant_runtime", "Deliver to tenant runtime", ["tenant"]);
    delivery_rule!("partner_delivery", "Deliver to partner (Google CAGE, MayIAI)", ["partner"]);

    let mut products = HashMap::new();

    macro_rules! product {
        ($id:expr, $desc:expr, $modules:expr, $workflows:expr, $invariants:expr, $constraints:expr, $artifacts:expr, $delivery:expr) => {{
            products.insert($id.to_string(), ProductSpec {
                id: $id.to_string(),
                description: $desc.to_string(),
                version: "1.0.0".to_string(),
                modules: $modules.iter().map(|s| s.to_string()).collect(),
                workflows: $workflows.iter().map(|s| s.to_string()).collect(),
                invariants: $invariants.iter().map(|s| s.to_string()).collect(),
                constraints: $constraints.iter().map(|s| s.to_string()).collect(),
                artifacts: $artifacts.iter().map(|s| s.to_string()).collect(),
                delivery: $delivery.iter().map(|s| s.to_string()).collect(),
            });
        }};
    }

    product!(
        "governance-pack",
        "Deterministic governance engine bundle",
        ["governance_engine", "invariant_engine", "constraint_engine", "routing_seal_engine"],
        ["contradiction_checker", "clause_mapper", "grievance_intake", "arbitration_precheck"],
        ["Replayability", "DeterministicTransition", "AuditAnchorDeterminism", "EnvelopeIdentityConsistency", "NoHiddenSideEffects", "MonotonicVersioning"],
        ["RoleBasedAccess", "TenantBoundary", "ActionAuthorization"],
        ["contradiction_report", "clause_map", "governance_decision_pack"],
        ["substrate", "supabase", "tenant_runtime"]
    );

    product!(
        "execution-pack",
        "Deterministic WASM execution modules",
        ["state_reducer", "audit_writer", "artifact_generator", "domain_logic_core"],
        ["execution_trace", "audit_chain_update"],
        ["DeterministicTransition", "Replayability", "AuditAnchorDeterminism"],
        ["ModuleVersionLock", "StateShapeConsistency"],
        ["audit_chain", "execution_trace_pack"],
        ["substrate", "tenant_runtime"]
    );

    product!(
        "workflow-pack",
        "Deterministic workflow bundle",
        ["workflow_engine"],
        ["contradiction_checker", "clause_mapper", "grievance_intake", "arbitration_precheck", "sales_pipeline", "marketing_campaign", "lead_qualification"],
        ["WorkflowDeterminism", "StepOrderConsistency"],
        ["WorkflowAuthorization"],
        ["workflow_report"],
        ["tenant_runtime", "supabase"]
    );

    product!(
        "tenant-runtime-pack",
        "Tenant identity + role + routing config",
        ["identity_engine", "role_engine", "routing_seal_engine"],
        ["tenant_onboarding", "tenant_configuration"],
        ["IdentityConsistency", "RoleConsistency"],
        ["TenantBoundary", "IdentityAuthorization"],
        ["tenant_config_pack"],
        ["tenant_runtime"]
    );

    product!(
        "artifact-pack",
        "Generated artifacts for governance and execution",
        ["artifact_generator"],
        ["artifact_generation"],
        ["ArtifactDeterminism"],
        ["ArtifactFormatConsistency"],
        ["contradiction_report", "clause_map", "audit_chain", "execution_trace_pack", "governance_decision_pack"],
        ["supabase", "tenant_runtime", "partner_delivery"]
    );

    product!(
        "sales-pack",
        "Deterministic sales automation bundle",
        ["sales_engine", "lead_scoring_engine"],
        ["sales_pipeline", "lead_qualification"],
        ["LeadScoreDeterminism", "PipelineStepConsistency"],
        ["SalesAuthorization"],
        ["sales_report", "lead_score_pack"],
        ["tenant_runtime", "partner_delivery"]
    );

    product!(
        "marketing-pack",
        "Deterministic marketing automation bundle",
        ["marketing_engine", "content_generator", "analytics_engine"],
        ["campaign_creation", "campaign_deployment", "content_generation", "marketing_analytics"],
        ["CampaignDeterminism", "ContentFormatConsistency"],
        ["MarketingAuthorization"],
        ["campaign_report", "content_pack", "analytics_pack"],
        ["tenant_runtime", "partner_delivery", "supabase"]
    );

    ProductRegistry {
        products,
        modules,
        workflows,
        artifacts,
        delivery,
    }
}
