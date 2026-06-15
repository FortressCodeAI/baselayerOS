# BaseLayerOS Compiler Specification

The BaseLayerOS compiler transforms a validated UES plan into a deterministic Domain-Specific Language (DSL). This DSL is consumed by the executor and is guaranteed to be reproducible across environments.

## 1. Compiler Responsibilities

The compiler performs the following deterministic steps:

1. Validate task structure

2. Validate capability reference

3. Validate preconditions

4. Generate deterministic DSL

5. Embed postconditions

6. Produce a `CompiledArtifact`

See: [Compiler Contract](ca://s?q=Show_compiler_contract)

## 2. Deterministic DSL Format

The DSL is a simple, line-oriented language:

`PHASE <id> <name>`
`TASK <id> <capability>`
`INPUTS <json>`
`OUTPUTS <json>`
`PRE <json>`
`POST <json>`
`END_TASK`
`END_PHASE`

### Deterministic Properties

- No indentation‑dependent semantics  
- No optional fields  
- No dynamic ordering  
- No implicit behavior  

The DSL is intentionally minimal to ensure reproducibility.

## 3. Compilation Steps

### Step 1 — Validate Plan Structure

The compiler ensures:

- phases are ordered deterministically  
- tasks are ordered deterministically  
- IDs are unique  
- required fields exist  

Invalid structures raise `CompilationError`.

### Step 2 — Validate Capabilities

Each task references a capability:

`"capability": "builtin.echo"`

The compiler ensures:

- capability exists in the registry  
- capability ID is deterministic  
- capability is allowed in the current environment  

See: [Capability Registry](ca://s?q=Show_capability_registry)

### Step 3 — Validate Preconditions

Task preconditions must be:

- deterministic  
- pure boolean expressions  
- independent of external state  

Example:

```json
"preconditions": [
  {"equals": ["x", 1]}
]
```

### Step 4 — Generate DSL

The compiler emits DSL in a strict order:

- phases
- tasks
- inputs
- outputs
- preconditions
- postconditions

This ordering is never changed.

### Step 5 — Embed Postconditions

Postconditions are embedded directly into the DSL:

`POST {"equals": ["result.x", 1]}`

The executor enforces these.

## 4. CompiledArtifact

The compiler returns:

```pthon
CompiledArtifact(
    dsl="...",
    metadata={...}
)
```

The artifact is immutable and deterministic.

## 5. Failure Modes

The compiler fails‑closed on:

missing capabilities

invalid preconditions

invalid postconditions

malformed plan

nondeterministic structures

All failures raise CompilationError.

## 6. Future Extensions

Future versions may include:

static type checking

capability‑level type signatures

optimization passes

DSL versioning

All extensions must preserve determinism.
