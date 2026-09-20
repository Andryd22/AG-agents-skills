---
name: frontend-design
description: Pensiero progettuale e scelte di design per le UI web. Usala quando progetti componenti, layout, palette di colori, tipografia o interfacce curate nell'estetica. Insegna principi, non valori fissi.
---

# Design system per il frontend

> **Filosofia:** ogni pixel ha uno scopo. La sobrietà è lusso. Le decisioni le guida la psicologia dell'utente.
> **Principio chiave:** PENSA, non memorizzare. CHIEDI, non dare per scontato.

---

## 🎯 Regola di lettura selettiva (OBBLIGATORIA)

**Leggi sempre i file OBBLIGATORI, quelli FACOLTATIVI solo se servono:**

| File | Stato | Quando leggerlo |
| --- | --- | --- |
| [ux-psychology.md](ux-psychology.md) | 🔴 **OBBLIGATORIO** | Sempre, per primo! |
| [color-system.md](color-system.md) | ⚪ Facoltativo | Scelte di colori e palette |
| [typography-system.md](typography-system.md) | ⚪ Facoltativo | Scelta e abbinamento dei font |
| [visual-effects.md](visual-effects.md) | ⚪ Facoltativo | Glassmorphism, ombre, gradienti |
| [animation-guide.md](animation-guide.md) | ⚪ Facoltativo | Quando servono animazioni |
| [motion-graphics.md](motion-graphics.md) | ⚪ Facoltativo | Lottie, GSAP, 3D |
| [decision-trees.md](decision-trees.md) | ⚪ Facoltativo | Template per contesto |

> 🔴 **ux-psychology.md = LEGGILO SEMPRE. Gli altri = solo se pertinenti.**

---

## 🔧 Script da eseguire

**Eseguili per gli audit (non leggerli, lanciali e basta):**

| Script | A cosa serve | Uso |
| --- | --- | --- |
| `scripts/ux_audit.py` | Audit di psicologia UX e accessibilità | `python .agents/skills/frontend-design/scripts/ux_audit.py <cartella_progetto>` |
| `scripts/accessibility_checker.py` | Audit WCAG di HTML/JSX/TSX | `python .agents/skills/frontend-design/scripts/accessibility_checker.py <cartella_progetto>` |

---

## ⚠️ CRITICO: CHIEDI PRIMA DI DARE PER SCONTATO (OBBLIGATORIO)

> **FERMATI! Se la richiesta dell'utente è aperta, NON ripiegare sulle tue scelte preferite.**

### Se la richiesta dell'utente è vaga, CHIEDI

**Colore non indicato?** Chiedi:
> "Che palette di colori preferisci? (blu/verde/arancio/neutra/altro?)"

**Stile non indicato?** Chiedi:
> "Che stile cerchi? (minimal/deciso/retrò/futuristico/organico?)"

**Layout non indicato?** Chiedi:
> "Hai una preferenza per il layout? (colonna singola/griglia/asimmetrico/a tutta larghezza?)"

### ⛔ TENDENZE PREDEFINITE DA EVITARE (NIENTE PORTO SICURO)

| Tendenza predefinita dell'AI | Perché è un problema | Pensa invece |
| --- | --- | --- |
| **Bento grid (cliché moderno)** | Compare in ogni design fatto dall'AI | Perché questo contenuto HA BISOGNO di una griglia? |
| **Hero diviso (sinistra/destra)** | Prevedibile e noioso | Perché non una tipografia enorme o una narrazione verticale? |
| **Gradienti mesh/aurora** | Il "nuovo" sfondo pigro | Qual è un abbinamento di colori radicale? |
| **Glassmorphism** | L'idea di "premium" dell'AI | Perché non un flat pieno e ad alto contrasto? |
| **Ciano scuro / blu fintech** | Il porto sicuro dopo il divieto del viola | Perché non rosso, nero o verde neon? |
| **"Orchestrare / Potenziare"** | Copy scritto dall'AI | Come lo direbbe una persona? |
| Sfondo scuro + bagliore neon | Abusato, "look da AI" | Di cosa ha BISOGNO davvero il BRAND? |
| **Tutto arrotondato** | Generico, sicuro | Dove posso usare spigoli vivi, brutalisti? |

> 🔴 **"Ogni struttura 'sicura' che scegli ti avvicina di un passo a un template generico. RISCHIA."**

---

