# Changelog

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
