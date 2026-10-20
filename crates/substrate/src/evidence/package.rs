use std::fs::{self, File};
use std::io::Write;
use serde::Serialize;

use crate::envelopes::execution_envelope::ExecutionEnvelope;
use crate::state_machine::snapshot::StateSnapshot;
use crate::execution::workflow::WorkflowResult;
use crate::audit::event::AuditEvent;
use crate::errors::substrate_error::SubstrateError;

#[derive(Debug, Serialize)]
pub struct EvidenceManifest {
    pub envelope_id: String,
    pub events_count: usize,
    pub decision_match: bool,
    pub snapshot_hash_match: bool,
    pub files: Vec<String>,
}

pub fn generate_evidence_package(
    output_dir: &str,
    package_name: &str,
    envelope: &ExecutionEnvelope,
    snapshot_before: &StateSnapshot,
    snapshot_after: &StateSnapshot,
    events: &[AuditEvent],
    workflow: &WorkflowResult,
    chain_seal: &str,
) -> Result<String, SubstrateError> {

    fs::create_dir_all(output_dir)?;

    let package_dir = format!("{}/{}", output_dir, package_name);
    fs::create_dir_all(&package_dir)?;

    let mut files = Vec::new();

    fn write_json<T: Serialize + ?Sized>(
    dir: &str,
    name: &str,
    value: &T,
    files: &mut Vec<String>,
) -> Result<(), SubstrateError> {
    let path = format!("{}/{}", dir, name);
    let mut f = File::create(&path)?;
    let data = serde_json::to_vec_pretty(value)?;
    f.write_all(&data)?;
    files.push(name.to_string());
    Ok(())
}


    fn write_text(
        dir: &str,
        name: &str,
        value: &str,
        files: &mut Vec<String>,
    ) -> Result<(), SubstrateError> {
        let path = format!("{}/{}", dir, name);
        let mut f = File::create(&path)?;
        f.write_all(value.as_bytes())?;
        files.push(name.to_string());
        Ok(())
    }

    write_json(&package_dir, "envelope.json", envelope, &mut files)?;
    write_json(&package_dir, "snapshot_before.json", snapshot_before, &mut files)?;
    write_json(&package_dir, "snapshot_after.json", snapshot_after, &mut files)?;
    write_json(&package_dir, "audit_events.json", events, &mut files)?;
    write_json(&package_dir, "replay_result.json", &workflow.replay, &mut files)?;
    write_text(&package_dir, "governance_decision.txt", &workflow.replay.replay_decision, &mut files)?;
    write_text(&package_dir, "chain_seal.txt", chain_seal, &mut files)?;

    let verify_script = "#!/usr/bin/env bash\n\necho \"Verify evidence package\"\n";
    write_text(&package_dir, "verification_script.sh", verify_script, &mut files)?;

    let manifest = EvidenceManifest {
        envelope_id: workflow.envelope_id.clone(),
        events_count: workflow.replay.events_count,
        decision_match: workflow.replay.decision_match,
        snapshot_hash_match: workflow.replay.snapshot_hash_match,
        files,
    };

    write_json(&package_dir, "manifest.json", &manifest, &mut Vec::new())?;

    Ok(package_dir)
}
