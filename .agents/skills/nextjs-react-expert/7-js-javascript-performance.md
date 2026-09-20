# 7. Prestazioni di JavaScript

> **Impatto:** MEDIO-BASSO
> **Obiettivo:** Le micro-ottimizzazioni negli hot path, sommate, possono portare a miglioramenti significativi.

---

## Panoramica

Questa sezione contiene **12 regole** dedicate alle prestazioni di JavaScript.

---

## Regola 7.1: Evita il layout thrashing

**Impatto:** MEDIO  
**Tag:** javascript, dom, css, performance, reflow, layout-thrashing  

## Evita il layout thrashing

Non alternare scritture di stile e letture di layout. Se leggi una proprietà di layout (come `offsetWidth`, `getBoundingClientRect()` o `getComputedStyle()`) tra una modifica di stile e l'altra, costringi il browser a un reflow sincrono.

**Questo va bene (il browser raggruppa le modifiche di stile):**

```typescript
function updateElementStyles(element: HTMLElement) {
  // Ogni riga invalida lo stile, ma il browser raggruppa il ricalcolo
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
}
```

**Sbagliato (letture e scritture alternate forzano i reflow):**

```typescript
function layoutThrashing(element: HTMLElement) {
  element.style.width = '100px'
  const width = element.offsetWidth  // Forza un reflow
  element.style.height = '200px'
  const height = element.offsetHeight  // Forza un altro reflow
}
```

**Corretto (prima tutte le scritture, poi una sola lettura):**

```typescript
function updateElementStyles(element: HTMLElement) {
  // Raggruppa tutte le scritture
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
  
  // Leggi dopo aver finito di scrivere (un solo reflow)
  const { width, height } = element.getBoundingClientRect()
}
```

**Corretto (prima tutte le letture, poi le scritture):**

```typescript
function avoidThrashing(element: HTMLElement) {
  // Fase di lettura: prima tutte le query di layout
  const rect1 = element.getBoundingClientRect()
  const offsetWidth = element.offsetWidth
  const offsetHeight = element.offsetHeight
  
  // Fase di scrittura: poi tutte le modifiche di stile
  element.style.width = '100px'
  element.style.height = '200px'
}
```

**Meglio ancora:** usa le classi CSS

```css
.highlighted-box {
  width: 100px;
  height: 200px;
  background-color: blue;
  border: 1px solid black;
}
```

```typescript
function updateElementStyles(element: HTMLElement) {
  element.classList.add('highlighted-box')
  
  const { width, height } = element.getBoundingClientRect()
}
```

**Esempio React:**

```tsx
// Sbagliato: alterna modifiche di stile e query di layout
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  const ref = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (ref.current && isHighlighted) {
      ref.current.style.width = '100px'
      const width = ref.current.offsetWidth // Forza il layout
      ref.current.style.height = '200px'
    }
  }, [isHighlighted])
  
  return <div ref={ref}>Content</div>
}

// Corretto: attiva/disattiva una classe
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  return (
    <div className={isHighlighted ? 'highlighted-box' : ''}>
      Content
    </div>
  )
}
```

Quando puoi, preferisci le classi CSS agli stili inline: i file CSS finiscono nella cache del browser e le classi separano meglio le responsabilità e sono più facili da mantenere.

