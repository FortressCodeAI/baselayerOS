use clap::{Parser, Subcommand};
use baselayeros::substrate::Substrate;

#[derive(Parser)]
#[command(name = "kali")]
#[command(about = "Kali CLI for BaselayerOS + MayIAI")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Validate {
        #[arg(value_enum)]
        target: ValidateTarget,
        path: String,
    },
    Score {
        #[arg(value_enum)]
        target: ScoreTarget,
        path: String,
    },
    Summary {
        #[arg(short, long)]
        project: Option<String>,
    },
    // add: Audit, Evidence, Market, etc.
}

#[derive(clap::ValueEnum, Clone)]
enum ValidateTarget {
    Envelope,
    Pack,
    Rulebook,
    Architecture,
    Module,
}

#[derive(clap::ValueEnum, Clone)]
enum ScoreTarget {
    Architecture,
    Project,
}

fn main() {
    let cli = Cli::parse();
    let mut substrate = Substrate::new(); // or load from config/state

    match cli.command {
        Commands::Validate { target, path } => {
            match target {
                ValidateTarget::Envelope => validate_envelope(&mut substrate, &path),
                ValidateTarget::Pack => validate_pack(&mut substrate, &path),
                ValidateTarget::Rulebook => validate_rulebook(&mut substrate, &path),
                ValidateTarget::Architecture => validate_architecture(&mut substrate, &path),
                ValidateTarget::Module => validate_module(&mut substrate, &path),
            }
        }
        Commands::Score { target, path } => {
            match target {
                ScoreTarget::Architecture => score_architecture(&mut substrate, &path),
                ScoreTarget::Project => score_project(&mut substrate, &path),
            }
        }
        Commands::Summary { project } => {
            summary(&mut substrate, project.as_deref());
        }
    }
}

fn validate_envelope(substrate: &mut Substrate, path: &str) {
    let data = std::fs::read_to_string(path).expect("read envelope");
    let env: baselayeros::envelopes::Envelope =
        serde_yaml::from_str(&data).expect("parse envelope");
    let result = substrate.validate_envelope(&env);
    println!("{:#?}", result);
}

fn validate_pack(substrate: &mut Substrate, path: &str) {
    let data = std::fs::read_to_string(path).expect("read pack");
    let pack: baselayeros::governance::CompliancePack =
        serde_yaml::from_str(&data).expect("parse pack");
    let result = substrate.validate_pack(&pack);
    println!("{:#?}", result);
}

fn validate_rulebook(substrate: &mut Substrate, path: &str) {
    let data = std::fs::read_to_string(path).expect("read rulebook");
    let rb: baselayeros::governance::Rulebook =
        serde_yaml::from_str(&data).expect("parse rulebook");
    let result = substrate.validate_rulebook(&rb);
    println!("{:#?}", result);
}

fn validate_architecture(substrate: &mut Substrate, path: &str) {
    let result = substrate.validate_architecture(path);
    println!("{:#?}", result);
}

fn validate_module(substrate: &mut Substrate, path: &str) {
    let result = substrate.validate_module(path);
    println!("{:#?}", result);
}

fn score_architecture(substrate: &mut Substrate, path: &str) {
    let score = substrate.score_architecture(path);
    println!("Kali Architecture Level: {}", score.level);
    println!("{:#?}", score.details);
}

fn score_project(substrate: &mut Substrate, path: &str) {
    let score = substrate.score_project(path);
    println!("Kali Project Level: {}", score.level);
    println!("{:#?}", score.details);
}

fn summary(substrate: &mut Substrate, project: Option<&str>) {
    let artifact = match project {
        Some(p) => substrate.generate_project_summary(p),
        None => substrate.generate_global_summary(),
    };
    println!("Summary ID: {}", artifact.summary_id);
    println!("Period: {} → {}", artifact.period_start, artifact.period_end);
    println!("Envelopes processed: {}", artifact.envelopes_processed.len());
    println!("Modules executed: {}", artifact.modules_executed.len());
    println!("Refusals: {}", artifact.refusals.len());
    println!("Governance decisions: {}", artifact.governance_decisions.len());
    println!("Evidence bundles: {}", artifact.evidence_bundles.len());
    println!("\nFull summary:\n{:#?}", artifact);
}
