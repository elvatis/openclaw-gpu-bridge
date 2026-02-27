# NEXT_ACTIONS - openclaw-gpu-bridge

> Priority order. Work top-down.
> Updated: 2026-02-27 (T-002 publish session)

---

## Manual Step: npm publish

**The package is ready to publish.** All code is merged to main, tagged v0.2.0, and the tarball is clean.

To publish:
```bash
npm adduser          # authenticate with npm registry (one-time)
npm publish --access public
```

---

## T-003: Add Python unit tests (optional hardening)

**Goal:** Add pytest unit tests for model-cache and `/status` endpoint.

**Context:**
- Currently no Python tests exist for gpu-service
- TS unit tests cover multi-host logic; Python side is untested

**What to do:**
1. Create `gpu-service/tests/test_gpu_service.py`
2. Test model cache hit/miss behavior
3. Test `/status` response shape

**Definition of done:**
- [ ] `pytest gpu-service/` passes
- [ ] Cache and status endpoint covered

---

## Recently Completed

| Item | Resolution |
|------|-----------|
| T-002 Publish npm package v0.2.0 | CHANGELOG, merge to main, tag v0.2.0, tarball cleanup. npm auth needed for final publish. |
| T-001 Live multi-host validation | 10 integration tests with real HTTP servers, 21/21 total passing |
| Multi-host config (hosts[]) | Implemented in v0.2, 21/21 tests passing |
| Load balancing (round-robin, least-busy) | Implemented and tested |
| Failover + health checks | Implemented and tested |
| Flexible model override + on-demand cache | Implemented |
| /status endpoint + progress logging | Implemented |
| Internet exposure documentation | README updated |
| asyncio.to_thread for non-blocking GPU inference | Fixed in P4 review (commit cf96278) |

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
