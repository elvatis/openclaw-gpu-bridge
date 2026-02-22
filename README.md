# @elvatis/openclaw-gpu-bridge

**OpenClaw plugin** — Offload GPU-intensive ML tasks (BERTScore, text embeddings) to a remote machine running a FastAPI microservice. No GPU required on the OpenClaw server.

---

## What it does

The plugin exposes four agent tools that transparently call a Python FastAPI service running on any machine with a CUDA or ROCm GPU:

| Tool | Description |
|---|---|
| `gpu_health` | Ping the GPU service — confirms it's reachable and shows which device is active |
| `gpu_info` | GPU name, VRAM usage, PyTorch version, and which models are loaded |
| `gpu_bertscore` | Compute BERTScore (precision, recall, F1) between candidate and reference texts |
| `gpu_embed` | Generate text embeddings using sentence-transformers |

---

## Architecture

```
OpenClaw (Linux server)
        │
        │  HTTP REST + JSON  (LAN / VPN)
        │  X-API-Key header (optional)
        ▼
FastAPI GPU Service (Python)
  ├── /health   GET  — liveness check
  ├── /info     GET  — GPU diagnostics
  ├── /bertscore POST — BERTScore computation
  └── /embed    POST — text embedding
        │
        │  PyTorch
        ▼
NVIDIA GPU (CUDA) or AMD GPU (ROCm)
```

Models are **pre-loaded at startup** — no cold-start latency on the first request.

---

## GPU Service Setup (on the GPU machine)

### Requirements

- Python 3.11 or 3.12
- NVIDIA GPU with CUDA 11.8+ drivers **or** AMD GPU with ROCm 5.7+
- At least 4 GB VRAM (8 GB+ recommended for BERTScore with `roberta-large`)

---

### Windows Setup (NVIDIA — recommended for v0.1)

**Step 1 — Install PyTorch with CUDA support**

The index URL you need depends on your **Python version**:

```powershell
# Python 3.11 or 3.12 — CUDA 12.1 (works with RTX 20xx / 30xx / 40xx)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

```powershell
# Python 3.13 — CUDA 12.4 (cu121 has NO cp313 wheels; use cu124 or newer)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

> **Python 3.13 notes:**
> - `torch>=2.5.0` is the first release with official Python 3.13 support.
> - The `cu121` index does **not** include `cp313` wheels — always use `cu124+` with Python 3.13.
> - If you see `distutils` errors during install, run: `pip install setuptools --upgrade`

> For older GPUs / CUDA 11.8 (Python 3.11/3.12 only):
> `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118`

**Step 2 — Install service dependencies**

```powershell
cd gpu-service
pip install -r requirements.txt
```

**Step 3 — Run the service**

```powershell
uvicorn gpu_service:app --host 0.0.0.0 --port 8765
```

---

### Linux Setup (NVIDIA)

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Python 3.11 / 3.12 — CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Python 3.13 — CUDA 12.4 (cu121 has no cp313 wheels)
# pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

# Install service dependencies
cd gpu-service
pip install -r requirements.txt

# Run the service
uvicorn gpu_service:app --host 0.0.0.0 --port 8765
```

---

### Linux Setup (AMD ROCm — future)

> **Note:** ROCm support is architecturally ready (PyTorch's `torch.cuda.is_available()` returns `True` on ROCm builds too). Not tested in v0.1.

```bash
# Install PyTorch with ROCm support
pip install torch torchvision --index-url https://download.pytorch.org/whl/rocm5.7

# Then follow the same steps as Linux/NVIDIA above
```

---

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MODEL_BERTSCORE` | `roberta-large` | BERTScore model to pre-load at startup |
| `MODEL_EMBED` | `all-MiniLM-L6-v2` | Sentence-transformers embedding model |
| `API_KEY` | _(none)_ | If set, all requests (except `/health`) require `X-API-Key: <value>` |
| `GPU_MAX_CONCURRENT` | `2` | Max simultaneous GPU inference requests (backpressure) |
| `TORCH_DEVICE` | _(auto)_ | Override device: `cuda`, `cpu`, or `cuda:1` for multi-GPU |

---

### Verify GPU is used

After starting the service, check the `/info` endpoint:

```bash
curl http://localhost:8765/info | python3 -m json.tool
```

Expected response on a GPU machine:

