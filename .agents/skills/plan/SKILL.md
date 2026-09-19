---
name: plan
description: Scrive il piano di un lavoro in docs/PLAN-{slug}.md senza scrivere codice. Chiede solo quello che manca, divide il lavoro in task piccoli e verificabili con agente e skill, chiude con la verifica finale. Usala quando l'utente lancia /plan, chiede un piano prima di costruire o scrive requisiti, user story, backlog o MVP; /orchestrate e l'orchestrator la usano come prima fase.
---

# /plan - Piano di lavoro

La richiesta è il testo che segue `/plan`. Il risultato è un solo file, `docs/PLAN-{slug}.md`: niente codice.

---

## 🔴 Regole

1. **Niente codice.** Scrivi solo `docs/PLAN-{slug}.md` (crea `docs/` se manca), nessun altro file.
2. **Il piano lo scrivi tu**, con i tuoi strumenti: non serve un agente dedicato. Non usare la modalità Plan nativa di Antigravity.
3. **Socratic Gate proporzionato** (vedi `GEMINI.md`): 1-2 domande se la richiesta è quasi chiara, fino a 3 per un progetto aperto. Non rifare domande a cui la conversazione ha già risposto.
4. **Niente invenzioni:** stime, scadenze e decisioni che l'utente non ha preso non vanno nel piano. Quello che non sai diventa una domanda o un rischio.

---

## Fase 0 - Contesto

Ordine delle fonti: conversazione > piani già in `docs/` > file del progetto > nome della cartella. Il tipo di progetto non si deduce mai dal nome della cartella.

| Se trovi | Allora |
| --- | --- |
| Richiesta e decisioni nel prompt (chiamata dall'orchestrator) | Usale così come sono, senza richiederle |
| Un `docs/PLAN-*.md` sullo stesso lavoro | Leggilo e continualo, non ripartire da zero |
| Un progetto esistente grande o poco chiaro | Fai mappare a `explorer-agent` le parti toccate, poi pianifica |
| Niente di tutto questo | Fai le domande della Fase 1 |

Controlla anche il sistema operativo: su Windows i comandi del piano sono PowerShell, su macOS e Linux bash.

## Fase 1 - Analisi

```text
Dalla richiesta ricava:
├── Dominio: che lavoro è (sito, API, script, analisi dati, appunti...)
├── Funzionalità: quelle chieste più quelle implicite
├── Vincoli: stack, tempi, scala, cose da non toccare
└── Rischi: integrazioni complesse, sicurezza, prestazioni
```

Se una di queste cambia il piano e non la sai, chiedila. Se la richiesta chiede solo di analizzare, spiegare o trovare qualcosa, non serve un piano: rispondi in chat (con `explorer-agent` se serve mappare il codice).

## Fase 2 - Il file

### Nome

| Richiesta | File |
| --- | --- |
| `/plan sito e-commerce con carrello` | `docs/PLAN-ecommerce-carrello.md` |
| `/plan aggiungi la dark mode` | `docs/PLAN-dark-mode.md` |
| `/plan correggi il bug del login` | `docs/PLAN-fix-login.md` |
| `/plan pipeline di classificazione sul dataset` | `docs/PLAN-classificazione.md` |

1. Prendi 2-3 parole chiave dalla richiesta.
2. Minuscole, separate da trattini, senza caratteri speciali.
3. Slug di al massimo 30 caratteri.
4. Mai nomi generici come `plan.md` o `PLAN.md`: lo slug tiene separati più piani. `/orchestrate` e l'orchestrator cercano i piani solo in `docs/PLAN-{slug}.md`.

### Sezioni

| Sezione | Cosa contiene |
| --- | --- |
| **Obiettivo** | Cosa si costruisce e perché |
| **Tipo di progetto** | WEB, BACKEND, ML, LATEX, SCROLL 3D... detto esplicitamente |
| **Criteri di successo** | Risultati misurabili |
| **Stack** | Tecnologie scelte e motivo (solo se il lavoro le sceglie) |
| **Struttura dei file** | Cartelle e file che nascono o cambiano |
| **Task** | Tutti i task, nel formato qui sotto |
| **Rischi e domande aperte** | Quello che può andare storto e quello che l'utente deve ancora decidere |
| **Fase X: verifica** | La checklist finale |

### Formato dei task

Ogni task ha: id, nome, agente, skill, dipendenze e INPUT → OUTPUT → VERIFICA. Un task senza verifica è incompleto.

```markdown
### T3 - Endpoint di login
- Agente: `backend-specialist` · Skill: `api-patterns`
- Dipende da: T1 (schema utenti)
- INPUT: schema `users`, decisione "JWT in cookie httpOnly"
- OUTPUT: `POST /api/auth/login` con test
- VERIFICA: i test di T3 passano, login errato → 401
```

| Principio | Regola |
| --- | --- |
| **Piccoli** | Un risultato chiaro per task, facile da verificare e da annullare |
| **Dipendenze vere** | Solo i blocchi reali, niente "forse" |
| **Parallelo** | Solo su file diversi; stesso file, componente → chi lo usa, schema → tipi vanno in serie |
| **Perché** | Ogni task dice perché serve, non solo cosa fa |
| **Tappe** | Ogni gruppo di task finisce con qualcosa che funziona |

L'agente di ogni task si sceglie con la tabella di `@[skills/intelligent-routing]`.

### Fase X: verifica

Il piano finisce sempre con questa checklist, adattata al progetto:

```markdown
## Fase X: verifica
- [ ] Lint e tipi con gli strumenti del progetto (`npm run lint`, `npx tsc --noEmit`, `ruff check`...)
- [ ] `python .agents/scripts/checklist.py .`
- [ ] Build (`npm run build` o equivalente)
- [ ] Con l'app avviata: `python .agents/scripts/verify_all.py . --url http://localhost:3000`
```

Chi implementa segna `[x]` solo dopo aver eseguito davvero il controllo; quando passano tutti aggiunge in fondo `## ✅ Fase X completata` con la data.

---

## Uscita

Prima di chiudere: il file esiste, rileggendolo ha tutte le sezioni. Poi scrivi all'utente:

```text
[OK] Piano creato: docs/PLAN-{slug}.md

Prossimi passi:
- rivedi il piano (puoi modificarlo a mano)
- chiedimi di implementarlo, oppure lancia /orchestrate se tocca più domini
```
