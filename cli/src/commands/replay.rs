use clap::{Parser};
use anyhow::Result;
use crate::helpers::{io, trace};

#[derive(Parser)]
pub struct ReplayCmd {
    #[arg(short, long)]
    envelope: String,
}

impl ReplayCmd {
    pub fn execute(&self) -> Result<()> {
        let envelope = io::load_json(&self.envelope)?;
        let replay = trace::replay_envelope(&envelope)?;
        println!("{}", replay);
        Ok(())
    }
}
