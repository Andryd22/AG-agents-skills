---
name: latex
description: 'University notes in LaTeX: set up a course folder, turn a lecture PDF (and its transcript) into a chapter with figures, references and a compile check, or review the whole project. Delegates to the latex-specialist agent with the latex-tutor and latex-review skills. Use when the user runs /latex or asks for LaTeX notes from slides.'
---

# /latex — University Notes in LaTeX

The request is the text that follows `/latex`.

---

## Modes

| Signal in the request | Mode | Skill |
| --- | --- | --- |
| "setup", "new course", "nuovo corso", empty folder without `main.tex` | **Setup** | `@[skills/latex-tutor]` (assets) |
| a PDF name or path, "chapter", "generate", "from these slides", an attached PDF or transcript | **Generation** | `@[skills/latex-tutor]` |
| "review", "check", "audit", "fix", "does it compile" | **Audit** | `@[skills/latex-review]` |
| unclear | ask one question: new course, new chapter or review? | |

Hand the work to `latex-specialist` with the request, the mode and the files involved (↪ `@latex-specialist: <mode> <files>`).

---

## Setup

1. Ask for the course title and the author name (skip what the request already says).
2. Create in the current folder, without overwriting anything that exists:
   - `main.tex` and `preamble.tex` from `.agents/skills/latex-tutor/assets/`, with the title and author filled in;
   - `chapters/`, `images/`, `transcripts/`, and `slides/` unless the lecture PDFs already sit in another folder.
3. Tell the user where to put the lecture PDFs and how to generate the first chapter (`/latex slides/1-Introduction.pdf`).

---

## Generation

Follow the Workflow of `latex-tutor` (Project Mode):

1. Read the preamble, map the existing chapters with `grep`, read the last edited chapter to copy its conventions.
2. Read the PDF (directly or with `slides.py text` and `render`) and the transcript if there is one.
3. Write `chapters/<PDF name>.tex` without overwriting an existing file; add the `\include` to `main.tex`.
4. Figures: TikZ for simple diagrams, crops with `slides.py crop` for complex ones, placeholders only as a fallback.
5. Compile, fix the errors of the new chapter, report sections, figures, references and warnings.

Without a course folder (a single PDF in a chat), `latex-tutor` works in Chat Mode: the chapter body in one `latex` code block.

---

## Audit

Follow the Review Workflow of `latex-review`: `check_project.py`, compile and log, style checklist, report by severity. Fix only after the user says which issues to fix.

---

## Usage

```text
/latex setup
/latex slides/5-Clustering.pdf
/latex slides/5-Clustering.pdf with transcripts/5-Clustering.txt
/latex review
/latex fix the critical issues of chapter 7
```

---

## Key Principles

- **The chapters are the user's**: never overwrite one, never restructure prose without approval.
- **It must compile**: every generation ends with a compile.
- **Synthesize, don't transcribe**: structure by topic, not by slide.
- **LaTeX in English**, conversation in the user's language.
- See `@[agents/latex-specialist]` for conventions and the full checklist.
