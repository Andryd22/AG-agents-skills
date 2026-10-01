# Changelog

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
