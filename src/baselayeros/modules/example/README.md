# Example Module — Deterministic Credit Risk Evaluation

This module provides a **fully deterministic**, **auditable**, and **compliance‑aligned**
credit risk evaluation action.

It demonstrates how BaseLayerOS governs AI decisions using transparent rules that
produce the **same output for the same input**, every time.

## Action

`credit_risk.evaluate`

### Inputs

- `income` — annual income (number)
- `credit_score` — FICO‑style score (number)
- `existing_debt` — total outstanding debt (number)

### Output

One of:

- `APPROVED`
- `REVIEW`
- `DECLINED`

With a human‑readable reason.

## Run Your First Governed Action

From the root of the BaseLayerOS repo:

### 1. Start the substrate server

`uvicorn substrate.api:app --reload`

### 2. Send a governed action

`curl -X POST http://localhost:8000/execute \`
`-H "X-Substrate-Identity: {\"subject\":\"demo-user\",\"roles\":[\"analyst\"]}" \`
`-H "X-Substrate-Signature: <signature>" \`
`-H "Content-Type: application/json" \`
`-d '{"action":"credit_risk.evaluate","payload":{"income":90000,"credit_score":720,"existing_debt":15000}}'`

### 3. Fetch the audit record

`curl http://localhost:8000/audit/<AUDIT_ID_FROM_STEP_2>`

You now have:

- a deterministic decision  
- a cryptographically signed audit envelope  
- a replayable execution trace  
- a governed AI action that satisfies Article 14 human oversight requirements  

This is the simplest possible end‑to‑end demonstration of BaseLayerOS.
