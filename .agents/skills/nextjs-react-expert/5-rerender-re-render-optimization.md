# 5. Ottimizzare i re-render

> **Impatto:** MEDIO
> **Obiettivo:** Ridurre i re-render non necessari evita calcoli sprecati e rende la UI più reattiva.

---

## Panoramica

Questa sezione contiene **12 regole** dedicate all'ottimizzazione dei re-render.

---

## Regola 5.1: Calcola lo stato derivato durante il rendering

**Impatto:** MEDIO  
**Tag:** rerender, derived-state, useEffect, state  

## Calcola lo stato derivato durante il rendering

Se un valore si può calcolare dalle prop o dallo state correnti, non salvarlo nello state e non aggiornarlo in un effect. Derivalo durante il render per evitare render extra e disallineamenti dello state. Non impostare lo state negli effect solo per reagire al cambio di una prop: preferisci valori derivati o reset tramite `key`.

**Sbagliato (state ed effect ridondanti):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const [fullName, setFullName] = useState('')

  useEffect(() => {
    setFullName(firstName + ' ' + lastName)
  }, [firstName, lastName])

  return <p>{fullName}</p>
}
```

**Corretto (derivato durante il render):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const fullName = firstName + ' ' + lastName

  return <p>{fullName}</p>
}
```

Riferimenti: [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)

---

## Regola 5.2: Rimanda la lettura dello state al punto in cui serve

**Impatto:** MEDIO  
**Tag:** rerender, searchParams, localStorage, optimization  

## Rimanda la lettura dello state al punto in cui serve

Non sottoscriverti a uno state dinamico (searchParams, localStorage) se lo leggi solo dentro le callback.

**Sbagliato (si sottoscrive a ogni cambio dei searchParams):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const searchParams = useSearchParams()

  const handleShare = () => {
    const ref = searchParams.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>Share</button>
}
```

**Corretto (legge al bisogno, nessuna sottoscrizione):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const params = new URLSearchParams(window.location.search)
    const ref = params.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>Share</button>
}
```

---

## Regola 5.3: Non avvolgere in useMemo un'espressione semplice con risultato primitivo

**Impatto:** MEDIO-BASSO  
**Tag:** rerender, useMemo, optimization  

## Non avvolgere in useMemo un'espressione semplice con risultato primitivo

Se un'espressione è semplice (pochi operatori logici o aritmetici) e restituisce un tipo primitivo (boolean, number, string), non avvolgerla in `useMemo`.
Chiamare `useMemo` e confrontare le dipendenze dell'hook può costare più dell'espressione stessa.

**Sbagliato:**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading
  }, [user.isLoading, notifications.isLoading])

  if (isLoading) return <Skeleton />
  // restituisce del markup
}
```

**Corretto:**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = user.isLoading || notifications.isLoading

  if (isLoading) return <Skeleton />
  // restituisce del markup
}
```

---

## Regola 5.4: Estrai in una costante il valore di default non primitivo di un componente memoizzato

**Impatto:** MEDIO  
**Tag:** rerender, memo, optimization  

## Estrai in una costante il valore di default non primitivo di un componente memoizzato

Se un componente memoizzato ha un valore di default per una prop opzionale non primitiva (un array, una funzione o un oggetto), chiamarlo senza quella prop rompe la memoizzazione: a ogni re-render si crea una nuova istanza del valore, che non supera il confronto di uguaglianza stretta di `memo()`.

Per risolvere, estrai il valore di default in una costante.

**Sbagliato (`onClick` ha un valore diverso a ogni re-render):**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
})

// Usato senza la prop opzionale onClick
<UserAvatar />
```

**Corretto (valore di default stabile):**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  // ...
})

// Usato senza la prop opzionale onClick
<UserAvatar />
```

---

## Regola 5.5: Estrai il lavoro in componenti memoizzati

**Impatto:** MEDIO  
**Tag:** rerender, memo, useMemo, optimization  

## Estrai il lavoro in componenti memoizzati

Sposta il lavoro costoso in componenti memoizzati, così puoi uscire in anticipo (early return) prima del calcolo.

