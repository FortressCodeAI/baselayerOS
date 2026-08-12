use clap::{Parser, Subcommand};

mod commands;
mod helpers;

#[derive(Parser)]
#[command(name = "baselayeros")]
#[command(about = "Deterministic governance CLI for BaseLayerOS substrate execution.")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Envelopes(commands::envelopes::EnvelopeCmd),
    Replay(commands::replay::ReplayCmd),
    Governance(commands::governance::GovernanceCmd),
    Policies(commands::policies::PolicyCmd),
    Rulebook(commands::rulebook::RulebookCmd),
    Sea(commands::sea::SeaCmd),
    Modules(commands::modules::ModuleCmd),
}

fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Envelopes(cmd) => cmd.execute()?,
        Commands::Replay(cmd) => cmd.execute()?,
        Commands::Governance(cmd) => cmd.execute()?,
        Commands::Policies(cmd) => cmd.execute()?,
        Commands::Rulebook(cmd) => cmd.execute()?,
        Commands::Sea(cmd) => cmd.execute()?,
        Commands::Modules(cmd) => cmd.execute()?,
    }

    Ok(())
}
