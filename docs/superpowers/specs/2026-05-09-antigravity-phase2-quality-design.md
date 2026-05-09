# Antigravity Kit — Phase 2: Prompt Quality Enhancement

**Date:** 2026-05-09
**Scope:** Phase 2 — Quality (Layer-by-Layer, step 2 of 3)

## Objective

Improve agent prompt quality by adding concrete examples, anti-hallucination guardrails, and eliminating agent↔skill redundancy. Focus on the 7 weakest agents first, then global improvements.

## Batch 1 — Strengthen 7 thin agents (<120 lines)

For each: `explorer-agent`, `product-owner`, `documentation-writer`, `code-archaeologist`, `qa-automation-engineer`, `product-manager`, `seo-specialist`

**Add to each:**
- 1-2 `EXAMPLE:` blocks showing real input→expected output
- Review checklist (if missing)
- Anti-patterns section (if missing)

**Agent-specific additions:**
- `explorer-agent`: search patterns, output format template
- `product-owner`: RICE/MoSCoW prioritization, MVP scoping, backlog structure
- `documentation-writer`: README template, API doc template, llms.txt format, good vs bad examples
- `code-archaeologist`: dependency mapping template, refactoring decision tree
- `qa-automation-engineer`: CI pipeline YAML, Playwright code snippets, flakiness debug guide
- `product-manager`: user story template, acceptance criteria format, PRD structure
- `seo-specialist`: meta tag templates, schema.org JSON-LD examples, audit checklist

## Batch 2 — Anti-hallucination guardrails on all 20 agents

Add before "When You Should Be Used" section:

```
## Never Invent

- Never reference fake APIs, packages, or libraries
- Never invent configuration keys or CLI flags
- Verify package versions exist before suggesting
- When unsure, delegate to correct domain agent via intelligent-routing
```

## Batch 3 — Eliminate 3 worst agent↔skill redundancies

| Pair | Overlap | Action |
|------|---------|--------|
| devops-engineer ↔ deployment-procedures | ~70% | Agent keeps checklists + safety warnings + emergency response. Delegates platform selection, 5-phase process, rollback strategies to `@[skills/deployment-procedures]`. |
| database-architect ↔ database-design | ~50% | Agent keeps DB platform selection (Neon/Turso/etc) + vector DB. Delegates normalization, indexing strategy, schema design to `@[skills/database-design]`. |
| frontend-specialist ↔ frontend-design | ~40% | Agent keeps React/Next.js/TypeScript. Delegates color systems, typography, design thinking process to `@[skills/frontend-design]`. |

## Not included

- New agents or skills (Phase 3)
- Creation of missing scripts (Phase 3)
- Web app modifications

## Execution order

1. Batch 1: 7 thin agents
2. Batch 2: Anti-hallucination on all 20
3. Batch 3: Redundancy elimination (3 pairs)
