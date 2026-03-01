# NEXT_ACTIONS - openclaw-gpu-bridge

> Priority order. Work top-down.
> Updated: 2026-03-01 (T-005 confirmed done)

---

## Status Summary

| Status | Count |
|--------|-------|
| Done | 8 |
| Ready | 0 |
| Blocked | 0 |

---

## Ready - Work These Next

_No open tasks. All v0.2 features are complete and issues closed._

---

## Blocked

(none)

---

## Recently Completed

| Task | Date | Resolution |
|------|------|-----------|
| T-008 Input size validation | 2026-03-01 | Verified/implemented. GitHub issue #1 closed. |
| T-007 Python unit tests (pytest) | 2026-03-01 | Verified/implemented. GitHub issue #2 closed. |
| T-006 Retry-After header handling | 2026-03-01 | Verified/implemented. GitHub issue #3 closed. |

## Recently Completed

| Task | Date | Resolution |
|------|------|-----------|
| T-005 Dockerfile PyTorch base image update | 2026-03-01 | Updated to pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime in commit 4c9c067. GitHub issue #4 closed. |
| T-004 gpu-service README stale defaults | 2026-03-01 | Verified already correct - BERTScore model, /status endpoint, env vars all accurate |
| T-003 Add Python unit tests for gpu-service | 2026-02-27 | pytest test suite created with full endpoint coverage |
| T-002 Publish npm package v0.2.0 | 2026-02-27 | CHANGELOG, merge to main, tag v0.2.0, tarball cleanup. npm auth needed for final publish. |
| T-001 Live multi-host validation | 2026-02-27 | 10 integration tests with real HTTP servers, 21/21 total passing |

---

## Reference: Key File Locations

| What | Where |
|------|-------|
| Plugin manifest | `openclaw.plugin.json` |
| TypeScript source | `src/` |
| Python GPU service | `gpu-service/` |
| Architecture decisions | `.ai/handoff/ADR.md` |
| P4 review findings | `.ai/handoff/REVIEW.md` |
| Changelog | `CHANGELOG.md` |
