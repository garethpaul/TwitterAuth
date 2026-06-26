# Account-Switch Post Invalidation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Prevent a prior account's live-post completion from owning demo state after replacement authentication begins.

**Architecture:** Extract the existing post generation invalidation and ownership clearing into one private helper. Invoke it before replacement OAuth state changes and from component disable, then enforce the lifecycle ordering through the focused portable contract and hostile mutations.

**Tech Stack:** Legacy Unity C#, Python 3 static contracts, GNU Make, GitHub Actions

---

Status: Completed

### Task 1: Write The Failing Ownership Contract

**Files:**
- Modify: `scripts/post_tweet_ownership_contract.py`
- Modify: `scripts/test_post_tweet_ownership_contract.py`

Require one invalidation helper, require replacement authentication to call it
before token-state replacement, and require `OnDisable` to use the same helper.
Run the focused mutation suite and confirm failure before production changes.

### Task 2: Implement Shared Invalidation

**Files:**
- Modify: `UnityTwitter/Assets/Demo.cs`

Extract the generation increment and in-flight clearing, call it before the
login button replaces OAuth state, and reuse it during disable.

### Task 3: Synchronize Evidence

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `SECURITY.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-26-account-switch-post-invalidation.md`

Document the prior-account completion boundary, exact validation, and runtime
limit that an already transmitted provider request cannot be revoked locally.

### Task 4: Validate And Merge

Run the focused mutation suite, all Make aliases from repository and external
working directories, syntax/diff/secret audits, Codex review, hosted checks, and
exact-head verification before merge.

## Verification Completed

- Red-first focused validation failed on the missing helper, account-switch
  invalidation, ordering, and disable reuse.
- The implemented shared helper passes the focused suite with ten hostile
  mutations rejected.
- Root and external-directory `make check` plus all six documented Make aliases
  passed with 26 canonical checks and every focused mutation suite.
- Compatible Unity runtime and live provider behavior remain intentionally
  outside credential-free validation.
