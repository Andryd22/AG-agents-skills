# Changelog

## 5.10.0 (19/11/2026)

- LaTeX: tutti i paragrafi con `parskip`, cioè senza rientro e separati da uno spazio verticale. Il preambolo dei corsi nuovi carica `\usepackage{parskip}`; `latex-tutor`, `latex-specialist` e `latex-review` tolgono la regola del `\noindent` dopo figure, tabelle ed elenchi, che con `parskip` non serve più.

## 5.9.0 (15/11/2026)

- LaTeX: niente virgola prima dell'ultima voce di un elenco nella prosa ("A, B e C", in inglese "A, B and C") e, in italiano, nemmeno prima di "e" o "o" che uniscono due frasi; la virgola resta solo quando chiude un inciso. La regola è in `latex-tutor` (Stile di scrittura), nella checklist di `latex-specialist` e fra i controlli di punteggiatura di `latex-review`.

## 5.8.0 (14/11/2026)

- LaTeX: figure mirate invece di tante. Entrano le figure delle slide che mostrano come funziona qualcosa e, se serve, un diagramma TikZ per un meccanismo spiegato solo a parole; restano fuori le illustrazioni di definizioni già chiare, i grafici di risultati sperimentali riassunti in una frase e le tabelle di esempi numerici. Tolti il "nel dubbio aggiungi" e il "mettine tante" della 5.5.0, che in un capitolo di prova hanno portato figure inutili (`latex-tutor`, `latex`, `latex-specialist`, `latex-review`).
- `/latex figure` prima propone le figure candidate, con una riga di motivo ciascuna, e aggiunge solo quelle che l'utente sceglie; i segnaposto li sostituisce sempre.

## 5.7.0 (13/11/2026)

- LaTeX: lo pseudocodice si scrive sempre in `\begin{algorithm}[H]` di `algorithm2e`, mai in un riquadro `\fbox` con un `enumerate`. `latex-tutor` ha le regole e un esempio (`\KwData` e `\KwResult`, `\Repeat`, `\ForEach`, `\eIf`, commenti a lato con `\tcp*`), che `latex-specialist` e `latex-review` riprendono.
- `check_project.py` segnala i riquadri `\fbox` o `\framebox` con dentro un elenco numerato: di solito sono pseudocodice scritto a mano.
- Il preambolo dei corsi nuovi numera gli algoritmi per capitolo, come figure e teoremi (`algochapter`: Algoritmo 3.1, numeri giusti anche con `\includeonly`), e li stacca dal testo con `\SetAlgoSkip{bigskip}`.

## 5.6.0 (13/11/2026)

- Nuova modalità `/latex figure <capitolo>`: aggiunge figure a un capitolo già scritto senza toccare la prosa, cioè le figure utili delle slide che mancano, i segnaposto sostituiti con i ritagli e i diagrammi TikZ per quello che il capitolo spiega solo a parole (`latex`, `latex-tutor`, `latex-specialist`).
- `slides.py render <radice>/main.pdf --labels fig:a,fig:b` salva le pagine del PDF compilato in cui stanno quelle label (le trova dai file `.aux` e dalle destinazioni di hyperref). Dopo la compilazione l'agente guarda così ogni figura TikZ nuova e corregge scritte sovrapposte, frecce sopra il testo e parti fuori dai margini.
- `GEMINI.md`: nuova regola "Schemi nelle spiegazioni". Quando l'agente spiega in chat un processo, un'architettura o un flusso di dati, aggiunge uno schema in un blocco `text`.

## 5.5.0 (13/11/2026)

- LaTeX: le figure diventano una priorità, perché aiutano l'utente a capire i concetti. Ogni figura utile delle slide entra nel capitolo e quello che le slide spiegano solo a parole (processi, architetture, strutture, idee geometriche, andamenti di funzioni) riceve un diagramma TikZ; nel dubbio la figura si aggiunge e l'utente toglie a mano quelle che non gli servono. Le figure aggiunte non si citano nel testo, così si tolgono cancellando solo il loro ambiente, e il resoconto le elenca con la label (`latex-tutor`, `latex`, `latex-specialist`, `latex-review`).
- `latex-tutor` ha un esempio di diagramma TikZ e le regole per disegnarli; per i corsi esistenti l'agente propone le righe da aggiungere al preambolo (`pgfplots`, `petri`, `automata`, `quantikz`). Il preambolo dei corsi nuovi carica `pgfplots` e la libreria TikZ `backgrounds`.
- `check_project.py` segnala anche i numeri di figura e di tabella scritti a mano (`Figura 3.2` invece di `Figura~\ref{...}`): diventano sbagliati quando si toglie una figura.
- Comandi delle skill LaTeX validi anche in PowerShell: niente variabili Bash negli esempi di `slides.py`, e la mappa di titoli e label si fa con `grep_search` o `Select-String`.

