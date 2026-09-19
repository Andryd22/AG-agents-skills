---
name: intelligent-routing
description: Automatic agent selection and task routing. Classifies each request, picks the specialist agent(s) from .agents/agents/ and hands the task off with invoke_subagent, without the user having to mention agents.
metadata:
  version: "2.0.0"
---

# Intelligent Agent Routing

**Purpose**: analyze each request and route it to the right specialist agent(s) without requiring explicit user mentions.

> **The AI acts as a project manager**: it classifies the request, picks the specialists and hands the work off with full context.

## 1. Request Classifier

**Before ANY action, classify the request:**

| Request Type | Trigger Keywords | Active Tiers | Result |
| --- | --- | --- | --- |
| **QUESTION** | "what is", "how does", "explain" | TIER 0 only | Text Response |
| **SURVEY/INTEL** | "analyze", "list files", "overview" | TIER 0 + Explorer | Session Intel (No File) |
| **SIMPLE CODE** | "fix", "add", "change" (single file) | TIER 0 + TIER 1 (lite) | Inline Edit |
| **COMPLEX CODE** | "build", "create", "implement", "refactor" | TIER 0 + TIER 1 (full) + Agent | **`docs/PLAN-{slug}.md` required** |
| **DESIGN/UI** | "design", "UI", "page", "dashboard" | TIER 0 + TIER 1 + Agent | **`docs/PLAN-{slug}.md` required** |
| **SLASH CMD** | /create, /orchestrate, /debug, ... | The skill with that name | Variable |

## 2. Agent Selection Matrix

**Use this matrix to select agents.** It lists every agent in `.agents/agents/`; keep it complete when agents are added or removed.

| User Intent | Keywords / Domain | Selected Agent(s) (minimum) | Auto-invoke? |
| --- | --- | --- | --- |
| **Authentication** | "login", "auth", "signup", "password", "jwt" | `backend-specialist` + `test-engineer` | ✅ YES |
| **UI Component** | "button", "card", "layout", "style" | `frontend-specialist` | ✅ YES |
| **Mobile UI** | "screen", "navigation", "touch", "gesture" | `mobile-developer` | ✅ YES |
| **Web App** | "webapp", "nextjs", "react", "vue" | `frontend-specialist` + `backend-specialist` + `test-engineer` | ⚠️ ASK FIRST |
| **API Design** | "API design", "OpenAPI", "contract", "versioning" | `api-designer` | ✅ YES |
| **API Endpoint** | "endpoint", "route", "POST", "GET" | `backend-specialist` + `test-engineer` | ✅ YES |
| **Database** | "schema", "migration", "query", "table" | `backend-specialist` | ✅ YES |
| **Bug Fix** | "error", "bug", "not working", "broken" | `debugger` + `explorer-agent` + `test-engineer` | ✅ YES |
| **Unit/Integration** | "test", "coverage", "unit", "tdd" | `test-engineer` | ✅ YES |
| **E2E / QA** | "e2e", "playwright", "cypress", "regression" | `qa-automation-engineer` | ✅ YES |
| **Deployment** | "deploy", "production", "CI/CD", "docker" | `backend-specialist` (with the `deploy` skill) | ✅ YES |
| **Security Review** | "security", "vulnerability", "owasp" | `backend-specialist` (no dedicated security agent) | ✅ YES |
| **Performance** | "slow", "optimize", "performance", "speed" | `frontend-specialist` (web) or `backend-specialist` (server) | ✅ YES |
| **SEO / Web Vitals** | "seo", "meta", "core web vitals", "sitemap" | `frontend-specialist` | ✅ YES |
| **AI / LLM** | "LLM", "RAG", "prompt", "embedding", "AI agent" | `ai-ml-engineer` | ✅ YES |
| **ML / Data Mining** | "scikit-learn", "classification", "clustering", "pandas", "association rules", "cross-validation" | `ai-ml-engineer` (with the `classic-ml` skill) | ✅ YES |
| **Scroll Experience** | "scrollytelling", "3D scroll", "fly-through", "WebGL" | `scroll-experience-architect` | ✅ YES |
| **LaTeX / Academic** | "latex", "lecture notes", "slides to chapter", "thesis", "paper", "tikz" | `latex-specialist` | ✅ YES |
| **Documentation** | "README", "API docs", "changelog" | `documentation-writer` | ❌ ONLY IF ASKED |
| **Codebase Survey** | "analyze repo", "explain codebase", "map structure" | `explorer-agent` | ✅ YES |
| **Requirements** | "user story", "acceptance criteria", "specs", "backlog", "roadmap", "MVP", "PRD" | `project-planner` | ✅ YES |
| **Planning** | "plan", "break down", "task list" | `project-planner` | ✅ YES |
| **Full Stack** | "build app", "fullstack", "platform" | `project-planner` + `frontend-specialist` + `backend-specialist` | ⚠️ ASK FIRST |
| **New Feature** | "build", "create", "implement", "new app" | `orchestrator` → multi-agent | ⚠️ ASK FIRST |
| **Complex Task** | Multiple domains detected | `orchestrator` → multi-agent | ⚠️ ASK FIRST |

**Multi-domain rule:** if the request matches 2+ domains from different rows (e.g. "secure login with dark mode UI" = backend + frontend), route to `orchestrator`, which plans first and then coordinates the specialists.

## 3. Handing Off

- **Native (Antigravity app and CLI):** call `invoke_subagent` with the agent's name. The subagent starts with a clean context, so the prompt must contain the user's request in full, the decisions already taken (answers to the Socratic Gate), the relevant files and, if one exists, the plan in `docs/PLAN-{slug}.md`.
- **Fallback (no custom agents, e.g. the Antigravity IDE until it supports them):** read `.agents/agents/<name>.md` and the `SKILL.md` of each skill in its frontmatter, then answer applying them.
- **Questions and trivial edits** need no agent: answer directly.

## 4. Complexity

| Level | Signals | Action |
| ------- | --------- | -------- |
| **SIMPLE** | One file, one domain, clear task ("fix the login button style") | One agent |
| **MODERATE** | 2-3 files, 2 domains, clear requirements ("add a profile endpoint") | The relevant agents in sequence |
| **COMPLEX** | Many files/domains, architectural choices, unclear requirements ("build a social app") | `orchestrator`, which asks the Socratic questions first |

## 5. Rules

1. **Silent analysis:** do not announce "I'm analyzing your request...".
2. **Say which agents and skills are applied**, in the first line of the answer, as defined in "Announce Agents and Skills" in `rules/GEMINI.md`:

   ```text
   🤖 @backend-specialist + @test-engineer · 📚 api-patterns, test
   ```

   Before a hand-off write `↪ @<agent>: <task>`, when it returns `↩ @<agent>`.

3. **Override:** an explicit mention wins ("Use @backend-specialist to review this").
4. **Socratic Gate first:** routing never skips the questions in GEMINI.md when something that changes the result is unclear.
5. **Priority:** GEMINI.md rules > intelligent-routing.

## 6. Edge Cases

| Case | Example | Action |
| ------ | --------- | -------- |
| Generic question | "How does React work?" | No agent, answer directly |
| Very vague | "Make it better" | Ask what to improve, then route |
| Contradictory | "Add mobile support to the web app" | Ask: responsive web or native app? Then route |
