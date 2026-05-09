# Antigravity Kit — Architecture Refinement (v3)

**Date:** 2026-05-09
**Scope:** Phase 1 — Architecture (Layer-by-Layer, step 1 of 3)

## Objective

Strengthen the architectural foundations of the `.agent/` kit by eliminating redundancies, consolidating routing, and standardizing agents/skills before proceeding with quality improvements (Phase 2) and expansion (Phase 3).

## Modifications

### 1. `intelligent-routing/SKILL.md` — Becomes the single source of truth for routing

Unify into a single file:
- Request Classifier (currently in GEMINI.md)
- Domain Detection Rules (already present)
- Agent Selection Matrix (unifying GEMINI.md + orchestrate.md + orchestrator.md)
- Complexity Assessment (already present)
- Auto-Selection Protocol (already present)
- Response Format (already present)

Result: one file, one matrix, zero divergences.

### 2. `GEMINI.md` — Trim from 273 to ~90 lines

**Removed:**
- Request Classifier → delegated to intelligent-routing
- Intelligent Agent Routing + checklist → delegated to intelligent-routing
- Table of 12 scripts → each agent knows which scripts to invoke
- Project Type Routing → present in orchestrate.md / orchestrator.md

**Kept:**
- Modular Skill Loading Protocol (P0)
- Universal Tier 0: language, clean-code, file dependency, read-understand-apply
- Socratic Gate (essential)
- Final Checklist Protocol with commands
- Quick Reference (pointers, not duplicates)

**Added:**
- Explicit rule: `intelligent-routing` is **always_on**, must execute before every response.
- Explicit reference to `@[skills/intelligent-routing]` for routing.

### 3. `workflows/orchestrate.md` + `agents/orchestrator.md` — Remove duplicates

Both files duplicate the agent selection matrix.

**Removed from both:**
- Agent Selection Matrix
- Available Agents table (when duplicated)

**Added:**
- Reference to `@[skills/intelligent-routing]` for agent selection

### 4. `verify_all.py` — Leave references to future scripts

`dependency_analyzer.py` and `bundle_analyzer.py` are referenced but not yet created.
No modifications: they remain as placeholders for future development.

### 5. 20 Agents — Frontmatter standardization

For each file in `.agent/agents/`:
- Verify that every skill in `skills:` exists as a folder with `SKILL.md`
- Remove references to renamed skills (e.g. `react-best-practices` → `nextjs-react-expert`)
- Standardize the frontmatter fields based on the following expected schema:

```yaml
---
name: "string (e.g., frontend-specialist)"
description: "string (Brief description of the agent's role)"
model: "string (e.g., gemini-2.5-pro-exp)"
tools:
  - "string (e.g., read_file, run_shell_command)"
skills:
  - "string (e.g., nextjs-react-expert, clean-code)"
---
```

### 6. New file `.agent/tasks/lessons.md`

Empty template to capture post-correction patterns:
```markdown
# Lessons Learned

## Patterns to avoid
-

## Patterns to repeat
-

## Architectural decisions
-
```

## Not included in this phase

- Creation of missing scripts (Phase 3 — Expansion)
- Improvement of agent prompt quality (Phase 2 — Quality)
- New agents/skills (Phase 3 — Expansion)
- Modifications to the Next.js web app

## Execution order

1. `intelligent-routing/SKILL.md`
2. `GEMINI.md`
3. `workflows/orchestrate.md` + `agents/orchestrator.md`
4. Standardization of 20 agents
5. `.agent/tasks/lessons.md`
