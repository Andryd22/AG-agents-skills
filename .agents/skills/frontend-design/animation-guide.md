# Riferimento linee guida per le animazioni

> Principi di animazione e psicologia dei tempi: impara a decidere, non a copiare.
> **Nessuna durata fissa da memorizzare: capisci cosa influisce sui tempi.**

---

## 1. Principi di durata

### Cosa influisce sui tempi

```text
Fattori che determinano la velocità dell'animazione:
├── DISTANZA: percorso più lungo = durata maggiore
├── DIMENSIONE: elementi più grandi = animazioni più lente
├── COMPLESSITÀ: più è complessa, più tempo serve per coglierla
├── IMPORTANZA: azioni critiche = feedback chiaro
└── CONTESTO: urgente = veloce, lussuoso = lento
```

### Durate per scopo

| Scopo | Intervallo | Perché |
| --- | --- | --- |
| Feedback istantaneo | 50-100ms | Sotto la soglia di percezione |
| Micro-interazioni | 100-200ms | Rapide ma percepibili |
| Transizioni standard | 200-300ms | Ritmo comodo |
| Animazioni complesse | 300-500ms | Danno il tempo di seguirle |
| Transizioni di pagina | 400-600ms | Passaggio fluido |
| **Effetti wow/premium** | 800ms+ | Drammatici, organici (basati su spring), a più livelli |

### Scegliere la durata

Chiediti:

1. Di quanto si sposta l'elemento?
2. Quanto è importante che il cambiamento venga notato?
3. L'utente sta aspettando o è un'animazione di sfondo?

---

## 2. Principi di easing

### Cosa fa l'easing

```text
Easing = come cambia la velocità nel tempo
├── Linear: velocità costante (meccanico, robotico)
├── Ease-out: parte veloce, finisce lento (entrata naturale)
├── Ease-in: parte lento, finisce veloce (uscita naturale)
└── Ease-in-out: lento alle due estremità (fluido, intenzionale)
```

### Quando usare ciascuno

| Easing | Ideale per | Sensazione |
| --- | --- | --- |
| **Ease-out** | Elementi in entrata | Arriva e si assesta |
| **Ease-in** | Elementi in uscita | Parte, se ne va |
| **Ease-in-out** | Enfasi, loop | Intenzionale, fluido |
| **Linear** | Movimento continuo | Meccanico, costante |
| **Bounce/Elastic** | UI giocose | Divertente, energico |

### Il pattern

```css
/* Entra nella vista = ease-out (decelera) */
.enter {
  animation-timing-function: ease-out;
}

/* Esce dalla vista = ease-in (accelera) */
.exit {
  animation-timing-function: ease-in;
}

/* Continuo = ease-in-out */
.continuous {
  animation-timing-function: ease-in-out;
}
```

---

## 3. Principi delle micro-interazioni

### Cosa rende buona una micro-interazione

```text
Scopo delle micro-interazioni:
├── FEEDBACK: conferma che l'azione è avvenuta
├── GUIDA: mostra cosa si può fare
├── STATO: indica lo stato attuale
└── PIACERE: piccoli momenti di gioia
```

### Stati del pulsante

```text
Hover → leggero cambiamento visivo (sollevamento, colore, scala)
Active → sensazione di pressione (scala ridotta, ombra diversa)
Focus → indicatore chiaro (outline, ring)
Loading → indicatore di avanzamento (spinner, skeleton)
Success → conferma (spunta, colore)
```

### Principi

1. **Rispondi subito** (sotto i 100ms la risposta sembra immediata)
2. **Adatta l'effetto all'azione** (pressione = `scale(0.95)`, hover = `translateY(-4px) + glow`)
3. **Osa, ma con fluidità** (deve sembrare curato)
4. **Sii coerente** (stesse azioni = stesso feedback)

---

## 4. Principi degli stati di caricamento

### Tipi in base al contesto

| Situazione | Approccio |
| --- | --- |
| Caricamento rapido (<1s) | Nessun indicatore |
| Medio (1-3s) | Spinner o animazione semplice |
| Lungo (3s+) | Barra di avanzamento o skeleton |
| Durata sconosciuta | Indicatore indeterminato |

### Skeleton screen

```text
Scopo: ridurre l'attesa percepita
├── Mostra subito la forma del layout
├── Anima con discrezione (shimmer, pulse)
├── Sostituisci con il contenuto quando è pronto
└── Sembra più veloce di uno spinner
```

### Indicatori di avanzamento

```text
Quando mostrare l'avanzamento:
├── Azioni avviate dall'utente
├── Upload/download di file
├── Processi in più passaggi
└── Operazioni lunghe

Quando NON serve:
├── Operazioni molto rapide
├── Attività in background
└── Primo caricamento della pagina (meglio lo skeleton)
```

---

## 5. Principi delle transizioni di pagina

### Strategia di transizione

```text
Regola semplice: uscita veloce, entrata più lenta
├── Il contenuto in uscita sfuma rapidamente
├── Il contenuto in entrata si anima
└── Eviti che "si muova tutto insieme"
```

