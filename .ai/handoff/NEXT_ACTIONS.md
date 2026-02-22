# NEXT_ACTIONS — openclaw-gpu-bridge

> Updated: 2026-02-22T18:14

## ✅ Completed

- **P1 — Research:** OSS libs, API patterns, OpenClaw plugin API
- **P2 — Architecture:** ADR (8 decisions), file structure, config schema, TS scaffolding, Python service code

## 🔜 P3 — Implementation (Sonnet)

Priority: **HIGH** | Branch: `main` (small project, direct commits OK for v0.1)

### Tasks

1. **`tsconfig.json`** — Create if missing, ensure `"module": "ESNext"`, `"outDir": "dist"`
2. **Verify TS compiles** — `npm run build` must succeed
3. **Test GPU service locally** — If Python available, run basic import checks
4. **Add `gpu-service/__init__.py`** — Empty, for Python module resolution
5. **Add `.gitignore`** — `node_modules/`, `dist/`, `venv/`, `__pycache__/`, `*.pyc`
6. **Write tests** — At minimum: TS unit tests for `client.ts` (mock fetch), type checks
7. **README.md** (root) — Project overview, quick start for both TS plugin + Python service
8. **Validate plugin loads** — If OpenClaw dev env available, test `openclaw plugins list`

### Acceptance Criteria

- `npm run build` produces `dist/` without errors
- All 4 tool schemas valid JSON Schema
- GPU service starts without errors (given CUDA available)
- Root README documents setup for both sides

## 📋 P4 — Integration Testing

- End-to-end: Plugin ↔ GPU service on LAN
- Test with actual RTX 2080 Ti
- Measure latency for BERTScore (20 pairs) and embeddings (100 texts)

## 📋 P5 — Polish & Publish

- npm publish `@elvatis/openclaw-gpu-bridge`
- Add to OpenClaw config on production server
- Windows service / startup script for GPU service
