# openclaw-gpu-bridge — Status

> Last updated: 2026-02-23
> Phase: v0.2 implemented (code + unit tests complete), awaiting multi-host live validation

## Project Overview

**Package:** `@elvatis_com/openclaw-gpu-bridge`
**Repo:** https://github.com/homeofe/openclaw-gpu-bridge
**Purpose:** Expose remote GPU compute (BERTScore, embeddings) as OpenClaw tools, now with multi-host orchestration.

## Build Health

| Component | Status | Notes |
|---|---|---|
| TypeScript strict build | (Verified) | `npm run build` passes with 0 TS errors |
| Unit tests | (Verified) | `npm test` 3/3 passed (multi-host logic) |
| `src/client.ts` | (Verified) | Multi-host pool, round-robin/least-busy, failover, health-check loop |
| `src/tools.ts` | (Verified) | Backward compatible tools + optional `gpu_status` |
| `src/index.ts` | (Verified) | Registers 5 tools (`gpu_status` added) |
| `openclaw.plugin.json` | (Verified) | v0.2 config schema (`hosts[]`, LB strategy, compatibility fields) |
| `gpu-service/gpu_service.py` | (Verified) | On-demand model loading + cache, `/status`, progress logging |
| `gpu-service/models.py` | (Verified) | Added status response models, updated defaults |
| README | (Verified) | Added internet exposure hardening + v0.2 usage |
| Live multi-host test | (Unknown) | Not yet run against 2+ real GPU hosts |
| npm publish | (Unknown) | Not yet published |

## v0.2 Feature Status

1. **Multi-GPU Support** — (Verified in code/tests)
   - `hosts: [{url, name, apiKey}]` config
   - v0.1 compatibility (`serviceUrl` / `url`)
   - Load balancing: `round-robin` + `least-busy`
   - Failover to next host on host failure
   - Periodic health checks with unhealthy host rotation

2. **Internet-Erreichbarkeit Doku** — (Verified)
   - README section: **Exposing to the Internet**
   - X-API-Key pre-shared key documented
   - TLS via nginx reverse proxy + uvicorn SSL example
   - WireGuard private-network alternative documented

3. **Flexible model selection** — (Verified)
   - `/embed` supports per-request `model`
   - `/bertscore` supports per-request `model_type`
   - Models load on demand and are cached server-side
   - Defaults: embed `all-MiniLM-L6-v2`, bertscore `microsoft/deberta-xlarge-mnli`

4. **Transfer progress / visibility** — (Verified, optional scope)
   - Added `/status` endpoint with queue + active jobs + progress
   - Batch progress logging for embed chunks
