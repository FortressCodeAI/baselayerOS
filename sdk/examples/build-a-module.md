# Building a BaseLayerOS Module

This guide shows how to build a deterministic module that runs on the
BaseLayerOS substrate. Modules expose actions, define invariants, and
operate under deterministic constraints enforced by the runtime.

## 1. Module Structure

A module is a Python class that subclasses `BaseLayerModule`:

```python
from baselayer.module import BaseLayerModule

class RiskModel(BaseLayerModule):

    def invariants(self):
        return {
            "non_negative_score": "Risk score must never be negative"
        }

    def actions(self):
        return {
            "score": "Compute a deterministic risk score"
        }

    def run_action(self, action_name, payload):
        if action_name == "score":
            income = payload["income"]
            credit_score = payload["credit_score"]
            debt = payload["existing_debt"]

            # Deterministic scoring logic
            score = (credit_score / 850) * 0.6 + (income / 200000) * 0.3 - (debt / 100000) * 0.1
            score = max(score, 0)  # enforce invariant

            return {"risk_score": round(score, 4)}

        raise ValueError(f"Unknown action: {action_name}")

## 2. Determinism Requirements

Modules must not:

- Call external APIs
- use non-seeded randomness
- read system time
- mutate global state

Modules must:

- produce identical output for identical input
- rely only on the payload
- enforce invariants through explicit logic

## 3. Registering the Module

Modules are referenced by ID inside workflows:

```yaml
module_id: "finance.risk_model"
module_action: "score"

The runtime maps this ID to your module implementation.

## 4. Testing Determinism

Run the same action 100 times:

```python
m = RiskModel()
outcomes = [m.run_action("score", payload) for _ in range(100)]
assert len(set([o["risk_score"] for o in outcomes])) === 1

if this fails, the module is not deterministic.

## 5. Packaging

A module directory typically contains:

my_module/
    __init__.py
    risk_model.py
    requirements.txt
    README.md

The runtime loads modules dynamically based on configuration.

## 6. Summary

A BaseLayerOS module is:

- deterministic
- explicit
- invariant‑checked
- substrate‑compatible

This ensures it can run under the BaseLayerOS execution engine with full
replay fidelity and auditability.
