# Pull Request template

## Pull Request Title

Short, descriptive title (e.g., `feat: add audit-chain signer`)

## Description

**What** this PR does:

-  

**Why** this change is needed:

-  

**Scope**:

- Bugfix / Feature / Chore / Docs / CI / Security

## Related Issues

- Closes: #ISSUENUMBER
- Related: #OTHER_ISSUE_NUMBER

## Implementation Notes

- Key design decisions and trade-offs.
- Any backwards-incompatible changes.
- Migration steps (if any).

## Checklist (required before merge)

- [ ] **Build**: `cargo build` passes locally.
- [ ] **Tests**: `cargo test` passes locally and in CI.
- [ ] **Lint**: `cargo clippy` and `cargo fmt --check` pass.
- [ ] **Security**: `cargo audit` run and no new critical vulnerabilities introduced.
- [ ] **Code review**: at least one approving review from a maintainer.
- [ ] **CI**: All GitHub Actions checks are green.
- [ ] **Docs**: README or docs updated if behavior or public API changed.
- [ ] **Audit artifacts**: If this PR affects audit generation or format, include:
  - Example `audit/*.json` filename(s) and SHA-256 hash(es).
  - Backwards compatibility notes for `audit_chain` signing tool.
- [ ] **Key management**: If this PR touches signing or key handling, include a key-rotation plan and confirm private keys are not committed.
- [ ] **Release notes**: Add a short entry for CHANGELOG.

## Testing & Demo

- How to reproduce the change locally (commands).
- Example demo commands (e.g., `cargo run -- --workflow --audit`).
- If applicable, include sample output or artifact filenames.

## Security & Privacy Considerations

- Does this change handle secrets, keys, or audit data? `yes` / `no`
- If `yes`, describe how secrets are protected and where they are stored (e.g., GitHub Secrets, KMS).
- Confirm no private keys or secrets are committed.

## Rollout Plan

- Feature flag? `yes` / `no`
- Migration steps and rollback plan.

## Reviewer Guidance

- Areas to focus review on (e.g., cryptographic correctness, deterministic filenames, CI changes).
- Files of interest:
  - `src/main.rs`
  - `audit_chain/src/main.rs` (signing tool)
  - `.github/workflows/*`
  - `Cargo.toml`

## Release Notes (for maintainers)

- Short summary for the release notes / changelog.

### Merge procedure

- Ensure at least one approving review and CI green.
- Squash or merge per repository policy.
- If signing keys or audit chain changed, run the signing workflow and publish `chain-public-key.pem` in the release assets.
