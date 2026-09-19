---
name: clean-code
description: Regole pragmatiche per scrivere codice - conciso, diretto, niente sovraingegnerizzazione, niente commenti inutili. Commenti in italiano, nomi in inglese.
metadata:
  version: "2.1"
  priority: CRITICAL
---

# Clean Code - Regole pragmatiche per l'AI

> **SKILL CRITICA** - Sii **conciso, diretto e concentrato sulla soluzione**.

---

## Principi

| Principio | Regola |
| --- | --- |
| **SRP** | Responsabilità singola: ogni funzione o classe fa UNA cosa |
| **DRY** | Non ripeterti: estrai i duplicati, riusa |
| **KISS** | Tienilo semplice: la soluzione più semplice che funziona |
| **YAGNI** | Non ti servirà: non costruire funzionalità che nessuno usa |
| **Boy Scout** | Lascia il codice più pulito di come l'hai trovato |

---

## Nomi e lingua

| Elemento | Convenzione |
| --- | --- |
| **Variabili** | Rivelano l'intento: `userCount`, non `n` |
| **Funzioni** | Verbo + nome: `getUserById()`, non `user()` |
| **Booleani** | Forma di domanda: `isActive`, `hasPermission`, `canEdit` |
| **Costanti** | SCREAMING_SNAKE: `MAX_RETRY_COUNT` |
| **Lingua** | Nomi (variabili, funzioni, classi, file) in inglese; commenti, docstring e messaggi per l'utente in italiano |

> **Regola:** se un nome ha bisogno di un commento per essere capito, cambia il nome.

---

## Funzioni

| Regola | Descrizione |
| --- | --- |
| **Piccole** | Massimo 20 righe, meglio 5-10 |
| **Una cosa** | Fa una cosa sola, e la fa bene |
| **Un livello** | Un solo livello di astrazione per funzione |
| **Pochi argomenti** | Massimo 3, meglio 0-2 |
| **Niente effetti collaterali** | Non modificare gli input quando nessuno se lo aspetta |

---

## Struttura del codice

| Schema | Come |
| --- | --- |
| **Guard clause** | Uscite anticipate per i casi limite |
| **Piatto > annidato** | Evita l'annidamento profondo (massimo 2 livelli) |
| **Composizione** | Funzioni piccole messe insieme |
| **Vicinanza** | Il codice che va insieme sta vicino |

---

## Stile dell'AI

| Situazione | Cosa fare |
| --- | --- |
| L'utente chiede una funzionalità | Scrivila direttamente |
| L'utente segnala un bug | Correggilo, senza fare lezioni |
| Requisito poco chiaro | Chiedi, non dare per scontato |

---

## Anti-pattern (DA NON FARE)

| ❌ Schema | ✅ Correzione |
| --- | --- |
| Commentare ogni riga | Togli i commenti ovvi |
| Helper per una riga | Scrivi il codice sul posto |
| Factory per 2 oggetti | Istanziali direttamente |
| utils.ts con 1 funzione | Metti il codice dove si usa |
| "Per prima cosa importiamo..." | Scrivi il codice e basta |
| Annidamento profondo | Guard clause |
| Numeri magici | Costanti con un nome |
| Funzioni onnipotenti | Dividile per responsabilità |

---

## 🔴 Prima di modificare QUALSIASI file (PRIMA PENSA!)

**Prima di cambiare un file, chiediti:**

| Domanda | Perché |
| --- | --- |
| **Chi importa questo file?** | Potrebbe rompersi |
| **Cosa importa questo file?** | Cambi di interfaccia |
| **Quali test lo coprono?** | I test potrebbero fallire |
| **È un componente condiviso?** | Cambia in più punti |

**Controllo rapido:**

```text
File da modificare: UserService.ts
└── Chi lo importa? → UserController.ts, AuthController.ts
└── Vanno cambiati anche loro? → Controlla le firme delle funzioni
```

> 🔴 **Regola:** modifica il file e tutti i file che ne dipendono NELLO STESSO task.
> 🔴 **Mai lasciare import rotti o aggiornamenti mancanti.**

