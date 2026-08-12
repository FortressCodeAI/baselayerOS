use clap::{Parser};
use anyhow::Result;
use crate::helpers::{io, validation};

#[derive(Parser)]
pub struct ModuleCmd {
    #[arg(short, long)]
    file: String,
}

impl ModuleCmd {
    pub fn execute(&self) -> Result<()> {
        let module = io::load_json(&self.file)?;
        validation::validate_module(&module)?;
        println!("Module spec is deterministic and invariant‑safe.");
        Ok(())
    }
}
