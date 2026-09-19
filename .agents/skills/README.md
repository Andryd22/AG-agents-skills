# Skill di Antigravity

> **Guida per creare e usare le skill nell'Antigravity Kit**

---

## 📋 Panoramica

I modelli di base di Antigravity (come Gemini) sono generalisti potenti, ma non conoscono il contesto del tuo progetto né gli standard del tuo team. Caricare ogni regola o strumento nella finestra di contesto dell'agente porta a "tool bloat": costi più alti, latenza e confusione.

Le **skill di Antigravity** risolvono il problema con la **divulgazione progressiva** (progressive disclosure). Una skill è un pacchetto di conoscenza specialistica che resta inattivo finché non serve: entra nel contesto dell'agente solo quando la tua richiesta corrisponde alla descrizione della skill.

---

## 📁 Struttura e ambito

Le skill sono pacchetti a cartella. Puoi definire questi ambiti secondo le tue esigenze:

| Ambito | Percorso | Descrizione |
| --- | --- | --- |
| **Workspace** | `<radice-del-workspace>/.agents/skills/` | Disponibile solo in un progetto specifico |

### Struttura della cartella di una skill

```text
my-skill/
├── SKILL.md      # (Obbligatorio) Metadati e istruzioni
├── scripts/      # (Facoltativo) Script Python o Bash
├── references/   # (Facoltativo) Testi, documentazione, modelli
└── assets/       # (Facoltativo) Immagini o loghi
```

---

## 🔍 Esempio 1: skill di code review

È una skill fatta solo di istruzioni: basta creare il file `SKILL.md`.

### Passo 1: crea la cartella

```bash
mkdir -p .agents/skills/code-review
```

### Passo 2: crea SKILL.md

```markdown
---
name: code-review
description: Rivede le modifiche al codice cercando bug, problemi di stile e violazioni delle buone pratiche. Usala per rivedere una PR o controllare la qualità del codice.
---

# Skill di code review

Quando rivedi il codice, segui questi passi:

## Checklist di revisione

1. **Correttezza**: il codice fa quello che deve?
2. **Casi limite**: le condizioni di errore sono gestite?
3. **Stile**: segue le convenzioni del progetto?
4. **Prestazioni**: ci sono inefficienze evidenti?

## Come dare il feedback

- Sii preciso su cosa va cambiato
- Spiega il perché, non solo il cosa
- Proponi alternative quando puoi
```

> **Nota**: il file `SKILL.md` contiene in cima i metadati (nome, descrizione), seguiti dalle istruzioni. L'agente legge solo i metadati e carica le istruzioni complete solo quando servono.

### Prova

Crea un file `demo_bad_code.py`:

```python
import time

def get_user_data(users, id):
    # Cerca l'utente per ID
    for u in users:
        if u['id'] == id:
            return u
    return None

def process_payments(items):
    total = 0
    for i in items:
        # Calcola la tassa
        tax = i['price'] * 0.1
        total = total + i['price'] + tax
        time.sleep(0.1)  # Simula una chiamata di rete lenta
    return total

def run_batch():
    users = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
    items = [{'price': 10}, {'price': 20}, {'price': 100}]

    u = get_user_data(users, 3)
    print("Utente trovato: " + u['name'])  # Va in crash se è None

    print("Totale: " + str(process_payments(items)))

if __name__ == "__main__":
    run_batch()
```

**Prompt**: `rivedi il file @demo_bad_code.py`

L'agente riconosce da solo la skill `code-review`, ne carica le istruzioni e le segue.

---

## 📄 Esempio 2: skill per l'intestazione di licenza

Questa skill usa un file di riferimento nella cartella `resources/` (o `references/`).

### Passo 1: crea la cartella

```bash
mkdir -p .agents/skills/license-header-adder/resources
```

### Passo 2: crea il file modello

**`.agents/skills/license-header-adder/resources/HEADER.txt`**:

```text
/*
 * Copyright (c) 2026 NOME_AZIENDA S.r.l.
 * Tutti i diritti riservati.
 * Codice proprietario e riservato.
 */
```

### Passo 3: crea SKILL.md

**`.agents/skills/license-header-adder/SKILL.md`**:

```markdown
---
name: license-header-adder
description: Aggiunge l'intestazione di licenza aziendale standard ai nuovi file sorgente.
---

# Intestazione di licenza

Questa skill fa in modo che ogni nuovo file sorgente abbia l'intestazione di copyright corretta.

## Istruzioni

1. **Leggi il modello**: leggi il contenuto di `resources/HEADER.txt`.
2. **Applicalo al file**: quando crei un nuovo file, metti in cima esattamente questo contenuto.
3. **Adatta la sintassi**:
   - Per i linguaggi in stile C (Java, TS) tieni il blocco `/* */`.
   - Per Python e shell trasformalo in commenti `#`.
```

### Prova

**Prompt**: `Crea un nuovo script Python chiamato data_processor.py che stampa 'Hello World'.`

L'agente legge il modello, trasforma i commenti nello stile di Python e li aggiunge da solo in cima al file.

---

## 🎯 Conclusione

Creando skill trasformi un modello di AI generico in un esperto del tuo progetto:

- ✅ Rendi sistematiche le buone pratiche
- ✅ Rispetti le regole di code review
- ✅ Aggiungi da solo le intestazioni di licenza
- ✅ L'agente sa già come lavorare con il tuo team

Invece di ricordare di continuo all'AI "ricordati di aggiungere la licenza" o "sistema il formato del commit", ora l'agente lo fa da solo.
