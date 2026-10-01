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

Quando funziona, l'installer scrive `Kit vX.Y.Z installato in …` con la versione installata e il numero di file gestiti.

**Windows con PowerShell:** se il comando torna al prompt senza scrivere niente, `npx` non ha avviato l'installer. Lancia lo stesso comando con `npx.cmd`:

```powershell
npx.cmd github:Andryd22/AG-agents-skills init -y
npx.cmd github:Andryd22/AG-agents-skills update
```

### Aggiornamenti e file personali

L'installer gestisce **singoli file**, identificati da hash SHA-256 in `.agents/.ag-kit.json`. Conserva le aggiunte personali anche dentro `scripts/` o dentro una skill del kit. Se un file gestito è stato modificato, o un nuovo file del kit collide con un file personale, si ferma prima di scrivere.

```powershell
# Mostra modifiche e conflitti senza modificare il progetto
npx.cmd github:Andryd22/AG-agents-skills update --dry-run

# Dopo aver confrontato i conflitti: sostituisce e conserva gli originali in un backup
npx.cmd github:Andryd22/AG-agents-skills update --force

# Aggiorna e conserva comunque un backup dei file sostituiti
npx.cmd github:Andryd22/AG-agents-skills update --backup

# Ripristina il backup indicato dall'installer (anteprima disponibile)
npx.cmd github:Andryd22/AG-agents-skills restore .agents.backups/<id> --dry-run
npx.cmd github:Andryd22/AG-agents-skills restore .agents.backups/<id>
```

Di norma l'installer non lascia backup: i file del kit si riscaricano quando servono. Li salva in `.agents.backups/` solo con `--backup`, oppure quando `--force` sostituisce file cambiati a mano; `restore` li rimette a posto e rileva le modifiche fatte dopo l'installazione. Un errore di scrittura avvia comunque il rollback dei file già scritti. Un download fallito restituisce errore e lascia i file installati intatti. `--force` non scavalca la validazione dei percorsi o del manifest.

Il manifest registra versione, repository e, quando disponibile, commit e stato locale della sorgente. Con un vecchio manifest senza hash, i file non identificabili restano e le collisioni richiedono `--force`: non si cancellano intere cartelle. Le voci del vecchio kit che non esistono più (per esempio `skills/plan/`) vengono elencate, da togliere a mano. La vecchia `.agent/` resta intatta e va controllata per evitare regole duplicate. Se il progetto è un repository git, aggiungi `.agents.install.lock` (e `.agents.backups/`, se usi i backup) al suo `.gitignore`.

Requisiti: Node.js 20 o successivo; Git per `update`; Python 3.11 o successivo per i controlli. Per sviluppare il kit serve anche PyYAML. Le dipendenze delle singole skill (per esempio PyMuPDF e una distribuzione TeX) si installano solo quando servono.

Un'interruzione forzata può lasciare `.agents.install.lock`: prima di rimuoverlo, verifica che l'installer non sia ancora in esecuzione. I backup in `.agents.backups/` si possono cancellare quando l'aggiornamento è verificato.

## Cosa è Incluso

| Componente | Quantità | Descrizione |
| --- | --- | --- |
| **Agenti** | 12 | Custom agent di Antigravity (frontend, backend, AI/ML, LaTeX, scroll 3D, ecc.) |
| **Skill** | 32 | Moduli di conoscenza e slash command (`/kit-plan`, `/debug`, `/test`, ...) |
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

Ogni risposta che usa un agente o una skill del kit comincia con una riga così: 🤖 indica l'agente, 📚 le skill lette per quella risposta (un comando `/nome` conta come skill). `↪` e `↩` segnano il passaggio del lavoro a un subagent e il suo ritorno; `📚 +` una skill caricata a metà risposta. La delega dipende dall'utilità e dai sottocompiti, senza un numero minimo di agenti; tutti possono usare tutte le skill e gli script pertinenti.

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
| `/kit-plan` | Scrive il piano del lavoro in `docs/PLAN-{slug}.md`, senza codice |
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
/kit-plan pagina di destinazione con varie sezioni
/debug perché il login fallisce
```

### Usare le Skill

Le skill vengono caricate automaticamente in base al contesto della task: ogni agente vede tutte le skill del kit (nome e descrizione), legge per prime quelle elencate nel suo corpo ("Le tue skill") e sceglie le altre dalla descrizione.

### Controlli finali

`python .agents/scripts/checklist.py .` esegue schema, test e UX, indicando i controlli non applicabili. Se trova `main.tex` in radice o `latex/main.tex`, esegue anche il controllo strutturale LaTeX; senza questi, controlla ogni `latex/<nome>/main.tex` (per esempio un progetto per docente). La compilazione resta una verifica separata.

`python .agents/scripts/verify_all.py .` aggiunge gli audit API e accessibilità; `--url http://localhost:3000` aggiunge uno **smoke test** browser, che non sostituisce i test dei flussi applicativi. L'URL non è necessario per progetti LaTeX o ML.

Entrambi accettano `--json` e conservano nel report gli output dei controlli.

| Stato | Significato |
| --- | --- |
| `passed` | Il controllo indicato è stato eseguito con successo |
| `failed` | Errore rilevato o impossibilità di eseguire uno script richiesto |
| `skipped` | Verifica mancante: per esempio test non configurati |
| `not_applicable` | Nessun elemento pertinente: per esempio nessuno schema database |

Codici di uscita delle suite: **0** controlli applicabili superati, **1** errori, **2** verifica incompleta (controlli saltati o nessun controllo eseguito). Gli audit euristici riportano anche avvisi: il loro successo non certifica l'intero progetto. I test e le verifiche ML del progetto restano necessari.

Per contribuire al kit: `npm test`, `npm run validate` e il lint Markdown della CI. La CI esegue i test su Windows e Linux. Questi sono test del software del kit; le valutazioni comparative dei comportamenti degli agenti sono una fase separata.

### Compatibilità Antigravity

Il comando del kit è **`/kit-plan`**; `/plan` resta quello nativo di Antigravity. Se provieni da un manifest precedente senza hash, confronta e rimuovi la vecchia cartella `skills/plan/` dentro `.agents/`, dopo averne conservato eventuali personalizzazioni.

La distribuzione corrente usa `.agents/` nel progetto. Le verifiche sul formato plugin, i limiti dei percorsi e le differenze tra app, CLI e IDE sono in [docs/ANTIGRAVITY-COMPATIBILITY.md](docs/ANTIGRAVITY-COMPATIBILITY.md).

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
