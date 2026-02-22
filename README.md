# @elvatis/openclaw-gpu-bridge

OpenClaw plugin to offload GPU-intensive ML tasks to a remote machine on the local network.

## What it does

Exposes a remote GPU compute service as an OpenClaw agent tool. The plugin connects to a FastAPI microservice running on a GPU-equipped machine and routes heavy workloads (BERTScore, embeddings, inference) through it instead of the local CPU.

## Use cases

- **BERTScore computation** for BMAS-style research pipelines
- **Text embeddings** (sentence-transformers, OpenAI-compatible API)
- **Local model inference** (any transformers model running on the GPU machine)

## Architecture

```
OpenClaw (CPU host)
  └── @elvatis/openclaw-gpu-bridge plugin
        └── HTTP → GPU PC (local network)
              └── FastAPI service (gpu-service.py)
                    └── bert-score / transformers / CUDA
```

## Installation

```bash
openclaw plugins install @elvatis/openclaw-gpu-bridge
```

## Configuration

```json
{
  "plugins": {
    "entries": {
      "openclaw-gpu-bridge": {
        "config": {
          "serviceUrl": "http://192.168.x.x:8765",
          "timeout": 120,
          "apiKey": "optional-secret"
        }
      }
    }
  }
}
```

## GPU Service Setup (on the GPU machine)

See `gpu-service/README.md` for setup instructions (Python + FastAPI + CUDA).

## Status

Work in progress. See `.ai/handoff/STATUS.md` for current build state.
