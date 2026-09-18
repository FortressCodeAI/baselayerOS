use substrate::envelope::Envelope;
use crate::evaluation::GovAiEvaluation;


pub struct GovAiPolicy;

impl GovAiPolicy {
    pub fn new() -> Self {
        Self
    }

    pub fn apply(&self, envelope: &Envelope) -> GovAiEvaluation {
        if envelope.tags.contains_key("provider") {
            GovAiEvaluation::compliant()
        } else {
            GovAiEvaluation::non_compliant("missing provider tag")
        }
    }
}
