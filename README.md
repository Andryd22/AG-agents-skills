# Antigravity Kit

## Installazione Rapida

Installa agenti, skill e regole del kit nella cartella `.agents/` del tuo progetto:

<table>
<thead>
<tr>
<th style="white-space: nowrap">Comando</th>
<th>Descrizione</th>
</tr>
</thead>
<tbody>
<tr>
<td style="white-space: nowrap"><code>npx github:Andryd22/⁠AG-⁠agents-⁠skills init -⁠y</code></td>
<td>Installa il kit in <code>.agents/</code> del progetto corrente</td>
</tr>
<tr>
<td style="white-space: nowrap"><code>npx github:Andryd22/⁠AG-⁠agents-⁠skills update</code></td>
<td>Aggiorna il kit all'ultima versione da GitHub</td>
</tr>
</tbody>
</table>

Quando funziona, l'installer scrive sempre `Kit vX.Y.Z installato in …` con la versione installata e il numero di file, agenti e skill.

**Windows con PowerShell:** se il comando torna al prompt senza scrivere niente, `npx` non ha avviato l'installer (succede con lo script `npx.ps1` che PowerShell usa al posto di `npx`). Lancia lo stesso comando con `npx.cmd`:

```powershell
npx.cmd github:Andryd22/AG-agents-skills init -y
npx.cmd github:Andryd22/AG-agents-skills update
```

Al primo avvio `npx.cmd` chiede `Ok to proceed? (y)`: rispondi `y`. Dal Prompt dei comandi (cmd), da Git Bash, su macOS e su Linux basta `npx`.

L'installer sostituisce solo agenti, skill, regole e script del kit (li annota in `.agents/.ag-kit.json`): le modifiche locali a quei file non vengono mantenute, mentre gli agenti, le skill e le regole tuoi restano. Se trova una vecchia installazione in `.agent/`, la sposta in `.agent.bak/`.

## Cosa è Incluso

| Componente | Quantità | Descrizione |
| --- | --- | --- |
| **Agenti** | 12 | Custom agent di Antigravity (frontend, backend, AI/ML, LaTeX, scroll 3D, ecc.) |
| **Skill** | 32 | Moduli di conoscenza e slash command (`/plan`, `/debug`, `/test`, ...) |
| **Regole** | 2 | `GEMINI.md` (sempre attiva) e `caveman-rules.md` |

La mappa completa di agenti, skill e script è in [`.agents/ARCHITECTURE.md`](.agents/ARCHITECTURE.md).

## Utilizzo

### Usare gli Agenti

Gli agenti sono custom agent di Antigravity in `.agents/agents/`. **Non c'è bisogno di menzionarli:** la regola `GEMINI.md` sceglie lo specialista giusto e gli passa il lavoro come subagent (`invoke_subagent`):

```text
Utente: "Aggiungi l'autenticazione JWT"
AI:     🤖 @backend-specialist + @test-engineer · 📚 api-patterns, test

Utente: "Correggi il pulsante della dark mode"
AI:     🤖 @frontend-specialist · 📚 frontend-design, tailwind-patterns

Utente: "Il login restituisce un errore 500"
AI:     🤖 @debugger · 📚 debug
        ↪ @explorer-agent: trova il codice del login
        ↩ @explorer-agent
```

Ogni risposta che usa un agente o una skill del kit comincia con una riga così: 🤖 indica l'agente, 📚 le skill lette per quella risposta (un comando `/nome` conta come skill). `↪` e `↩` segnano il passaggio del lavoro a un subagent e il suo ritorno; `📚 +` una skill caricata a metà risposta.

**Come funziona:**

- Analizza silenziosamente la tua richiesta
- Rileva automaticamente i domini di competenza (frontend, backend, sicurezza, ecc.)
- Seleziona i migliori specialisti
- Ti dice quale agente e quali skill sta usando
- Ottieni risposte a livello di specialista senza dover conoscere l'architettura del sistema

**Vantaggi:**

- ✅ Nessuna curva di apprendimento: descrivi solo ciò di cui hai bisogno
- ✅ Ottieni sempre risposte da esperti
- ✅ Trasparenza: mostra quale agente viene utilizzato
- ✅ Puoi sempre forzare l'uso di un agente menzionandolo esplicitamente, o sceglierlo come agente principale (selettore nell'app, `/agents` nella CLI)

### Usare i comandi

I comandi del kit sono già skill e si richiamano con `/nome`.

| Comando | Descrizione |
| --- | --- |
| `/brainstorm` | Esplora le opzioni prima dell'implementazione |
| `/debug` | Debugging sistematico |
| `/orchestrate` | Coordinazione multi-agente |
| `/plan` | Scrive il piano del lavoro in `docs/PLAN-{slug}.md`, senza codice |
| `/status` | Controlla lo stato del progetto |
| `/test` | Genera ed esegue i test |
| `/ui-ux-pro-max` | Progetta interfacce con 58 stili e 96 palette |
| `/caveman` | Attiva la modalità di risposta per risparmiare token |
| `/scroll-film` | Costruisce siti animati cinematici a scorrimento continuo (scrollytelling) |
| `/latex` | Appunti LaTeX: prepara un corso, scrive un capitolo da un PDF (con figure ritagliate e compilazione), revisiona il progetto |
| `/scroll-experience` | Esperienze scroll immersive unificate: 3D (three-js) + cinematico (scroll-film) + video (scroll-world) |
| `/classic-ml` | Data mining e machine learning classico con pandas e scikit-learn |

Esempio:

```text
/brainstorm sistema di autenticazione
/plan pagina di destinazione con varie sezioni
/debug perché il login fallisce
```

### Usare le Skill

Le skill vengono caricate automaticamente in base al contesto della task: ogni agente vede tutte le skill del kit (nome e descrizione), legge per prime quelle elencate nel suo corpo ("Le tue skill") e sceglie le altre dalla descrizione.

### Controlli finali

`python .agents/scripts/checklist.py .` esegue i controlli di base (schema, test, UX); con `--url http://localhost:3000` aggiunge i test E2E.

Per la suite completa prima di un rilascio: `python .agents/scripts/verify_all.py . --url <URL>`.

## 🪨 Caveman Mode

Riduci l'uso dei token di circa il 65% con risposte concise e tecnicamente accurate.

### Utilizzo

- Abilita: `/caveman on`
- Disabilita: `/caveman off`
- Livelli di intensità:
  - Lite: `/caveman lite`
  - Full (predefinito): `/caveman full`
  - Ultra: `/caveman ultra`

## Licenza

MIT ©
