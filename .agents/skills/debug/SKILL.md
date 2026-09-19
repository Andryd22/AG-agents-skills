---
name: debug
description: 'Indagine sistematica sui bug: raccogli le prove, ordina le ipotesi, verificale una alla volta, correggi la causa radice e impedisci che si ripresenti. Usala quando l''utente lancia /debug o segnala un errore, un crash o un comportamento inatteso.'
---

# /debug - Indagine sistematica su un problema

La richiesta è il testo che segue `/debug`.

---

## Scopo

Questo comando attiva la modalità DEBUG per indagare in modo sistematico su problemi, errori o comportamenti inattesi.

---

## Comportamento

Quando parte `/debug`:

1. **Raccogli le informazioni**
   - Messaggio di errore
   - Passi per riprodurlo
   - Comportamento atteso e comportamento reale
   - Modifiche recenti

2. **Formula le ipotesi**
   - Elenca le cause possibili
   - Ordinale per probabilità

3. **Indaga con metodo**
   - Verifica ogni ipotesi
   - Controlla i log e il flusso dei dati
   - Procedi per eliminazione

4. **Correggi e previeni**
   - Applica la correzione
   - Spiega la causa radice
   - Aggiungi misure che impediscano di ricaderci

---

## Formato dell'output

````markdown
## 🔍 Debug: [problema]

### 1. Sintomo
[cosa succede]

### 2. Informazioni raccolte
- Errore: `[messaggio di errore]`
- File: `[percorso]`
- Riga: [numero di riga]

### 3. Ipotesi
1. ❓ [causa più probabile]
2. ❓ [seconda possibilità]
3. ❓ [causa meno probabile]

### 4. Indagine

**Verifica dell'ipotesi 1:**
[cosa ho controllato] → [risultato]

**Verifica dell'ipotesi 2:**
[cosa ho controllato] → [risultato]

### 5. Causa radice
🎯 **[spiegazione del perché è successo]**

### 6. Correzione
```[linguaggio]
// Prima
[codice rotto]

// Dopo
[codice corretto]
```

### 7. Prevenzione
🛡️ [come evitare che succeda di nuovo]
````

---

## Esempi

```text
/debug il login non funziona
/debug l'API restituisce 500
/debug il form non si invia
/debug i dati non vengono salvati
```

---

## Principi chiave

- **Chiedi prima di supporre** - fatti dare il contesto completo dell'errore
- **Verifica le ipotesi** - non tirare a indovinare
- **Spiega il perché** - non solo cosa correggere
- **Evita le ricadute** - aggiungi test e validazioni