**Sbagliato (calcola l'avatar anche durante il caricamento):**

```tsx
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user)
    return <Avatar id={id} />
  }, [user])

  if (loading) return <Skeleton />
  return <div>{avatar}</div>
}
```

**Corretto (salta il calcolo durante il caricamento):**

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user])
  return <Avatar id={id} />
})

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  )
}
```

**Nota:** se nel progetto è attivo il [React Compiler](https://react.dev/learn/react-compiler) (stabile dalla v1.0; in Next.js 16 si abilita con `reactCompiler: true` in `next.config`), di solito la memoizzazione manuale con `memo()` e `useMemo()` non serve: il compiler ottimizza i re-render in automatico.

---

## Regola 5.6: Restringi le dipendenze degli effect

**Impatto:** BASSO  
**Tag:** rerender, useEffect, dependencies, optimization  

## Restringi le dipendenze degli effect

Indica dipendenze primitive invece di oggetti, per ridurre al minimo le riesecuzioni degli effect.

**Sbagliato (si riesegue a ogni cambio di un campo di user):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**Corretto (si riesegue solo quando cambia id):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**Per lo stato derivato, calcolalo fuori dall'effect:**

```tsx
// Sbagliato: si esegue con width=767, 766, 765...
useEffect(() => {
  if (width < 768) {
    enableMobileMode()
  }
}, [width])

// Corretto: si esegue solo quando il boolean cambia
const isMobile = width < 768
useEffect(() => {
  if (isMobile) {
    enableMobileMode()
  }
}, [isMobile])
```

---

## Regola 5.7: Metti la logica delle interazioni negli event handler

**Impatto:** MEDIO  
**Tag:** rerender, useEffect, events, side-effects, dependencies  

## Metti la logica delle interazioni negli event handler

Se un side effect è causato da un'azione specifica dell'utente (submit, click, drag), eseguilo nel relativo event handler. Non modellare l'azione come state + effect: l'effect si riesegue per cambiamenti non correlati e l'azione può essere duplicata.

**Sbagliato (evento modellato come state + effect):**

```tsx
function Form() {
  const [submitted, setSubmitted] = useState(false)
  const theme = useContext(ThemeContext)

  useEffect(() => {
    if (submitted) {
      post('/api/register')
      showToast('Registered', theme)
    }
  }, [submitted, theme])

  return <button onClick={() => setSubmitted(true)}>Submit</button>
}
```

**Corretto (fallo nell'handler):**

```tsx
function Form() {
  const theme = useContext(ThemeContext)

  function handleSubmit() {
    post('/api/register')
    showToast('Registered', theme)
  }

  return <button onClick={handleSubmit}>Submit</button>
}
```

Riferimento: [Should this code move to an event handler?](https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler)

---

## Regola 5.8: Sottoscriviti allo stato derivato

**Impatto:** MEDIO  
**Tag:** rerender, derived-state, media-query, optimization  

## Sottoscriviti allo stato derivato

Sottoscriviti a uno stato derivato booleano invece che a valori continui, per ridurre la frequenza dei re-render.

**Sbagliato (re-render a ogni pixel di differenza):**

```tsx
function Sidebar() {
  const width = useWindowWidth()  // si aggiorna di continuo
  const isMobile = width < 768
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

**Corretto (re-render solo quando cambia il boolean):**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)')
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

---

## Regola 5.9: Usa gli aggiornamenti funzionali di setState

**Impatto:** MEDIO  
**Tag:** react, hooks, useState, useCallback, callbacks, closures  

## Usa gli aggiornamenti funzionali di setState

Quando aggiorni lo state in base al suo valore corrente, usa la forma funzionale di setState invece di riferirti direttamente alla variabile di state. Eviti closure obsolete (stale closure), elimini dipendenze inutili e ottieni riferimenti stabili alle callback.

**Sbagliato (richiede lo state come dipendenza):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // La callback dipende da items e viene ricreata a ogni cambio di items
  const addItems = useCallback((newItems: Item[]) => {
    setItems([...items, ...newItems])
  }, [items])  // ❌ la dipendenza da items causa ricreazioni
  
  // Rischio di stale closure se si dimentica la dipendenza
  const removeItem = useCallback((id: string) => {
    setItems(items.filter(item => item.id !== id))
  }, [])  // ❌ Manca la dipendenza da items: userà items obsoleti!
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

La prima callback viene ricreata ogni volta che `items` cambia, e questo può causare re-render inutili dei componenti figli. La seconda ha un bug di stale closure: farà sempre riferimento al valore iniziale di `items`.

**Corretto (callback stabili, nessuna stale closure):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // Callback stabile, mai ricreata
  const addItems = useCallback((newItems: Item[]) => {
    setItems(curr => [...curr, ...newItems])
  }, [])  // ✅ Nessuna dipendenza necessaria
  
  // Usa sempre lo state più recente, nessun rischio di stale closure
  const removeItem = useCallback((id: string) => {
    setItems(curr => curr.filter(item => item.id !== id))
  }, [])  // ✅ Sicura e stabile
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

**Vantaggi:**

