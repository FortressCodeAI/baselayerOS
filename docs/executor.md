# BaseLayerOS Executor Specification

The executor interprets the deterministic DSL produced by the compiler and
invokes capabilities in strict order. It enforces postconditions and produces
deterministic outputs.

## 1. Executor Responsibilities

The executor performs:

1. DSL parsing
2. Capability lookup
3. Capability invocation
4. Output collection
5. Postcondition enforcement
6. Deterministic result assembly

See: [Executor Runtime](ca://s?q=Show_executor_runtime)

## 2. DSL Parsing

The executor reads the DSL line‑by‑line.

Example:

`PHASE phase1 Test Phase`
`TASK task1 builtin.echo`
`INPUTS {"x": 1}`
`OUTPUTS{}`
`PRE []`
`POST []`
`END_TASK`
`END_PHASE`

Parsing is:

- deterministic  
- whitespace‑insensitive  
- order‑preserving  

## 3. Capability Invocation

For each task:

1. Lookup capability by ID  
2. Call `run(inputs)`  
3. Capture deterministic output  
4. Store output under task ID  

Example:

```python
result["task1"] = capability.run({"x": 1})
```

See: Capabilities

## 4. Postcondition Enforcement

Postconditions are evaluated after capability execution.

Example:

```json
"postconditions": [
  {"equals": ["result.x", 1]}
]
```

If a postcondition fails:

- execution stops
- audit event is emitted
- ExecutionError is raised

## 5. Deterministic Output Structure

The executor returns:

{
  "task1": {"x": 1},
  "task2": {...}
}

Ordering is deterministic:

- tasks appear in the order defined in the UES plan
- no additional fields are added
- no nondeterministic metadata is included

## 6. Failure Modes

The executor fails‑closed on:

- unknown capability
- malformed DSL
- failed postconditions
- capability exceptions
- nondeterministic behavior

All failures raise ExecutionError.

## 7. Deterministic Guarantees

The executor guarantees:

- identical DSL → identical outputs
- no external side effects
- no randomness
- no time‑dependent logic
- no nondeterministic ordering

This is essential for enterprise reproducibility.

## 8. Future Extensions

Future versions may include:

- capability sandboxing
- resource limits
- distributed execution
- capability provenance tracking

All extensions must preserve deterministic semantics.
