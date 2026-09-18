# Antigravity Kit Architecture

> Agents, skills and rules that turn Antigravity into a team of specialists.

---

## 📋 Overview

Antigravity Kit is a modular system consisting of:

- **15 Specialist Agents** - Antigravity custom agents, run as subagents
- **39 Skills** - Domain knowledge and slash commands (`/plan`, `/debug`, `/test`, ...)
- **2 Rules** - `GEMINI.md` (always on) and `caveman-rules.md`

Antigravity deprecated workflows and retires them on 1 November 2026: every former workflow of the kit is now a skill with the same slash command.

---

## 🏗️ Directory Structure

```plaintext
.agents/
├── ARCHITECTURE.md          # This file
├── agents/                  # 15 Specialist Agents (custom agents)
├── skills/                  # 39 Skills (also slash commands)
├── rules/                   # GEMINI.md (always on), caveman-rules.md
├── scripts/                 # 4 Master Scripts
└── .ag-kit.json             # Written by the installer: what the kit installed
```

The installer only replaces its own agents, skills, rules and scripts: a project's own files in `.agents/` are kept.

---

## 🤖 Agents (15)

Antigravity custom agents (`.agents/agents/<name>.md`): the frontmatter sets the tools (Antigravity names), the model (`inherit`) and the skills (`skills/<name>`); the body is the system prompt. `GEMINI.md` routes every request through `intelligent-routing` and delegates with `invoke_subagent`; where custom agents are not available (the Antigravity IDE, for now) the agent file is read and applied directly.

| Agent | Focus | Skills |
| ----- | ----- | ------ |
| `orchestrator` | Multi-agent coordination | clean-code, parallel-agents, brainstorm, architecture, powershell-windows |
| `project-planner` | Discovery, task planning | clean-code, app-builder, brainstorm |
| `explorer-agent` | Codebase analysis | clean-code, architecture, brainstorm, debug |
| `frontend-specialist` | Web UI/UX, performance, SEO | clean-code, nextjs-react-expert, web-design-guidelines, tailwind-patterns, frontend-design, scroll-film |
| `backend-specialist` | API, database, security review, deployment | clean-code, nodejs-best-practices, python-patterns, api-patterns, database-design, powershell-windows, rust-pro |
| `api-designer` | API contracts, OpenAPI | clean-code, api-patterns, nodejs-best-practices |
| `mobile-developer` | iOS, Android, RN, Flutter | clean-code, mobile-design |
| `test-engineer` | Testing strategies, TDD | clean-code, test, webapp-testing |
| `qa-automation-engineer` | E2E testing, CI test jobs | clean-code, webapp-testing, test, web-design-guidelines |
| `debugger` | Root cause analysis | clean-code, debug |
| `ai-ml-engineer` | LLM, RAG, prompts; classical ML and data mining | clean-code, prompt-engineering, classic-ml, api-patterns |
| `scroll-experience-architect` | Scroll experiences 3D/cinematic/video | three-js, scroll-film, scroll-world |
| `latex-specialist` | Academic LaTeX, papers | clean-code, latex-tutor, latex-review, html-it |
| `documentation-writer` | Docs (only on request) | clean-code, html-it |
| `product-owner` | Requirements, user stories, backlog, MVP | clean-code, brainstorm |

There is no dedicated security, performance, SEO, database or DevOps agent: security reviews, schema and deployment belong to `backend-specialist`, web performance and SEO to `frontend-specialist`.

---

## ⌨️ Commands (16)

Skills written to be invoked by name. Antigravity also loads them on its own when the request matches their description.

| Command              | Description                                             |
| -------------------- | ------------------------------------------------------- |
| `/brainstorm`        | Socratic Gate and option exploration                    |
| `/plan`              | Plan into `docs/PLAN-{slug}.md`, no code                |
| `/create`            | Create a new app                                        |
| `/enhance`           | Add or change features in an existing app               |
| `/orchestrate`       | Multi-agent coordination                                |
| `/debug`             | Systematic bug investigation                            |
| `/test`              | Generate and run tests                                  |
| `/preview`           | Start/stop/status of the local dev server               |
| `/deploy`            | Deploy with pre-flight checks and rollback              |
| `/status`            | Project and agent status                                |
| `/caveman`           | Terse answers (on, off, lite, full, ultra)              |
| `/ui-ux-pro-max`     | Design with the searchable design database              |
| `/html-it`           | HTML output instead of markdown                         |
| `/latex`             | Academic LaTeX writing/review                           |
| `/scroll-film`       | Animated scroll-film sites                              |
| `/scroll-experience` | Unifies three-js + scroll-film + scroll-world           |

`/classic-ml` also works: it is a knowledge skill (below) with a command-like name.

---

## 🧩 Skills (39)

The 16 commands above plus 23 knowledge skills that agents load from their frontmatter or that Antigravity picks by description.

### Core

| Skill                  | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `intelligent-routing`  | Picks the right agent(s) and hands the task off   |
| `clean-code`           | Coding standards (global)                         |
| `parallel-agents`      | Multi-agent orchestration patterns                |

### Frontend & UI

| Skill                   | Description                                             |
| ----------------------- | ------------------------------------------------------- |
| `nextjs-react-expert`   | React & Next.js performance optimization (Vercel rules) |
| `web-design-guidelines` | Web UI audit - accessibility, UX, performance           |
| `tailwind-patterns`     | Tailwind CSS v4 utilities                               |
| `frontend-design`       | UI/UX patterns, design systems                          |

### Scroll Experiences

| Skill          | Description                                                       |
| -------------- | ----------------------------------------------------------------- |
| `three-js`     | Scroll-driven Three.js/WebGL scenes — scene, camera, scroll, perf |
| `scroll-world` | "Fly through the world" landing pages from pre-rendered video     |