Per approfondire le operazioni che forzano il layout, vedi [questo gist](https://gist.github.com/paulirish/5d52fb081b3570c81e3a) e [CSS Triggers](https://csstriggers.com/).

---

## Regola 7.2: Costruisci mappe indice per i lookup ripetuti

**Impatto:** MEDIO-BASSO  
**Tag:** javascript, map, indexing, optimization, performance  

## Costruisci mappe indice per i lookup ripetuti

Se fai più chiamate a `.find()` sulla stessa chiave, usa una Map.

**Sbagliato (O(n) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map(order => ({
    ...order,
    user: users.find(u => u.id === order.userId)
  }))
}
```

**Corretto (O(1) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map(u => [u.id, u]))

  return orders.map(order => ({
    ...order,
    user: userById.get(order.userId)
  }))
}
```

Costruisci la mappa una volta sola (O(n)), poi ogni lookup è O(1).
Con 1000 ordini × 1000 utenti: da 1M di operazioni a 2K.

---

## Regola 7.3: Metti in cache l'accesso alle proprietà nei loop

**Impatto:** MEDIO-BASSO  
**Tag:** javascript, loops, optimization, caching  

## Metti in cache l'accesso alle proprietà nei loop

Negli hot path salva in cache i lookup delle proprietà degli oggetti.

**Sbagliato (3 lookup × N iterazioni):**

```typescript
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value)
}
```

**Corretto (1 lookup in tutto):**

```typescript
const value = obj.config.settings.value
const len = arr.length
for (let i = 0; i < len; i++) {
  process(value)
}
```

---

## Regola 7.4: Metti in cache le chiamate di funzione ripetute

**Impatto:** MEDIO  
**Tag:** javascript, cache, memoization, performance  

## Metti in cache le chiamate di funzione ripetute

Usa una Map a livello di modulo per mettere in cache i risultati quando durante il render chiami più volte la stessa funzione con gli stessi input.

**Sbagliato (calcoli ridondanti):**

```typescript
function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // slugify() chiamata 100+ volte per gli stessi nomi di progetto
        const slug = slugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**Corretto (risultati in cache):**

```typescript
// Cache a livello di modulo
const slugifyCache = new Map<string, string>()

function cachedSlugify(text: string): string {
  if (slugifyCache.has(text)) {
    return slugifyCache.get(text)!
  }
  const result = slugify(text)
  slugifyCache.set(text, result)
  return result
}

function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // Calcolato una sola volta per ogni nome di progetto distinto
        const slug = cachedSlugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**Pattern più semplice per le funzioni che restituiscono un solo valore:**

```typescript
let isLoggedInCache: boolean | null = null

function isLoggedIn(): boolean {
  if (isLoggedInCache !== null) {
    return isLoggedInCache
  }
  
  isLoggedInCache = document.cookie.includes('auth=')
  return isLoggedInCache
}

// Svuota la cache quando cambia l'autenticazione
function onAuthChange() {
  isLoggedInCache = null
}
```

Usa una Map (non un hook), così funziona ovunque: nelle utility e negli event handler, non solo nei componenti React.

Riferimento: [How we made the Vercel Dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)

---

## Regola 7.5: Metti in cache le chiamate alle Storage API

**Impatto:** MEDIO-BASSO  
**Tag:** javascript, localStorage, storage, caching, performance  

## Metti in cache le chiamate alle Storage API

`localStorage`, `sessionStorage` e `document.cookie` sono sincroni e costosi. Tieni in memoria i valori letti.

**Sbagliato (legge lo storage a ogni chiamata):**

```typescript
function getTheme() {
  return localStorage.getItem('theme') ?? 'light'
}
// Chiamata 10 volte = 10 letture dello storage
```

**Corretto (cache con una Map):**

```typescript
const storageCache = new Map<string, string | null>()

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key))
  }
  return storageCache.get(key)
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value)
  storageCache.set(key, value)  // mantiene la cache allineata
}
```

Usa una Map (non un hook), così funziona ovunque: nelle utility e negli event handler, non solo nei componenti React.

**Cache dei cookie:**

```typescript
let cookieCache: Record<string, string> | null = null

function getCookie(name: string) {
  if (!cookieCache) {
    cookieCache = Object.fromEntries(
      document.cookie.split('; ').map(c => c.split('='))
    )
  }
  return cookieCache[name]
}
```

**Importante (invalida la cache sui cambi esterni):**

Se lo storage può cambiare dall'esterno (un'altra scheda, cookie impostati dal server), invalida la cache:

```typescript
window.addEventListener('storage', (e) => {
  if (e.key) storageCache.delete(e.key)
})

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    storageCache.clear()
  }
})
```

---

## Regola 7.6: Unisci più iterazioni sullo stesso array

**Impatto:** MEDIO-BASSO  
**Tag:** javascript, arrays, loops, performance  

## Unisci più iterazioni sullo stesso array

Più chiamate a `.filter()` o `.map()` scorrono l'array più volte. Uniscile in un solo loop.

**Sbagliato (3 iterazioni):**

```typescript
const admins = users.filter(u => u.isAdmin)
const testers = users.filter(u => u.isTester)
const inactive = users.filter(u => !u.isActive)
```

**Corretto (1 iterazione):**