## 1. Analisi dei vincoli (SEMPRE PER PRIMA)

Prima di qualsiasi lavoro di design, RISPONDI a queste domande o CHIEDI all'utente:

| Vincolo | Domanda | Perché conta |
| --- | --- | --- |
| **Tempi** | Quanto tempo c'è? | Determina la complessità |
| **Contenuti** | Pronti o segnaposto? | Incide sulla flessibilità del layout |
| **Brand** | Ci sono linee guida? | Possono imporre colori e font |
| **Tecnologia** | Quale stack? | Incide su cosa puoi fare |
| **Pubblico** | Chi, esattamente? | Guida tutte le scelte visive |

### Pubblico → approccio al design

| Pubblico | A cosa pensare |
| --- | --- |
| **Gen Z** | Deciso, veloce, mobile-first, autentico |
| **Millennial** | Pulito, minimal, orientato ai valori |
| **Gen X** | Familiare, affidabile, chiaro |
| **Boomer** | Leggibile, alto contrasto, semplice |
| **B2B** | Professionale, centrato sui dati, fiducia |
| **Lusso** | Eleganza sobria, spazio bianco |

---

## 2. Principi di psicologia UX

### Leggi fondamentali (interiorizzale)

| Legge | Principio | Applicazione |
| --- | --- | --- |
| **Legge di Hick** | Più scelte = decisioni più lente | Limita le opzioni, usa la progressive disclosure |
| **Legge di Fitts** | Più grande + più vicino = più facile da cliccare | Dimensiona bene le CTA |
| **Legge di Miller** | ~7 elementi nella memoria di lavoro | Raggruppa i contenuti in blocchi |
| **Effetto Von Restorff** | Diverso = memorabile | Rendi le CTA visivamente distinte |
| **Posizione seriale** | Si ricordano di più il primo e l'ultimo | Informazioni chiave all'inizio e alla fine |

### Livelli del design emotivo

```text
VISCERALE (istante)   → Prima impressione: colori, immagini, sensazione generale
COMPORTAMENTALE (uso) → Durante l'uso: velocità, feedback, efficienza
RIFLESSIVO (ricordo)  → Dopo: "Mi piace quello che dice di me"
```

### Costruire la fiducia

- Indicatori di sicurezza nelle azioni sensibili
- Riprova sociale dove serve
- Accesso chiaro a contatti e assistenza
- Design coerente e professionale
- Policy trasparenti

---

## 3. Principi di layout

### Sezione aurea (φ = 1.618)

```text
Usala per proporzioni armoniose:
├── Contenuto : sidebar = circa 62% : 38%
├── Ogni dimensione dei titoli = precedente × 1.618 (per una scala d'impatto)
├── La spaziatura può seguire: sm → md → lg (ognuno × 1.618)
```

### Griglia da 8 punti

```text
Tutte le spaziature e le dimensioni in multipli di 8:
├── Stretto: 4px (mezzo passo per i micro-dettagli)
├── Piccolo: 8px
├── Medio: 16px
├── Grande: 24px, 32px
├── XL: 48px, 64px, 80px
└── Adatta in base alla densità dei contenuti
```

### Principi chiave di dimensionamento

| Elemento | Cosa considerare |
| --- | --- |
| **Touch target** | Dimensione minima comoda per il tocco |
| **Pulsanti** | Altezza in base alla gerarchia di importanza |
| **Input** | Stessa altezza dei pulsanti, per l'allineamento |
| **Card** | Padding coerente, che lasci respirare |
| **Larghezza di lettura** | Ottimale 45-75 caratteri |

---

## 4. Principi del colore

### Regola 60-30-10

```text
60% → Primario/sfondo (base calma e neutra)
30% → Secondario (aree di supporto)
10% → Accento (CTA, evidenziazioni, attenzione)
```

### Psicologia del colore (per decidere)

| Se ti serve... | Considera le tonalità | Evita |
| --- | --- | --- |
| Fiducia, calma | Famiglia dei blu | Rossi aggressivi |
| Crescita, natura | Famiglia dei verdi | Grigi industriali |
| Energia, urgenza | Arancio, rosso | Blu passivi |
| Lusso, creatività | Verde petrolio scuro, oro, smeraldo | Colori accesi che sanno di economico |
| Pulito, minimal | Neutri | Troppo colore |

### Processo di scelta

