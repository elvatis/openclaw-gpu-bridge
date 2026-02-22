# openclaw-gpu-bridge — Log

## 2026-02-22 — Project Initialized

- Repo cloned from github.com/homeofe/openclaw-gpu-bridge
- AAHP handoff structure created
- README.md written with architecture + config schema
- Context: spawned from BMAS metrics pipeline running BERTScore on CPU (slow); Emre wants to offload to GPU PC on local network
- Fortinet digest script already has the Python patterns needed for the service side

## 2026-02-22 — P2 Architecture (Opus)

- **ADR written** with 8 decisions: GPU auto-detection (D1), endpoints (D2), model pre-loading (D3), concurrency semaphore (D4), deployment strategy (D5), TS plugin structure (D6), timeouts (D7), auth (D8)
- **D5 updated:** v0.1 targets Windows + Python venv (no Docker). Target hardware: RTX 2080 Ti on Emre's Windows PC, OpenClaw on separate Linux server.
- **TypeScript scaffolding:** `src/index.ts` (4 tools), `src/tools.ts`, `src/client.ts`, `src/types.ts`
- **Python GPU service:** `gpu-service/gpu_service.py` (FastAPI + lifespan), `models.py` (Pydantic), `device.py` (auto-detect)
- **Plugin manifest updated:** config schema with `models.embed`/`models.bertscore` + uiHints
- **gpu-service/README.md:** Windows setup guide, env vars, AMD ROCm future note
- Removed ROCm Dockerfile / requirements-rocm.txt (not needed for v0.1)
