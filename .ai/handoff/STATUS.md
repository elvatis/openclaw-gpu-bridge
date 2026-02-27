# openclaw-gpu-bridge: Current State of the Nation

> Last updated: 2026-02-27 by claude-opus-4.6 (T-001 live multi-host validation)
>
> **Rule:** This file is rewritten (not appended) at the end of every session.
> It reflects the *current* reality, not history. History lives in LOG.md.

---

<!-- SECTION: summary -->
v0.2 multi-GPU validated with 10 integration tests using real HTTP servers. 21 total tests passing (11 unit + 10 integration). Round-robin, least-busy, failover, auth, 503 retry, and all endpoints verified end-to-end. T-002 npm publish now unblocked.
<!-- /SECTION: summary -->

<!-- SECTION: build_health -->
## Build Health

| Check | Result | Notes |
|-------|--------|-------|
| `npm run build` (TypeScript) | (Verified) | 0 TS errors |
| `npm test` (Jest) | (Verified) | 21/21 tests passing (11 unit + 10 integration) |
| `lint` | (Unknown) | Not configured |
| `type-check` | (Verified) | Included in build |

<!-- /SECTION: build_health -->

---

<!-- SECTION: project_overview -->
## Project Overview

**Package:** `@elvatis_com/openclaw-gpu-bridge`
**Repo:** https://github.com/homeofe/openclaw-gpu-bridge
**Purpose:** Expose remote GPU compute (BERTScore, embeddings) as OpenClaw tools, now with multi-host orchestration.

<!-- /SECTION: project_overview -->

---

<!-- SECTION: component_status -->
## Component Status

| Component | Status | Notes |
|-----------|--------|-------|
| `src/client.ts` | (Verified) | Multi-host pool, round-robin/least-busy, failover, health-check loop |
| `src/tools.ts` | (Verified) | 5 tools including gpu_status |
| `src/index.ts` | (Verified) | Registers 5 tools |
| `src/client.test.ts` | (Verified) | 11 unit tests passing |
| `src/integration.test.ts` | (Verified) | 10 integration tests with real HTTP servers |
| `openclaw.plugin.json` | (Verified) | v0.2 config schema with hosts[] |
| `gpu-service/gpu_service.py` | (Verified) | On-demand model loading + cache, /status |
| `gpu-service/models.py` | (Verified) | Status response models, updated defaults |
| README | (Verified) | Internet exposure hardening + v0.2 usage |
| Live multi-host test | (Verified) | Integration tests validate all multi-host scenarios |
| npm publish | (Unknown) | Not yet published |

<!-- /SECTION: component_status -->

---

<!-- SECTION: what_is_missing -->
## What is Missing

| Gap | Severity | GitHub Issue | Description |
|-----|----------|-------------|-------------|
| npm publish | HIGH | - | Not yet published to npm registry |
| Python unit tests | MEDIUM | [#2](https://github.com/homeofe/openclaw-gpu-bridge/issues/2) | No tests for model-cache and /status |
| Outdated Dockerfile | MEDIUM | [#4](https://github.com/homeofe/openclaw-gpu-bridge/issues/4) | Base image PyTorch 2.2.0 vs required 2.5.0+ |
| Stale gpu-service README | LOW | [#5](https://github.com/homeofe/openclaw-gpu-bridge/issues/5) | Wrong defaults, missing /status endpoint |

<!-- /SECTION: what_is_missing -->

---

## Trust Levels

- **(Verified)**: confirmed by running code/tests
- **(Assumed)**: derived from docs/config, not directly tested
- **(Unknown)**: needs verification
