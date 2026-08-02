# Design — Skill `three-js` + Unificatore Scroll Experience

Data: 2026-08-02
Stato: approvato (brainstorming, 4 sezioni)

## Contesto

Kit Antigravity ha già due skill scroll-driven:

- **scroll-film-studio** — siti cinematici scroll-scrubbed, lane pure-code (GSAP/Lenis) o video footage
- **scroll-world** — landing "fly-through the world" con clip video pre-renderizzate (Higgsfield)

Manca una skill per il terzo pilastro: **Three.js/WebGL code-based** (scroll 3D). Inoltre, nessun agente/workflow unifica le tre in una pipeline completa.

Decisioni utente:

1. Focus skill three.js: **Scroll 3D** (scroll-driven, non generalista)
2. Unificatore: **agent + workflow** (entrambi)
3. Motore: **code-first Three.js + video opzionale** (Higgsfield solo se richiesto/fattibile)

Approcci approvati: skill **modulare con references** (B), unificatore **agent persona + workflow pipeline** (A).

## 1. Skill `three-js`

Posizione: `.agent/skills/three-js/`

```
three-js/
├── SKILL.md                    # core ~250 righe
└── references/
    ├── scene-architecture.md   # geometrie, materiali, lighting, texture, scene graph
    ├── scroll-integration.md   # ScrollTrigger/GSAP + Lenis, scroll-scrub, parallax
    ├── camera-choreography.md  # camera rigs, fly-through, path following, easing
    ├── performance.md          # draw calls, instancing, LOD, pixel ratio, budget fps
    └── verification.md         # jank test, GPU stats, console warnings, checklist
```

### SKILL.md — contenuto

- Frontmatter: `name: three-js`; description con trigger: "3D scene", "WebGL", "scroll 3D", "camera fly-through", "Three.js"
- **Quando usarla** vs scroll-film-studio (code-cinematic) vs scroll-world (video): tabella decisionale motore
- **Golden rules**: scene graph pulito, budget draw calls, renderer config (antialias, pixel ratio), dispose pattern, rAF + ScrollTrigger senza conflitti
- **Flusso build**: HTML shell → scene → camera rig → scroll integration → lighting/materiali → perf → verifica
- **Errori comuni**: memory leak su dispose, z-fighting, fog vs far plane, scroll hijacking
- **Checklist finale** + quando delegare a `scroll-experience-architect`

### References (100–200 righe ciascuna)

Pattern concreti con snippet riusabili, non teoria. Caricate on-demand (progressive disclosure, coerente con `.agent/skills/README.md` e con scroll-film-studio).

## 2. Agent `scroll-experience-architect`

Posizione: `.agent/agents/scroll-experience-architect.md`

Frontmatter:

```yaml
"name": "scroll-experience-architect"
"description": "Creative-technical architect for immersive scroll-driven web experiences... Triggers on scroll experience, scroll 3D, fly-through, scrollytelling, cinematic website, WebGL scroll..."
"model": "inherit"
"tools": [Read, Grep, Glob, Bash, Edit, Write]
"skills":
- "three-js"
- "scroll-film-studio"
- "scroll-world"
```

Persona: architetto creativo-tecnico — direzione artistica + ingegneria 3D. Ogni sezione = shot, camera = narratrice.

### Decisione motore (code-first + video opzionale)

1. Baseline: **Three.js code** — sempre possibile, zero dipendenze esterne
2. Video opzionale: foto-realismo/asset reali richiesti + accesso Higgsfield → clip da `scroll-world`
3. Lane cinematiche pura code (GSAP/Lenis scrub) → `scroll-film-studio`
4. Ibrido: sezioni hero in Three.js, sezioni video intercalate — seam check tra sezioni

### Output standard

Specifica in 5 blocchi: concept, scene list, camera path, motore scelto, budget perf + verifica.

## 3. Workflow `/scroll-experience`

Posizione: `.agent/workflows/scroll-experience.md`

Frontmatter: `name: scroll-experience`, description → orchestrazione 3 skill.

Flow:

- **Step 0 — Interview**: topic, story beats, brand kit, budget, mobile tier. Decide motore: 3D code, video, cinematic code, ibrido
- **Step 1 — Concept pitch**: 2-3 concetti nominati con camera path
- **Step 2 — Build**: delega al motore scelto (skill `three-js` / `scroll-world` / `scroll-film-studio`)
- **Step 3 — Seam & hybrid check**: transizioni tra sezioni 3D/video/code (SSIM se video, visual check se code)
- **Step 4 — Verify & Deploy**: jank test, budget fps, deploy opzionale

Usage:

```
/scroll-experience 3D fly-through world per brand caffè
/scroll-experience scrollytelling ibrido: hero 3D + sezioni video
```

## 4. Integrazione documentazione

- `.agent/ARCHITECTURE.md`:
  - Skills (50) → (51): riga `three-js` in Frontend & UI
  - Agenti (25) → (26): `scroll-experience-architect` + riga tabella
  - Workflow (14) → (15): `/scroll-experience`
- `README.md`: Skill 50 → 51, Workflow 14 → 15, riga `/scroll-experience` in tabella workflow
- `.agent/skills/README.md`: nessuna modifica (guida generica)
- `tasks/todo.md`: piano implementazione (CLAUDE.md workflow)

## Criteri di successo

1. Skill `three-js` attiva su richieste "3D scroll" — trigger corretti in description
2. Agent auto-detectato su richieste scroll experience
3. `/scroll-experience` guida pipeline end-to-end scegliendo il motore giusto
4. Conteggi in ARCHITECTURE.md e README.md coerenti (51 skill, 26 agenti, 15 workflow)
5. Kit installabile invariato (`npx ... init -y`)
