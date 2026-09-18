pub mod model;
pub mod evaluation;
pub mod policy;

use substrate::envelope::Envelope;
use crate::evaluation::GovAiEvaluation;
use crate::policy::GovAiPolicy;


pub struct GovAiEngine {
    policy: GovAiPolicy,
}

impl GovAiEngine {
    pub fn new() -> Self {
        Self {
            policy: GovAiPolicy::new(),
        }
    }

    pub fn evaluate(&self, envelope: &Envelope) -> GovAiEvaluation {
        self.policy.apply(envelope)
    }
}