1. **Riferimenti stabili alle callback**: non serve ricreare le callback quando cambia lo state
2. **Nessuna stale closure**: lavori sempre sul valore più recente dello state
3. **Meno dipendenze**: array delle dipendenze più semplici e meno memory leak
4. **Meno bug**: elimini la causa più comune dei bug di closure in React

**Quando usare gli aggiornamenti funzionali:**

- Qualsiasi setState che dipende dal valore corrente dello state
- Dentro useCallback/useMemo quando serve lo state
- Event handler che fanno riferimento allo state
- Operazioni asincrone che aggiornano lo state

**Quando gli aggiornamenti diretti vanno bene:**

- Impostare lo state su un valore statico: `setCount(0)`
- Impostare lo state solo da prop/argomenti: `setName(newName)`
- Lo state non dipende dal valore precedente

**Nota:** se nel progetto è attivo il [React Compiler](https://react.dev/learn/react-compiler), il compiler può ottimizzare automaticamente alcuni casi, ma gli aggiornamenti funzionali restano consigliati per correttezza e per evitare bug di stale closure.

---

## Regola 5.10: Usa l'inizializzazione lazy dello state

**Impatto:** MEDIO  
**Tag:** react, hooks, useState, performance, initialization  

## Usa l'inizializzazione lazy dello state

Passa una funzione a `useState` per i valori iniziali costosi. Senza la forma funzionale, l'inizializzatore viene eseguito a ogni render anche se il valore serve una sola volta.

**Sbagliato (eseguito a ogni render):**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() viene eseguito a OGNI render, anche dopo l'inizializzazione
  const [searchIndex, setSearchIndex] = useState(buildSearchIndex(items))
  const [query, setQuery] = useState('')
  
  // Quando query cambia, buildSearchIndex viene rieseguito inutilmente
  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse viene eseguito a ogni render
  const [settings, setSettings] = useState(
    JSON.parse(localStorage.getItem('settings') || '{}')
  )
  
  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

**Corretto (eseguito una sola volta):**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() viene eseguito SOLO al render iniziale
  const [searchIndex, setSearchIndex] = useState(() => buildSearchIndex(items))
  const [query, setQuery] = useState('')
  
  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse viene eseguito solo al render iniziale
  const [settings, setSettings] = useState(() => {
    const stored = localStorage.getItem('settings')
    return stored ? JSON.parse(stored) : {}
  })
  
  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

Usa l'inizializzazione lazy quando calcoli i valori iniziali da localStorage/sessionStorage, costruisci strutture dati (indici, map), leggi dal DOM o esegui trasformazioni pesanti.

Per primitivi semplici (`useState(0)`), riferimenti diretti (`useState(props.value)`) o literal economici (`useState({})`), la forma funzionale non serve.

---

## Regola 5.11: Usa le transition per gli aggiornamenti non urgenti

**Impatto:** MEDIO  
**Tag:** rerender, transitions, startTransition, performance  

## Usa le transition per gli aggiornamenti non urgenti

Marca come transition gli aggiornamenti di state frequenti e non urgenti, per mantenere la UI reattiva.

**Sbagliato (blocca la UI a ogni scroll):**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```

**Corretto (aggiornamenti non bloccanti):**

```tsx
import { startTransition } from 'react'

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY))
    }
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```

---

## Regola 5.12: Usa useRef per i valori transitori

**Impatto:** MEDIO  
**Tag:** rerender, useref, state, performance  

## Usa useRef per i valori transitori

Se un valore cambia spesso e non vuoi un re-render a ogni aggiornamento (per esempio tracker del mouse, intervalli, flag temporanei), salvalo in `useRef` invece che in `useState`. Tieni lo state del componente per la UI e usa le ref per valori temporanei legati al DOM. Aggiornare una ref non provoca un re-render.

**Sbagliato (render a ogni aggiornamento):**

```tsx
function Tracker() {
  const [lastX, setLastX] = useState(0)

  useEffect(() => {
    const onMove = (e: MouseEvent) => setLastX(e.clientX)
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: lastX,
        width: 8,
        height: 8,
        background: 'black',
      }}
    />
  )
}
```

**Corretto (nessun re-render per il tracking):**

```tsx
function Tracker() {
  const lastXRef = useRef(0)
  const dotRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      lastXRef.current = e.clientX
      const node = dotRef.current
      if (node) {
        node.style.transform = `translateX(${e.clientX}px)`
      }
    }
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      ref={dotRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: 8,
        height: 8,
        background: 'black',
        transform: 'translateX(0px)',
      }}
    />
  )
}
```
