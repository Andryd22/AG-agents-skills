# Changelog

## Non rilasciato

- Manifest per file con hash, conflitti, anteprima, backup/ripristino e rollback.
- Gli aggiornamenti falliti non reinstallano la copia locale; le cartelle legacy
  senza hash non vengono eliminate o spostate automaticamente.
- Controlli con stati distinti e report JSON; uscita 2 per verifiche incomplete.
- Esecuzione npm/npx risolta su Windows; CI e regressioni su Windows/Linux.
- Il pacchetto esclude cache Python e output locali di compilazione LaTeX.
- Verifica strutturale LaTeX riconosciuta in radice e nella sottocartella `latex/`.
- Tutti gli agenti possono usare le skill e gli script pertinenti, senza quote
  minime di agenti né richieste ripetute di autorizzazione.
- `/kit-plan` sostituisce il comando omonimo del `/plan` nativo di Antigravity.
- Compatibilità plugin investigata e documentata; nessuna migrazione automatica.
- `scroll-world` invariata; valutazioni comparative degli agenti rinviate.
