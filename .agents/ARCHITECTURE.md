# Antigravity Kit Architecture

> Agents, skills and workflows that turn Antigravity into a team of specialists.

---

## 📋 Overview

Antigravity Kit is a modular system consisting of:

- **18 Specialist Agents** - Role-based AI personas
- **30 Skills** - Domain-specific knowledge modules
- **16 Workflows** - Slash command procedures

> ⚠️ Antigravity deprecated workflows: they are retired on 1 November 2026 and become skills invoked with the same `/name`. The migration of this kit is planned.

---

## 🏗️ Directory Structure

```plaintext
.agents/
├── ARCHITECTURE.md          # This file
├── agents/                  # 18 Specialist Agents
├── skills/                  # 30 Skills
├── workflows/               # 16 Slash Commands
├── rules/                   # Global Rules (GEMINI.md always on, caveman-rules.md)
├── scripts/                 # 4 Master Scripts
└── .shared/ui-ux-pro-max/   # Design database (CSV) + search.py, used by /ui-ux-pro-max
```

---

## 🤖 Agents (18)

Specialist AI personas. `GEMINI.md` routes every request through `intelligent-routing`, which lists all of them. Every agent also loads `clean-code`.

| Agent | Focus | Skills (besides clean-code) |
| ----- | ----- | --------------------------- |
| `orchestrator` | Multi-agent coordination | parallel-agents, brainstorming, architecture, powershell-windows |
| `project-planner` | Discovery, task planning | app-builder, brainstorming |
| `explorer-agent` | Codebase analysis | architecture, brainstorming, systematic-debugging |
| `frontend-specialist` | Web UI/UX, performance, SEO | nextjs-react-expert, typescript-expert, web-design-guidelines, tailwind-patterns, frontend-design, scroll-film-studio |
| `backend-specialist` | API, business logic, security review | nodejs-best-practices, typescript-expert, python-patterns, api-patterns, database-design, powershell-windows, rust-pro |
| `api-designer` | API contracts, OpenAPI | api-patterns, nodejs-best-practices |
| `database-architect` | Schema, SQL, migrations | database-design |
| `mobile-developer` | iOS, Android, RN, Flutter | mobile-design |
| `devops-engineer` | CI/CD, deploy, servers | server-management, powershell-windows |
| `test-engineer` | Testing strategies, TDD | testing-patterns, webapp-testing |
| `qa-automation-engineer` | E2E testing, CI test jobs | webapp-testing, testing-patterns, web-design-guidelines |
| `debugger` | Root cause analysis | systematic-debugging |
| `ai-ml-engineer` | LLM, RAG, prompt design | prompt-engineering, api-patterns |
| `scroll-experience-architect` | Scroll experiences 3D/cinematic/video | three-js, scroll-film-studio, scroll-world |
| `latex-specialist` | Academic LaTeX, papers | latex-tutor, latex-review, html-it |
| `documentation-writer` | Docs (only on request) | html-it |
| `product-manager` | Requirements, user stories | brainstorming |
| `product-owner` | Strategy, backlog, MVP | brainstorming |

There is no dedicated security, performance or SEO agent: security reviews belong to `backend-specialist`, web performance and SEO to `frontend-specialist`.

---

## 🧩 Skills (30)

Modular knowledge domains that agents load on demand, based on task context.

### Core (always relevant)

| Skill                  | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `intelligent-routing`  | Picks the right agent(s) for each request         |
| `clean-code`           | Coding standards (global)                         |
| `brainstorming`        | Socratic Gate, clarifying questions               |
| `parallel-agents`      | Multi-agent orchestration patterns                |
| `systematic-debugging` | 4-phase root cause analysis                       |
| `caveman-mode`         | Terse, token-efficient responses                  |

### Frontend & UI

| Skill                   | Description                                                             |
| ----------------------- | ----------------------------------------------------------------------- |
| `nextjs-react-expert`   | React & Next.js performance optimization (Vercel rules)                 |
| `web-design-guidelines` | Web UI audit - accessibility, UX, performance                           |
| `tailwind-patterns`     | Tailwind CSS v4 utilities                                               |
| `frontend-design`       | UI/UX patterns, design systems                                          |
| `typescript-expert`     | Type-level programming, performance                                     |

### Scroll Experiences

| Skill                | Description                                                            |
| -------------------- | ---------------------------------------------------------------------- |
| `three-js`           | Scroll-driven Three.js/WebGL scenes — scene, camera, scroll, perf      |
| `scroll-film-studio` | Continuous cinematic scroll-scrubbed websites (scrollytelling)         |
| `scroll-world`       | "Fly through the world" landing pages from pre-rendered video          |

### Backend & API

| Skill                   | Description                    |
| ----------------------- | ------------------------------ |
| `api-patterns`          | REST, GraphQL, tRPC            |
| `nodejs-best-practices` | Node.js async, modules         |
| `python-patterns`       | Python standards, FastAPI      |
| `rust-pro`              | Modern async Rust, systems     |
| `database-design`       | Schema design, indexing, ORMs  |

### Infrastructure & Shell

