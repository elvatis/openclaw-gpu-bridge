# NEXT_ACTIONS — openclaw-gpu-bridge

> Updated: 2026-02-22T18:22

## ✅ Completed

- **P1 — Research:** OSS libs, API patterns, OpenClaw plugin API
- **P2 — Architecture:** ADR (8 decisions), file structure, config schema, TS scaffolding, Python service code
- **P3 — Implementation:** TypeScript verified (0 errors), Python service fixed, README written, deps updated for Python 3.13

## 🔜 P4 — Integration Testing

Priority: **HIGH** | Requires: Emre's Windows PC with RTX 2080 Ti running the GPU service

### Tasks

1. **GPU service startup test** — Run `uvicorn gpu_service:app --host 0.0.0.0 --port 8765` on Windows
   - Confirm both models load without errors (BERTScore + embedding)
   - Confirm device logs show `cuda` (not `cpu`)
   
2. **Health + info endpoints** — Hit `/health` and `/info` from OpenClaw server
   - Verify `device_name` shows "NVIDIA GeForce RTX 2080 Ti"
   - Verify `loaded_models` lists both models

3. **BERTScore end-to-end** — From OpenClaw agent, call `gpu_bertscore`
   - Test batch of 5-10 pairs
   - Measure latency (target: <10s for 10 pairs on RTX 2080 Ti)

4. **Embeddings end-to-end** — From OpenClaw agent, call `gpu_embed`
   - Test 50 texts
   - Verify `dimensions=384` for all-MiniLM-L6-v2

5. **Auth test** — Set `API_KEY` env var, verify 401 on bad key, 200 on correct key

6. **Concurrency test** — Send 3 simultaneous requests, verify 3rd gets 503 + `Retry-After: 5`

### Acceptance Criteria

- All 4 agent tools return correct responses against live GPU service
- Latency within expected bounds
- Auth and concurrency guards confirmed working

## 📋 P5 — Polish & Publish

- Write unit tests (TypeScript: mock fetch; Python: pytest with mock torch)
- npm publish `@elvatis/openclaw-gpu-bridge`
- Add plugin to OpenClaw config on production Linux server
- Windows startup script / task for auto-starting GPU service on boot
- Consider adding a `Dockerfile` (NVIDIA CUDA base image) for future containerized deployment