## 5.4.1 (08/10/2026)

- LaTeX: tolto il tetto implicito di 3-6 sezioni per capitolo (`latex-tutor`, `latex-specialist`, `latex-review`). Se il capitolo è lungo e si legge meglio spezzettato, 8, 10 o 12 sezioni vanno bene.

## 5.4.0 (01/10/2026)

- L'installer non crea più `.agents.backups/` a ogni aggiornamento: salva i file sostituiti solo con la nuova opzione `--backup`, oppure quando `--force` sostituisce file cambiati a mano. Il rollback dopo un errore di scrittura resta, con gli originali in memoria.

## 5.3.0 (01/10/2026)

- `GEMINI.md`: nuova regola "Formule matematiche nelle spiegazioni", nata nel corso di Quantum. Nelle risposte all'utente niente LaTeX grezzo: le formule vanno in blocchi `text`, con notazione Unicode o ASCII.

## 5.2.0 (01/10/2026)

- Nuova convenzione LaTeX: una formula nel titolo di un capitolo o di una sezione va dentro `\texorpdfstring{<formula>}{<testo>}`, così `hyperref` scrive i segnalibri del PDF senza avvisi (`latex-tutor`, `latex-review`, `latex-specialist`).
- `check_project.py` segnala (IMPORTANTE) le formule nei titoli fuori da `\texorpdfstring`; i titoli con asterisco non vanno nei segnalibri e non vengono controllati, e se c'è un titolo breve tra `[]` controlla quello.

## 5.1.0 (30/09/2026)

- Corsi con più documenti LaTeX indipendenti in `latex/<nome>/` (per esempio uno per docente, con i PDF in `Teoria/<nome>/`): `/latex` sceglie il documento dal nome dato dall'utente o dalla sottocartella di `Teoria/` del PDF, altrimenti chiede; la revisione li controlla tutti o quello nominato; `/latex setup` non li scambia più per un corso da preparare e con `/latex setup <nome>` aggiunge un documento.
- `check_project.py` lanciato sulla cartella del corso controlla ogni `latex/<nome>/main.tex`, uno dopo l'altro. Con `main.tex` sia in `latex/` sia nella cartella, sceglie `latex/`, come le skill e `checklist.py`.
- Un PDF che raccoglie più capitoli (tutte le slide di un docente) si divide per parti e intervalli di slide indicati dall'utente.

## 5.0.2 (30/09/2026)

- `check_project.py` riconosce le label date nelle opzioni dei listati (`\begin{lstlisting}[label={lst:...}]`, `\lstinputlisting[label=...]`): prima i riferimenti a quelle label risultavano non definiti (CRITICO) anche se la compilazione li risolve.

## 5.0.1 (30/09/2026)

- `checklist.py` e `verify_all.py` trovano anche i progetti LaTeX in `latex/<nome>/main.tex` (per esempio un progetto per docente) e li controllano tutti: prima il controllo LaTeX risultava non applicabile e la verifica incompleta.

## 5.0.0 (30/09/2026)

### Incompatibili

- La skill `plan` diventa `kit-plan` (`/kit-plan`), così non si scontra con il `/plan` nativo di Antigravity.
- L'installer usa un manifest con l'hash di ogni file. Da un'installazione precedente, senza hash, `update` si ferma sui file cambiati: confrontali e rilancia con `--force`. La vecchia `skills/plan/` resta e l'installer la elenca, da togliere a mano.

### Installer

- Anteprima (`--dry-run`), conflitti espliciti, backup in `.agents.backups/`, `restore` e rollback.
- Un aggiornamento fallito non reinstalla la copia locale; le cartelle legacy senza hash e la vecchia `.agent/` non vengono eliminate né spostate.
- `update` non installa più `.agents/.npmignore`, come già `init`.
- Il pacchetto esclude cache Python e output locali di compilazione LaTeX.

### Controlli

- Stati distinti (`passed`, `failed`, `skipped`, `not_applicable`) e report JSON; uscita 2 per verifiche incomplete.
- Controllo strutturale LaTeX quando c'è `main.tex` in radice o in `latex/`.
- npm e npx eseguiti correttamente su Windows; CI e test di regressione su Windows e Linux.

### Agenti e regole

- Tutti gli agenti possono usare le skill e gli script pertinenti, senza un numero minimo di agenti né richieste ripetute di autorizzazione.
- Compatibilità con i plugin di Antigravity verificata sul formato e documentata in `docs/ANTIGRAVITY-COMPATIBILITY.md`; nessuna migrazione automatica.
- `scroll-world` invariata; le valutazioni comparative degli agenti sono rinviate.
