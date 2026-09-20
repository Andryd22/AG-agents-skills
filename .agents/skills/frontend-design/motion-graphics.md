# Riferimento motion graphics

> Tecniche di animazione avanzate per esperienze web premium: Lottie, GSAP, SVG, 3D, particelle.
> **Impara i principi, crea effetti WOW.**

---

## 1. Animazioni Lottie

### Cos'è Lottie?

```text
Animazioni vettoriali basate su JSON:
├── Esportate da After Effects con Bodymovin
├── Leggere (più piccole di GIF/video)
├── Scalabili (vettoriali, niente pixel sgranati)
├── Interattive (controllo della riproduzione, segmenti)
└── Multipiattaforma (web, iOS, Android, React Native)
```

### Quando usare Lottie

| Caso d'uso | Perché Lottie? |
| --- | --- |
| **Animazioni di caricamento** | Brandizzate, fluide, leggere |
| **Stati vuoti** | Illustrazioni coinvolgenti |
| **Flussi di onboarding** | Animazioni complesse in più passaggi |
| **Feedback di successo/errore** | Micro-interazioni piacevoli |
| **Icone animate** | Coerenti su tutte le piattaforme |

### Principi

- Tieni il file sotto i 100KB per le prestazioni
- Usa il loop con parsimonia (evita le distrazioni)
- Prevedi un fallback statico per il reduced-motion
- Se possibile, carica i file di animazione in lazy load

### Fonti

- LottieFiles.com (libreria gratuita)
- After Effects + Bodymovin (animazioni su misura)
- Plugin di Figma (esportazione dal design)

---

## 2. GSAP (GreenSock)

### Cosa rende diverso GSAP

```text
Animazioni professionali basate su timeline:
├── Controllo preciso delle sequenze
├── ScrollTrigger per le animazioni guidate dallo scroll
├── MorphSVG per le transizioni tra forme
├── Easing basato sulla fisica
└── Funziona con qualsiasi elemento del DOM
```

### Concetti chiave

| Concetto | Scopo |
| --- | --- |
| **Tween** | Singola animazione da A a B |
| **Timeline** | Animazioni in sequenza/sovrapposte |
| **ScrollTrigger** | La posizione di scroll controlla la riproduzione |
| **Stagger** | Effetto a cascata su più elementi |

### Quando usare GSAP

- ✅ Animazioni complesse in sequenza
- ✅ Rivelazioni attivate dallo scroll
- ✅ Quando serve un controllo preciso dei tempi
- ✅ Effetti di morphing SVG
- ❌ Semplici effetti di hover/focus (usa il CSS)
- ❌ Mobile con prestazioni critiche (è più pesante)

### Principi

- Usa le timeline per orchestrare (non tween singoli)
- Ritardo di stagger: 0.05-0.15s tra un elemento e l'altro
- ScrollTrigger: fai partire l'animazione quando l'elemento entra al 70-80% del viewport
- Termina le animazioni allo smontaggio (evita memory leak)

---

## 3. Animazioni SVG

### Tipi di animazione SVG

| Tipo | Tecnica | Caso d'uso |
| --- | --- | --- |
| **Disegno di linee** | stroke-dashoffset | Rivelazione di loghi, firme |
| **Morph** | Interpolazione dei path | Transizioni tra icone |
| **Transform** | rotate, scale, translate | Icone interattive |
| **Colore** | Transizione di fill/stroke | Cambi di stato |

### Principi del disegno di linee

```text
Come funziona il disegno con stroke-dashoffset:
├── Imposta dasharray alla lunghezza del path
├── Imposta dashoffset uguale a dasharray (nascosto)
├── Anima dashoffset fino a 0 (visibile)
└── Ottieni l'effetto "disegno"
```

### Quando usare le animazioni SVG

- ✅ Rivelazione di loghi, momenti di brand
- ✅ Transizioni di stato delle icone (hamburger ↔ X)
- ✅ Infografiche, visualizzazione di dati
- ✅ Illustrazioni interattive
- ❌ Contenuti fotorealistici (usa un video)
- ❌ Scene molto complesse (prestazioni)

### Principi

- Ricava la lunghezza del path in modo dinamico, per precisione
- Durata: 1-3s per i disegni completi
- Easing: ease-out per un effetto naturale
- I riempimenti semplici completano, non competono

---

## 4. Trasformazioni 3D in CSS

### Proprietà chiave

```text
Spazio 3D in CSS:
├── perspective: profondità del campo 3D (di solito 500-1500px)
├── transform-style: preserve-3d (attiva il 3D nei figli)
├── rotateX/Y/Z: rotazione per asse
├── translateZ: avvicina/allontana dall'osservatore
└── backface-visibility: mostra/nasconde il retro
```

### Pattern 3D comuni

| Pattern | Caso d'uso |
| --- | --- |
| **Card flip** | Rivelazioni, flashcard, viste prodotto |
| **Tilt all'hover** | Card interattive, profondità 3D |
| **Livelli in parallax** | Sezioni hero, scroll immersivo |
| **Carosello 3D** | Gallerie di immagini, slider |

### Principi

