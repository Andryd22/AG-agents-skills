---
trigger: always_on
---

# GEMINI.md - Antigravity Kit

> Questo file stabilisce come si comporta l'AI in questo workspace.

---

## CRITICO: PROTOCOLLO DI AGENTI E SKILL (PARTI DA QUI)

> **OBBLIGATORIO:** prima di qualsiasi implementazione, assegna la richiesta all'agente giusto e carica le sue skill. È la regola con la priorità più alta.

Gli agenti del kit sono custom agent di Antigravity in `.agents/agents/`. Le skill stanno in `.agents/skills/` e fanno anche da slash command (`/plan`, `/debug`, `/test`, `/orchestrate`, ...).

### 1. Delegare a un agente

- **Scegli** l'agente con `@[skills/intelligent-routing]`.
- **Delega** con `invoke_subagent`. Il subagent parte con un contesto pulito, ha gli strumenti del suo frontmatter e vede tutte le skill del workspace; il suo corpo nomina le skill da leggere per prime. Il prompt deve contenere la richiesta dell'utente, le decisioni già prese e i file o il piano che servono.
- **Ripiego:** dove i custom agent non ci sono (l'IDE di Antigravity finché non li supporta), leggi `.agents/agents/<nome>.md` e lo `SKILL.md` di ogni skill nominata nella sua riga "Le tue skill", poi applicali tu.
- L'utente può anche scegliere un agente del kit come agente principale (selettore nell'app, `/agents` nella CLI).
- **Strumenti:** un agente del kit ha solo gli strumenti del suo frontmatter (più `manage_task`); l'agente di default della CLI non ha `list_dir` e `grep_search`, e nella CLI nessun agente ha `multi_replace_file_content`. Senza `list_dir` o `grep_search`, elenca le cartelle e cerca con `run_command` (`Get-ChildItem`, `Select-String` su Windows; `ls`, `grep` altrove); non tirare mai a indovinare i nomi dei file. Modifica solo le righe che cambiano: una sostituzione per ogni punto separato, non un blocco che riscrive anche le righe in mezzo.

### 2. Caricare le skill

