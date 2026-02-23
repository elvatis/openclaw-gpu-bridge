# NEXT_ACTIONS — openclaw-gpu-bridge

> Updated: 2026-02-23

## ✅ Completed (v0.2 code scope)

- Multi-host support with failover and health checks
- Load balancing (`round-robin`, `least-busy`)
- Backward compatibility with v0.1 config
- Flexible model override + on-demand model cache in GPU service
- `/status` endpoint + progress logging
- README security/internet exposure documentation
- TypeScript unit tests for multi-host behavior (3/3 passing)

## 🔜 Priority 1 — Live Validation (real hardware)

1. Start two GPU service instances/hosts and configure `hosts[]`
2. Verify round-robin distribution across hosts
3. Verify least-busy picks lower VRAM host under load
4. Kill one host during requests; verify automatic failover
5. Check `/status` reflects active jobs and progress
6. Auth verification on all hosts (`API_KEY`, 401/200 behavior)

## 🔜 Priority 2 — Packaging & Release

1. Bump package release notes/changelog for v0.2.0
2. Publish npm package
3. Update production OpenClaw config to use `hosts[]`
4. Tag release in GitHub (`v0.2.0`)

## 🔜 Priority 3 — Optional Hardening

- Add Python unit tests for model-cache and `/status`
- Add retry/backoff tuning per host (optional)
- Add host-level metrics endpoint/dashboard (optional)
