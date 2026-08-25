pub trait KernelInvariantSource {
    fn invariants_for_action(&self, action_slug: &str) -> Vec<String>;
}

pub fn select_invariants(
    kernel: &dyn KernelInvariantSource,
    action_slug: &str,
) -> Vec<String> {
    kernel.invariants_for_action(action_slug)
}
