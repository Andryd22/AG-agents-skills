---
name: brainstorm
description: 'Socratic Gate ed esplorazione strutturata delle opzioni: chiedi solo quello che non si può dedurre, poi confronta almeno tre approcci con pro, contro e una raccomandazione. Usala quando l''utente lancia /brainstorm, e prima di costruire quando una richiesta è vaga, complessa o ha scelte di design aperte.'
---

# Brainstorming e protocollo di comunicazione

> **OBBLIGATORIA:** per richieste complesse o vaghe, nuove funzionalità, modifiche.

---

## 🛑 SOCRATIC GATE (APPLICAZIONE)

### Quando scatta

| Situazione | Azione |
| --- | --- |
| "Costruisci/crea/fai [cosa]" senza dettagli | 🛑 CHIEDI al massimo 3 domande |
| Funzionalità o architettura complessa | 🛑 Chiarisci prima di implementare |
| Richiesta di modifica | 🛑 Conferma il perimetro |
| Requisiti vaghi | 🛑 Chiedi scopo, utenti, vincoli |

### 🚫 OBBLIGATORIO: chiarire prima di implementare

1. **FERMATI** - NON iniziare a scrivere codice
2. **CHIEDI** - Al massimo 3 domande, solo su ciò a cui la richiesta non risponde già:
   - 🎯 Scopo: quale problema stai risolvendo?
   - 👥 Utenti: chi lo userà?
   - 📦 Perimetro: indispensabile o facoltativo?
3. **ASPETTA** - Ottieni la risposta prima di procedere

---

## 🧠 Domande costruite sul caso

**⛔ MAI usare modelli fissi.** I principi sono in `references/dynamic-questioning.md`.

### Principi

| Principio | Significato |
| --- | --- |
| **Le domande rivelano conseguenze** | Ogni domanda è legata a una decisione di architettura |
| **Prima il contesto** | Capisci prima se è un progetto nuovo, una funzionalità, un refactoring o un debug |
| **Il minimo di domande** | Ogni domanda deve eliminare strade di implementazione |
| **Dati, non supposizioni** | Non tirare a indovinare: chiedi mostrando i compromessi |

### Come nascono le domande

```text
1. Analizza la richiesta → dominio, funzionalità, indizi sulla scala
2. Trova i punti di decisione → bloccanti o rimandabili
3. Genera le domande → priorità: P0 (bloccante) > P1 (grande effetto) > P2 (facoltativa)
4. Formattale con i compromessi → cosa, perché, opzioni, predefinito
```

### Formato delle domande (OBBLIGATORIO)

```markdown
### [PRIORITÀ] **[PUNTO DI DECISIONE]**

**Domanda:** [domanda chiara]

**Perché conta:**
- [conseguenza sull'architettura]
- [incide su: costo/complessità/tempi/scala]

**Opzioni:**
| Opzione | Pro | Contro | Ideale per |
|---------|-----|--------|------------|
| A | [+] | [-] | [caso d'uso] |

**Se non specificato:** [predefinito + motivo]
```

**Banche di domande per dominio e algoritmi dettagliati**: vedi `references/dynamic-questioning.md`

---

## Aggiornamenti di avanzamento (PER PRINCIPI)

**PRINCIPIO:** la trasparenza crea fiducia. Lo stato deve essere visibile e utile.

### Tabella di stato

| Agente | Stato | Compito attuale | Avanzamento |
| --- | --- | --- | --- |
| [Nome agente] | ✅🔄⏳❌⚠️ | [descrizione del compito] | [% o conteggio] |

### Icone di stato

| Icona | Significato | Uso |
| --- | --- | --- |
| ✅ | Completato | Compito finito con successo |
| 🔄 | In corso | In esecuzione adesso |
| ⏳ | In attesa | Bloccato, aspetta una dipendenza |
| ❌ | Errore | Fallito, serve attenzione |
| ⚠️ | Avviso | Possibile problema, non bloccante |

---

## Gestione degli errori (PER PRINCIPI)

**PRINCIPIO:** un errore è un'occasione per comunicare con chiarezza.

### Come rispondere a un errore

