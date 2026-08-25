pub trait KernelInvariantSource {
    fn invariants_for_product(&self, product_id: &str) -> Vec<String>;
}

pub trait KernelConstraintSource {
    fn validate_product(
        &self,
        product_id: &str,
        tenant: &str,
    ) -> Result<(), Vec<String>>;
}

pub struct KernelRulebook;

impl KernelInvariantSource for KernelRulebook {
    fn invariants_for_product(&self, product_id: &str) -> Vec<String> {
        vec![]
    }
}

impl KernelConstraintSource for KernelRulebook {
    fn validate_product(
        &self,
        _product_id: &str,
        _tenant: &str,
    ) -> Result<(), Vec<String>> {
        Ok(())
    }
}
