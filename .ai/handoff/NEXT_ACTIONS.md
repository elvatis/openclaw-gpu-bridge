# openclaw-gpu-bridge — Next Actions

> Prioritized by strategic importance. Top = do first.

## P1 — Research (Sonar)
- [ ] Research: best FastAPI + bert-score + transformers setup for CUDA
- [ ] Research: OpenClaw plugin agent tool patterns (plugin.md + agent-tools.md)
- [ ] Research: onnxruntime-node as alternative to Python service

## P2 — Architecture (Opus)
- [ ] Define plugin config schema (serviceUrl, timeout, apiKey, tools to expose)
- [ ] Define FastAPI endpoints: /bertscore, /embed, /health
- [ ] Define agent tool schemas for OpenClaw

## P3 — Implementation (Sonnet)
- [ ] Create package.json + tsconfig.json + openclaw.plugin.json
- [ ] Implement plugin: register tools (bertscore_compute, embed_text, health_check)
- [ ] Create gpu-service/gpu_service.py (FastAPI stub)
- [ ] Create gpu-service/requirements.txt
- [ ] Create gpu-service/README.md (setup guide for GPU machine)
- [ ] Write tests

## P4 — Docs + Publish
- [ ] Update README.md with final config examples
- [ ] npm publish @elvatis/openclaw-gpu-bridge
- [ ] Blog article: "How I tapped my GPU from OpenClaw over the network"
- [ ] Submit to OpenClaw community plugins page (PR)