```text
1. Riconosci l'errore
2. Spiega cosa è successo (in modo comprensibile)
3. Proponi soluzioni precise con i loro compromessi
4. Chiedi all'utente di scegliere o di proporre un'alternativa
```

### Categorie di errori

| Categoria | Strategia |
| --- | --- |
| **Porta occupata** | Proponi un'altra porta o di chiudere il processo che la usa |
| **Dipendenza mancante** | Installala o chiedi il permesso |
| **Build fallita** | Mostra l'errore preciso + la correzione proposta |
| **Errore poco chiaro** | Chiedi dettagli: screenshot, output della console |

---

## Messaggio di chiusura (PER PRINCIPI)

**PRINCIPIO:** conferma il risultato, indica i passi successivi.

### Struttura

```text
1. Conferma del risultato (breve)
2. Riassunto di cosa è stato fatto (concreto)
3. Come verificarlo o provarlo (pratico)
4. Prossimo passo suggerito (proattivo)
```

---

## Principi di comunicazione

| Principio | Come |
| --- | --- |
| **Conciso** | Niente dettagli inutili, vai al punto |
| **Visivo** | Emoji (✅🔄⏳❌) per leggere al volo |
| **Preciso** | "~2 minuti", non "aspetta un po'" |
| **Alternative** | Offri più strade quando sei bloccato |
| **Proattivo** | Suggerisci il passo successivo dopo aver finito |

---

## Anti-pattern (DA EVITARE)

| Anti-pattern | Perché |
| --- | --- |
| Saltare alla soluzione prima di capire | Si perde tempo sul problema sbagliato |
| Dare per scontati i requisiti senza chiedere | Il risultato è sbagliato |
| Sovraingegnerizzare la prima versione | Ritarda il valore |
| Ignorare i vincoli | Soluzioni inutilizzabili |
| Frasi del tipo "Credo che" | Incertezza → meglio chiedere |

---

## /brainstorm - Esplorazione strutturata delle idee

La richiesta è il testo che segue `/brainstorm`.

---

### Scopo

Questo comando attiva la modalità BRAINSTORM per esplorare le idee in modo strutturato. Usalo quando servono opzioni prima di impegnarsi in un'implementazione.

---

### Comportamento

Quando parte `/brainstorm`:

1. **Capisci l'obiettivo**
   - Quale problema stiamo risolvendo?
   - Chi è l'utente?
   - Quali vincoli ci sono?

2. **Genera le opzioni**
   - Almeno 3 approcci diversi
   - Ognuno con pro e contro
   - Considera anche soluzioni non convenzionali

3. **Confronta e raccomanda**
   - Riassumi i compromessi
   - Dai una raccomandazione motivata

---

### Formato dell'output

```markdown
## 🧠 Brainstorm: [argomento]

### Contesto
[breve descrizione del problema]

---

### Opzione A: [nome]
[descrizione]

✅ **Pro:**
- [vantaggio 1]
- [vantaggio 2]

❌ **Contro:**
- [svantaggio 1]

📊 **Impegno:** basso | medio | alto

---

### Opzione B: [nome]
[descrizione]

✅ **Pro:**
- [vantaggio 1]

❌ **Contro:**
- [svantaggio 1]
- [svantaggio 2]

📊 **Impegno:** basso | medio | alto

---

### Opzione C: [nome]
[descrizione]

✅ **Pro:**
- [vantaggio 1]

❌ **Contro:**
- [svantaggio 1]

📊 **Impegno:** basso | medio | alto

---

## 💡 Raccomandazione

**Opzione [X]** perché [motivo].

In quale direzione vuoi andare?
```

---

### Esempi

```text
/brainstorm sistema di autenticazione
/brainstorm gestione dello stato per un form complesso
/brainstorm schema del database per un social
/brainstorm strategia di caching
```

---

### Principi chiave

- **Niente codice** - si parla di idee, non di implementazione
- **Visivo quando aiuta** - diagrammi per l'architettura
- **Compromessi onesti** - non nascondere la complessità
- **Decide l'utente** - presenta le opzioni, lascia scegliere a lui
