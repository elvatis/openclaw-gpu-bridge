# openclaw-gpu-bridge — Status

> Last updated: 2026-02-22T18:22 (P3 complete)
> Phase: P3 ✅ → P4 next (Integration Test)

## Project Overview

**Package:** `@elvatis/openclaw-gpu-bridge`
**Repo:** https://github.com/homeofe/openclaw-gpu-bridge
**Purpose:** Expose remote GPU compute (via FastAPI microservice) as OpenClaw agent tools.
**Target GPU:** NVIDIA RTX 2080 Ti (11GB VRAM) on Emre's Windows PC (Python 3.13), connected via LAN to OpenClaw Linux server.

## Build Health

| Component | Status | Notes |
|---|---|---|
| Repo / Structure | (Verified) | All files in place |
| Plugin manifest | (Verified) | `openclaw.plugin.json` with config schema + uiHints |
| TypeScript source | (Verified) | `npx tsc --noEmit` → 0 errors, strict mode |
| GPU service (Py) | (Verified) | FastAPI app, device detection, lifespan model pre-loading |
| Python 3.13 compat | (Verified) | torch>=2.5.0, setuptools>=75.0, cu124 index URL documented |
| requirements.txt | (Verified) | All deps listed, cu121 vs cu124 guidance for py3.13 |
| README | (Verified) | Full user guide — Windows/Linux setup, Python 3.13 notes, API reference |
| ADR | (Verified) | 8 architecture decisions |
| Agent tools | (Assumed) | 4 tools defined, not yet integration-tested |
| Tests | (Unknown) | Unit tests not yet written |
| npm publish | (Unknown) | Not yet published |

## Architecture

- **Plugin (TS):** 4 tools (`gpu_health`, `gpu_info`, `gpu_bertscore`, `gpu_embed`) → HTTP calls to GPU service
- **GPU service (Python):** FastAPI on Windows, CUDA auto-detection, model pre-loading at startup via lifespan, semaphore concurrency guard
- **Communication:** REST JSON over LAN, optional `X-API-Key` auth
- **Config:** `serviceUrl` (required), `timeout` (45s), `apiKey`, `models.embed`, `models.bertscore`
- **Deployment:** Python venv + uvicorn on Windows with Python 3.13 (torch>=2.5.0 + cu124)

## Known Constraints

- Python 3.13 requires `cu124` index URL (not cu121); both documented in README
- Models are pre-loaded at startup; per-request model switching is not supported (by design — ADR D3)
- `model` field in responses reflects the pre-loaded model name, not the request's `model_type` field (corrected in P3)
