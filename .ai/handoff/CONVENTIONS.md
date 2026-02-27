# openclaw-gpu-bridge: Agent Conventions

> Every agent working on this project must read and follow these conventions.
> Update this file whenever a new standard is established.

---

## Language

- All code, comments, commits, and documentation in **English only**

## Code Style

- **TypeScript:** strict mode, Node 18+ native fetch (no external HTTP libs), Prettier formatting
- **Python:** FastAPI + Pydantic v2, asyncio.to_thread for blocking GPU ops, type annotations required

## Branching & Commits

```
feat/<scope>-<short-name>    - new feature
fix/<scope>-<short-name>     - bug fix
docs/<scope>-<short-name>    - documentation only
refactor/<scope>-<name>      - no behaviour change

Commit format:
  feat(scope): add description [AAHP-auto]
  fix(scope): resolve issue [AAHP-fix]
```

## Architecture Principles

- **TypeScript plugin** calls Python GPU service via HTTP (never direct GPU access from TS)
- **Python service** handles all GPU compute; exposes REST API only
- **asyncio.to_thread** required for all blocking GPU inference calls (never call sync GPU in async handler)
- **Multi-host config** uses `hosts[]` array; v0.1 `serviceUrl`/`url` compatibility maintained
- **X-API-Key** for auth; if API_KEY env var not set, no auth required (local LAN mode)

## Testing

- All TypeScript changes must maintain or improve Jest test coverage (`npm test`)
- Python changes: add pytest tests for new endpoints/logic
- `npm run build` must pass (0 TS errors) before every commit

## Formatting

- **No em dashes (`-`)**: Never use Unicode em dashes in any file. Use a regular hyphen (`-`) instead.

## What Agents Must NOT Do

- Push directly to `main`
- Install new dependencies without documenting the reason in LOG.md
- Write secrets or credentials into source files
- Delete existing tests (fix or replace instead)
- Call blocking sync GPU ops in async FastAPI handlers (use asyncio.to_thread)
- Use em dashes (`-`) anywhere in the codebase

---

*This file is maintained by agents and humans together. Update it when conventions evolve.*
