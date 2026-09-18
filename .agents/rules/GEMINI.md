---
trigger: always_on
---

# GEMINI.md - Antigravity Kit

> This file defines how the AI behaves in this workspace.

---

## CRITICAL: AGENT & SKILL PROTOCOL (START HERE)

> **MANDATORY:** You MUST read the appropriate agent file and its skills BEFORE performing any implementation. This is the highest priority rule.

### 1. Modular Skill Loading Protocol

Agent activated → Check frontmatter "skills:" → Read SKILL.md (INDEX) → Read specific sections.

- **Selective Reading:** DO NOT read ALL files in a skill folder. Read `SKILL.md` first, then only read sections matching the user's request.
- **Rule Priority:** P0 (GEMINI.md) > P1 (Agent .md) > P2 (SKILL.md). All rules are binding.

### 2. Enforcement Protocol

1. **When agent is activated:**
    - ✅ Activate: Read Rules → Check Frontmatter → Load SKILL.md → Apply All.
2. **Forbidden:** Never skip reading agent rules or skill instructions. "Read → Understand → Apply" is mandatory.

---

## 🤖 INTELLIGENT AGENT ROUTING

**ALWAYS ACTIVE: Before responding to ANY request, automatically analyze and select the best agent(s).**

> 🔴 **MANDATORY:** You MUST follow the protocol defined in `@[skills/intelligent-routing]` for Request Classification and Agent Routing. This rule is **always_on** and must execute before every response.

---

## TIER 0: UNIVERSAL RULES (Always Active)

### 🌐 Language Handling

When user's prompt is NOT in English:

1. **Internally translate** for better comprehension
2. **Respond in user's language** - match their communication
3. **Code comments/variables** remain in English

### 🧹 Clean Code (Global Mandatory)

**ALL code MUST follow `@[skills/clean-code]` rules. No exceptions.**

- **Code**: Concise, direct, no over-engineering. Self-documenting.
- **Testing**: Mandatory. Pyramid (Unit > Int > E2E) + AAA Pattern.
- **Performance**: Measure first. Adhere to 2025 standards (Core Web Vitals).
- **Infra/Safety**: 5-Phase Deployment. Verify secrets security.

### 📁 File Dependency Awareness

**Before modifying ANY file:**

1. Find what depends on it: search for its imports/usages (and, if the project has a `CODEBASE.md`, read its File Dependencies section)
2. Identify dependent files
3. Update ALL affected files together

### 🗺️ System Map Read

> 🔴 **MANDATORY:** Read `.agents/ARCHITECTURE.md` at session start to understand Agents, Skills, and Scripts.

**Path Awareness:**

- Agents: `.agents/` (Project)
- Skills: `.agents/skills/` (Project)
- Runtime Scripts: `.agents/skills/<skill>/scripts/`

### 🧠 Read → Understand → Apply

```
❌ WRONG: Read agent file → Start coding
✅ CORRECT: Read → Understand WHY → Apply PRINCIPLES → Code
```

---

## TIER 1: CODE RULES (When Writing Code)

### 🛑 Socratic Gate

**MANDATORY: Every user request must pass through the Socratic Gate before ANY tool use or implementation.**

| Request Type            | Strategy       | Required Action                                                   |
| ----------------------- | -------------- | ----------------------------------------------------------------- |
| **New Feature / Build** | Discovery      | ASK up to 3 strategic questions on what you cannot infer (purpose, users, scope) |
| **Code Edit / Bug Fix** | Context Check  | Confirm understanding; ask about impact only if it is unclear     |
| **Vague / Simple**      | Clarification  | Ask only what is missing among purpose, users and scope           |
| **Full Orchestration**  | Gatekeeper     | **STOP** subagents until user confirms plan details               |
| **Direct "Proceed"**    | Validation     | Proceed. Raise an edge case (max 1-2) only if it would change the implementation |

**Protocol:**

1. **Never Assume:** If something that would change the result is unclear, ASK. If the request already answers it, state your assumption and move on.
2. **Handle Spec-heavy Requests:** When the user gives detailed answers (Answers 1, 2, 3...), do not re-ask them. Mention a **Trade-off** or **Edge Case** only when it changes what you will build (e.g., "LocalStorage confirmed: should old data be migrated when the format changes?").
3. **Wait:** Do NOT invoke subagents or write code while a blocking question is open.
4. **Reference:** Full protocol in `@[skills/brainstorming]`.
5. **Proportion:** The orchestrator and the planner follow the same rule: 1-2 quick questions when the request is mostly clear, more only for open-ended builds.

### 🏁 Final Checklist Protocol

**Trigger:** When the user says "final checks", "run all checks", "controlli finali", or similar phrases in any language.

| Task Stage       | Command                                            | Purpose                        |
| ---------------- | -------------------------------------------------- | ------------------------------ |
| **Manual Audit** | `python .agents/scripts/checklist.py .`             | Core checks: schema, tests, UX |
| **Pre-Deploy**   | `python .agents/scripts/verify_all.py . --url <URL>` | Full suite + E2E              |

**Priority Execution Order:**

1. **Lint & types** (project tooling: `npm run lint`, `tsc --noEmit`, `ruff`...) → 2. **Schema** → 3. **Tests** → 4. **UX** → 5. **E2E** (with `--url`)

**Rules:**

- **Completion:** A task is NOT finished until `checklist.py` returns success.
- **Reporting:** If it fails, fix the blocking failures first (tests, schema).

> 🔴 **Agents & Skills can invoke ANY script** via `python .agents/skills/<skill>/scripts/<script>.py` (See `ARCHITECTURE.md` or Agent `.md` for available scripts).

### 🎭 Gemini Mode Mapping

| Mode     | Agent             | Behavior                                     |
| -------- | ----------------- | -------------------------------------------- |
| **plan** | `project-planner` | 4-phase methodology. NO CODE before Phase 4. |
| **ask**  | -                 | Focus on understanding. Ask questions.       |
| **edit** | `orchestrator`    | Execute. Check `docs/PLAN-{slug}.md` first.  |

---

## 📁 QUICK REFERENCE

### Agents & Skills

- **Masters**: `orchestrator`, `project-planner`, `backend-specialist` (API/DB/security), `frontend-specialist` (UI/UX/performance/SEO), `mobile-developer`, `debugger`
- **Key Skills**: `clean-code`, `intelligent-routing`, `brainstorming`, `app-builder`, `frontend-design`, `mobile-design`

### Key Scripts

- **Verify**: `.agents/scripts/verify_all.py`, `.agents/scripts/checklist.py`
- **Audits**: `ux_audit.py`, `accessibility_checker.py`, `mobile_audit.py`, `schema_validator.py`, `api_validator.py`
- **Test**: `playwright_runner.py`, `test_runner.py`
