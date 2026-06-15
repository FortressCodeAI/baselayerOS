# Integrating Regulus with BaseLayerOS

Regulus is a standalone application that connects to BaseLayerOS to provide
deterministic, auditable AI assistance for enterprise workflows.  
This document explains how Regulus invokes BaseLayerOS and how the two systems
exchange data.

## 1. Architecture Overview

Regulus acts as the **front‑end intelligence layer**, while BaseLayerOS is the
**deterministic execution substrate**.

`User → Regulus → BaseLayerOS → Deterministic Output → Regulus UI`

Regulus handles:

- user interaction  
- workflow context  
- natural‑language interpretation  
- proposal generation  

BaseLayerOS handles:

- deterministic validation  
- deterministic compilation  
- deterministic execution  
- audit chain generation  

See: [Architecture](ca://s?q=Show_architecture)

## 2. Communication Model

Regulus communicates with BaseLayerOS through the `BaseLayerService` API:

```python
from baselayeros.app.service import BaseLayerService

service = BaseLayerService()

result = service.run(
    proposal=ues_dict,
    actor="regulus",
    actor_org="enterprise",
    actor_roles=["assistant"]
)
```

The output is a deterministic JSON object.

See: Service API

## 3. Regulus → UES Proposal Generation

Regulus generates UES proposals from:

- user intent
- workflow context
- enterprise rules
- historical patterns

A typical Regulus‑generated UES includes:

- intent name
- audit metadata
- deterministic plan
- capability references
- pre/postconditions

See: UES Format

## 4. BaseLayerOS Execution

Once Regulus submits a proposal:

-Councils validate
-State transitions to REVIEWED
-Compiler generates DSL
-State transitions to COMPILED
-Executor runs DSL
-State transitions to EXECUTED
-Audit chain is updated

See: Pipeline

## 5. Regulus Rendering

Regulus receives:

```json
{
  "proposal_id": "...",
  "state": "EXECUTED",
  "result": {...},
  "success": true
}
```

Regulus then:

- displays results
- explains reasoning
- shows audit trail
- allows user approval or rejection

## 6. Error Handling

If BaseLayerOS fails:

- Regulus receives a deterministic error
- Regulus displays a structured explanation
- Regulus may regenerate or refine the proposal

Example error:

```json
{
  "success": false,
  "error": "Postcondition failed: equals(result.x, 2)"
}
```

## 7. Security & Isolation

Regulus and BaseLayerOS communicate through:

- isolated process boundaries
- deterministic payloads
- no shared mutable state

This ensures enterprise‑grade safety.

## 8. Future Extensions

- Regulus‑generated optimization passes
- Regulus‑side capability previews
- Regulus‑side audit visualization
