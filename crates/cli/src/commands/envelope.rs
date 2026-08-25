use clap::{Parser, Subcommand};
use anyhow::Result;
use crate::helpers::{io, validation};

#[derive(Parser)]
pub struct EnvelopeCmd {
    #[command(subcommand)]
    action: EnvelopeAction,
}

#[derive(Subcommand)]
pub enum EnvelopeAction {
    Create {
        #[arg(short, long)]
        spec: String,
    },
    Validate {
        #[arg(short, long)]
        file: String,
    },
    Trace {
        #[arg(short, long)]
        file: String,
    },
}

impl EnvelopeCmd {
    pub fn execute(&self) -> Result<()> {
        match &self.action {
            EnvelopeAction::Create { spec } => {
                let envelope = io::load_json(spec)?;
                validation::validate_envelope(&envelope)?;
                println!("Deterministic envelope created.");
            }
            EnvelopeAction::Validate { file } => {
                let envelope = io::load_json(file)?;
                validation::validate_envelope(&envelope)?;
                println!("Envelope is valid and invariant‑safe.");
            }
            EnvelopeAction::Trace { file } => {
                let envelope = io::load_json(file)?;
                let trace = crate::helpers::trace::generate_trace(&envelope)?;
                println!("{}", trace);
            }
        }
        Ok(())
    }
}