### Backend & API

| Skill                   | Description                    |
| ----------------------- | ------------------------------ |
| `api-patterns`          | REST, GraphQL, tRPC            |
| `nodejs-best-practices` | Node.js async, modules         |
| `python-patterns`       | Python standards, FastAPI      |
| `rust-pro`              | Modern async Rust, systems     |
| `database-design`       | Schema design, indexing, ORMs  |
| `powershell-windows`    | Windows PowerShell pitfalls    |

### Testing & Mobile

| Skill            | Description           |
| ---------------- | --------------------- |
| `webapp-testing` | E2E, Playwright       |
| `mobile-design`  | Mobile UI/UX patterns |

### AI & Data

| Skill                | Description                                                        |
| -------------------- | ------------------------------------------------------------------ |
| `prompt-engineering` | LLM prompts, RAG, design                                           |
| `classic-ml`         | Data mining and classical ML with pandas and scikit-learn          |

### Academic

| Skill          | Description                         |
| -------------- | ----------------------------------- |
| `latex-tutor`  | LaTeX textbook chapters from slides |
| `latex-review` | LaTeX project audit & QA            |

### Architecture & Planning

| Skill          | Description                  |
| -------------- | ---------------------------- |
| `app-builder`  | Full-stack app scaffolding   |
| `architecture` | System design, ADRs          |

---

## 🎯 Skill Loading Protocol

```plaintext
User Request → Skill Description Match (or /name) → Load SKILL.md
                                                        ↓
                                                Read references/
                                                        ↓
                                                  Run scripts/
```

### Skill Structure

```plaintext
skill-name/
├── SKILL.md           # (Required) Metadata & instructions, under 500 lines
├── scripts/           # (Optional) Python/Bash/JS scripts
├── references/        # (Optional) Templates, docs
└── data/, assets/     # (Optional) Data files, images
```

`SKILL.md` follows the Agent Skills spec: `name` equals the folder name (lowercase letters, digits, hyphens), `description` says what the skill does and when to use it.

---

## 📊 Scripts

### Master Scripts (4)

| Script               | Purpose                                                   | When to Use              |
| -------------------- | --------------------------------------------------------- | ------------------------ |
| `checklist.py`       | Core checks: schema, tests, UX (+ E2E with `--url`)       | Development, pre-commit  |
| `verify_all.py`      | Full suite: core checks + API, accessibility, E2E, mobile | Pre-deployment, releases |
| `auto_preview.py`    | Start/stop/status of the dev server (`/preview`)          | Local preview            |
| `session_manager.py` | Project status: stack, files, stats (`/status`)           | Any time                 |

```bash
# Quick validation during development
python .agents/scripts/checklist.py .

# Full verification before deployment
python .agents/scripts/verify_all.py . --url http://localhost:3000
```

The audit scripts skip `node_modules/`, build folders and `.agents/` itself.

### Skill Scripts (15)

| Skill                 | Script                                  | Purpose                                   |
| --------------------- | --------------------------------------- | ----------------------------------------- |
| `api-patterns`        | `api_validator.py`                      | API best-practice checks                  |
| `database-design`     | `schema_validator.py`                   | Prisma / Drizzle schema checks            |
| `frontend-design`     | `ux_audit.py`                           | UX psychology + accessibility audit       |
| `frontend-design`     | `accessibility_checker.py`              | WCAG checks                               |
| `mobile-design`       | `mobile_audit.py`                       | Touch targets, mobile patterns            |
| `nextjs-react-expert` | `react_performance_checker.py`          | Static React performance hints            |
| `nextjs-react-expert` | `convert_rules.py`                      | Rebuilds the rule files                   |
| `test`                | `test_runner.py`                        | Runs the project's test suite             |
| `webapp-testing`      | `playwright_runner.py`                  | E2E smoke test of a running URL           |
| `ui-ux-pro-max`       | `search.py`, `core.py`, `design_system.py` | Searches the design database in `data/` |
| `scroll-film`         | `assemble.sh`, `chain-step.sh`          | Video chain assembly (bash, ffmpeg ≥ 5.1) |
| `scroll-film`         | `verify.js`                             | Screenshots + jank test (puppeteer-core)  |

`scroll-world/references/` also ships `knockout.py` (background removal) and `scrub-engine.js` (the scrub engine).

---

## 📊 Statistics

| Metric              | Value                           |
| ------------------- | ------------------------------- |
| **Total Agents**    | 15                              |
| **Total Skills**    | 39 (16 commands)                |
| **Total Rules**     | 2                               |
| **Total Scripts**   | 4 (master) + 15 (skill-level)   |

Counts are checked by `.github/scripts/validate_kit.py` in CI.

---

## 🔗 Quick Reference

| Need         | Agent                         | Skills                                 |
| ------------ | ----------------------------- | -------------------------------------- |
| Web App      | `frontend-specialist`         | nextjs-react-expert, frontend-design   |
| API          | `backend-specialist`          | api-patterns, nodejs-best-practices    |
| Database     | `backend-specialist`          | database-design                        |
| Deploy       | `backend-specialist`          | deploy                                 |
| Mobile       | `mobile-developer`            | mobile-design                          |
| Testing      | `test-engineer`               | test, webapp-testing                   |
| E2E          | `qa-automation-engineer`      | webapp-testing                         |
| Debug        | `debugger`                    | debug                                  |
| Plan         | `project-planner`             | brainstorm, app-builder                |
| AI / LLM     | `ai-ml-engineer`              | prompt-engineering                     |
| ML / Data    | `ai-ml-engineer`              | classic-ml                             |
| Scroll / 3D  | `scroll-experience-architect` | three-js, scroll-film, scroll-world    |
| LaTeX        | `latex-specialist`            | latex-tutor, latex-review              |
