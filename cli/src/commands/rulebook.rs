use clap::{Parser};
use anyhow::Result;
use crate::helpers::io;

#[derive(Parser)]
pub struct RulebookCmd {
    #[arg(short, long)]
    file: String,
}

impl RulebookCmd {
    pub fn execute(&self) -> Result<()> {
        let rulebook = io::load_json(&self.file)?;
        println!("{}", serde_json::to_string_pretty(&rulebook)?);
        Ok(())
    }
}
