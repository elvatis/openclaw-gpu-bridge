# openclaw-gpu-bridge — Status

> Last updated: 2026-02-22 (initial setup)
> Phase: P0 — Project initialized, not yet started

## Project Overview

**Package:** `@elvatis/openclaw-gpu-bridge`
**Repo:** https://github.com/homeofe/openclaw-gpu-bridge
**Purpose:** Expose remote GPU compute (via FastAPI microservice) as OpenClaw agent tools.

## Build Health

| Component         | Status       | Notes                              |
| ----------------- | ------------ | ---------------------------------- |
| Repo / Structure  | (Verified)   | Initialized 2026-02-22             |
| Plugin manifest   | (Unknown)    | Not yet created                    |
| TypeScript setup  | (Unknown)    | Not yet created                    |
| GPU service (Py)  | (Unknown)    | FastAPI stub needed                |
| Agent tools       | (Unknown)    | Not yet implemented                |
| Tests             | (Unknown)    | Not yet created                    |
| npm publish       | (Unknown)    | Not yet published                  |

## Architecture Decision

- **Plugin side (Node.js/TS):** Registers agent tools (bertscore, embed, infer) that call the GPU service via HTTP
- **GPU service (Python):** FastAPI + bert-score + transformers + CUDA, runs on GPU machine
- **Communication:** REST (JSON), optional API key auth
- **Config:** serviceUrl, timeout, apiKey

## Open Questions

- GPU machine OS and CUDA version (Emre to provide)
- IP/hostname of GPU machine on local network
- Which ML tasks to support first (BERTScore confirmed; embeddings TBD)
