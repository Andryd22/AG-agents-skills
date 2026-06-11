---
name: latex
description: Write or review academic LaTeX. Delegates to the latex-specialist agent, which applies the latex_tutor (generation) and latex_review (audit) skills. Use to turn slides/notes into textbook chapters or to audit a LaTeX project before submission.
---

# /latex — Academic LaTeX Workflow

$ARGUMENTS

---

## Purpose

Activate the **latex-specialist** agent to write or recheck LaTeX. The agent runs in one of two modes, each backed by a dedicated skill:

| Mode | Skill | When |
|------|-------|------|
| **Generation** | `@[skills/latex_tutor]` | Turn PDF slides, notes, or transcripts into textbook-quality chapters |
| **Audit** | `@[skills/latex_review]` | Review an existing LaTeX project for compiler-breaking and style issues |

---

## Mode Detection

Read `$ARGUMENTS` and pick the mode:

| Signal in request | Mode |
|-------------------|------|
| "write", "generate", "create chapter", "from these slides", uploaded PDF/transcript | **Generation** |
| "review", "audit", "check", "fix", "does this compile", points at `main.tex` / a project | **Audit** |
| Ambiguous | Ask one question: "Generate new LaTeX or audit existing files?" |

---

## Flow

1. **Detect mode** from `$ARGUMENTS` (see table above).
2. **Delegate to the agent** with full context:

   ```
   Use the latex-specialist agent to [generate chapter from / audit] the LaTeX in $ARGUMENTS.

   CONTEXT:
   - User Request: [full text]
   - Mode: Generation | Audit
   - Inputs: [PDF / transcript / project path / main.tex]
   ```

3. **Generation mode** — agent applies `@[skills/latex_tutor]`:
   - Reads `preamble.tex` + course context first
   - Synthesizes slides by theme (not 1:1)
   - Emits LaTeX **body only** — no `\documentclass`, no preamble
   - Strips all `[cite]` / `<source>` tags

4. **Audit mode** — agent applies `@[skills/latex_review]`:
   - Reads `main.tex`, then every `\include`d file
   - Traces all `\label` → `\ref` chains
   - Reports by severity: 🔴 Critical → 🟡 Important → 🔵 Minor

5. **Verify before done** — agent runs its Review Checklist:
   matched `\begin`/`\end`, zero citation tags, `&` only in tables, `_`/`^` in math mode, captions placed right, `\cleardoublepage` per chapter.

---

## Usage

```
/latex generate a chapter from these lecture slides on neural networks
/latex turn this transcript into a textbook section
/latex audit my thesis project in ./thesis (start from main.tex)
/latex review chapters/03-methods.tex and fix compile errors
```

---

## Key Principles

- **Compilation is sacred** — if it doesn't compile, nothing else matters.
- **Synthesize, don't transcribe** — structure by logic, not by slide order.
- **Strip citation tags** — `[cite]`, `<source>`, `[ref]` crash the compiler.
- **Output in English** — user communication stays in the user's language.
- See `@[agents/latex-specialist]` for full conventions, anti-patterns, and checklist.
