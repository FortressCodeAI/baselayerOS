# Contributing to BaseLayerOS

BaseLayerOS is a deterministic compute substrate.  
Contributions must preserve determinism, invariants, and governance physics.

## Contribution Principles

1. No nondeterministic behavior  
2. No stochastic branching  
3. No uncontrolled external calls  
4. No ungoverned data access  
5. No probabilistic execution paths  

## Required Components

All contributions must include:

- deterministic envelope  
- invariant definition  
- replay path  
- governance boundary mapping  
- cross‑cloud consistency notes  

## Architectural Requirements

Contributions must align with:

- deterministic kernel  
- substrate state machine  
- GDTAL  
- cross‑cloud governance fabric  
- replay engine  

## Review Process

All PRs undergo:

- invariant verification  
- deterministic replay validation  
- governance boundary review  
- cross‑cloud consistency check  