1. **Qual è il settore?** (restringe le opzioni)
2. **Qual è l'emozione?** (sceglie il primario)
3. **Light o dark mode?** (definisce la base)
4. **CHIEDI ALL'UTENTE** se non è specificato

Per la teoria del colore nel dettaglio: [color-system.md](color-system.md)

---

## 5. Principi di tipografia

### Scelta della scala

| Tipo di contenuto | Rapporto di scala | Effetto |
| --- | --- | --- |
| UI densa | 1.125-1.2 | Compatta, efficiente |
| Web generico | 1.25 | Bilanciata (la più comune) |
| Editoriale | 1.333 | Leggibile, ariosa |
| Hero/display | 1.5-1.618 | Impatto drammatico |

### Abbinamento dei font

```text
Contrasto + armonia:
├── Abbastanza DIVERSI per creare gerarchia
├── Abbastanza SIMILI per restare coerenti
└── Di solito: display + neutro, oppure serif + sans
```

### Regole di leggibilità

- **Lunghezza della riga**: ottimale 45-75 caratteri
- **Interlinea**: 1.4-1.6 per il testo
- **Contrasto**: verifica i requisiti WCAG
- **Dimensione**: almeno 16px per il testo sul web

Per la tipografia nel dettaglio: [typography-system.md](typography-system.md)

---

## 6. Principi degli effetti visivi

### Glassmorphism (quando è appropriato)

```text
Proprietà chiave:
├── Sfondo semitrasparente
├── Sfocatura dello sfondo (backdrop blur)
├── Bordo sottile per definire la forma
└── ⚠️ **ATTENZIONE:** il glassmorphism standard blu/bianco è un cliché moderno. Usalo in modo radicale o non usarlo.
```

### Gerarchia delle ombre

```text
Concetto di elevazione:
├── Elementi più in alto = ombre più ampie
├── Offset Y > offset X (luce dall'alto)
├── Più livelli = più realismo
└── Dark mode: può servire un bagliore (glow) al posto dell'ombra
```

### Uso dei gradienti

```text
Gradienti armoniosi:
├── Colori adiacenti sulla ruota (analoghi)
├── OPPURE stessa tonalità, luminosità diversa
├── Evita coppie complementari stridenti
├── 🚫 **NIENTE gradienti mesh/aurora** (blob fluttuanti)
└── CAMBIA radicalmente da un progetto all'altro
```

Per la guida completa agli effetti: [visual-effects.md](visual-effects.md)

---

## 7. Principi di animazione

### Tempi

```text
La durata dipende da:
├── Distanza (più lontano = più lunga)
├── Dimensione (più grande = più lenta)
├── Importanza (critica = chiara)
└── Contesto (urgente = veloce, lusso = lenta)
```

### Scelta dell'easing

| Azione | Easing | Perché |
| --- | --- | --- |
| Entrata | Ease-out | Rallenta e si assesta |
| Uscita | Ease-in | Accelera ed esce |
| Enfasi | Ease-in-out | Fluida, intenzionale |
| Giocosa | Bounce | Divertente, energica |

### Prestazioni

- Anima solo transform e opacity
- Rispetta la preferenza per il movimento ridotto (reduced motion)
- Testa su dispositivi di fascia bassa

Per i pattern di animazione: [animation-guide.md](animation-guide.md), per quelli avanzati: [motion-graphics.md](motion-graphics.md)

---

## 8. Checklist "effetto wow"

### Segnali di qualità premium

- [ ] Spazio bianco generoso (lusso = respiro)
- [ ] Profondità e dimensione sottili
- [ ] Animazioni fluide e con uno scopo
- [ ] Cura dei dettagli (allineamento, coerenza)
- [ ] Ritmo visivo coerente
- [ ] Elementi personalizzati (non tutto di default)

### Elementi che creano fiducia

- [ ] Segnali di sicurezza dove servono
- [ ] Riprova sociale / testimonianze
- [ ] Proposta di valore chiara
- [ ] Immagini professionali
- [ ] Linguaggio di design coerente

### Leve emotive

- [ ] Hero che suscita l'emozione voluta
- [ ] Elementi umani (volti, storie)
- [ ] Indicatori di progresso e traguardi
- [ ] Piccoli momenti di sorpresa piacevole

---

## 9. Anti-pattern (cosa NON fare)

### ❌ Segnali di design pigro

- Font di sistema predefiniti scelti senza riflettere
- Foto stock che non c'entrano
- Spaziature incoerenti
- Troppi colori in competizione
- Muri di testo senza gerarchia
- Contrasto non accessibile