- Perspective: 800-1200px per un effetto sottile, 400-600px per uno drammatico
- Mantieni le trasformazioni semplici (rotate + translate)
- Assicurati di impostare backface-visibility: hidden per i flip
- Prova su Safari (renderizza in modo diverso)

---

## 5. Effetti particellari

### Tipi di sistemi di particelle

| Tipo | Sensazione | Caso d'uso |
| --- | --- | --- |
| **Geometriche** | Tech, rete | SaaS, siti tech |
| **Coriandoli** | Festa | Momenti di successo |
| **Neve/pioggia** | Atmosfera | Stagionali, mood |
| **Polvere/bokeh** | Sognante | Fotografia, lusso |
| **Lucciole** | Magia | Giochi, fantasy |

### Librerie

| Libreria | Ideale per |
| --- | --- |
| **tsParticles** | Configurabile, leggera |
| **particles.js** | Sfondi semplici (non più mantenuta: preferisci tsParticles) |
| **Canvas API** | Effetti su misura, massimo controllo |
| **Three.js** | Particelle 3D complesse |

### Principi

- Predefinito: 30-50 particelle (senza esagerare)
- Movimento: lento, organico (velocità 0.5-2)
- Opacità: 0.3-0.6 (non devono competere con il contenuto)
- Connessioni: linee sottili per l'effetto "rete"
- ⚠️ Disattivale o riducile su mobile

### Quando usarle

- ✅ Sfondi hero (atmosfera)
- ✅ Festeggiare un successo (esplosione di coriandoli)
- ✅ Visualizzazioni tech (nodi collegati)
- ❌ Pagine ricche di contenuto (distraggono)
- ❌ Dispositivi poco potenti (consumano batteria)

---

## 6. Animazioni guidate dallo scroll

### CSS nativo (moderno)

```text
Scroll timeline in CSS:
├── animation-timeline: scroll() - progresso dello scroll del contenitore
├── animation-timeline: view() - visibilità dell'elemento nel viewport
├── animation-range: soglie di entrata/uscita
└── Nessun JavaScript necessario
```

### Principi

| Punto di attivazione | Caso d'uso |
| --- | --- |
| **Entry 0%** | Quando l'elemento inizia a entrare |
| **Entry 50%** | Quando è visibile per metà |
| **Cover 50%** | Quando è al centro del viewport |
| **Exit 100%** | Quando è uscito del tutto |

### Buone pratiche

- Animazioni di rivelazione: parti a circa il 25% di entry
- Parallax: segui il progresso continuo dello scroll
- Elementi sticky: usa il range cover
- Verifica sempre le prestazioni dello scroll

---

## 7. Principi di prestazioni

### Animazioni su GPU e su CPU

```text
ECONOMICHE (accelerate dalla GPU):
├── transform (translate, scale, rotate)
├── opacity
└── filter (con parsimonia)

COSTOSE (causano reflow):
├── width, height
├── top, left, right, bottom
├── padding, margin
└── box-shadow complessi
```

### Checklist di ottimizzazione

- [ ] Anima solo transform/opacity
- [ ] Usa `will-change` prima delle animazioni pesanti (e poi rimuovilo)
- [ ] Prova su dispositivi di fascia bassa
- [ ] Implementa `prefers-reduced-motion`
- [ ] Carica le librerie di animazione in lazy load
- [ ] Limita la frequenza (throttle) dei calcoli legati allo scroll

---

## 8. Albero decisionale per le motion graphics

```text
Che animazione ti serve?
│
├── Animazione complessa e brandizzata?
│   └── Lottie (esportata da After Effects)
│
├── Sequenza attivata dallo scroll?
│   └── GSAP + ScrollTrigger
│
├── Animazione di logo/icona?
│   └── Animazione SVG (stroke o morph)
│
├── Effetto 3D interattivo?
│   └── CSS 3D Transforms (semplice) o Three.js (complesso)
│
├── Sfondo d'atmosfera?
│   └── tsParticles o Canvas
│
└── Semplice entrata/hover?
    └── CSS @keyframes o Motion (ex Framer Motion)
```

---

## 9. Anti-pattern

| ❌ Non fare | ✅ Fai |
| --- | --- |
| Animare tutto insieme | Usa stagger e sequenze |
| Usare librerie pesanti per effetti semplici | Parti dal CSS |
| Ignorare il reduced-motion | Prevedi sempre un fallback |
| Bloccare il main thread | Ottimizza per i 60fps |
| Le stesse particelle in ogni progetto | Adattale a brand e contesto |
| Effetti complessi su mobile | Usa la feature detection |

---

## 10. Riferimento rapido

| Effetto | Strumento | Prestazioni |
| --- | --- | --- |
| Spinner di caricamento | CSS/Lottie | Leggero |
| Rivelazione a cascata | GSAP/Motion | Medio |
| Disegno di path SVG | CSS stroke | Leggero |
| Card flip 3D | CSS transforms | Leggero |
| Sfondo particellare | tsParticles | Pesante |
| Parallax allo scroll | GSAP ScrollTrigger | Medio |
| Morphing di forme | GSAP MorphSVG | Medio |

---

> **Ricorda**: le motion graphics devono valorizzare, non distrarre. Ogni animazione deve avere uno SCOPO: feedback, guida, piacere o storytelling.