```typescript
const admins: User[] = []
const testers: User[] = []
const inactive: User[] = []

for (const user of users) {
  if (user.isAdmin) admins.push(user)
  if (user.isTester) testers.push(user)
  if (!user.isActive) inactive.push(user)
}
```

---

## Regola 7.7: Controlla subito la lunghezza quando confronti array

**Impatto:** MEDIO-ALTO  
**Tag:** javascript, arrays, performance, optimization, comparison  

## Controlla subito la lunghezza quando confronti array

Quando confronti array con operazioni costose (ordinamento, uguaglianza profonda, serializzazione), controlla prima la lunghezza: se è diversa, gli array non possono essere uguali.

Nelle applicazioni reali questa ottimizzazione conta soprattutto quando il confronto gira in un hot path (event handler, loop di render).

**Sbagliato (esegue sempre il confronto costoso):**

```typescript
function hasChanges(current: string[], original: string[]) {
  // Ordina e unisce sempre, anche quando le lunghezze sono diverse
  return current.sort().join() !== original.sort().join()
}
```

Vengono eseguiti due ordinamenti O(n log n) anche quando `current.length` vale 5 e `original.length` vale 100. In più c'è il costo di unire gli array e confrontare le stringhe.

**Corretto (prima il controllo O(1) sulla lunghezza):**

```typescript
function hasChanges(current: string[], original: string[]) {
  // Early return se le lunghezze sono diverse
  if (current.length !== original.length) {
    return true
  }
  // Ordina solo quando le lunghezze coincidono
  const currentSorted = current.toSorted()
  const originalSorted = original.toSorted()
  for (let i = 0; i < currentSorted.length; i++) {
    if (currentSorted[i] !== originalSorted[i]) {
      return true
    }
  }
  return false
}
```

Questo approccio è più efficiente perché:

- evita di ordinare e unire gli array quando le lunghezze sono diverse
- non consuma memoria per le stringhe unite (importante soprattutto con array grandi)
- non modifica gli array originali
- esce appena trova una differenza

---

## Regola 7.8: Usa l'early return nelle funzioni

**Impatto:** MEDIO-BASSO  
**Tag:** javascript, functions, optimization, early-return  

## Usa l'early return nelle funzioni

Esci dalla funzione appena il risultato è noto, così salti le elaborazioni inutili.

**Sbagliato (elabora tutti gli elementi anche dopo aver trovato la risposta):**

```typescript
function validateUsers(users: User[]) {
  let hasError = false
  let errorMessage = ''
  
  for (const user of users) {
    if (!user.email) {
      hasError = true
      errorMessage = 'Email required'
    }
    if (!user.name) {
      hasError = true
      errorMessage = 'Name required'
    }
    // Continua a controllare tutti gli utenti anche dopo aver trovato un errore
  }
  
  return hasError ? { valid: false, error: errorMessage } : { valid: true }
}
```

**Corretto (esce subito al primo errore):**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) {
      return { valid: false, error: 'Email required' }
    }
    if (!user.name) {
      return { valid: false, error: 'Name required' }
    }
  }

  return { valid: true }
}
```

---

## Regola 7.9: Sposta fuori dal render la creazione delle RegExp

**Impatto:** MEDIO-BASSO  
**Tag:** javascript, regexp, optimization, memoization  

## Sposta fuori dal render la creazione delle RegExp

Non creare RegExp dentro il render. Spostale a livello di modulo o memoizzale con `useMemo()`.

**Sbagliato (una nuova RegExp a ogni render):**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${query})`, 'gi')
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**Corretto (memoizza o sposta fuori):**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Highlighter({ text, query }: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, 'gi'),
    [query]
  )
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**Attenzione (le regex globali hanno uno stato mutabile):**

Una regex globale (`/g`) ha uno stato mutabile, `lastIndex`:

```typescript
const regex = /foo/g
regex.test('foo')  // true, lastIndex = 3
regex.test('foo')  // false, lastIndex = 0
```

---

## Regola 7.10: Usa un loop invece di sort per trovare min/max

**Impatto:** BASSO  
**Tag:** javascript, arrays, performance, sorting, algorithms  

## Usa un loop invece di sort per trovare min/max

Per trovare l'elemento più piccolo o più grande basta una sola passata sull'array. Ordinarlo è uno spreco ed è più lento.

