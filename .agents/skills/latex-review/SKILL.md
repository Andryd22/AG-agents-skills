---
name: latex-review
description: Revisiona un progetto LaTeX di un corso cercando errori di compilazione, riferimenti rotti, immagini mancanti, segnaposto rimasti e scostamenti dalle regole di stile di latex-tutor, poi corregge quello che l'utente approva. Usala dopo aver generato i capitoli, dopo averli modificati a mano o prima di stampare o condividere gli appunti.
---

# latex-review

Sei `latex-review`, il controllo qualità di un progetto LaTeX di un corso scritto con `latex-tutor` e poi modificato a mano. Trovi prima quello che rompe la compilazione o i riferimenti, poi quello che si allontana dalle regole di stile, e lo riporti per gravità.

I capitoli sono lavoro dell'utente: segnala i problemi di stile, non riscrivere la prosa di tua iniziativa.

---

## Procedura di revisione

1. **Struttura.** Trova la radice del progetto (`latex/` se esiste `latex/main.tex`, altrimenti la cartella corrente) e leggi `<radice>/main.tex`: preambolo, ordine degli `\include`, capitoli presenti. Dal `babel` del preambolo ricavi la lingua del corso.
2. **Controlli meccanici.** Lancia lo script incluso dalla cartella del progetto:

   ```bash
   python .agents/skills/latex-review/scripts/check_project.py .
   ```

   Se il progetto sta in `latex/`, lo script lo trova da solo; i percorsi nel suo elenco sono relativi alla radice. Segue `\input`/`\include` ed elenca riferimenti non definiti, label duplicate, file di immagine mancanti, tag di citazione, figure e tabelle senza didascalia o label o con la didascalia dal lato sbagliato, segnaposto da sostituire, numeri di capitolo o di sezione scritti a mano, immagini non usate, `\uline`, `\tikzstyle` e `cases`.
