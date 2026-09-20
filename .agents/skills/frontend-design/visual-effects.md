# Riferimento effetti visivi

> Principi e tecniche degli effetti CSS moderni: impara i concetti, crea le tue varianti.
> **Nessun valore fisso da copiare: capisci i pattern.**

---

## 1. Principi del glassmorphism

### Cosa fa funzionare il glassmorphism

```text
Proprietà chiave:
├── Sfondo semitrasparente (non pieno)
├── Blur dello sfondo (effetto vetro smerigliato)
├── Bordo sottile (per definire i contorni)
└── Spesso: ombra leggera per dare profondità
```

### Il pattern (personalizza i valori)

```css
.glass {
  /* Trasparenza: regola l'opacità in base alla leggibilità del contenuto */
  background: rgba(R, G, B, OPACITY);
  /* OPACITY: 0.1-0.3 su sfondo scuro, 0.5-0.8 su sfondo chiaro */
  
  /* Blur: più alto = più smerigliato */
  backdrop-filter: blur(AMOUNT);
  /* AMOUNT: 8-12px leggero, 16-24px marcato */
  
  /* Bordo: definisce i contorni */
  border: 1px solid rgba(255, 255, 255, OPACITY);
  /* OPACITY: di solito 0.1-0.3 */
  
  /* Raggio: allinealo al tuo design system */
  border-radius: YOUR_RADIUS;
}
```

### Quando usare il glassmorphism

- ✅ Sopra sfondi colorati o immagini
- ✅ Modali, overlay, card
- ✅ Barre di navigazione con contenuto che scorre sotto
- ❌ Contenuti con molto testo (problemi di leggibilità)
- ❌ Sfondi semplici a tinta unita (non serve a niente)

### Quando NON usarlo

- Situazioni a basso contrasto
- Contenuti in cui l'accessibilità è critica
- Dispositivi con prestazioni limitate

---

## 2. Principi del neumorphism

### Cosa fa funzionare il neumorphism

```text
Concetto chiave: elementi morbidi, in rilievo, con DUE ombre
├── Ombra chiara (dal lato della fonte di luce)
├── Ombra scura (lato opposto)
└── Sfondo uguale a ciò che lo circonda (stesso colore)
```

### Il pattern

```css
.neo-raised {
  /* Lo sfondo DEVE essere uguale a quello del genitore */
  background: SAME_AS_PARENT;
  
  /* Due ombre: scura dal lato opposto alla luce + chiara dal lato della luce */
  box-shadow: 
    OFFSET OFFSET BLUR rgba(dark-color),
    -OFFSET -OFFSET BLUR rgba(light-color);
  
  /* OFFSET: di solito 6-12px */
  /* BLUR: di solito 12-20px */
}

.neo-pressed {
  /* inset crea l'effetto "premuto" */
  box-shadow: 
    inset OFFSET OFFSET BLUR rgba(dark-color),
    inset -OFFSET -OFFSET BLUR rgba(light-color);
}
```

### Avviso di accessibilità

⚠️ **Basso contrasto**: usalo con parsimonia e assicurati che i contorni si distinguano bene

### Quando usarlo

- Elementi decorativi
- Stati interattivi discreti
- UI minimaliste con colori piatti

---

## 3. Principi della gerarchia delle ombre

### Concetto: le ombre indicano l'elevazione

```text
Più elevazione = ombra più grande
├── Livello 0: nessuna ombra (appoggiato sulla superficie)
├── Livello 1: ombra leggera (appena sollevato)
├── Livello 2: ombra media (card, pulsanti)
├── Livello 3: ombra grande (modali, dropdown)
└── Livello 4: ombra profonda (elementi fluttuanti)
```

### Proprietà dell'ombra da regolare

```css
box-shadow: OFFSET-X OFFSET-Y BLUR SPREAD COLOR;

/* Offset: direzione dell'ombra */
/* Blur: morbidezza (più grande = più morbida) */
/* Spread: quanto si allarga */
/* Color: di solito nero con opacità bassa */
```

### Principi per ombre naturali

