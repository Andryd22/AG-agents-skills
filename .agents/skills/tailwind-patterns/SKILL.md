---
name: tailwind-patterns
description: Principi di Tailwind CSS v4. Configurazione nel CSS, container query, schemi moderni, architettura dei design token.
---

# Schemi di Tailwind CSS (v4)

> CSS utility-first moderno con configurazione nativa nel CSS.

---

## 1. Architettura di Tailwind v4

### Cosa è cambiato rispetto alla v3

| v3 (vecchia) | v4 (attuale) |
| --- | --- |
| `tailwind.config.js` | Direttiva `@theme` nel CSS |
| Plugin PostCSS | Motore Oxide (molto più veloce) |
| Modalità JIT | Nativa, sempre attiva |
| Sistema di plugin | Funzioni native del CSS |
| Direttiva `@apply` | Funziona ancora, sconsigliata |

### Concetti base della v4

| Concetto | Descrizione |
| --- | --- |
| **Prima il CSS** | Configurazione nel CSS, non in JavaScript |
| **Motore Oxide** | Compilatore in Rust, molto più veloce |
| **Annidamento nativo** | Annidamento CSS senza PostCSS |
| **Variabili CSS** | Tutti i token esposti come variabili `--*` |

---

## 2. Configurazione nel CSS

### Definire il tema

