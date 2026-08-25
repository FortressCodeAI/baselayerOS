#[derive(Debug, Clone)]
pub struct ActorIdentity {
    pub actor_id: String,
    pub tenant_id: String,
    pub roles: Vec<String>,
}

impl ActorIdentity {
    pub fn new(
        actor_id: impl Into<String>,
        tenant_id: impl Into<String>,
        roles: Vec<String>,
    ) -> Self {
        Self {
            actor_id: actor_id.into(),
            tenant_id: tenant_id.into(),
            roles,
        }
    }
}