### ❌ Pattern tipici dell'AI (EVITALI!)

- **Stessi colori in ogni progetto**
- **Scuro + neon come default**
- **Viola/violetto ovunque (DIVIETO DEL VIOLA ✅)**
- **Bento grid per landing page semplici**
- **Gradienti mesh ed effetti glow**
- **Stessa struttura di layout / clone di Vercel**
- **Non chiedere le preferenze all'utente**

### ❌ Dark pattern (non etici)

- Costi nascosti
- Falsa urgenza
- Azioni forzate
- UI ingannevole
- Confirmshaming (far sentire in colpa chi rifiuta)

---

## 10. Riepilogo del processo decisionale

```text
Per OGNI attività di design:

1. VINCOLI
   └── Quali sono tempi, brand, tecnologia e pubblico?
   └── Se non è chiaro → CHIEDI

2. CONTENUTI
   └── Quali contenuti esistono?
   └── Qual è la gerarchia?

3. DIREZIONE STILISTICA
   └── Cosa è adatto al contesto?
   └── Se non è chiaro → CHIEDI (niente default!)

4. ESECUZIONE
   └── Applica i principi qui sopra
   └── Confronta il risultato con gli anti-pattern

5. REVISIONE
   └── "Serve davvero all'utente?"
   └── "È diverso dalle mie scelte di default?"
   └── "Ne andrei fiero?"
```

---

## File di riferimento

Per approfondire aree specifiche:

- [color-system.md](color-system.md) - Teoria del colore e processo di scelta
- [typography-system.md](typography-system.md) - Abbinamento dei font e scelta della scala
- [visual-effects.md](visual-effects.md) - Principi e tecniche degli effetti
- [animation-guide.md](animation-guide.md) - Principi di motion design
- [motion-graphics.md](motion-graphics.md) - Avanzato: Lottie, GSAP, SVG, 3D, particelle
- [decision-trees.md](decision-trees.md) - Template specifici per contesto
- [ux-psychology.md](ux-psychology.md) - Psicologia dell'utente in profondità

---

## Skill collegate

| Skill | Quando usarla |
| --- | --- |
| **frontend-design** (questa) | Prima di scrivere codice: impara i principi di design (colore, tipografia, psicologia UX) |
| **[web-design-guidelines](../web-design-guidelines/SKILL.md)** | Dopo aver scritto il codice: audit di accessibilità, prestazioni e buone pratiche |

## Workflow dopo il design

Dopo aver implementato il design, esegui l'audit:

```text
1. DESIGN   → Leggi i principi di frontend-design ← SEI QUI
2. CODICE   → Implementa il design
3. AUDIT    → Esegui la revisione con web-design-guidelines
4. CORREGGI → Risolvi i problemi emersi dall'audit
```

> **Passo successivo:** dopo aver scritto il codice, usa la skill `web-design-guidelines` per verificare l'implementazione: accessibilità, stati di focus, animazioni e prestazioni.

---

> **Ricorda:** il design è PENSARE, non copiare. Ogni progetto merita una riflessione nuova, basata sul suo contesto e sui suoi utenti. **Evita il porto sicuro del SaaS moderno!**

---

## 11. Pattern moderni per i form in Next.js 16+

> [!IMPORTANT]
> Nei progetti Next.js 16+ usa il componente nativo `next/form` al posto del normale `<form>` HTML per tutte le operazioni di ricerca e filtro basate su GET.

### I vantaggi del componente `<Form>`

- **Navigazione automatica lato client:** all'invio esegue una transizione lato client.
- **Progressive enhancement:** funziona anche senza JavaScript.
- **Sincronizzazione con l'URL:** codifica automaticamente i valori degli input nei search params.

### Esempio di implementazione (barra di ricerca)

```tsx
import Form from 'next/form'

export default function SearchBar() {
  return (
    <Form action="/search" className="flex gap-2">
      <input 
        name="q" 
        placeholder="Search products..." 
        className="border p-2"
      />
      <button type="submit">Search</button>
    </Form>
  )
}
```

### Quando usare `<Form>` e quando il normale `<form>`

- **Usa `next/form`** per: ricerca, filtri, ordinamento, paginazione (richieste GET).
- **Usa il normale `<form>`** per: mutazioni, login, inserimento dati (richieste POST tramite Server Actions).