| Skill                | Description                        |
| -------------------- | ---------------------------------- |
| `server-management`  | Processes, monitoring, scaling     |
| `powershell-windows` | Windows PowerShell pitfalls        |

### Testing

| Skill              | Description              |
| ------------------ | ------------------------ |
| `testing-patterns` | Unit, integration, mocks |
| `webapp-testing`   | E2E, Playwright          |

### Mobile

| Skill           | Description           |
| --------------- | --------------------- |
| `mobile-design` | Mobile UI/UX patterns |

### AI

| Skill                | Description              |
| -------------------- | ------------------------ |
| `prompt-engineering` | LLM prompts, RAG, design |

### Academic & Publishing

| Skill          | Description                                     |
| -------------- | ----------------------------------------------- |
| `latex-tutor`  | LaTeX textbook chapters from slides             |
| `latex-review` | LaTeX project audit & QA                        |
| `html-it`      | HTML instead of markdown; HTML university notes |

### Architecture & Planning

| Skill          | Description                  |
| -------------- | ---------------------------- |
| `app-builder`  | Full-stack app scaffolding   |
| `architecture` | System design, ADRs          |

---

## 🔄 Workflows (16)

Slash command procedures. Invoke with `/command`.

| Command              | Description                                             |
| -------------------- | ------------------------------------------------------- |
| `/brainstorm`        | Socratic discovery                                      |
| `/create`            | Create new features or apps                             |
| `/debug`             | Debug issues                                            |
| `/deploy`            | Deploy application                                      |
| `/enhance`           | Improve existing code                                   |
| `/orchestrate`       | Multi-agent coordination                                |
| `/plan`              | Task breakdown into `docs/PLAN-{slug}.md`              |
| `/preview`           | Start/stop/status of the local dev server               |
| `/status`            | Check project status                                    |
| `/test`              | Generate and run tests                                  |
| `/ui-ux-pro-max`     | Design with the searchable design database              |
| `/html-it`           | HTML output instead of markdown                         |
| `/scroll-film`       | Animated scroll-film sites                              |
| `/scroll-experience` | Unifies three-js + scroll-film-studio + scroll-world    |
| `/caveman`           | Toggle Caveman Mode                                     |
| `/latex`             | Academic LaTeX writing/review                           |

---

## 🎯 Skill Loading Protocol

```plaintext
User Request → Skill Description Match → Load SKILL.md
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
└── assets/            # (Optional) Images, logos
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

### Skill Scripts

| Skill                 | Script                          | Purpose                                   |
| --------------------- | ------------------------------- | ----------------------------------------- |
| `api-patterns`        | `api_validator.py`              | API best-practice checks                  |
| `database-design`     | `schema_validator.py`           | Prisma / Drizzle schema checks            |
| `frontend-design`     | `ux_audit.py`                   | UX psychology + accessibility audit       |
| `frontend-design`     | `accessibility_checker.py`      | WCAG checks                               |
| `mobile-design`       | `mobile_audit.py`               | Touch targets, mobile patterns            |
| `nextjs-react-expert` | `react_performance_checker.py`  | Static React performance hints            |
| `nextjs-react-expert` | `convert_rules.py`              | Rebuilds the rule files                   |
| `testing-patterns`    | `test_runner.py`                | Runs the project's test suite             |
| `webapp-testing`      | `playwright_runner.py`          | E2E smoke test of a running URL           |
| `scroll-film-studio`  | `assemble.sh`, `chain-step.sh`  | Video chain assembly (bash, ffmpeg ≥ 5.1) |
| `scroll-film-studio`  | `verify.js`                     | Screenshots + jank test (puppeteer-core)  |

`scroll-world/references/` also ships `knockout.py` (background removal) and `scrub-engine.js` (the scrub engine).

---

## 📊 Statistics

| Metric              | Value                           |
| ------------------- | ------------------------------- |
| **Total Agents**    | 18                              |
| **Total Skills**    | 30                              |
| **Total Workflows** | 16                              |
| **Total Scripts**   | 4 (master) + 12 (skill-level)   |

Counts are checked by `.github/scripts/validate_kit.py` in CI.

---

## 🔗 Quick Reference

| Need         | Agent                         | Skills                                 |
| ------------ | ----------------------------- | -------------------------------------- |
| Web App      | `frontend-specialist`         | nextjs-react-expert, frontend-design   |
| API          | `backend-specialist`          | api-patterns, nodejs-best-practices    |
| Mobile       | `mobile-developer`            | mobile-design                          |
| Database     | `database-architect`          | database-design                        |
| Testing      | `test-engineer`               | testing-patterns, webapp-testing       |
| E2E          | `qa-automation-engineer`      | webapp-testing                         |
| Debug        | `debugger`                    | systematic-debugging                   |
| Plan         | `project-planner`             | brainstorming, app-builder             |
| AI / LLM     | `ai-ml-engineer`              | prompt-engineering                     |
| Scroll / 3D  | `scroll-experience-architect` | three-js, scroll-film-studio, scroll-world |
| LaTeX        | `latex-specialist`            | latex-tutor, latex-review              |
