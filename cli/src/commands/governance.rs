use clap::{Parser, Subcommand};
use anyhow::Result;
use crate::helpers::{io, validation};

#[derive(Parser)]
pub struct GovernanceCmd {
    #[command(subcommand)]
    action: GovernanceAction,
}

#[derive(Subcommand)]
pub enum GovernanceAction {
    Validate {
        #[arg(short, long)]
        file: String,
    },
    Inspect {
        #[arg(short, long)]
        file: String,
    },
}

impl GovernanceCmd {
    pub fn execute(&self) -> Result<()> {
        match &self.action {
            GovernanceAction::Validate { file } => {
                let env = io::load_json(file)?;
                validation::validate_governance(&env)?;
                println!("Governance envelope is valid.");
            }
            GovernanceAction::Inspect { file } => {
                let env = io::load_json(file)?;
                println!("{}", serde_json::to_string_pretty(&env)?);
            }
        }
        Ok(())
    }
}
