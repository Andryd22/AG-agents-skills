# html-it — University Notes

Details for lecture notes built with html-it. The design system (palette, typography) is in `../SKILL.md`; components are in `components.md`.

## A4 Fixed Layout (default for notes)

**Use this layout for all lecture notes.** Fixed 794px canvas scales uniformly to any viewport — phone, laptop, desktop all show identical layout, like a PDF.

```css
/* ── Shell centres the page on ivory background ── */
body {
  background: var(--ivory);
  font-family: var(--sans);
  color: var(--slate);
  padding-top: 44px; /* nav height */
}

.shell {
  display: flex;
  justify-content: center;
  padding: 48px 0 80px;
}

/* ── A4 page: 794px = A4 at 96dpi ── */
.page {
  width: 794px;
  flex-shrink: 0;
  background: var(--paper);
  box-shadow: 0 2px 6px rgba(0,0,0,0.07), 0 12px 48px rgba(0,0,0,0.10);
  padding: 68px 76px 88px;
}

/* ── Scale uniformly on narrow viewports ── */
@media (max-width: 870px) {
  nav.toc { display: none; }
  .shell  { padding: 24px 0 60px; }
  .page {
    transform-origin: top center;
    transform: scale(calc((100vw - 8px) / 794px));
    /* compensate collapsed height after scale */
    margin-bottom: calc(((100vw - 8px) / 794px - 1) * 1100px);
  }
}

/* ── Floating TOC — sits to the left of the A4 page ── */
nav.toc {
  position: fixed;
  top: 80px;
  left: max(16px, calc(50% - 520px));
  width: 148px;
}
```

### Top navigation bar (inter-file linking)

```css
nav.topnav {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 44px;
  background: var(--slate);
  display: flex;
  align-items: center;
  padding: 0 20px;
  z-index: 200;
  overflow-x: auto;
  scrollbar-width: none;
}
```

```html
<nav class="topnav">
  <span class="course-chip">Course Name · MSc</span>
  <a href="01-lecture.html">01 · TODO</a>
  <a href="#" class="active">02 · This lecture</a>
  <a href="03-lecture.html">03 · TODO</a>
</nav>
```

### MathJax (LaTeX math in HTML)