---

## Riassunto

| Fai | Non fare |
| --- | --- |
| Scrivi il codice direttamente | Scrivere tutorial |
| Lascia che il codice si spieghi | Aggiungere commenti ovvi |
| Correggi subito i bug | Spiegare la correzione prima di farla |
| Scrivi sul posto le cose piccole | Creare file inutili |
| Dai nomi chiari | Usare abbreviazioni |
| Tieni piccole le funzioni | Scrivere funzioni da 100+ righe |

> **Ricorda: l'utente vuole codice che funziona, non una lezione di programmazione.**

---

## 🔴 Controllo prima di chiudere (OBBLIGATORIO)

**Prima di dire "fatto", verifica:**

| Controllo | Domanda |
| --- | --- |
| ✅ **Obiettivo raggiunto?** | Ho fatto esattamente quello che l'utente ha chiesto? |
| ✅ **File modificati?** | Ho cambiato tutti i file necessari? |
| ✅ **Il codice funziona?** | Ho provato o verificato la modifica? |
| ✅ **Nessun errore?** | Lint e TypeScript passano? |
| ✅ **Niente di dimenticato?** | Ho saltato qualche caso limite? |

> 🔴 **Regola:** se QUALSIASI controllo fallisce, correggilo prima di chiudere.

---

## Script di verifica (OBBLIGATORI)

> 🔴 **CRITICO:** ogni agente, finito il lavoro, esegue SOLO gli script delle proprie skill.

### Agente → script

| Agente | Script | Comando |
| --- | --- | --- |
| **frontend-specialist** | Audit UX | `python .agents/skills/frontend-design/scripts/ux_audit.py .` |
| **frontend-specialist** | Accessibilità | `python .agents/skills/frontend-design/scripts/accessibility_checker.py .` |
| **backend-specialist** | Validazione API | `python .agents/skills/api-patterns/scripts/api_validator.py .` |
| **backend-specialist** | Validazione schema | `python .agents/skills/database-design/scripts/schema_validator.py .` |
| **frontend-specialist** | Prestazioni React | `python .agents/skills/nextjs-react-expert/scripts/react_performance_checker.py .` |
| **test-engineer** | Test | `python .agents/skills/test/scripts/test_runner.py .` |
| **qa-automation-engineer** | Playwright | `python .agents/skills/webapp-testing/scripts/playwright_runner.py <url>` |
| **latex-specialist** | Controllo del progetto | `python .agents/skills/latex-review/scripts/check_project.py .` |
| **Qualsiasi agente** | Lint e tipi | gli strumenti del progetto: `npm run lint`, `npx tsc --noEmit`, `ruff check`, `mypy` |

> ❌ **SBAGLIATO:** `test-engineer` che lancia `ux_audit.py`
> ✅ **GIUSTO:** `frontend-specialist` che lancia `ux_audit.py`

---

### 🔴 Output degli script (LEGGI → RIASSUMI → CHIEDI)

**Quando lanci uno script di validazione, DEVI:**

1. **Lanciare lo script** e raccogliere TUTTO l'output
2. **Analizzare l'output**: errori, avvisi, controlli superati
3. **Riassumere all'utente** in questo formato:

```markdown
## Risultati dello script: [nome_script.py]

### ❌ Errori (X)
- [File:riga] Descrizione dell'errore 1
- [File:riga] Descrizione dell'errore 2

### ⚠️ Avvisi (Y)
- [File:riga] Descrizione dell'avviso

### ✅ Superati (Z)
- Controllo 1 superato
- Controllo 2 superato

**Correggo gli X errori?**
```

1. **Aspettare la conferma dell'utente** prima di correggere
2. **Dopo la correzione** → rilanciare lo script per conferma

> 🔴 **VIOLAZIONE:** lanciare lo script e ignorarne l'output = task FALLITO.
> 🔴 **VIOLAZIONE:** correggere da solo senza chiedere = non permesso.
> 🔴 **Regola:** sempre LEGGI l'output → RIASSUMI → CHIEDI → poi correggi.