**Sbagliato (O(n log n): ordina per trovare il più recente):**

```typescript
interface Project {
  id: string
  name: string
  updatedAt: number
}

function getLatestProject(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => b.updatedAt - a.updatedAt)
  return sorted[0]
}
```

Ordina l'intero array solo per trovare il valore massimo.

**Sbagliato (O(n log n): ordina per trovare il più vecchio e il più recente):**

```typescript
function getOldestAndNewest(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => a.updatedAt - b.updatedAt)
  return { oldest: sorted[0], newest: sorted[sorted.length - 1] }
}
```

Ordina comunque senza motivo, anche se servono solo il minimo e il massimo.

**Corretto (O(n): un solo loop):**

```typescript
function getLatestProject(projects: Project[]) {
  if (projects.length === 0) return null
  
  let latest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt > latest.updatedAt) {
      latest = projects[i]
    }
  }
  
  return latest
}

function getOldestAndNewest(projects: Project[]) {
  if (projects.length === 0) return { oldest: null, newest: null }
  
  let oldest = projects[0]
  let newest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt < oldest.updatedAt) oldest = projects[i]
    if (projects[i].updatedAt > newest.updatedAt) newest = projects[i]
  }
  
  return { oldest, newest }
}
```

Una sola passata sull'array, senza copie e senza ordinamenti.

**Alternativa (Math.min/Math.max per array piccoli):**

```typescript
const numbers = [5, 2, 8, 1, 9]
const min = Math.min(...numbers)
const max = Math.max(...numbers)
```

Funziona con gli array piccoli, ma con array molto grandi può essere più lento o addirittura generare un errore, per i limiti dello spread operator. La lunghezza massima è di circa 124000 elementi in Chrome 143 e 638000 in Safari 18; i valori esatti possono variare, vedi [questo fiddle](https://jsfiddle.net/qw1jabsx/4/). Per andare sul sicuro usa il loop.

---

## Regola 7.11: Usa Set/Map per lookup O(1)

**Impatto:** MEDIO-BASSO  
**Tag:** javascript, set, map, data-structures, performance  

## Usa Set/Map per lookup O(1)

Converti gli array in Set/Map quando devi verificare più volte se contengono un elemento.

**Sbagliato (O(n) per controllo):**

```typescript
const allowedIds = ['a', 'b', 'c', ...]
items.filter(item => allowedIds.includes(item.id))
```

**Corretto (O(1) per controllo):**

```typescript
const allowedIds = new Set(['a', 'b', 'c', ...])
items.filter(item => allowedIds.has(item.id))
```

---

## Regola 7.12: Usa toSorted() invece di sort() per l'immutabilità

**Impatto:** MEDIO-ALTO  
**Tag:** javascript, arrays, immutability, react, state, mutation  

## Usa toSorted() invece di sort() per l'immutabilità

`.sort()` modifica l'array sul posto e può causare bug con state e prop di React. Usa `.toSorted()` per creare un nuovo array ordinato senza mutazioni.

**Sbagliato (modifica l'array originale):**

```typescript
function UserList({ users }: { users: User[] }) {
  // Modifica l'array della prop users!
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**Corretto (crea un nuovo array):**

```typescript
function UserList({ users }: { users: User[] }) {
  // Crea un nuovo array ordinato, l'originale resta invariato
  const sorted = useMemo(
    () => users.toSorted((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**Perché conta in React:**

1. Mutare prop e state viola il modello di immutabilità di React: React si aspetta che prop e state vengano trattati in sola lettura
2. Causa bug di stale closure: mutare gli array dentro le closure (callback, effect) può portare a comportamenti inattesi

**Supporto dei browser (fallback per i browser più vecchi):**

`.toSorted()` è disponibile in tutti i browser moderni (Chrome 110+, Safari 16+, Firefox 115+, Node.js 20+). Negli ambienti più vecchi usa lo spread operator:

```typescript
// Fallback per i browser più vecchi
const sorted = [...items].sort((a, b) => a.value - b.value)
```

**Altri metodi immutabili degli array:**

- `.toSorted()`: ordinamento immutabile
- `.toReversed()`: inversione immutabile
- `.toSpliced()`: splice immutabile
- `.with()`: sostituzione immutabile di un elemento