- **Lettura selettiva:** NON leggere TUTTI i file di una skill. Leggi prima `SKILL.md`, poi solo le sezioni e i file di riferimento che servono alla richiesta.
- **Priorità delle regole:** P0 (GEMINI.md) > P1 (file .md dell'agente) > P2 (SKILL.md). Tutte le regole sono vincolanti.
- **Vietato:** saltare le regole dell'agente o le istruzioni della skill. "Leggi → Capisci → Applica" è obbligatorio.

### 3. Annuncia agenti e skill

L'utente deve sempre vedere quale agente e quali skill sono al lavoro. Ogni risposta che usa un agente o una skill del kit comincia con una riga:

```text
🤖 @debugger · 📚 debug, clean-code
```

- **🤖** l'agente di cui stai applicando le regole: quello con cui stai girando o quello a cui hai assegnato la richiesta (`@frontend-specialist + @backend-specialist` quando ne combini due). Girare come agente del kit (`--agent`, subagent, file di un agente applicato nell'IDE) conta sempre: la riga c'è anche per una risposta di una riga.
- **📚** ogni skill di cui hai letto lo `SKILL.md` per questa risposta; uno slash command è una skill (`/plan` → `📚 plan`). Nessuna skill: togli `· 📚 …`.
- **Delega:** scrivi `↪ @explorer-agent: <compito in poche parole>` prima di chiamare `invoke_subagent`, e `↩ @explorer-agent` quando torna il risultato.
- **Skill caricata a metà:** scrivi `📚 + <skill>` nel punto in cui inizi a usarla.
- **Niente di usato** (l'agente di default che risponde a una domanda semplice, senza routing e senza skill): nessuna riga.

---

## 🤖 ROUTING INTELLIGENTE DEGLI AGENTI

**SEMPRE ATTIVO: prima di rispondere a QUALSIASI richiesta, analizzala e scegli da solo gli agenti migliori.**

> 🔴 **OBBLIGATORIO:** segui il protocollo di `@[skills/intelligent-routing]` per classificare la richiesta e scegliere l'agente. Questa regola è **always_on** e va eseguita prima di ogni risposta.

---

## LIVELLO 0: REGOLE UNIVERSALI (sempre attive)

### 🌐 Lingua

1. **Rispondi in italiano**, o nella lingua dell'utente se scrive in un'altra.
2. **Codice:** commenti, docstring e messaggi per chi lo usa (log, errori, output) in italiano; nomi di variabili, funzioni, classi e file in inglese.
3. **Documenti** (piani, README, appunti): in italiano. Gli appunti di un corso già scritto in un'altra lingua seguono quella lingua (vedi `latex-tutor`).
4. **Nomi del kit** (agenti, skill, comandi, percorsi) restano in inglese.

### 🧹 Clean Code (obbligatorio ovunque)

**TUTTO il codice DEVE seguire le regole di `@[skills/clean-code]`. Nessuna eccezione.**

- **Codice**: conciso, diretto, niente sovraingegnerizzazione. Si spiega da solo.
- **Test**: obbligatori. Piramide (unit > integrazione > E2E) + schema AAA.
- **Prestazioni**: prima misura. Segui gli standard attuali (Core Web Vitals).
- **Infrastruttura e sicurezza**: controlla che i segreti siano al sicuro.

### 📁 Dipendenze tra file

**Prima di modificare QUALSIASI file:**

1. Trova cosa dipende da lui: cerca import e usi (e, se il progetto ha un `CODEBASE.md`, leggi la sua sezione File Dependencies)
2. Individua i file che ne dipendono
3. Aggiorna INSIEME tutti i file coinvolti

### 🗺️ Mappa del sistema

> 🔴 **OBBLIGATORIO:** a inizio sessione leggi `.agents/ARCHITECTURE.md` per conoscere agenti, skill e script.

**Percorsi:**

- Agenti: `.agents/agents/`
- Skill (e slash command): `.agents/skills/`
- Script master: `.agents/scripts/`
- Script delle skill: `.agents/skills/<skill>/scripts/`

### 🧠 Leggi → Capisci → Applica

```text
❌ SBAGLIATO: leggi il file dell'agente → inizia a scrivere codice
✅ GIUSTO: leggi → capisci il PERCHÉ → applica i PRINCIPI → scrivi codice
```

---

## LIVELLO 1: REGOLE PER IL CODICE (quando scrivi codice)

### 🛑 Socratic Gate

**OBBLIGATORIO: ogni richiesta dell'utente passa dal Socratic Gate prima dell'implementazione (scrivere codice, creare file, delegare lavoro). Leggere file per capire la richiesta è sempre permesso.**

| Tipo di richiesta | Strategia | Cosa fare |
| --- | --- | --- |
| **Nuova funzionalità / costruzione** | Scoperta | CHIEDI al massimo 3 domande strategiche su ciò che non puoi dedurre (scopo, utenti, perimetro) |
| **Modifica / bug fix** | Verifica del contesto | Conferma di aver capito; chiedi dell'impatto solo se non è chiaro |
| **Vaga / semplice** | Chiarimento | Chiedi solo ciò che manca tra scopo, utenti e perimetro |
| **Orchestrazione completa** | Guardiano | **FERMA** i subagent finché l'utente non conferma i dettagli del piano |
| **"Procedi" diretto** | Convalida | Procedi. Segnala un caso limite (massimo 1-2) solo se cambierebbe l'implementazione |

**Protocollo:**

1. **Mai dare per scontato:** se non è chiaro qualcosa che cambierebbe il risultato, CHIEDI. Se la richiesta ha già la risposta, dichiara la tua ipotesi e vai avanti.
2. **Richieste già dettagliate:** quando l'utente dà risposte precise (Risposta 1, 2, 3...), non richiederle. Nomina un **compromesso** o un **caso limite** solo quando cambia ciò che costruirai (es. "LocalStorage confermato: i dati vecchi vanno migrati quando cambia il formato?").
3. **Aspetta:** NON invocare subagent e non scrivere codice finché c'è una domanda bloccante aperta.
4. **Riferimento:** il protocollo completo è in `@[skills/brainstorm]`.
5. **Proporzione:** l'orchestrator e `/plan` seguono la stessa regola: 1-2 domande veloci quando la richiesta è quasi chiara, di più solo per costruzioni aperte.

### 🏁 Controlli finali

**Quando:** l'utente dice "controlli finali", "esegui tutti i controlli", "final checks" o frasi simili.

| Fase | Comando | Scopo |
| --- | --- | --- |
| **Controllo manuale** | `python .agents/scripts/checklist.py .` | Controlli di base: schema, test, UX |
| **Prima del deploy** | `python .agents/scripts/verify_all.py . --url <URL>` | Suite completa + E2E |

**Ordine di esecuzione:**

1. **Lint e tipi** (strumenti del progetto: `npm run lint`, `tsc --noEmit`, `ruff`...) → 2. **Schema** → 3. **Test** → 4. **UX** → 5. **E2E** (con `--url`)

**Regole:**

- **Completamento:** un task NON è finito finché `checklist.py` non passa.
- **Report:** se fallisce, correggi prima i problemi bloccanti (test, schema).

> 🔴 **Agenti e skill possono lanciare QUALSIASI script** con `python .agents/skills/<skill>/scripts/<script>.py` (gli script disponibili sono in `ARCHITECTURE.md` o nel file `.md` dell'agente).

### 🎭 Modalità di Gemini

| Modalità | Agente | Comportamento |
| --- | --- | --- |
| **plan** | skill `/plan` | Piano in `docs/PLAN-{slug}.md`. NIENTE CODICE finché il piano non è approvato. |
| **ask** | - | Punta a capire. Fai domande. |
| **edit** | agente scelto dal routing | Esegui. Il lavoro su più domini va all'`orchestrator`, che prima controlla `docs/PLAN-{slug}.md`. |

---

## 📁 RIFERIMENTO RAPIDO

### Agenti e skill

- **Principali**: `orchestrator`, `backend-specialist` (API/DB/sicurezza/deploy), `frontend-specialist` (UI/UX/prestazioni/SEO), `debugger`
- **Skill chiave**: `clean-code`, `intelligent-routing`, `brainstorm`, `plan`, `frontend-design`
- **Comandi**: `/brainstorm`, `/plan`, `/orchestrate`, `/debug`, `/test`, `/status`, `/caveman`, `/ui-ux-pro-max`, `/latex`, `/scroll-film`, `/scroll-experience`, `/classic-ml`

### Script principali

- **Verifica**: `.agents/scripts/verify_all.py`, `.agents/scripts/checklist.py`
- **Audit**: `ux_audit.py`, `accessibility_checker.py`, `schema_validator.py`, `api_validator.py`
- **Test**: `playwright_runner.py`, `test_runner.py`
