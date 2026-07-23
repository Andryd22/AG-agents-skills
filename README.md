# Antigravity Kit

## Installazione Rapida

Installa la cartella `.agent/` contenente tutti i template nel tuo progetto:

```bash
npx github:Andryd22/AG-agents-skills init -y
```

| Comando | Descrizione |
| ------- | ----------- |
| `npx github:Andryd22/AG-agents-skills init` | Installa `.agent/` nel progetto corrente |
| `npx github:Andryd22/AG-agents-skills init -y` | Installa automaticamente e sovrascrive se già presente |
| `npx github:Andryd22/AG-agents-skills update` | Aggiorna `.agent/` all'ultima versione da GitHub |
| `npx github:Andryd22/AG-agents-skills status` | Mostra i componenti inclusi |
| `npx github:Andryd22/AG-agents-skills force` | Reinstalla e forza la sovrascrittura di `.agent/` |

## Cosa è Incluso

| Componente    | Quantità | Descrizione                                                        |
| ------------- | -------- | ------------------------------------------------------------------ |
| **Agenti**    | 25       | Personas AI specializzate (frontend, backend, AI/ML, IoT, LaTeX, ecc.) |
| **Skill**     | 48       | Moduli di conoscenza specifici per dominio                         |
| **Workflow**  | 13       | Procedure attivabili tramite slash command                         |

## Utilizzo

### Usare gli Agenti

**Non c'è bisogno di menzionare esplicitamente gli agenti!** Il sistema rileva automaticamente e applica l'Agent (o gli Agents) giusti:

```
Utente: "Aggiungi l'autenticazione JWT"
AI: 🤖 Applico @security-auditor + @backend-specialist...

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
| `/ui-ux-pro-max` | Progetta interfacce con 50 stili       |
| `/caveman`       | Attiva la modalità di risposta per risparmiare token |
| `/html-it`       | Framework per output HTML di alta qualità |
| `/latex`         | Scrive o revisiona LaTeX accademico (agent latex-specialist) |

Esempio:

```text
/brainstorm sistema di autenticazione
/create pagina di destinazione con varie sezioni
/debug perché il login fallisce
```

### Usare le Skill

Le skill vengono caricate automaticamente in base al contesto della task. L'AI legge le descrizioni delle skill e applica le conoscenze pertinenti.

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