Always include — user writes math in standard LaTeX syntax, MathJax renders it.
Full config with the usual LaTeX macros (mirror the user's own preamble if they have one):

```html
<script>
  window.MathJax = {
    tex: {
      inlineMath: [['\\(','\\)'], ['$','$']],
      displayMath: [['\\[','\\]']],
      tags: 'ams',          // automatic equation numbering
      macros: {
        argmin: ['\\operatorname*{arg\\,min}'],
        argmax: ['\\operatorname*{arg\\,max}'],
        bm:    ['\\boldsymbol{#1}', 1],   // \bm{v} — bold vector
        dv:    ['\\frac{d#1}{d#2}', 2],   // \dv{f}{x}
        pdv:   ['\\frac{\\partial #1}{\\partial #2}', 2], // \pdv{f}{x}
        R:     ['\\mathbb{R}'],
        N:     ['\\mathbb{N}'],
        Z:     ['\\mathbb{Z}'],
        E:     ['\\mathbb{E}'],
        P:     ['\\mathbb{P}'],
        norm:  ['\\left\\|#1\\right\\|', 1],
        abs:   ['\\left|#1\\right|', 1],
      }
    },
    svg: { fontCache: 'global' }
  };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
```

Inline: `\(\nabla_\theta \mathcal{L}\)` | Display: `\[ \theta_{t+1} = \theta_t - \eta \cdot \nabla_\theta \mathcal{L} \]`

---

## Where notes live

Notes live in the folder the user works in (ask once, then reuse it). Two ways to work:

1. **Single file (default).** Each lecture is one standalone `.html` with the CSS, MathJax config and scripts inlined. No build step: this is what the rest of the skill assumes.
2. **Multi-file with a build step (optional).** Only if the user's notes folder already has a shared preamble (for example `_preamble.html` + `build.py`): write just the lecture content as `NN-slug/content.html` (format below) and tell the user to run their build. The kit does not ship these files; create them only if the user asks for this setup.

### From a lecture PDF to notes

1. The user sends the lecture PDF (or slides)
2. Read it and extract structure and content
3. Write the lecture file (single file, or `NN-slug/content.html` in the multi-file setup)
4. Update the top navigation with the link to the new lecture

### content.html format (multi-file setup only) — front matter + pure sections

```html
---
eyebrow: Lecture 03 · Machine Learning
title: Gradient <em>Descent</em>
meta: 2025/26 · ~20 min read
tldr: Self-contained 2-4 line summary. Supports formulas like \(\theta^*\).
---

<section id="intro">
  <h2 id="intro">1. Introduction</h2>   <!-- id on h2 → auto-generated TOC -->
  <p>...</p>
</section>

<section id="recap">
  <h2 id="recap">Review flashcards</h2>
  <div class="flashcards">...</div>
</section>
```

**Critical rule:** every `<h2>` needs an `id="..."`: the TOC (inline script or the user's build) is generated from them.

### Anatomy of a lecture note (Level 2 default)

```text
topnav          — fixed bar, links to every lecture of the course
toc (floating)  — left of A4, highlights active section on scroll
page (.page)    — A4 794px container
  eyebrow       — "Lecture 0X · Course Name" (mono, clay)
  h1            — Title with <em>key word</em>
  .meta         — academic year, last update, reading time
  .tldr         — self-contained 2-4 line summary
  section#s1    — h2 + text + components
  section#recap — review flashcards (always last)
```

### amsthm environments → HTML equivalents

For users whose LaTeX preamble uses `amsthm` + `physics` + `algorithm2e`, mirror the environments like this.
**All colours are design-system variables — no external colours.**

| LaTeX | HTML class | Bordo sinistro | Sfondo |
| --- | --- | --- | --- |
| `\begin{theorem}` | `.thm-block.theorem` | `var(--slate)` black | `var(--g100)` |
| `\begin{definition}` | `.thm-block.definition` | `var(--clay)` orange | `var(--g100)` |
| `\begin{lemma}` | `.thm-block.lemma` | `var(--clay-d)` dark orange | `var(--g100)` |
| `\begin{corollary}` | `.thm-block.corollary` | `var(--g700)` dark grey | `var(--g100)` |
| `\begin{proposition}` | `.thm-block.proposition` | `var(--g700)` dark grey | `var(--g100)` |
| `\begin{example}` | `.thm-block.example` | `var(--olive)` green | `var(--g100)` |
| `\begin{proof}` | `.proof` | `var(--oat)` beige + □ QED | — |
| `\begin{algorithm}` | `.algorithm` | `var(--oat)` beige | header `var(--g100)` |

Automatic numbering via CSS `counter` — no JS needed.

Usage:

```html
<div class="thm-block theorem">
  <p>Theorem statement. Formula: \(\theta^* = \argmin_\theta \mathcal{L}(\theta)\).</p>
</div>

<div class="thm-block definition">
  <p>Formal definition.</p>
</div>

<div class="thm-block example">
  <p>Concrete example.</p>
</div>

<div class="proof">
  <p>Proof... (□ QED is added automatically)</p>
</div>
```

### MathJax macros

Configured in the MathJax block above — use them as in LaTeX:

| Macro | Result |
| --- | --- |
| `\argmin` | argmin operator with limits |
| `\argmax` | argmax operator with limits |
| `\bm{v}` | bold vector (as the `bm` package) |
| `\dv{f}{x}` | total derivative |
| `\pdv{f}{x}` | partial derivative |
| `\R`, `\N`, `\Z`, `\E`, `\P` | blackboard bold sets |
| `\norm{v}` | norm `‖v‖` |
| `\abs{x}` | absolute value `\|x\|` |

### Algorithm block — like algorithm2e

Design-system colours: header `var(--g100)`, border `var(--oat)`, keyword `var(--clay-d)`.
Lines numbered automatically via CSS counter — no JS.

```html
<div class="algorithm">
  <div class="algorithm-header">
    <span class="algorithm-name">Algorithm 1</span>
    <span class="algorithm-caption">Gradient Descent</span>
  </div>
  <div class="algorithm-body">
    <div class="algo-line"><span><span class="algo-kw">Input:</span> \(X, y, \eta, T\)</span></div>
    <div class="algo-line"><span><span class="algo-kw">Output:</span> \(\theta^*\)</span></div>
    <div class="algo-line"><span><span class="algo-kw">for</span> \(t = 1, \ldots, T\) <span class="algo-kw">do</span></span></div>
    <div class="algo-line"><span><span class="algo-ind"></span>\(\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}(\theta)\) <span class="algo-cm">// gradient step</span></span></div>
    <div class="algo-line"><span><span class="algo-kw">end for</span></span></div>
    <div class="algo-line"><span><span class="algo-kw">return</span> \(\theta\)</span></div>
  </div>
</div>
```

Algorithm token classes: `.algo-kw` (clay-d, bold), `.algo-fn` (slate), `.algo-cm` (g500 italic), `.algo-ind` (1.5em indent).

### Rules specific to university notes

- **Language: English by default** — same rule as `latex-tutor`: titles, body, labels, callouts and flashcards in English unless the user asks for another language. Code comments always in English.
- **Default layout: A4 fixed** — not responsive/fluid
- **Math: MathJax always** — never plain text for equations
- **`<h2>` with id always** — required for automatic TOC generation
- **At least one SVG per main visual concept**
- **Flashcards at the bottom** — fixed `id="recap"` section
- **One file per lecture** — never merge topics
