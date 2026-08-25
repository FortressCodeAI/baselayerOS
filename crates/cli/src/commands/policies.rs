use clap::{Parser, Subcommand};
use anyhow::Result;
use crate::helpers::{io, validation};

#[derive(Parser)]
pub struct PolicyCmd {
    #[command(subcommand)]
    action: PolicyAction,
}

#[derive(Subcommand)]
pub enum PolicyAction {
    Validate {
        #[arg(short, long)]
        file: String,
    },
}

impl PolicyCmd {
    pub fn execute(&self) -> Result<()> {
        match &self.action {
            PolicyAction::Validate { file } => {
                let policy = io::load_json(file)?;
                validation::validate_policy(&policy)?;
                println!("Policy is deterministic and governance‑safe.");
            }
        }
        Ok(())
    }
}
