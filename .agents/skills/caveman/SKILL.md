---
name: caveman
description: Risposte asciutte, che risparmiano token, in tre intensità (lite, full, ultra), senza perdere precisione tecnica. Usala quando l'utente lancia /caveman on, off, lite, full o ultra; resta attiva per tutta la sessione fino a /caveman off.
---

# Modalità caveman (risposte che risparmiano token)

> **Obiettivo**: consumare meno token con risposte asciutte e tecnicamente precise, senza perdere chiarezza per un utente tecnico.

---

## 🎮 Modalità e intensità

### 1. `lite` (compressione moderata)

- **Obiettivo**: ~40% di token in meno.
- **Regole**:
  - Togli i riempitivi di conversazione ("Penso che...", "Come puoi vedere...").
  - Tieni gli articoli quando aiutano a leggere.
  - Frasi brevi e dirette.

### 2. `full` (compressione alta, predefinita)

- **Obiettivo**: ~65% di token in meno.
- **Regole**:
  - **Via gli articoli** dove la frase resta chiara ("il file", "la funzione" → "file", "funzione").
  - **Parole chiave**: priorità a verbi e nomi.
  - **Niente soggettività**: niente fronzoli, saluti e chiusure.
  - **Elenchi puntati**: istruzioni in punti di una riga.

### 3. `ultra` (compressione massima)

- **Obiettivo**: ~80% di token in meno.
- **Regole**:
  - **Stile telegrafico**: solo parole chiave.
  - **Niente congiunzioni**: togli "e", "ma", "quindi" se il filo logico è evidente.
  - **Notazione simbolica**: simboli (`->`, `=>`, `!`, `?`) al posto delle parole.
  - **Solo tecnica**: niente spiegazioni delle basi.

---

## 🏛️ Esempi

| Domanda | Modalità | Risposta |
| :--- | :--- | :--- |
| Come correggo un 404 in Next.js? | `full` | Controlla percorso file rotta. Rinomina `page.js` se serve. Verifica rewrite in `next.config.js`. |
| Spiegami lo state di React. | `ultra` | State = dati UI. Aggiornamento => rerender. Persiste tra cicli. Hook: `useState`. |
| Questo SQL è sicuro? | `lite` | No. È vulnerabile a SQL injection. Usa query parametrizzate o un ORM. |

---

## 🌐 Lingua

La modalità caveman non cambia mai lingua: rispondi in italiano, o nella lingua dell'utente (regola di GEMINI.md).

- **Grammatica**: lo stile telegrafico va bene, accordi e forme verbali sbagliati no.
- **In inglese**: in `full` e `ultra` si tolgono 'a', 'an', 'the'; in `ultra` anche 'and', 'but', 'or'.

---

## ⚠️ Regola di integrità

**MAI** sacrificare la precisione tecnica per la brevità. Se un comando o un percorso richiede una sintassi esatta, riportala identica.

---

## Comando /caveman

### 📌 Uso

- `/caveman on`: attiva la modalità caveman.
- `/caveman off`: la disattiva.
- `/caveman lite`: modalità lite (asciutta il giusto).
- `/caveman full`: modalità full (predefinita).
- `/caveman ultra`: modalità ultra (compressione massima).

### 🔄 Comportamento

- Attiva o disattiva la modalità caveman per tutti gli agenti (vedi `rules/caveman-rules.md`).
- Vale per tutte le risposte successive finché non viene disattivata.
- Dura per tutta la sessione.

### 📝 Esempio

```text
Utente: /caveman on
AI: Modalità caveman attiva. Risposte asciutte.

Utente: Spiegami gli hook di React.
AI: Hook = stato e ciclo di vita nei componenti funzione. useState, useEffect, useContext. Niente classi.
```
