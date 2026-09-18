use substrate::envelope::Envelope;
use crate::evaluation::AaifEvaluation;


pub struct AaifAuthority;

impl AaifAuthority {
    pub fn new() -> Self {
        Self
    }

    pub fn evaluate(&self, envelope: &Envelope) -> AaifEvaluation {
        if envelope.payload.is_null() {
            return AaifEvaluation::fail("empty payload");
        }

        if !envelope.tags.contains_key("provider") {
            return AaifEvaluation::fail("missing provider tag");
        }

        AaifEvaluation::pass()
    }
}
