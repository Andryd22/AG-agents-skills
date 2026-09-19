# Architettura dell'Antigravity Kit

> Agenti, skill e regole che trasformano Antigravity in una squadra di specialisti.

---

## 📋 Panoramica

L'Antigravity Kit è un sistema modulare fatto di:

- **12 agenti specialisti**: custom agent di Antigravity, eseguiti come subagent
- **32 skill**: conoscenze di dominio e slash command (`/plan`, `/debug`, `/test`, ...)
- **2 regole**: `GEMINI.md` (sempre attiva) e `caveman-rules.md`

Antigravity ha deprecato i workflow e li ritira il 1° novembre 2026: ogni vecchio workflow del kit ora è una skill con lo stesso slash command.

---

## 🏗️ Struttura delle cartelle

```plaintext
.agents/
├── ARCHITECTURE.md          # Questo file
├── agents/                  # 12 agenti specialisti (custom agent)
├── skills/                  # 32 skill (anche slash command)
├── rules/                   # GEMINI.md (sempre attiva), caveman-rules.md
├── scripts/                 # 3 script master
├── .markdownlint.jsonc      # Regole markdownlint per i file .md del kit
└── .ag-kit.json             # Scritto dall'installer: cosa ha installato il kit
```

L'installer sostituisce solo i propri agenti, skill, regole e script: i file del progetto in `.agents/` restano.

---

## 🤖 Agenti (12)

