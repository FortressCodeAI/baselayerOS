use substrate::envelope::Envelope;
use crate::evaluation::OscalEvaluation;

pub struct OscalControls;

impl OscalControls {
    pub fn new() -> Self {
        Self
    }

    pub fn check(&self, envelope: &Envelope) -> OscalEvaluation {
        if envelope.tags.contains_key("provider") {
            OscalEvaluation::pass()
        } else {
            OscalEvaluation::fail("OSCAL control: provider tag missing")
        }
    }
}
