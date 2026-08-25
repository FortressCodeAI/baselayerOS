pub mod adjudications;
pub mod compiler;
pub mod console;
pub mod constraints;
pub mod delivery;
pub mod envelopes;
pub mod governance;
pub mod identity;
pub mod invariants;
pub mod kernel;
pub mod manifest;
pub mod marketing;
pub mod proposal;
pub mod qc;
pub mod registry;
pub mod runtime;
pub mod safety;
pub mod sales;

pub mod catalog;

pub use identity::ActorIdentity;
pub use envelopes::{ExecutionEnvelope, GovernanceEnvelope};
pub use proposal::GovernedProposal;
pub use constraints::{KernelConstraintSource, ConstraintViolation};
pub use invariants::KernelInvariantSource;
pub use governance::KaliGovernance;
pub use console::run_cli;
pub use registry::{
    ModuleSpec,
    WorkflowSpec,
    ArtifactSpec,
    DeliverySpec,
    ProductSpec,
    ProductRegistry,
};
pub use manifest::ProductManifest;
pub use kernel::{
    KernelInvariantSource,
    KernelConstraintSource,
    KernelRulebook,
};
pub use delivery::KaliDelivery;
pub use runtime::KaliRuntime;
pub use marketing::KaliMarketing;
pub use sales::KaliSales;
pub use console::{
    KaliCli,
    Commands,
};