1. **Offset Y maggiore di X** (la luce arriva dall'alto)
2. **Opacità bassa** (5-15% per ombre leggere, 15-25% per ombre marcate)
3. **Più livelli** per il realismo (luce ambientale + luce diretta)
4. **Il blur cresce con l'offset** (offset maggiore = blur maggiore)

### Ombre in dark mode

- Sugli sfondi scuri le ombre si vedono meno
- Può servire aumentare l'opacità
- Oppure usa un glow o un'evidenziazione al posto dell'ombra

---

## 4. Principi dei gradienti

### Tipi e quando usarli

| Tipo | Pattern | Caso d'uso |
| --- | --- | --- |
| **Lineare** | Colore A → colore B lungo una linea | Sfondi, pulsanti, header |
| **Radiale** | Dal centro verso l'esterno | Spotlight, punti focali |
| **Conico** | Attorno al centro | Grafici a torta, effetti creativi |

### Creare gradienti armoniosi

```text
Regole per un buon gradiente:
├── Usa colori VICINI sulla ruota (analoghi)
├── Oppure la stessa tinta con luminosità diverse
├── Evita i complementari (possono risultare stridenti)
└── Aggiungi stop intermedi per transizioni più morbide
```

### Sintassi del gradiente

```css
.gradient {
  background: linear-gradient(
    DIRECTION,           /* angolo o parola chiave to */
    COLOR-STOP-1,        /* colore + posizione facoltativa */
    COLOR-STOP-2,
    /* ... altri stop */
  );
}

/* Esempi di DIRECTION: */
/* 90deg, 135deg, to right, to bottom right */
```

### Mesh gradient

```text
Più gradienti radiali sovrapposti:
├── Ognuno in una posizione diversa
├── Ognuno che sfuma nel trasparente
├── **OBBLIGATORIO per l'effetto "wow" nelle sezioni hero**
└── Crea un effetto organico e colorato (cerca: "Aurora Gradient CSS")
```

---

## 5. Principi degli effetti sui bordi

### Bordi con gradiente

```text
Tecnica: pseudo-elemento con sfondo a gradiente
├── L'elemento ha un padding pari allo spessore del bordo
├── Lo pseudo-elemento si riempie con il gradiente
└── Una mask o un clip crea l'effetto bordo
```

### Bordi animati

```text
Tecnica: gradiente che ruota o sweep conico
├── Pseudo-elemento più grande del contenuto
├── L'animazione fa ruotare il gradiente
└── overflow: hidden ritaglia la forma
```

### Bordi con glow

```css
/* Più box-shadow sovrapposte creano il glow */
box-shadow:
  0 0 SMALL-BLUR COLOR,
  0 0 MEDIUM-BLUR COLOR,
  0 0 LARGE-BLUR COLOR;

/* Ogni livello rafforza il glow */
```

---

## 6. Principi degli effetti glow

### Glow del testo

```css
text-shadow: 
  0 0 BLUR-1 COLOR,
  0 0 BLUR-2 COLOR,
  0 0 BLUR-3 COLOR;

/* Più livelli = glow più intenso */
/* Blur più grande = alone più morbido */
```

### Glow dell'elemento

```css
box-shadow:
  0 0 BLUR-1 COLOR,
  0 0 BLUR-2 COLOR;

/* Usa un colore simile a quello dell'elemento per un glow realistico */
/* Opacità più bassa per un effetto discreto, più alta per il neon */
```

### Animazione di glow pulsante

```css
@keyframes glow-pulse {
  0%, 100% { box-shadow: 0 0 SMALL-BLUR COLOR; }
  50% { box-shadow: 0 0 LARGE-BLUR COLOR; }
}

/* Easing e durata cambiano la sensazione */
```

---

## 7. Tecniche di overlay

### Overlay con gradiente sulle immagini

```text
Scopo: rendere più leggibile il testo sopra le immagini
Pattern: gradiente da trasparente a opaco
Posizione: dove comparirà il testo
```

```css
.overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    DIRECTION,
    transparent PERCENTAGE,
    rgba(0,0,0,OPACITY) 100%
  );
}
```

### Overlay colorato

```css
/* Blend mode o gradiente sovrapposto */
background: 
  linear-gradient(YOUR-COLOR-WITH-OPACITY),
  url('image.jpg');
```

---

## 8. Tecniche CSS moderne

### Container query (concetto)

```text
Invece dei breakpoint sul viewport:
├── Il componente risponde al SUO contenitore
├── Componenti davvero modulari e riutilizzabili
└── Sintassi: @container (condition) { }
```

### Selettore :has() (concetto)

```text
Stile del genitore in base ai figli:
├── "Genitore che contiene un figlio X"
├── Rende possibili pattern prima impossibili
└── Da usare come progressive enhancement
```

### Animazioni guidate dallo scroll (concetto)

```text
Avanzamento dell'animazione legato allo scroll:
├── Animazioni di entrata/uscita durante lo scroll
├── Effetti parallax
├── Indicatori di avanzamento
└── Timeline basata sulla visibilità (view) o sullo scroll
```

---

## 9. Principi di prestazioni

### Proprietà accelerate dalla GPU

```text
ECONOMICHE da animare (GPU):
├── transform (translate, scale, rotate)
└── opacity

COSTOSE da animare (CPU):
├── width, height
├── top, left, right, bottom
├── margin, padding
└── box-shadow (viene ricalcolata)
```

### Uso di will-change

```css
/* Usalo con parsimonia, solo per animazioni pesanti */
.heavy-animation {
  will-change: transform;
}

/* Se puoi, rimuovilo alla fine dell'animazione */
```

### Movimento ridotto

```css
@media (prefers-reduced-motion: reduce) {
  /* Disattiva le animazioni o riducile al minimo */
  /* Rispetta la preferenza dell'utente */
}
```

---

## 10. Checklist per scegliere gli effetti

Prima di applicare un effetto:

- [ ] **Ha uno scopo?** (non è solo decorazione)
- [ ] **È adatto al contesto?** (brand, pubblico)
- [ ] **Ti sei discostato dai progetti precedenti?** (evita le ripetizioni)
- [ ] **È accessibile?** (contrasto, sensibilità al movimento)
- [ ] **È performante?** (soprattutto su mobile)
- [ ] **Hai chiesto la preferenza dell'utente?** (se lo stile è libero)

### Anti-pattern

- ❌ Glassmorphism su ogni elemento (kitsch)
- ❌ Scuro + neon come scelta predefinita (look da AI pigra)
- ❌ **Design statici/piatti senza profondità (BOCCIATO)**
- ❌ Effetti che peggiorano la leggibilità
- ❌ Animazioni senza scopo

---

> **Ricorda**: gli effetti rafforzano il significato. Sceglili in base allo scopo e al contesto, non perché "fanno scena".
