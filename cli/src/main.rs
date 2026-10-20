mod commands;

use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "baselayeros")]
#[command(about = "BaseLayerOS deterministic substrate CLI")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Execute a deterministic envelope
    Execute {
        envelope: String,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Execute { envelope } => {
            commands::execute::run(envelope);
        }
    }
}