Custom agent di Antigravity (`.agents/agents/<nome>.md`): il frontmatter fissa gli strumenti (con i nomi di Antigravity) e il modello (`inherit`); il corpo è il system prompt e nomina le skill dell'agente ("Le tue skill"). I custom agent ereditano tutte le skill del workspace, quindi il frontmatter non ha la chiave `skills`: i suoi percorsi verrebbero risolti dalla cartella dell'agente e fallirebbero per gli agenti fatti di un solo file. `GEMINI.md` fa passare ogni richiesta da `intelligent-routing` e delega con `invoke_subagent`; dove i custom agent non ci sono (per ora l'IDE di Antigravity) il file dell'agente viene letto e applicato direttamente.

| Agente | Ambito | Skill |
| --- | --- | --- |
| `orchestrator` | Coordinamento di più agenti | clean-code, parallel-agents, brainstorm, architecture, powershell-windows |
| `explorer-agent` | Analisi del codice | clean-code, architecture, brainstorm, debug |
| `frontend-specialist` | UI/UX web, prestazioni, SEO | clean-code, nextjs-react-expert, web-design-guidelines, tailwind-patterns, frontend-design, scroll-film |
| `backend-specialist` | API, database, revisione di sicurezza, deploy | clean-code, nodejs-best-practices, python-patterns, api-patterns, database-design, powershell-windows, rust-pro |
| `api-designer` | Contratti API, OpenAPI | clean-code, api-patterns, nodejs-best-practices |
| `test-engineer` | Strategie di test, TDD | clean-code, test, webapp-testing |
| `qa-automation-engineer` | Test E2E, job di test in CI | clean-code, webapp-testing, test, web-design-guidelines |
| `debugger` | Analisi della causa radice | clean-code, debug |
| `ai-ml-engineer` | LLM, RAG, prompt; ML classico e data mining | clean-code, prompt-engineering, classic-ml, api-patterns |
| `scroll-experience-architect` | Esperienze scroll 3D, cinematiche, video | three-js, scroll-film, scroll-world |
| `latex-specialist` | LaTeX accademico, appunti, paper | clean-code, latex-tutor, latex-review |
| `documentation-writer` | Documentazione (solo su richiesta) | clean-code |

Non c'è un agente dedicato a sicurezza, prestazioni, SEO, database o DevOps: revisioni di sicurezza, schema e deploy spettano a `backend-specialist`, prestazioni web e SEO a `frontend-specialist`. Anche i piani non hanno un agente: li scrive la skill `plan`, lanciata dall'agente di turno o dall'`orchestrator`.

---

## ⌨️ Comandi (11)

Skill scritte per essere chiamate per nome. Antigravity le carica anche da solo quando la richiesta corrisponde alla loro descrizione.

| Comando | Descrizione |
| --- | --- |
| `/brainstorm` | Socratic Gate ed esplorazione delle opzioni |
| `/plan` | Piano in `docs/PLAN-{slug}.md`, senza codice |
| `/orchestrate` | Coordinamento di più agenti |
| `/debug` | Indagine sistematica sui bug |
| `/test` | Genera ed esegue i test |
| `/status` | Stato del progetto e degli agenti |
| `/caveman` | Risposte asciutte (on, off, lite, full, ultra) |
| `/ui-ux-pro-max` | Design con il database di stili cercabile |
| `/latex` | Appunti LaTeX: prepara il corso, capitolo da un PDF, revisione |
| `/scroll-film` | Siti animati a scorrimento (scroll film) |
| `/scroll-experience` | Unisce three-js, scroll-film e scroll-world |

Funziona anche `/classic-ml`: è una skill di conoscenza (sotto) con un nome da comando.

---

## 🧩 Skill (32)

Gli 11 comandi qui sopra più 21 moduli di conoscenza, che gli agenti leggono quando il loro corpo li nomina o che Antigravity sceglie dalla descrizione.

### Base

| Skill | Descrizione |
| --- | --- |
| `intelligent-routing` | Sceglie gli agenti giusti e passa loro il lavoro |
| `clean-code` | Regole di scrittura del codice (globali) |
| `parallel-agents` | Schemi per coordinare più agenti |

### Frontend e UI

| Skill | Descrizione |
| --- | --- |
| `nextjs-react-expert` | Ottimizzazione delle prestazioni React e Next.js (regole Vercel) |
| `web-design-guidelines` | Audit di UI web: accessibilità, UX, prestazioni |
| `tailwind-patterns` | Utility di Tailwind CSS v4 |
| `frontend-design` | Pattern UI/UX, design system |

### Esperienze scroll

| Skill | Descrizione |
| --- | --- |
| `three-js` | Scene Three.js/WebGL guidate dallo scroll: scena, camera, scroll, prestazioni |
| `scroll-world` | Landing page "volo attraverso il mondo" da video pre-renderizzati |

### Backend e API

| Skill | Descrizione |
| --- | --- |
| `api-patterns` | REST, GraphQL, tRPC |
| `nodejs-best-practices` | Node.js: async, moduli |
| `python-patterns` | Standard Python, FastAPI |
| `rust-pro` | Rust moderno asincrono, sistemi |
| `database-design` | Schema, indici, ORM |
| `powershell-windows` | Trappole di PowerShell su Windows |

### Test

| Skill | Descrizione |
| --- | --- |
| `webapp-testing` | E2E, Playwright |

### AI e dati

| Skill | Descrizione |
| --- | --- |
| `prompt-engineering` | Prompt per LLM, RAG, progettazione |
| `classic-ml` | Data mining e ML classico con pandas e scikit-learn |

### Accademico

| Skill | Descrizione |
| --- | --- |
| `latex-tutor` | Capitoli LaTeX in stile libro dalle slide |
| `latex-review` | Controllo e revisione di un progetto LaTeX |

### Architettura

| Skill | Descrizione |
| --- | --- |
| `architecture` | Progettazione di sistemi, ADR |

---

## 🎯 Come si carica una skill

```plaintext
Richiesta → corrispondenza con la descrizione (o /nome) → legge SKILL.md
                                                             ↓
                                                     legge references/
                                                             ↓
                                                    esegue scripts/
```

### Struttura di una skill

```plaintext
nome-skill/
├── SKILL.md           # (Obbligatorio) Metadati e istruzioni, sotto le 500 righe
├── scripts/           # (Facoltativo) Script Python/Bash/JS
├── references/        # (Facoltativo) Modelli, documentazione
└── data/, assets/     # (Facoltativo) File di dati, immagini
```

`SKILL.md` segue la spec Agent Skills: `name` è uguale al nome della cartella (lettere minuscole, cifre, trattini), `description` dice cosa fa la skill e quando usarla.

---

## 📊 Script

### Script master (3)

| Script | Scopo | Quando |
| --- | --- | --- |
| `checklist.py` | Controlli di base: schema, test, UX (+ E2E con `--url`) | Durante lo sviluppo, prima del commit |
| `verify_all.py` | Suite completa: controlli di base + API, accessibilità, E2E | Prima del deploy, rilasci |
| `session_manager.py` | Stato del progetto: stack, file, statistiche (`/status`) | Quando serve |

```bash
# Controllo rapido durante lo sviluppo
python .agents/scripts/checklist.py .

# Verifica completa prima del deploy
python .agents/scripts/verify_all.py . --url http://localhost:3000
```

Gli script di audit saltano `node_modules/`, le cartelle di build e la stessa `.agents/`.

### Script delle skill

| Skill | Script | Scopo |
| --- | --- | --- |
| `api-patterns` | `api_validator.py` | Controlli sulle buone pratiche delle API |
| `database-design` | `schema_validator.py` | Controlli sugli schema Prisma / Drizzle |
| `frontend-design` | `ux_audit.py` | Audit di psicologia UX e accessibilità |
| `frontend-design` | `accessibility_checker.py` | Controlli WCAG |
| `nextjs-react-expert` | `react_performance_checker.py` | Suggerimenti statici sulle prestazioni React |
| `nextjs-react-expert` | `convert_rules.py` | Ricostruisce i file delle regole |
| `test` | `test_runner.py` | Esegue la suite di test del progetto |
| `latex-tutor` | `slides.py` | Testo e immagini delle slide e ritagli delle figure dai PDF delle lezioni |
| `latex-review` | `check_project.py` | Label, riferimenti, immagini e segnaposto di un progetto LaTeX |
| `webapp-testing` | `playwright_runner.py` | Smoke test E2E di un URL in esecuzione |
| `ui-ux-pro-max` | `search.py`, `core.py`, `design_system.py` | Cercano nel database di design in `data/` |
| `scroll-film` | `assemble.sh`, `chain-step.sh` | Montaggio della catena di video (bash, ffmpeg ≥ 5.1) |
| `scroll-film` | `verify.js` | Screenshot e test di jank (puppeteer-core) |

In `scroll-world/references/` ci sono anche `knockout.py` (rimozione dello sfondo) e `scrub-engine.js` (il motore di scrub).

---

## 📊 Numeri

| Voce | Valore |
| --- | --- |
| **Agenti** | 12 |
| **Skill** | 32 (11 comandi) |
| **Regole** | 2 |
| **Script** | 3 master + 16 nelle skill |

I numeri li controlla `.github/scripts/validate_kit.py` nella CI.

---

## 🔗 Riferimento rapido

| Serve | Agente | Skill |
| --- | --- | --- |
| App web | `frontend-specialist` | nextjs-react-expert, frontend-design |
| API | `backend-specialist` | api-patterns, nodejs-best-practices |
| Database | `backend-specialist` | database-design |
| Test | `test-engineer` | test, webapp-testing |
| E2E | `qa-automation-engineer` | webapp-testing |
| Debug | `debugger` | debug |
| Piano | nessuno | plan, brainstorm |
| AI / LLM | `ai-ml-engineer` | prompt-engineering |
| ML / dati | `ai-ml-engineer` | classic-ml |
| Scroll / 3D | `scroll-experience-architect` | three-js, scroll-film, scroll-world |
| LaTeX | `latex-specialist` | latex-tutor, latex-review |
