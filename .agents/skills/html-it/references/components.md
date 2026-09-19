# html-it — Component Library

Copy-paste components for html-it pages. All inline, no build step: paste the HTML and add the CSS hints to the page's `<style>`. Colours come from the design system in `../SKILL.md`.

## TL;DR card

```html
<div class="tldr">
  <div class="tldr-label">TL;DR</div>
  <p>2-4 self-contained lines. Someone who reads only this gets the main point.</p>
</div>
```

## Definition box

```html
<div class="def">
  <div class="def-term">Concept Name</div>
  <p>Definition. Inline formula: \(f(x) = x^2\).</p>
</div>
```

## Callout / warning

```html
<div class="callout">
  <div class="callout-label">⚠ Watch out</div>
  <p>Common mistakes, warnings, things not to forget.</p>
</div>
```

CSS: `background: #FFF7ED; border: 1.5px solid #FED7AA;` — label color `#C2410C`, text `#7C2D12`.

## Math display block

```html
<div class="math-block">
  \[ \theta_{t+1} = \theta_t - \eta \cdot \nabla_\theta \mathcal{L}(\theta_t) \]
</div>
```

CSS: `background: var(--g100); border-radius: 6px; padding: 16px 24px; text-align: center;`

## Code block with syntax highlighting

Theme: Catppuccin Mocha (`background: #1E1E2E; color: #CDD6F4`).

```html
<div class="code-label">Python · NumPy</div>
<pre><span class="kw">def</span> <span class="fn">f</span>(x):
    <span class="cm"># comment</span>
    <span class="kw">return</span> x <span class="op">**</span> <span class="nm">2</span>
</pre>
```

Token classes:

- `.kw` → keyword (`def`, `return`, `import`) — `#CBA6F7` violet
- `.fn` → function name — `#89DCEB` cyan
- `.cm` → comment — `#6C7086` grey italic
- `.st` → string — `#A6E3A1` green
- `.nm` → number/literal — `#FAB387` orange
- `.op` → operator — `#89DCEB` cyan

## SVG diagram

```html
<figure class="diagram">
  <svg viewBox="0 0 640 270" xmlns="http://www.w3.org/2000/svg">
    <rect width="640" height="270" fill="#FAFAF7" rx="8"/>
    <!-- SVG elements: circle, rect, line, path, text -->
    <!-- arrows: marker-end="url(#arr)" + define the marker in <defs> -->
    <defs>
      <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="var(--slate)"/>
      </marker>
    </defs>
  </svg>
  <figcaption>Caption in mono 10.5px var(--g500)</figcaption>
</figure>
```

**SVG best practices:**

- Always `viewBox` + `width="100%"` — never fixed sizes
- Background rect with `fill="#FAFAF7"` and `rx="8"`
- Grid lines: `stroke="#E8E5DC" stroke-width="0.8"`
- Use the CSS custom properties in fill/stroke when possible
- Axis labels: `font-family="monospace" font-size="11" fill="#87867F"`

## 2 / 3 column grid

```html
<div class="two-col">   <!-- grid-template-columns: 1fr 1fr -->
  <div class="def">...</div>
  <div class="def">...</div>
</div>

<div class="three-col"> <!-- grid-template-columns: 1fr 1fr 1fr -->
  <div class="def">...</div>
  <div class="def">...</div>
  <div class="def">...</div>
</div>
```

## Comparison table

```html
<table>
  <thead><tr><th>Method</th><th>Advantage</th><th>Use</th></tr></thead>
  <tbody>
    <tr><td>SGD</td><td>Fast</td><td>Deep Learning</td></tr>
  </tbody>
</table>
```

First `td` renders in mono clay — ideal for method/variant names.

## Flashcards (Level 3 interactive)

```html
<div class="flashcards"> <!-- 2-column grid -->
  <div class="card" onclick="toggle(this)">
    <div class="card-q">Question?</div>
    <div class="card-a">Answer. Formulas like \(\theta^*\) work.</div>
    <div class="card-hint">↩ click for the answer</div>
  </div>
</div>

<script>
function toggle(card) {
  card.classList.toggle('revealed');
  card.querySelector('.card-hint').textContent =
    card.classList.contains('revealed') ? '↩ click to hide' : '↩ click for the answer';
}
</script>
```

## TOC active-section tracker (JS)

```js
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      document.querySelectorAll('.toc a').forEach(l => l.classList.remove('active'));
      const lnk = document.querySelector(`.toc a[href="#${e.target.id}"]`);
      if (lnk) lnk.classList.add('active');
    }
  });
}, { rootMargin: '-20% 0px -60% 0px' });
document.querySelectorAll('section[id]').forEach(s => observer.observe(s));
```
