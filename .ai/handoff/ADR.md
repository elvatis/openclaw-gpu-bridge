# ADR — openclaw-gpu-bridge Architecture Decisions

> Date: 2026-02-22 | Author: Opus (P2 Architect) | Status: Accepted

---

## D1: GPU Auto-Detection Strategy

**Decision:** Use `torch.cuda.is_available()` as the single detection call. PyTorch's ROCm build exposes the same CUDA API surface, so this call returns `True` for both NVIDIA (CUDA) and AMD (ROCm) GPUs.

**Details:**
- `device.py` calls `torch.cuda.is_available()` at import time
- If `True`: `torch.device("cuda")` — works for both vendors
- If `False`: falls back to `torch.device("cpu")` with a warning log
- `/info` endpoint exposes `torch.cuda.get_device_name(0)` and `torch.version.cuda` (or ROCm version) for diagnostics
- Optional `TORCH_DEVICE` env var overrides auto-detection (e.g., force CPU for testing)

**Rationale:** No vendor-specific branching needed in application code. The PyTorch abstraction handles both backends identically.

---

## D2: Service Endpoints

**Decision:** Four REST endpoints on the FastAPI GPU service.

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Liveness check (`{"status":"ok","device":"cuda"}`) |
| `/info` | GET | GPU name, VRAM, PyTorch version, loaded models |
| `/bertscore` | POST | Compute BERTScore (candidates vs references) |
| `/embed` | POST | Generate text embeddings |

**Request/Response contracts:**

```
POST /bertscore
{ "candidates": ["..."], "references": ["..."], "lang": "en", "model_type": "roberta-large" }
→ { "precision": [...], "recall": [...], "f1": [...], "model": "roberta-large" }

POST /embed
{ "texts": ["..."], "model": "all-MiniLM-L6-v2" }
→ { "embeddings": [[...]], "model": "all-MiniLM-L6-v2", "dimensions": 384 }
```

---

## D3: Model Pre-Loading Strategy

**Decision:** Use FastAPI's lifespan context manager to pre-load models at startup.

```python
@asynccontextmanager
async def lifespan(app):
    app.state.models = load_models(config)
    yield
    # cleanup on shutdown
```

**Details:**
- BERTScore model (`roberta-large`) and embedding model (`all-MiniLM-L6-v2`) loaded once at startup
- Models stored in `app.state.models` dict
- Configurable via `MODEL_EMBED` and `MODEL_BERTSCORE` env vars
- First request has zero cold-start latency

**Rationale:** GPU model loading takes 5-15s. Doing it at startup avoids timeout on first request.

---

## D4: Concurrency Handling

**Decision:** `asyncio.Semaphore(max=2)` guards GPU inference. Return HTTP 503 with `Retry-After: 5` when semaphore is full.

**Details:**
- GPU memory is limited; concurrent large batches cause OOM
- Semaphore value configurable via `GPU_MAX_CONCURRENT` env var (default: 2)
- Non-blocking: uses `semaphore.acquire()` with `asyncio.wait_for(timeout=1.0)`
- If acquire times out → 503 Service Unavailable

**Rationale:** Simple, effective backpressure. The plugin TS client can retry or surface the error to the agent.

---

## D5: Deployment Strategy

**Decision:** For v0.1, plain Python venv + uvicorn on Windows (NVIDIA RTX 2080 Ti, 11GB VRAM). No Docker required initially.

**Target hardware:** Emre's Windows PC with RTX 2080 Ti (CUDA). OpenClaw runs on a separate Linux server (Quadro M2000) and connects via LAN HTTP.

**v0.1 setup (Windows):**
```
python -m venv venv
venv\Scripts\activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
uvicorn gpu_service:app --host 0.0.0.0 --port 8765
```

**Future:** A `Dockerfile` (NVIDIA/CUDA) is included for containerized deployment. AMD/ROCm support is architecturally possible (see D1 — `torch.cuda.is_available()` works for both) but not needed now; noted in README as future option.

**Rationale:** Docker adds complexity for a single-machine Windows setup. A Python venv is simpler to debug and iterate on during development.

---

## D6: Plugin TypeScript Structure

**Decision:** Four tools registered via `api.registerTool()`:

| Tool Name | Description | Parameters |
|---|---|---|
| `gpu_health` | Check GPU service liveness | none |
| `gpu_info` | Get GPU device info and loaded models | none |
| `gpu_bertscore` | Compute BERTScore between text pairs | `candidates`, `references`, `lang?`, `model_type?` |
| `gpu_embed` | Generate text embeddings | `texts`, `model?` |

**File structure:**
- `src/index.ts` — Plugin entry, reads config, registers 4 tools
- `src/tools.ts` — Tool execute functions (call client methods)
- `src/client.ts` — `GpuBridgeClient` class (fetch wrapper with baseUrl, apiKey, timeout)
- `src/types.ts` — TypeScript interfaces for requests/responses

**Dependencies:** Node 18+ native `fetch` — no external HTTP library needed.

---

## D7: Timeout Values

**Decision:**

| Layer | Timeout | Rationale |
|---|---|---|
| TS client (`AbortSignal`) | 45s | Agent tool calls should not hang indefinitely |
| FastAPI server (uvicorn `--timeout-keep-alive`) | 65s | Must exceed client timeout to avoid mid-response disconnects |
| GPU inference internal | 60s | Per-request guard; kills stuck inference |
| Health check (TS client) | 5s | Fast fail for liveness |

**Rationale:** Client < server prevents the client from disconnecting while the server is still processing. The 45s client timeout is generous for BERTScore on moderate batches (~20 pairs).

---

## D8: Authentication

**Decision:** Optional `X-API-Key` header, validated in FastAPI middleware.

**Details:**
- If `API_KEY` env var is set on the server → middleware checks `X-API-Key` header on every request
- If `API_KEY` is not set → no auth (local network trust model)
- Plugin TS client sends `X-API-Key` header if `apiKey` is configured
- 401 Unauthorized on mismatch

**Rationale:** Simple shared-secret auth sufficient for LAN deployment. No need for OAuth/JWT for a single-client internal service.

---

## Project File Structure (Final)

```
openclaw-gpu-bridge/
├── .ai/handoff/           — AAHP handoff docs
│   ├── STATUS.md
│   ├── ADR.md             — This file
│   ├── LOG.md
│   ├── NEXT_ACTIONS.md
│   └── DASHBOARD.md
├── src/
│   ├── index.ts           — Plugin entry, registerTool x4
│   ├── tools.ts           — Tool execute implementations
│   ├── client.ts          — GpuBridgeClient (fetch wrapper)
│   └── types.ts           — Shared TS interfaces
├── gpu-service/
│   ├── gpu_service.py     — FastAPI app (endpoints + lifespan)
│   ├── models.py          — Pydantic request/response models
│   ├── device.py          — GPU detection + device selection
│   ├── requirements.txt   — Python deps (torch, fastapi, etc.)
│   ├── README.md          — Setup guide (Windows + Docker)
│   └── Dockerfile         — NVIDIA/CUDA image (optional)
├── openclaw.plugin.json   — Plugin manifest
├── package.json
├── tsconfig.json
└── README.md
```
