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

L'installer sostituisce solo agenti, skill, regole e script del kit (li annota in `.agents/.ag-kit.json`): le modifiche locali a quei file non vengono mantenute, mentre gli agenti, le skill e le regole tuoi restano. Se trova una vecchia installazione in `.agent/`, la sposta in `.agent.bak/`.

## Cosa è Incluso

| Componente    | Quantità | Descrizione                                                        |
| ------------- | -------- | ------------------------------------------------------------------ |
| **Agenti**    | 15       | Custom agent di Antigravity (frontend, backend, AI/ML, LaTeX, scroll 3D, ecc.) |
| **Skill**     | 39       | Moduli di conoscenza e slash command (`/plan`, `/debug`, `/test`, ...) |
| **Regole**    | 2        | `GEMINI.md` (sempre attiva) e `caveman-rules.md`                   |

La mappa completa di agenti, skill e script è in [`.agents/ARCHITECTURE.md`](.agents/ARCHITECTURE.md).

## Utilizzo

### Usare gli Agenti

Gli agenti sono custom agent di Antigravity in `.agents/agents/`. **Non c'è bisogno di menzionarli:** la regola `GEMINI.md` sceglie lo specialista giusto e gli passa il lavoro come subagent (`invoke_subagent`):

```
Utente: "Aggiungi l'autenticazione JWT"
AI: 🤖 Applico @backend-specialist + @test-engineer...

Utente: "Correggi il pulsante della dark mode"
AI: 🤖 Uso @frontend-specialist...

Utente: "Il login restituisce un errore 500"
AI: 🤖 Uso @debugger per un'analisi sistematica...
```

**Come funziona:**

- Analizza silenziosamente la tua richiesta
- Rileva automaticamente i domini di competenza (frontend, backend, sicurezza, ecc.)
- Seleziona i migliori specialisti
- Ti informa su quale competenza sta venendo applicata
- Ottieni risposte a livello di specialista senza dover conoscere l'architettura del sistema

**Vantaggi:**

- ✅ Nessuna curva di apprendimento: descrivi solo ciò di cui hai bisogno
- ✅ Ottieni sempre risposte da esperti
- ✅ Trasparenza: mostra quale agente viene utilizzato
- ✅ Puoi sempre forzare l'uso di un agente menzionandolo esplicitamente, o sceglierlo come agente principale (selettore nell'app, `agy --agent <nome>` nella CLI)

L'IDE di Antigravity non supporta ancora i custom agent: lì il modello legge il file dell'agente e lo applica direttamente.

### Usare i comandi

Antigravity ha deprecato i workflow e li ritira il 1° novembre 2026: i comandi del kit sono già skill e si richiamano con lo stesso `/nome`.

| Comando          | Descrizione                           |
| ---------------- | ------------------------------------- |
| `/brainstorm`    | Esplora le opzioni prima dell'implementazione |
| `/create`        | Crea nuove funzionalità o applicazioni |
| `/debug`         | Debugging sistematico                  |
| `/deploy`        | Esegue il deploy dell'applicazione     |
| `/enhance`       | Migliora il codice esistente           |
| `/orchestrate`   | Coordinazione multi-agente             |
| `/plan`          | Crea un piano dettagliato per le task  |
| `/preview`       | Visualizza un'anteprima delle modifiche in locale |
| `/status`        | Controlla lo stato del progetto        |
| `/test`          | Genera ed esegue i test                |
| `/ui-ux-pro-max` | Progetta interfacce con 58 stili e 96 palette |
| `/caveman`       | Attiva la modalità di risposta per risparmiare token |
| `/html-it`       | Framework per output HTML di alta qualità |
| `/scroll-film`   | Costruisce siti animati cinematici a scorrimento continuo (scrollytelling) |
| `/latex`         | Scrive o revisiona LaTeX accademico (agent latex-specialist) |
| `/scroll-experience` | Esperienze scroll immersive unificate: 3D (three-js) + cinematico (scroll-film) + video (scroll-world) |
| `/classic-ml`    | Data mining e machine learning classico con pandas e scikit-learn |

Esempio:

```text
/brainstorm sistema di autenticazione
/create pagina di destinazione con varie sezioni
/debug perché il login fallisce
```

### Usare le Skill

Le skill vengono caricate automaticamente in base al contesto della task: ogni agente carica quelle del suo frontmatter, e Antigravity sceglie le altre leggendone la descrizione.

### Controlli finali

`python .agents/scripts/checklist.py .` esegue i controlli di base (schema, test, UX); con `--url http://localhost:3000` aggiunge i test E2E. Per la suite completa prima di un rilascio: `python .agents/scripts/verify_all.py . --url <URL>`. Lint e type check restano quelli del progetto (`npm run lint`, `tsc --noEmit`, ...).

## 🪨 Caveman Mode
Riduci l'uso dei token di circa il 65% con risposte concise e tecnicamente accurate.

### Utilizzo:
- Abilita: `/caveman on`
- Disabilita: `/caveman off`
- Livelli di intensità:
  - Lite: `/caveman lite`
  - Full (predefinito): `/caveman full`
  - Ultra: `/caveman ultra`

## Licenza

MIT ©
