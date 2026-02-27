# openclaw-gpu-bridge: Trust Register

> Tracks verification status of critical system properties.
> In multi-agent pipelines, hallucinations and drift are real risks.
> Every claim here has a confidence level tied to how it was verified.

---

## Confidence Levels

| Level | Meaning |
|-------|---------|
| **verified** | An agent executed code, ran tests, or observed output to confirm this |
| **assumed** | Derived from docs, config files, or chat, not directly tested |
| **untested** | Status unknown; needs verification |

---

## Build System

| Property | Status | Last Verified | TTL | Expires | Agent | Notes |
|----------|--------|---------------|-----|---------|-------|-------|
| `npm run build` passes | verified | 2026-02-23 | 7d | 2026-03-02 | Sonnet | 0 TS errors |
| `npm test` passes | verified | 2026-02-23 | 7d | 2026-03-02 | Sonnet | 3/3 Jest tests |
| TypeScript strict mode | verified | 2026-02-23 | 30d | 2026-03-25 | Sonnet | tsconfig strict=true |

---

## Infrastructure

| Property | Status | Last Verified | TTL | Expires | Agent | Notes |
|----------|--------|---------------|-----|---------|-------|-------|
| GPU service starts (uvicorn) | assumed | 2026-02-22 | 7d | 2026-03-01 | Sonnet | Live test at 192.168.177.3 - RTX 2080 Ti CUDA |
| /health endpoint responds | verified | 2026-02-22 | 7d | 2026-03-01 | Sonnet | Live test confirmed |
| /bertscore F1 returns correct value | verified | 2026-02-22 | 14d | 2026-03-08 | Sonnet | F1=0.9645 live test |
| Multi-host config works | untested | - | - | - | - | Never tested against 2+ real hosts |
| Failover triggers on host death | untested | - | - | - | - | Only unit test mock |

---

## Integrations

| Property | Status | Last Verified | TTL | Expires | Agent | Notes |
|----------|--------|---------------|-----|---------|-------|-------|
| OpenClaw plugin install | assumed | 2026-02-25 | 7d | 2026-03-04 | openclaw-ops | openclaw.extensions added |
| npm package published | untested | - | - | - | - | Not yet published |

---

## Security

| Property | Status | Last Verified | TTL | Expires | Agent | Notes |
|----------|--------|---------------|-----|---------|-------|-------|
| X-API-Key auth middleware | verified | 2026-02-22 | 30d | 2026-03-23 | Sonnet (P4) | Reviewed - no bypass possible |
| No injection risks | verified | 2026-02-22 | 30d | 2026-03-23 | Sonnet (P4) | Model names from app.state, not user input |
| No secrets in source | assumed | 2026-02-26 | 7d | 2026-03-05 | - | API_KEY from env var only |

---

## Update Rules (for agents)

- Change `untested` - `verified` only after **running actual code/tests**
- Change `assumed` - `verified` after direct confirmation
- Never downgrade `verified` without explaining why in `LOG.md`
- Add new rows when new system properties become critical

---

*Trust degrades over time. Re-verify periodically, especially after major refactors.*