3. **Compilazione.** `latexmk -cd -pdf -interaction=nonstopmode <radice>/main.tex`, poi leggi `<radice>/main.log`: errori (righe con `!`), riferimenti `undefined`, label `multiply defined`, `Overfull \hbox` più larghi di 10pt, file mancanti. Per ciascuno indica file e riga. Se non c'è una distribuzione TeX installata, dillo e vai avanti.
4. **Stile.** Leggi i capitoli da rivedere (tutti, o quelli che l'utente nomina) confrontandoli con la checklist qui sotto.
5. **Resoconto** in italiano, nel formato qui sotto.

---

## Checklist

### 1. Sicurezza della compilazione (🔴 critico)

| Controllo | Cosa cercare |
| --- | --- |
| Tag di citazione | `[cite]`, `<source>`, `[source]`, `<ref>`, `[citation]` |
| Caratteri speciali | `&` fuori dalle tabelle, `_` o `^` fuori dalla matematica, `%`, `#`, `$` senza escape |
| Ambienti | ogni `\begin{...}` chiuso, graffe bilanciate |
| Label e riferimenti | label duplicate, `\ref` a label che non esistono |
| Immagini | file di `\includegraphics` che non esistono |
| Pacchetti | comandi il cui pacchetto non è nel preambolo (`\hl` richiede `soul`) |

### 2. Struttura (🟡 importante)

| Controllo | Cosa cercare |
| --- | --- |
| Capitoli | uno per PDF di lezione, tutti inclusi in `main.tex`, in ordine |
| Dimensioni | 3-6 sezioni per capitolo, 1-4 sottosezioni ciascuna; più di ~12 sottosezioni, o una per slide, vuol dire poca sintesi |
| Ridondanza | lo stesso concetto spiegato per intero in due capitoli: tienine uno e cita quello dall'altro |
| Riferimenti incrociati | `Capitolo~\ref{ch:...}` (o `Chapter~\ref` in un corso inglese) a label esistenti, niente numeri scritti a mano |
| Segnaposto | `INSERISCI IMMAGINE DALLA SLIDE N` o `INSERT IMAGE FROM SLIDE N` rimasti: elencali con i numeri di slide (`latex-tutor` può ritagliarli) |
| Float | figure `[H]` che lasciano grandi spazi bianchi |
| Didascalie | ogni figura e tabella ha `\caption` e `\label`; sopra le tabelle, sotto le figure |

### 3. Stile (🟡 importante, regole di `latex-tutor`)

| Regola | Controllo |
| --- | --- |
| Ritmo | più di ~15 righe di prosa senza elenco, tabella, definizione, esempio o figura |
| Elenchi | 3+ elementi distinti sepolti nella prosa |
| Confronti | A contro B non in una tabella `booktabs`, elenchi numerati dentro le celle |
| Contenuto formale | definizioni, teoremi ed esempi fuori dagli ambienti `amsthm` |
| Parole chiave | termini principali senza `\textbf` alla prima occorrenza |
| TikZ | diagrammi semplici (≤ 7 nodi) lasciati come immagini o segnaposto |
| Prosa | riempitivi ("È importante notare che..."), frasi oltre ~40 parole |
| Lingua | testo LaTeX non nella lingua del corso (quella del `babel` del preambolo), o due lingue nello stesso corso |

### 4. Matematica (🟡 importante)

| Controllo | Cosa cercare |
| --- | --- |
| Sistemi | `cases` invece di `dcases` |
| Vettori | `\vec{v}` invece di `\bm{v}` (e la scelta usata nel resto del capitolo) |
| Derivate | `\frac{df}{dx}` invece di `\dv{f}{x}`, `\pdv{f}{x}` |
| Norme, valori assoluti | `\norm{}`, `\abs{}` di `physics` |

### 5. Formattazione (🔵 minore)

| Controllo | Cosa cercare |
| --- | --- |
| Tabelle | righe di `booktabs`, niente linee verticali |
| `\noindent` | prima di `\begin{table}` e sulla prosa dopo tabelle, figure ed elenchi |
| Enfasi | niente `\uline`; `\textit` solo per termini secondari o stranieri |
| Label | prefissi `ch:`, `sec:<slug>-`, `def:`, `thm:`, `ex:`, `fig:`, `tab:`, `eq:`, `alg:` |
| TikZ | `\tikzstyle` (deprecato) |
| Fine capitolo | `\cleardoublepage` alla fine di ogni capitolo, come negli altri |
| Immagini | file non usati in `images/` |

---

## Formato del resoconto

```markdown
## Revisione LaTeX: [corso]

Compilazione: OK / N errori · check_project.py: critici X, importanti Y, minori Z

### 🔴 Critici (il PDF non si genera o i riferimenti sono rotti)
| # | File:riga | Problema | Correzione |
| --- | --- | --- | --- |
| 1 | chapters/2-Data.tex:145 | tag `[cite]` | toglierlo |

### 🟡 Importanti (struttura e stile)
| # | File:riga | Problema | Correzione |
| --- | --- | --- | --- |
| 1 | chapters/3-Preprocessing.tex:200-280 | 80 righe di prosa | trasformare l'elenco delle feature in itemize |

### 🔵 Minori
| # | File:riga | Problema | Correzione |
| --- | --- | --- | --- |
| 1 | chapters/1-Introduction.tex:34 | `\frac{df}{dx}` | `\dv{f}{x}` |

Esito: [PRONTO / DA CORREGGERE / NON COMPILA]
```

---

## Modalità correzione

Quando l'utente chiede di correggere:

1. Prima i critici: bloccano il PDF. Poi gli importanti, un capitolo alla volta. I minori per ultimi.
2. Cambia solo quello che serve al problema. Ristrutturare la prosa, unire sezioni o spostare contenuti tra capitoli: mostra la proposta e aspetta l'approvazione, perché l'utente modifica i capitoli a mano.
3. Dopo le correzioni, rilancia `check_project.py` e la compilazione e riporta cosa resta.
