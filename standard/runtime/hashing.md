# Hashing Rules

This document defines the canonical hashing rules for BaseLayerOS.

All conformant runtimes must follow these rules exactly.

## 1. Purpose of Hashing

Hashing is used to:

- anchor audit events  
- anchor replay traces  
- validate integrity  
- detect tampering  
- ensure reproducibility  

## 2. Hash Function

The standard hash function is:

- **SHA‑256**

Implementations must produce identical hashes for identical inputs.

## 3. Canonical Serialization

Before hashing, objects must be serialized using:

- JSON
- UTF‑8 encoding
- sorted keys
- no insignificant whitespace
- no trailing commas
- no comments

This ensures cross‑language reproducibility.

## 4. Hashing Rules

### 4.1 Hashing Arbitrary Objects

To hash an object:

1. Serialize to canonical JSON  
2. Compute SHA‑256 digest  
3. Encode as lowercase hex string  

### 4.2 Hashing Audit Events

Audit events must be hashed over:

- all fields except `event_hash`

### 4.3 Hashing Replay Traces

Replay traces must be hashed over:

- all fields except `trace_hash`

### 4.4 Hashing Workflow Inputs and Outputs

Workflow inputs and outputs must be hashed using the same canonical rules.

## 5. Hash Linking

Audit logs must form a hash chain:

- `prev_hash` = hash of previous event  
- `event_hash` = hash of current event  

This provides tamper‑evidence.

## 6. Validation

A conformant runtime must:

- recompute hashes during replay  
- validate audit log hash chains  
- validate trace hashes  

Any mismatch indicates non‑conformance.
