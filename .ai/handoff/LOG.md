# openclaw-gpu-bridge — Log

## 2026-02-23 — v0.2 Multi-GPU Implementation (Sonnet)

- Implemented **multi-host config** in TypeScript client: `hosts[]` with per-host `apiKey`, plus v0.1 compatibility fallback (`serviceUrl` / `url`).
- Added host orchestration logic:
  - health state tracking per host
  - load balancing: `round-robin` and `least-busy` (VRAM usage from `/info`)
  - automatic failover to next host when request fails
  - periodic health checks (`healthCheckIntervalSeconds`)
- Added `gpu_status` tool and `/status` client support.
- Updated plugin schema (`openclaw.plugin.json`) to v0.2.0 and documented new fields.
- Upgraded defaults to requested models:
  - embed: `all-MiniLM-L6-v2`
  - bertscore: `microsoft/deberta-xlarge-mnli`
- Reworked Python GPU service (v0.2):
  - on-demand model loading + in-memory cache for BERTScore and embedding models
  - new `/status` endpoint with queue + active jobs + progress
  - embed batch processing with progress logs
  - active job tracking with UUIDs and timestamps
- Added TypeScript unit tests for multi-host logic (`src/client.test.ts`):
  - legacy single-host compatibility
  - host failover behavior
  - least-busy host selection
- Added Jest config (`jest.config.cjs`).
- Validation:
  - `npm run build` ✅
  - `npm test` ✅ (3/3)


## 2026-02-22 — P4 Discussion Round (Sonnet Reviewer)

- **Full code review** of all 7 source files against ADR and checklist
- **TypeScript plugin:** All 4 tools (gpu_health, gpu_info, gpu_bertscore, gpu_embed) correctly map to FastAPI endpoints. Timeout handling (AbortController + clearTimeout), X-API-Key header injection, and error wrapping all correct. `tsc --noEmit` → 0 errors.
- **Python service:** GPU detection (`torch.cuda.is_available()`), lifespan model pre-loading, semaphore backpressure (semaphore.acquire with wait_for timeout=1.0), Pydantic v2 syntax, and `/health` endpoint all verified correct.
- **Security:** X-API-Key middleware correctly guards non-health endpoints; no injection risks found; model names not user-controllable.
- **Critical bug found and fixed:** `scorer.score()` and `embedder.encode()` were blocking synchronous GPU operations called directly in async FastAPI handlers — freezing the asyncio event loop during inference. Fixed by wrapping both calls with `asyncio.to_thread()`, making inference non-blocking.
- **Commit:** `cf96278` — `fix(review): P4 fixes — asyncio.to_thread for non-blocking GPU inference [AAHP-P4]`
- **REVIEW.md written** with full checklist results and detailed bug analysis

## 2026-02-22 — Project Initialized

- Repo cloned from github.com/homeofe/openclaw-gpu-bridge
- AAHP handoff structure created
- README.md written with architecture + config schema
- Context: spawned from BMAS metrics pipeline running BERTScore on CPU (slow); Emre wants to offload to GPU PC on local network
- Fortinet digest script already has the Python patterns needed for the service side

## 2026-02-22 — P3 Implementation (Sonnet)

- **TypeScript verified:** `npx tsc --noEmit` → 0 errors. All 4 source files clean under strict mode.
- **Bug fix — response model names:** `gpu_service.py` was returning `req.model_type` / `req.model` in responses instead of the actual pre-loaded model name. Fixed by storing `bertscore_model_name` and `embed_model_name` in `app.state` at lifespan startup and referencing those in endpoint responses.
- **requirements.txt updated:**
  - Added `torch>=2.5.0` (Python 3.13 requires 2.5.0+)
  - Added `pydantic>=2.0.0` (was implicit via fastapi, now explicit)
  - Added `setuptools>=75.0` (prevents distutils errors on Python 3.13)
  - Added `bert-score>=0.3.13` (was already correct, confirmed)
  - Clarified: `cu121` index has **no cp313 wheels** — Python 3.13 users must use `cu124+` (verified via pytorch.org WHL index inspection)
- **README.md rewritten:** Full user guide covering Windows (NVIDIA cu121 for py3.11/3.12, cu124 for py3.13), Linux, AMD ROCm (future), environment variables, agent tool reference, API endpoint reference.
- **Added files:** `gpu-service/__init__.py`, updated `.gitignore` with Python venv/pycache/pyc entries
- **AAHP docs updated:** DASHBOARD, STATUS, NEXT_ACTIONS, LOG all updated to P3 complete

## 2026-02-22 — P2 Architecture (Opus)

- **ADR written** with 8 decisions: GPU auto-detection (D1), endpoints (D2), model pre-loading (D3), concurrency semaphore (D4), deployment strategy (D5), TS plugin structure (D6), timeouts (D7), auth (D8)
- **D5 updated:** v0.1 targets Windows + Python venv (no Docker). Target hardware: RTX 2080 Ti on Emre's Windows PC, OpenClaw on separate Linux server.
- **TypeScript scaffolding:** `src/index.ts` (4 tools), `src/tools.ts`, `src/client.ts`, `src/types.ts`
- **Python GPU service:** `gpu-service/gpu_service.py` (FastAPI + lifespan), `models.py` (Pydantic), `device.py` (auto-detect)
- **Plugin manifest updated:** config schema with `models.embed`/`models.bertscore` + uiHints
- **gpu-service/README.md:** Windows setup guide, env vars, AMD ROCm future note
- Removed ROCm Dockerfile / requirements-rocm.txt (not needed for v0.1)

## 2026-02-22 — v0.1 Complete + Live Test

- AAHP P1-P4 complete (commits d94bce4 → 7cc0fda)
- Live test: Emre's RTX 2080 Ti at 192.168.177.3 — CUDA detected, /health OK, /bertscore F1=0.9645
- /info bug fixed: total_mem → total_memory
- Verbose logging added: timing per request, VRAM stats
- Plugin currently NOT in openclaw.json (pre-npm-publish, using direct HTTP for test)
- v0.2 planned: multi-GPU host pool with load balancing + failover