```json
{
  "device": "cuda",
  "device_name": "NVIDIA GeForce RTX 2080 Ti",
  "vram_total_mb": 11264,
  "vram_used_mb": 4096,
  "pytorch_version": "2.2.0+cu121",
  "cuda_version": "12.1",
  "loaded_models": ["bertscore:roberta-large", "embed:all-MiniLM-L6-v2"]
}
```

If `"device": "cpu"` appears, PyTorch is not using your GPU. Re-check your CUDA/ROCm installation.

---

## OpenClaw Plugin Setup

### Install

```bash
openclaw plugins install @elvatis/openclaw-gpu-bridge
```

### Configuration

Add to your OpenClaw config (or configure via the UI):

```json
{
  "plugins": {
    "@elvatis/openclaw-gpu-bridge": {
      "serviceUrl": "http://192.168.1.100:8765",
      "timeout": 45,
      "apiKey": "your-secret-key",
      "models": {
        "embed": "all-MiniLM-L6-v2",
        "bertscore": "roberta-large"
      }
    }
  }
}
```

**Config fields:**

| Field | Required | Default | Description |
|---|---|---|---|
| `serviceUrl` | ✅ | — | URL of the FastAPI GPU service |
| `timeout` | ❌ | `45` | HTTP timeout in seconds (health check always uses 5s) |
| `apiKey` | ❌ | — | Shared secret for `X-API-Key` auth |
| `models.embed` | ❌ | `all-MiniLM-L6-v2` | Default embedding model |
| `models.bertscore` | ❌ | `roberta-large` | Default BERTScore model |

---

## Agent Tools

### `gpu_health`

Check if the GPU service is reachable.

```
No parameters required.
```

**Example response:**
```json
{
  "status": "ok",
  "device": "cuda"
}
```

---

### `gpu_info`

Get detailed GPU diagnostics.

```
No parameters required.
```

**Example response:**
```json
{
  "device": "cuda",
  "device_name": "NVIDIA GeForce RTX 2080 Ti",
  "vram_total_mb": 11264,
  "vram_used_mb": 2048,
  "pytorch_version": "2.2.0+cu121",
  "cuda_version": "12.1",
  "loaded_models": ["bertscore:roberta-large", "embed:all-MiniLM-L6-v2"]
}
```

---

### `gpu_bertscore`

Compute BERTScore between candidate and reference texts.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `candidates` | `string[]` | ✅ | — | Texts to evaluate |
| `references` | `string[]` | ✅ | — | Reference texts (same length as candidates) |
| `lang` | `string` | ❌ | `en` | Language code |
| `model_type` | `string` | ❌ | `roberta-large` | BERTScore model override |

**Example:**
```json
{
  "candidates": ["The cat sat on the mat."],
  "references": ["A cat was sitting on the rug."],
  "lang": "en"
}
```

**Response:**
```json
{
  "precision": [0.9234],
  "recall": [0.9187],
  "f1": [0.9210],
  "model": "roberta-large"
}
```

---

### `gpu_embed`

Generate text embeddings using sentence-transformers.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `texts` | `string[]` | ✅ | — | Texts to embed |
| `model` | `string` | ❌ | `all-MiniLM-L6-v2` | Embedding model override |

**Example:**
```json
{
  "texts": ["OpenClaw is an AI assistant.", "GPU acceleration makes ML faster."]
}
```

**Response:**
```json
{
  "embeddings": [[0.023, -0.145, ...], [0.087, 0.312, ...]],
  "model": "all-MiniLM-L6-v2",
  "dimensions": 384
}
```

---

## API Reference

All endpoints are on the FastAPI GPU service. See the auto-generated docs at `http://<host>:8765/docs`.

| Endpoint | Method | Auth required | Description |
|---|---|---|---|
| `/health` | GET | No | Liveness check |
| `/info` | GET | Yes (if API_KEY set) | GPU diagnostics |
| `/bertscore` | POST | Yes (if API_KEY set) | BERTScore computation |
| `/embed` | POST | Yes (if API_KEY set) | Text embedding |

---

## Timeouts

| Layer | Value | Notes |
|---|---|---|
| Health check (TS client) | 5s | Fast fail |
| BERTScore / Embed (TS client) | 45s | Configurable via `timeout` |
| GPU service (uvicorn) | 65s | Exceeds client timeout |
| Concurrency limit | 2 concurrent | 503 + `Retry-After: 5` when exceeded |

---

## License

MIT — © [Elvatis](https://elvatis.com)
