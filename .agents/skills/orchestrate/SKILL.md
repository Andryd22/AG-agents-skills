---
name: orchestrate
description: 'Coordina gli specialisti necessari per un compito con sottocompiti separabili: usa il piano già approvato o prepara /kit-plan quando serve, assegna il lavoro e verifica i risultati. Usala quando l''utente lancia /orchestrate o serve coordinare competenze diverse.'
---

# Orchestrazione proporzionata al lavoro

La richiesta è il testo che segue `/orchestrate`.

## Scelta e dimensionamento

1. Ricava risultato atteso, vincoli, decisioni e autorizzazioni dalla conversazione.
2. Individua sottocompiti, dipendenze e file coinvolti.
3. Scegli gli specialisti con `@[skills/intelligent-routing]`.
4. Delega solo quando offre un beneficio concreto. **Non esiste un numero minimo di agenti**: può bastare l'agente corrente con più skill, oppure uno o più specialisti.
5. Esegui in parallelo soltanto attività indipendenti, senza modifiche concorrenti agli stessi file. Esegui in sequenza ciò che dipende da un risultato precedente.

Ogni agente può utilizzare tutte le skill e tutti gli script pertinenti del kit.

## Piano e autorizzazione

- Se esiste un piano approvato in `docs/PLAN-{slug}.md`, continualo senza richiedere l'approvazione delle stesse decisioni.
- Per un lavoro complesso ancora da definire, usa `@[skills/kit-plan]` e presenta le scelte da approvare prima dell'implementazione.
- Per un intervento circoscritto già autorizzato, procedi senza imporre un nuovo piano.
- Chiedi solo informazioni che cambiano concretamente il risultato e che mancano sia nella richiesta sia nei file. Le letture utili restano consentite.
- Se l'utente chiede soltanto analisi o revisione, mantieni quel perimetro.

## Delega

Prima di invocare un subagent scrivi `↪ @<agente>: <compito>`; al ritorno `↩ @<agente>`. Il prompt di ogni delega contiene:

- richiesta dell'utente e risultato verificabile assegnato;
- decisioni e autorizzazioni già date;
- file pertinenti, responsabilità di modifica ed eventuale piano;
- dipendenze e risultati già ottenuti dagli altri agenti;
- verifiche necessarie e forma del risultato da restituire.

Non delegare a un agente che non dispone degli strumenti necessari. Dove la piattaforma non espone subagent, applica direttamente lo specialista e le skill utili.

## Verifica e consegna

L'agente corrente integra i risultati e verifica i criteri del compito. Può eseguire direttamente qualunque controllo pertinente; non serve chiamare un agente aggiuntivo soltanto per raggiungere una quota o lanciare uno script.

```bash
python .agents/scripts/checklist.py .
# Verifica estesa; --url solo quando esiste un'app web da controllare
python .agents/scripts/verify_all.py .
```

Distingui controlli superati, falliti, saltati e non applicabili. LaTeX richiede anche la compilazione; ML richiede controlli della pipeline, dei dati e del protocollo sperimentale. Gli audit statici non sostituiscono queste verifiche.

Consegna un resoconto unico: risultato, verifiche realmente eseguite, eventuali limiti ed elenco degli agenti effettivamente coinvolti. Correggi i problemi nel perimetro approvato; chiedi solo per estensioni del lavoro o decisioni ancora aperte.
