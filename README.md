# Antigravity Kit

## Installazione Rapida

Installa la cartella `.agents/` contenente tutti i template nel tuo progetto:

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
<td>Installa <code>.agents/</code> nel progetto corrente (sovrascrive se già presente)</td>
</tr>
<tr>
<td style="white-space: nowrap"><code>npx github:Andryd22/⁠AG-⁠agents-⁠skills update</code></td>
<td>Aggiorna <code>.agents/</code> all'ultima versione da GitHub (le modifiche locali a <code>.agents/</code> non vengono mantenute)</td>
</tr>
</tbody>
</table>

## Cosa è Incluso

| Componente    | Quantità | Descrizione                                                        |
| ------------- | -------- | ------------------------------------------------------------------ |
| **Agenti**    | 18       | Personas AI specializzate (frontend, backend, AI/ML, LaTeX, scroll 3D, ecc.) |
| **Skill**     | 30       | Moduli di conoscenza specifici per dominio                         |
| **Workflow**  | 16       | Procedure attivabili tramite slash command                         |

La mappa completa di agenti, skill e script è in [`.agents/ARCHITECTURE.md`](.agents/ARCHITECTURE.md).

## Utilizzo

### Usare gli Agenti

**Non c'è bisogno di menzionare esplicitamente gli agenti!** Il sistema rileva automaticamente e applica l'Agent (o gli Agents) giusti:

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
- ✅ Puoi sempre forzare l'uso di un agente menzionandolo esplicitamente

### Usare i Workflow

> ⚠️ Antigravity ha deprecato i workflow: dal 1° novembre 2026 vengono ritirati e diventano skill richiamate con lo stesso `/nome`. La migrazione del kit è in programma.

Richiama i workflow tramite gli slash command:

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

Esempio:

```text
/brainstorm sistema di autenticazione
/create pagina di destinazione con varie sezioni
/debug perché il login fallisce
```

### Usare le Skill

Le skill vengono caricate automaticamente in base al contesto della task. L'AI legge le descrizioni delle skill e applica le conoscenze pertinenti.

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
