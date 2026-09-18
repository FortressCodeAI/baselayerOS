use crate::audit_chain::{AuditChainBackend, AuditChainError, AuditEntry};
use serde_json::to_string;
use std::fs::{File, OpenOptions};
use std::io::{BufRead, BufReader, Write};
use std::path::PathBuf;


pub struct LocalAuditChain {
    path: PathBuf,
}

impl LocalAuditChain {
    pub fn new(path: impl Into<PathBuf>) -> Result<Self, AuditChainError> {
        let path = path.into();

        if !path.exists() {
            File::create(&path)
                .map_err(|e| AuditChainError::LoadError(e.to_string()))?;
        }

        Ok(Self { path })
    }

    fn count_entries(&self) -> Result<u64, AuditChainError> {
        let file = File::open(&self.path)
            .map_err(|e| AuditChainError::LoadError(e.to_string()))?;

        let reader = BufReader::new(file);
        let mut count = 0u64;

        for line in reader.lines() {
            if line.is_ok() {
                count += 1;
            }
        }

        Ok(count)
    }
}

impl AuditChainBackend for LocalAuditChain {
    fn append_entry(&mut self, entry: AuditEntry) -> Result<(), AuditChainError> {
        let serialized = to_string(&entry)
            .map_err(|e| AuditChainError::AppendError(e.to_string()))?;

        let mut file = OpenOptions::new()
            .append(true)
            .open(&self.path)
            .map_err(|e| AuditChainError::AppendError(e.to_string()))?;

        writeln!(file, "{}", serialized)
            .map_err(|e| AuditChainError::AppendError(e.to_string()))?;

        Ok(())
    }

    fn current_sequence(&self) -> Result<u64, AuditChainError> {
        self.count_entries()
    }

    fn seal_chain(&mut self) -> Result<(), AuditChainError> {
        let file = File::open(&self.path)
            .map_err(|e| AuditChainError::SealError(e.to_string()))?;

        let mut reader = BufReader::new(file);
        let mut hasher = sha2::Sha256::new();
        let mut buf = Vec::new();

        while reader.read_until(b'\n', &mut buf)
            .map_err(|e| AuditChainError::SealError(e.to_string()))? > 0
        {
            hasher.update(&buf);
            buf.clear();
        }

        let digest = hex::encode(hasher.finalize());

        let mut seal_path = self.path.clone();
        seal_path.set_extension("seal");

        let mut seal_file = File::create(&seal_path)
            .map_err(|e| AuditChainError::SealError(e.to_string()))?;

        writeln!(seal_file, "{}", digest)
            .map_err(|e| AuditChainError::SealError(e.to_string()))?;

        Ok(())
    }
}
