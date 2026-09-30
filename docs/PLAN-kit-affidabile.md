# Consolidamento del kit

Stato: implementazione e verifica tecnica completate il 29 settembre 2026; valutazioni comparative dei modelli rinviate come richiesto.

## Obiettivo e vincoli

Proteggere le installazioni, rendere veritieri i controlli e semplificare le regole. Tutte le skill restano disponibili; `scroll-world` resta invariata. LaTeX è il caso d'uso principale, ML il secondo. I profili separati e le valutazioni comparative degli agenti restano rinviati alla versione definitiva.

## Interventi

1. Installer: manifest per file con hash e origine, anteprima, conflitti espliciti, backup/ripristino, rollback e aggiornamenti senza ripiego alla copia locale.
2. Controlli: stati distinti, npm su Windows, suite adatta ai file presenti, test di regressione e CI Windows/Linux.
3. Regole: tutti gli agenti possono usare gli script pertinenti; nessuna quota di agenti; domande solo quando necessarie e autorizzazioni già date rispettate.
4. Antigravity: verifica plugin e nomi dei comandi; documentazione della compatibilità senza migrare le installazioni dell'utente automaticamente.

## Criteri di successo

- File personali e modifiche locali non vengono cancellati implicitamente.
- Un download fallito lascia invariata l'installazione e restituisce un errore.
- Ripristino verificato e nessuna scrittura fuori dalla destinazione.
- Progetto vuoto, test assenti e controlli non applicabili non risultano superati.
- Test Node eseguiti anche su Windows; gli errori dei figli restano visibili.
- Nessuna modifica al contenuto di `scroll-world`.
- Validatore, test e lint passano; limiti delle prove native documentati.

## Verifica

Test con `unittest` in cartelle temporanee, validatore esistente, lint Markdown, controllo sintattico Node e validazione del formato plugin con la CLI disponibile. Le prove del comportamento dei modelli richiedono la versione finale e sono rinviate.

## Esito

- 30 test di regressione passati su Windows, anche tramite la checklist del kit.
- Checklist: un controllo eseguito con successo (suite test), tre non applicabili.
- Validatore: 12 agenti, 32 skill, zero errori e zero avvisi.
- Lint Markdown senza problemi; sintassi Python e Node verificata.
- Contenuto del pacchetto npm verificato senza cache Python o output LaTeX locali.
- CLI `agy 1.2.12`: formato plugin accettato in directory temporanea; attivazione ed esecuzione non provate. Dettagli in `ANTIGRAVITY-COMPATIBILITY.md`.
- CI estesa a Windows/Linux; esecuzione remota Linux non avviata in questa sessione.
- `scroll-world` invariata. Profili separati e comando doctor restano proposte, non sono necessari per utilizzare tutti gli strumenti del kit.
