# openclaw-gpu-bridge: Autonomous Multi-Agent Workflow

> Based on the [AAHP Protocol](https://github.com/homeofe/AAHP).
> No manual triggers. Agents read `handoff/DASHBOARD.md` and work autonomously.

---

## Agent Roles

| Agent | Model | Role | Responsibility |
|-------|-------|------|---------------|
| Researcher | perplexity/sonar-pro | Researcher | GPU library research, Python/TS ecosystem |
| Architect | claude-opus | Architect | System design, ADRs, interface definitions |
| Implementer | claude-sonnet | Implementer | Code, tests, refactoring, commits |
| Reviewer | gpt-4 or second model | Reviewer | Second opinion, edge cases, security review |

---

## The Pipeline

### Phase 1: Research & Context

```
Reads:   handoff/NEXT_ACTIONS.md or DASHBOARD.md (top unblocked task)
         handoff/STATUS.md (current project state)
         handoff/ADR.md (architecture decisions)

Does:    Researches relevant libraries / PyTorch updates / CUDA changes
         Checks compatibility requirements

Writes:  handoff/LOG.md - research findings + recommendation
```

### Phase 2: Architecture Decision

```
Reads:   Research output from LOG.md
         handoff/ADR.md (existing decisions)
         Source files

Does:    Defines interface changes
         Updates ADR.md if decisions change

Writes:  handoff/LOG.md - ADR update or new ADR entry
```

### Phase 3: Implementation

```
Reads:   ADR from LOG.md or ADR.md
         CONVENTIONS.md (MANDATORY before first commit)

Does:    Creates feature branch: git checkout -b feat/<scope>-<name>
         Writes code + unit tests
         Runs: npm run build && npm test
         Commits and pushes branch

Commit format:
  feat(scope): description [AAHP-auto]
  fix(scope): description [AAHP-fix]
```

### Phase 4: Discussion Round

```
All agents review the completed code.

Architect  - "Does the implementation match the ADR?"
Reviewer   - "Any asyncio bugs? Security issues? Edge cases?"

Outcome documented in LOG.md and REVIEW.md
```

### Phase 5: Completion & Handoff

```
DASHBOARD.md:    Update build status, pipeline state
STATUS.md:       Update component status (Verified / Assumed / Unknown)
LOG.md:          Append session summary
NEXT_ACTIONS.md: Check off completed task, add new tasks with T-IDs

Git:     Branch pushed, PR-ready
```

---

## Autonomy Boundaries

| Allowed | Not allowed |
|---------|-------------|
| Write & commit code | Push directly to `main` |
| Write & run tests | Install new dependencies without documenting |
| Push feature branches | Write secrets into source |
| Research & propose OSS libraries | Perform npm publish without human review |
| Make architecture decisions | Call blocking GPU ops in async handlers |

---

*This document lives in the repo and is continuously refined by the agents themselves.*
