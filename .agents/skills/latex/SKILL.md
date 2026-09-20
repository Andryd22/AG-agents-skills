---
name: latex
description: 'Appunti universitari in LaTeX: prepara la cartella di un corso, trasforma il PDF di una lezione (e la sua trascrizione) in un capitolo con figure, riferimenti e compilazione, oppure revisiona tutto il progetto. Passa il lavoro all''agente latex-specialist con le skill latex-tutor e latex-review. Usala quando l''utente lancia /latex o chiede appunti LaTeX dalle slide.'
---

# /latex — Appunti universitari in LaTeX

La richiesta è il testo che segue `/latex`.

---

## Modalità

| Segnale nella richiesta | Modalità | Skill |
| --- | --- | --- |
| "setup", "nuovo corso", "new course", cartella del corso senza `latex/main.tex` né `main.tex` | **Setup** | `@[skills/latex-tutor]` (assets) |
| il nome o il percorso di un PDF, "capitolo", "genera", "da queste slide", un PDF o una trascrizione allegati | **Generazione** | `@[skills/latex-tutor]` |
| "revisiona", "controlla", "review", "correggi", "compila?" | **Revisione** | `@[skills/latex-review]` |
| non chiaro | una domanda: nuovo corso, nuovo capitolo o revisione? | |

Passa il lavoro a `latex-specialist` con la richiesta, la modalità e i file coinvolti (↪ `@latex-specialist: <modalità> <file>`).

---

## Setup

Il progetto LaTeX sta nella sottocartella `latex/` della cartella del corso (quella in cui è installato il kit); i PDF delle lezioni e gli altri materiali del corso possono restare fuori.

1. Chiedi il titolo del corso e il nome dell'autore (salta quello che la richiesta dice già). Il corso nuovo è in italiano; in inglese solo se l'utente lo chiede.
2. Se esiste già `latex/main.tex`, o un `main.tex` nella cartella corrente, il corso è già pronto: dillo all'utente e non creare niente.
3. Crea la cartella `latex/` e, dentro, senza sovrascrivere niente di quello che esiste:
   - `main.tex` e `preamble.tex` da `.agents/skills/latex-tutor/assets/`, con titolo e autore compilati (per un corso in inglese segui il commento in cima a `preamble.tex`);
   - `chapters/`, `images/`, `transcripts/`, e `slides/` a meno che i PDF delle lezioni non stiano già in un'altra cartella (per esempio nella cartella del corso, accanto a `latex/`).
4. Di' all'utente dove mettere i PDF delle lezioni e come generare il primo capitolo (`/latex latex/slides/1-Introduzione.pdf`, oppure il percorso del PDF dove sta già).

---

## Generazione

Segui la Procedura di `latex-tutor` (modalità Progetto) sulla radice del progetto: `latex/` se esiste `latex/main.tex`, altrimenti la cartella corrente (i corsi preparati prima, come DMML, hanno `main.tex` lì).

1. Leggi il preambolo (e la lingua del corso dal suo `babel`), mappa i capitoli esistenti con `grep`, leggi l'ultimo capitolo modificato per copiarne le convenzioni.
2. Leggi il PDF (direttamente o con `slides.py text` e `render`) e la trascrizione, se c'è.
3. Scrivi `<radice>/chapters/<nome del PDF>.tex` senza sovrascrivere un file esistente; aggiungi l'`\include` a `<radice>/main.tex`.
4. Figure: TikZ per i diagrammi semplici, ritagli con `slides.py crop` per quelli complessi, segnaposto solo come ripiego.
5. Compila, correggi gli errori del nuovo capitolo, riporta sezioni, figure, riferimenti e avvisi.

Senza una cartella di corso (un solo PDF in chat), `latex-tutor` lavora in modalità Chat: il corpo del capitolo in un blocco di codice `latex`.

---

## Revisione

Segui la Procedura di revisione di `latex-review`: `check_project.py`, compilazione e log, checklist di stile, resoconto per gravità. Correggi solo dopo che l'utente ha detto quali problemi correggere.

---

## Uso

```text
/latex setup
/latex latex/slides/5-Clustering.pdf
/latex latex/slides/5-Clustering.pdf con latex/transcripts/5-Clustering.txt
/latex 5-Clustering.pdf
/latex revisione
/latex correggi i problemi critici del capitolo 7
```

---

## Principi

- **I capitoli sono dell'utente**: mai sovrascriverne uno, mai ristrutturare la prosa senza approvazione.
- **Deve compilare**: ogni generazione finisce con una compilazione.
- **Sintetizza, non trascrivere**: struttura per argomento, non per slide.
- **LaTeX nella lingua del corso** (italiano per i corsi nuovi, quella dei capitoli già scritti per i corsi esistenti), conversazione in italiano.
- Convenzioni e checklist completa in `@[agents/latex-specialist]`.
