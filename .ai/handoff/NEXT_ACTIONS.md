# NEXT_ACTIONS - openclaw-gpu-bridge

> Priority order. Work top-down.
> Updated: 2026-03-01 (T-005 confirmed done)

---

## Status Summary

| Status | Count |
|--------|-------|
| Done | 5 |
| Ready | 3 |
| Blocked | 0 |

---

## Ready - Work These Next

### T-006 [high]: TS client should honor Retry-After header on 503 responses

**Goal:** Make the TypeScript client respect the Retry-After header instead of marking the host unhealthy on 503.

**Context:**
- GPU service returns HTTP 503 with `Retry-After: 5` when concurrency semaphore is full
- Client currently treats 503 as a failure and marks the host unhealthy
- A 503 with Retry-After means the host is alive but temporarily busy

**What to do:**
1. Update `src/client.ts` to detect 503 + Retry-After header
2. Implement wait-and-retry logic instead of marking host unhealthy
3. Add tests for the new retry behavior

**Files:** `src/client.ts`, `src/client.test.ts`

**Definition of done:**
- Client waits and retries on 503 with Retry-After (does not mark host unhealthy)
- Unit tests cover the retry behavior
- `npm test` and `npm run build` pass
- GitHub issue #3 closed

---

### T-007 [medium]: Add Python unit tests for gpu-service (pytest)

**Goal:** Create pytest test suite for the Python GPU service endpoints and logic.

**Context:**
- Python GPU service has no test coverage
- TypeScript plugin has 21 Jest tests but Python side is untested
- Need to cover endpoints, model caching, auth, concurrency

**What to do:**
1. Create `gpu-service/tests/` with pytest tests
2. Cover endpoint response shapes, model cache, auth middleware, concurrency guard
3. Add `requirements-dev.txt` with test dependencies if needed

**Files:** `gpu-service/gpu_service.py`, `gpu-service/tests/`

**Definition of done:**
- `pytest gpu-service/tests/` passes
- Key endpoints and logic covered (health, info, status, bertscore, embed)
- GitHub issue #2 closed

---

### T-008 [medium]: Add input size validation to prevent GPU OOM on large batches

**Goal:** Add batch size and text length limits to prevent GPU out-of-memory crashes.

**Context:**
- `/bertscore` and `/embed` accept arbitrarily large input arrays
- Very large batches (10,000+ pairs) can exhaust VRAM and crash the service
- Flagged in P4 code review as recommended for v0.2

**What to do:**
1. Add validation for max batch size and max text length in request models
2. Return 422 with clear error messages when limits are exceeded
3. Make limits configurable via environment variables
4. Add tests for the validation

**Files:** `gpu-service/gpu_service.py`, `gpu-service/models.py`

**Definition of done:**
- Requests exceeding batch/text limits return 422 with clear error
- Limits configurable via env vars (GPU_MAX_BATCH_SIZE, GPU_MAX_TEXT_LENGTH)
- Tests cover validation behavior
- GitHub issue #1 closed

---

## Blocked

(none)

---

## Recently Completed

| Task | Date | Resolution |
|------|------|-----------|
| T-005 Dockerfile PyTorch base image update | 2026-03-01 | Updated to pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime in commit 4c9c067. GitHub issue #4 closed. |
| T-004 gpu-service README stale defaults | 2026-03-01 | Verified already correct - BERTScore model, /status endpoint, env vars all accurate |
| T-003 Add Python unit tests for gpu-service | 2026-02-27 | pytest test suite created with full endpoint coverage |
| T-002 Publish npm package v0.2.0 | 2026-02-27 | CHANGELOG, merge to main, tag v0.2.0, tarball cleanup. npm auth needed for final publish. |
| T-001 Live multi-host validation | 2026-02-27 | 10 integration tests with real HTTP servers, 21/21 total passing |

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
