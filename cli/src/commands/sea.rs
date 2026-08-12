use clap::{Parser, Subcommand};
use anyhow::Result;
use crate::helpers::{io, trace};

#[derive(Parser)]
pub struct SeaCmd {
    #[command(subcommand)]
    action: SeaAction,
}

#[derive(Subcommand)]
pub enum SeaAction {
    Generate {
        #[arg(short, long)]
        envelope: String,
    },
    Inspect {
        #[arg(short, long)]
        file: String,
    }
}

impl SeaCmd {
    pub fn execute(&self) -> Result<()> {
        match &self.action {
            SeaAction::Generate { envelope } => {
                let env = io::load_json(envelope)?;
                let artifact = trace::generate_sea(&env)?;
                println!("{}", serde_json::to_string_pretty(&artifact)?);
            }
            SeaAction::Inspect { file } => {
                let artifact = io::load_json(file)?;
                println!("{}", serde_json::to_string_pretty(&artifact)?);
            }
        }
        Ok(())
    }
}
