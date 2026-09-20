# 6. Prestazioni del rendering

> **Impatto:** MEDIO
> **Obiettivo:** Ottimizzare il processo di rendering riduce il lavoro che il browser deve svolgere.

---

## Panoramica

Questa sezione contiene **9 regole** dedicate alle prestazioni del rendering.

---

## Regola 6.1: Anima il wrapper dell'SVG invece dell'elemento SVG

**Impatto:** BASSO  
**Tag:** rendering, svg, css, animation, performance  

## Anima il wrapper dell'SVG invece dell'elemento SVG

Molti browser non applicano l'accelerazione hardware alle animazioni CSS3 sugli elementi SVG. Avvolgi l'SVG in un `<div>` e anima il wrapper.

**Sbagliato (anima direttamente l'SVG, senza accelerazione hardware):**

```tsx
function LoadingSpinner() {
  return (
    <svg 
      className="animate-spin"
      width="24" 
      height="24" 
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  )
}
```

**Corretto (anima il div wrapper, con accelerazione hardware):**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg 
        width="24" 
        height="24" 
        viewBox="0 0 24 24"
      >
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  )
}
```

Vale per tutte le trasformazioni e le transizioni CSS (`transform`, `opacity`, `translate`, `scale`, `rotate`). Il div wrapper permette al browser di usare l'accelerazione GPU e rende le animazioni più fluide.

---

## Regola 6.2: CSS content-visibility per le liste lunghe

**Impatto:** ALTO  
**Tag:** rendering, css, content-visibility, long-lists  

## CSS content-visibility per le liste lunghe

Applica `content-visibility: auto` per rimandare il rendering degli elementi fuori schermo.

**CSS:**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**Esempio:**

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map(msg => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  )
}
```

Con 1000 messaggi il browser salta layout e paint di circa 990 elementi fuori schermo (rendering iniziale 10× più veloce).

---

## Regola 6.3: Fai l'hoisting degli elementi JSX statici

**Impatto:** BASSO  
**Tag:** rendering, jsx, static, optimization  

## Fai l'hoisting degli elementi JSX statici

Porta il JSX statico fuori dai componenti, così non viene ricreato.

**Sbagliato (ricrea l'elemento a ogni render):**

```tsx
function LoadingSkeleton() {
  return <div className="animate-pulse h-20 bg-gray-200" />
}

function Container() {
  return (
    <div>
      {loading && <LoadingSkeleton />}
    </div>
  )
}
```

**Corretto (riusa lo stesso elemento):**

```tsx
const loadingSkeleton = (
  <div className="animate-pulse h-20 bg-gray-200" />
)

function Container() {
  return (
    <div>
      {loading && loadingSkeleton}
    </div>
  )
}
```

È utile soprattutto con nodi SVG grandi e statici, costosi da ricreare a ogni render.

**Nota:** se nel progetto è attivo il [React Compiler](https://react.dev/learn/react-compiler), il compilatore fa automaticamente l'hoisting degli elementi JSX statici e ottimizza i re-render dei componenti: l'hoisting manuale diventa superfluo.

---

## Regola 6.4: Ottimizza la precisione degli SVG

**Impatto:** BASSO  
**Tag:** rendering, svg, optimization, svgo  

## Ottimizza la precisione degli SVG

Riduci la precisione delle coordinate SVG per alleggerire i file. La precisione ottimale dipende dalla dimensione del viewBox, ma in generale conviene valutare di ridurla.

**Sbagliato (precisione eccessiva):**

```svg
<path d="M 10.293847 20.847362 L 30.938472 40.192837" />
```

**Corretto (1 cifra decimale):**

```svg
<path d="M 10.3 20.8 L 30.9 40.2" />
```

**Automatizza con SVGO:**

```bash
npx svgo --precision=1 --multipass icon.svg
```

---

## Regola 6.5: Evita l'hydration mismatch senza sfarfallio

**Impatto:** MEDIO  
**Tag:** rendering, ssr, hydration, localStorage, flicker  

## Evita l'hydration mismatch senza sfarfallio

Quando renderizzi contenuti che dipendono da uno storage lato client (localStorage, cookie), evita sia la rottura dell'SSR sia lo sfarfallio dopo l'idratazione: inietta uno script sincrono che aggiorna il DOM prima che React esegua l'idratazione.

**Sbagliato (rompe l'SSR):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  // localStorage non esiste sul server: lancia un errore
  const theme = localStorage.getItem('theme') || 'light'
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

Il rendering lato server fallisce perché `localStorage` non è definito.

**Sbagliato (sfarfallio visibile):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState('light')
  
  useEffect(() => {
    // Gira dopo l'idratazione: causa un flash visibile
    const stored = localStorage.getItem('theme')
    if (stored) {
      setTheme(stored)
    }
  }, [])
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

Il componente renderizza prima il valore di default (`light`) e si aggiorna solo dopo l'idratazione: per un attimo si vede il contenuto sbagliato.

**Corretto (niente sfarfallio né hydration mismatch):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <>
      <div id="theme-wrapper">
        {children}
      </div>
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                var theme = localStorage.getItem('theme') || 'light';
                var el = document.getElementById('theme-wrapper');
                if (el) el.className = theme;
              } catch (e) {}
            })();
          `,
        }}
      />
    </>
  )
}
```

