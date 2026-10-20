use crate::errors::substrate_error::SubstrateError;

pub fn generate_chain_seal(path: &str) -> Result<String, SubstrateError> {
    let content = std::fs::read_to_string(path)?;
    let hash = format!("{:x}", md5::compute(content));
    Ok(hash)
}

pub fn verify_chain_seal(path: &str, seal: &str) -> Result<bool, SubstrateError> {
    let new_seal = generate_chain_seal(path)?;
    Ok(new_seal == seal)
}
