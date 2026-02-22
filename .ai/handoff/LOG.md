# openclaw-gpu-bridge — Log

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