Lo script inline viene eseguito in modo sincrono prima che l'elemento sia mostrato, quindi il DOM ha già il valore corretto. Niente sfarfallio, niente hydration mismatch.

Il pattern è utile soprattutto per switch del tema, preferenze utente, stato di autenticazione e qualunque dato solo client che deve comparire subito, senza mostrare prima i valori di default.

---

## Regola 6.6: Silenzia gli hydration mismatch previsti

**Impatto:** MEDIO-BASSO  
**Tag:** rendering, hydration, ssr, nextjs  

## Silenzia gli hydration mismatch previsti

Nei framework SSR (per es. Next.js) alcuni valori sono volutamente diversi tra server e client (ID casuali, date, formattazione per locale/fuso orario). Per questi mismatch *previsti*, avvolgi il testo dinamico in un elemento con `suppressHydrationWarning` ed elimini i warning superflui. Non usarlo per nascondere bug reali e non abusarne.

**Sbagliato (warning per mismatch noti):**

```tsx
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>
}
```

**Corretto (silenzia solo il mismatch previsto):**

```tsx
function Timestamp() {
  return (
    <span suppressHydrationWarning>
      {new Date().toLocaleString()}
    </span>
  )
}
```

---

## Regola 6.7: Usa il componente Activity per mostrare e nascondere

**Impatto:** MEDIO  
**Tag:** rendering, activity, visibility, state-preservation  

## Usa il componente Activity per mostrare e nascondere

Usa `<Activity>` di React per preservare stato e DOM dei componenti costosi che vengono mostrati e nascosti spesso.

**Uso:**

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

Eviti re-render costosi e la perdita dello stato.

---

## Regola 6.8: Usa un rendering condizionale esplicito

**Impatto:** BASSO  
**Tag:** rendering, conditional, jsx, falsy-values  

## Usa un rendering condizionale esplicito

Nel rendering condizionale usa l'operatore ternario esplicito (`? :`) invece di `&&` quando la condizione può valere `0`, `NaN` o altri valori falsy che vengono renderizzati.

**Sbagliato (renderizza "0" quando count è 0):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  )
}

// Con count = 0 renderizza: <div>0</div>
// Con count = 5 renderizza: <div><span class="badge">5</span></div>
```

**Corretto (non renderizza nulla quando count è 0):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  )
}

// Con count = 0 renderizza: <div></div>
// Con count = 5 renderizza: <div><span class="badge">5</span></div>
```

---

## Regola 6.9: Preferisci useTransition agli stati di caricamento manuali

**Impatto:** BASSO  
**Tag:** rendering, transitions, useTransition, loading, state  

## Preferisci useTransition agli stati di caricamento manuali

Per gli stati di caricamento usa `useTransition` invece di gestirli a mano con `useState`: ottieni lo stato `isPending` già pronto e la gestione automatica delle transizioni.

**Sbagliato (stato di caricamento manuale):**

```tsx
function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async (value: string) => {
    setIsLoading(true)
    setQuery(value)
    const data = await fetchResults(value)
    setResults(data)
    setIsLoading(false)
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isLoading && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**Corretto (useTransition con lo stato pending integrato):**

```tsx
import { useTransition, useState } from 'react'

function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  const handleSearch = (value: string) => {
    setQuery(value) // Aggiorna subito l'input
    
    startTransition(async () => {
      // Recupera i risultati
      const data = await fetchResults(value)
      // Gli aggiornamenti dopo un await vanno riavvolti in startTransition
      startTransition(() => {
        setResults(data)
      })
    })
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**Vantaggi:**

- **Stato pending automatico**: non devi gestire a mano `setIsLoading(true/false)`
- **Resilienza agli errori**: lo stato pending si azzera correttamente anche se la transizione lancia un'eccezione
- **Reattività migliore**: la UI resta reattiva durante gli aggiornamenti
- **Gestione delle interruzioni**: gli aggiornamenti in transizione vengono interrotti da quelli urgenti (per es. la digitazione); le richieste già partite però non vengono annullate, quindi se serve gestisci le risposte che arrivano fuori ordine

Riferimento: [useTransition](https://react.dev/reference/react/useTransition)