```css
@theme {
  /* Colori: usa nomi semantici */
  --color-primary: oklch(0.7 0.15 250);
  --color-surface: oklch(0.98 0 0);
  --color-surface-dark: oklch(0.15 0 0);

  /* Scala degli spazi */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;

  /* Tipografia */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### Estendere o sostituire

| Azione | Quando |
| --- | --- |
| **Estendere** | Aggiungi valori nuovi accanto a quelli predefiniti |
| **Sostituire** | Rimpiazzi del tutto la scala predefinita |
| **Token semantici** | Nomi specifici del progetto (primary, surface) |

---

## 3. Container query (native nella v4)

### Breakpoint o container

| Tipo | Risponde a |
| --- | --- |
| **Breakpoint** (`md:`) | Larghezza del viewport |
| **Container** (`@container`) | Larghezza dell'elemento genitore |

### Come si usano

| Schema | Classi |
| --- | --- |
| Definire il container | `@container` sul genitore |
| Breakpoint del container | `@sm:`, `@md:`, `@lg:` sui figli |
| Container con nome | `@container/card` (e `@md/card:` sui figli) per essere precisi |

### Quando usarle

| Scenario | Usa |
| --- | --- |
| Layout a livello di pagina | Breakpoint del viewport |
| Responsive a livello di componente | Container query |
| Componenti riutilizzabili | Container query (indipendenti dal contesto) |

---

## 4. Design responsive

### Breakpoint

| Prefisso | Larghezza minima | Destinazione |
| --- | --- | --- |
| (nessuno) | 0px | Base mobile-first |
| `sm:` | 640px | Telefono grande / tablet piccolo |
| `md:` | 768px | Tablet |
| `lg:` | 1024px | Portatile |
| `xl:` | 1280px | Desktop |
| `2xl:` | 1536px | Desktop grande |

### Prima il mobile

1. Scrivi prima gli stili per mobile (senza prefisso)
2. Aggiungi le varianti per gli schermi più grandi con i prefissi
3. Esempio: `w-full md:w-1/2 lg:w-1/3`

---

## 5. Dark mode

### Strategie

| Metodo | Comportamento | Quando |
| --- | --- | --- |
| Predefinito (media query) | Segue la preferenza del sistema | Nessun controllo da parte dell'utente |
| Classe `.dark` | `@custom-variant dark (&:where(.dark, .dark *));` nel CSS | Selettore del tema a mano |
| Attributo `data-theme` | `@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));` | Temi più complessi |

Nella v4 la dark mode non si configura più in `tailwind.config.js` (`darkMode: 'class'`): si ridefinisce la variante `dark` nel CSS con `@custom-variant`.

### Schema della dark mode

| Elemento | Chiaro | Scuro |
| --- | --- | --- |
| Sfondo | `bg-white` | `dark:bg-zinc-900` |
| Testo | `text-zinc-900` | `dark:text-zinc-100` |
| Bordi | `border-zinc-200` | `dark:border-zinc-700` |

---

## 6. Layout moderni

### Flexbox

| Schema | Classi |
| --- | --- |
| Centrato (entrambi gli assi) | `flex items-center justify-center` |
| Pila verticale | `flex flex-col gap-4` |
| Riga orizzontale | `flex gap-4` |
| Spazio tra gli elementi | `flex justify-between items-center` |
| Griglia che va a capo | `flex flex-wrap gap-4` |

### Grid

| Schema | Classi |
| --- | --- |
| Responsive con auto-fit | `grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))]` |
| Asimmetrico (Bento) | `grid grid-cols-3 grid-rows-2` con span |
| Layout con barra laterale | `grid grid-cols-[auto_1fr]` |

> **Nota:** meglio i layout asimmetrici/Bento delle griglie simmetriche a 3 colonne.

---

## 7. Sistema dei colori moderno

### OKLCH, RGB o HSL

| Formato | Vantaggio |
| --- | --- |
| **OKLCH** | Uniforme per la percezione, migliore per il design |
| **HSL** | Tinta e saturazione intuitive |
| **RGB** | Compatibilità con il vecchio |

### Architettura dei token di colore

| Livello | Esempio | Scopo |
| --- | --- | --- |
| **Primitivo** | `--blue-500` | Valori di colore grezzi |
| **Semantico** | `--color-primary` | Nomi in base allo scopo |
| **Componente** | `--button-bg` | Specifici del componente |

---

## 8. Tipografia

### Pile di font

| Tipo | Consigliati |
| --- | --- |
| Sans | `'Inter', 'SF Pro', system-ui, sans-serif` |
| Mono | `'JetBrains Mono', 'Fira Code', monospace` |
| Titoli | `'Outfit', 'Poppins', sans-serif` |

### Scala tipografica

| Classe | Dimensione | Uso |
| --- | --- | --- |
| `text-xs` | 0.75rem | Etichette, didascalie |
| `text-sm` | 0.875rem | Testo secondario |
| `text-base` | 1rem | Testo del corpo |
| `text-lg` | 1.125rem | Testo introduttivo |
| `text-xl`+ | 1.25rem+ | Titoli |

---

## 9. Animazioni e transizioni

### Animazioni integrate

| Classe | Effetto |
| --- | --- |
| `animate-spin` | Rotazione continua |
| `animate-ping` | Pulsazione per attirare l'attenzione |
| `animate-pulse` | Leggera pulsazione dell'opacità |
| `animate-bounce` | Effetto rimbalzo |

### Transizioni

| Schema | Classi |
| --- | --- |
| Tutte le proprietà | `transition-all duration-200` |
| Una proprietà | `transition-colors duration-150` |
| Con easing | `ease-out` o `ease-in-out` |
| Effetto hover | `hover:scale-105 transition-transform` |

---

## 10. Estrarre componenti

### Quando estrarre

| Segnale | Azione |
| --- | --- |
| La stessa combinazione di classi 3+ volte | Estrai un componente |
| Varianti di stato complesse | Estrai un componente |
| Elemento del design system | Estrai + documenta |

### Come estrarre

| Metodo | Quando |
| --- | --- |
| **Componente React/Vue** | Dinamico, serve JS |
| **@apply nel CSS** | Statico, niente JS |
| **Design token** | Valori riutilizzabili |

---

## 11. Anti-pattern

| Da non fare | Da fare |
| --- | --- |
| Valori arbitrari ovunque | Usa la scala del design system |
| `!important` | Risolvi la specificità come si deve |
| `style=` in linea | Usa le utility |
| Lunghe liste di classi duplicate | Estrai un componente |
| Mescolare la configurazione v3 con la v4 | Migra tutto alla configurazione nel CSS |
| Abusare di `@apply` | Meglio i componenti |

---

## 12. Prestazioni

| Principio | Implementazione |
| --- | --- |
| **Togli l'inutilizzato** | Automatico nella v4 |
| **Evita le classi dinamiche** | Niente classi costruite con template string |
| **Usa Oxide** | Predefinito nella v4, molto più veloce |
| **Cache delle build** | Cache nella CI/CD |

---

> **Ricorda:** Tailwind v4 mette il CSS al primo posto. Sfrutta variabili CSS, container query e funzioni native. Il file di configurazione ora è facoltativo.