### Pattern comuni

| Pattern | Quando usarlo |
| --- | --- |
| **Fade** | Scelta sicura, funziona ovunque |
| **Slide** | Navigazione sequenziale (precedente/successivo) |
| **Scale** | Apertura/chiusura di modali |
| **Shared element** | Mantenere la continuità visiva |

### Direzione coerente

```text
Direzione di navigazione = direzione dell'animazione
├── Avanti → slide da destra
├── Indietro → slide da sinistra
├── Più in profondità → scale up dal centro
├── Risalita → scale down
```

---

## 6. Principi delle animazioni allo scroll

### Rivelazione progressiva

```text
Il contenuto compare mentre l'utente scorre:
├── Riduce il carico cognitivo iniziale
├── Premia l'esplorazione
├── Non deve sembrare lento
└── Deve poter essere disattivato (accessibilità)
```

### Punti di attivazione

| Quando attivarla | Effetto |
| --- | --- |
| Appena entra nel viewport | Rivelazione standard |
| Al centro del viewport | Per dare enfasi |
| Parzialmente visibile | Rivelazione anticipata |
| Completamente visibile | Attivazione tardiva |

### Proprietà da animare

- Fade in (opacity)
- Slide up (transform)
- Scale (transform)
- Una combinazione delle precedenti

### Prestazioni

- Usa Intersection Observer
- Anima solo transform/opacity
- Se serve, riduci le animazioni su mobile

---

## 7. Principi degli effetti hover

### Effetto adatto all'azione

| Elemento | Effetto | Intento |
| --- | --- | --- |
| **Card cliccabile** | Sollevamento + ombra | "Questo è interattivo" |
| **Pulsante** | Cambio di colore/luminosità | "Premimi" |
| **Immagine** | Zoom/scale | "Guarda da vicino" |
| **Link** | Sottolineatura/colore | "Vai qui" |

### Principi

1. **Segnala l'interattività**: l'hover mostra che l'elemento è cliccabile
2. **Non esagerare**: bastano cambiamenti leggeri
3. **Proporziona all'importanza**: cambiamento più grande = elemento più importante
4. **Prevedi alternative touch**: su mobile l'hover non funziona

---

## 8. Principi delle animazioni di feedback

### Stati di successo

```text
Festeggia nella giusta misura:
├── Azione minore → spunta o colore discreti
├── Azione importante → animazione più marcata
├── Completamento → animazione appagante
└── In linea con la personalità del brand
```

### Stati di errore

```text
Attira l'attenzione senza allarmare:
├── Cambio di colore (rosso semantico)
├── Animazione shake (breve!)
├── Focus sul campo con l'errore
└── Messaggi chiari
```

### Tempi

- Successo: un po' più lungo (goditi il momento)
- Errore: rapido (non rallentare l'azione)
- Caricamento: continuo fino al completamento

---

## 9. Principi di prestazioni

### Cosa costa poco animare

```text
Accelerato dalla GPU (VELOCE):
├── transform: translate, scale, rotate
└── opacity: da 0 a 1

Pesante per la CPU (LENTO):
├── width, height
├── top, left, right, bottom
├── margin, padding
├── modifiche a border-radius
└── modifiche a box-shadow
```

### Strategie di ottimizzazione

1. **Anima transform/opacity** ogni volta che puoi
2. **Evita di innescare il ricalcolo del layout** (cambi di dimensione/posizione)
3. **Usa will-change con parsimonia** (è un suggerimento al browser)
4. **Prova su dispositivi di fascia bassa** (non solo sulla tua macchina di sviluppo)

### Rispettare le preferenze dell'utente

```css
@media (prefers-reduced-motion: reduce) {
  /* Rispetta questa preferenza */
  /* Solo le animazioni essenziali */
  /* Riduci o elimina il movimento decorativo */
}
```

---

## 10. Checklist per decidere le animazioni

Prima di aggiungere un'animazione:

- [ ] **Ha uno scopo?** (feedback/guida/piacere)
- [ ] **I tempi sono adatti?** (né troppo veloce né troppo lenta)
- [ ] **Hai scelto l'easing giusto?** (entrata/uscita/enfasi)
- [ ] **È performante?** (solo transform/opacity)
- [ ] **Hai provato con il movimento ridotto?** (accessibilità)
- [ ] **È coerente con le altre animazioni?** (stessa sensazione di tempi)
- [ ] **Non sono le tue impostazioni predefinite?** (controllo della varietà)
- [ ] **Hai chiesto all'utente che stile vuole, se non era chiaro?**

### Anti-pattern

- ❌ Gli stessi valori di tempo in ogni progetto
- ❌ Animazioni fini a se stesse
- ❌ Ignorare la preferenza `prefers-reduced-motion`
- ❌ Animare proprietà costose
- ❌ Troppe cose animate nello stesso momento
- ❌ Ritardi che frustrano l'utente

---

> **Ricorda**: l'animazione è comunicazione. Ogni movimento deve avere un significato ed essere al servizio dell'esperienza utente.
