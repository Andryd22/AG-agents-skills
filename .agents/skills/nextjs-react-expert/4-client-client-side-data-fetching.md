# 4. Recupero dei dati lato client

> **Impatto:** MEDIO-ALTO
> **Obiettivo:** La deduplicazione automatica e pattern di fetch efficienti riducono le richieste di rete ridondanti.

---

## Panoramica

Questa sezione contiene **4 regole** dedicate al recupero dei dati lato client.

---

## Regola 4.1: Deduplica gli event listener globali

**Impatto:** BASSO  
**Tag:** client, swr, event-listeners, subscription  

## Deduplica gli event listener globali

Usa `useSWRSubscription()` per condividere gli event listener globali tra le istanze di un componente.

**Sbagliato (N istanze = N listener):**

```tsx
function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === key) {
        callback()
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [key, callback])
}
```

Se usi l'hook `useKeyboardShortcut` più volte, ogni istanza registra un nuovo listener.

**Corretto (N istanze = 1 listener):**

```tsx
import useSWRSubscription from 'swr/subscription'

// Map a livello di modulo per tracciare le callback per ogni tasto
const keyCallbacks = new Map<string, Set<() => void>>()

function useKeyboardShortcut(key: string, callback: () => void) {
  // Registra questa callback nella Map
  useEffect(() => {
    if (!keyCallbacks.has(key)) {
      keyCallbacks.set(key, new Set())
    }
    keyCallbacks.get(key)!.add(callback)

    return () => {
      const set = keyCallbacks.get(key)
      if (set) {
        set.delete(callback)
        if (set.size === 0) {
          keyCallbacks.delete(key)
        }
      }
    }
  }, [key, callback])

  useSWRSubscription('global-keydown', () => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && keyCallbacks.has(e.key)) {
        keyCallbacks.get(e.key)!.forEach(cb => cb())
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  })
}

function Profile() {
  // Più scorciatoie condivideranno lo stesso listener
  useKeyboardShortcut('p', () => { /* ... */ }) 
  useKeyboardShortcut('k', () => { /* ... */ })
  // ...
}
```

---

## Regola 4.2: Usa passive listener per le prestazioni dello scroll

**Impatto:** MEDIO  
**Tag:** client, event-listeners, scrolling, performance, touch, wheel  

## Usa passive listener per le prestazioni dello scroll

Aggiungi `{ passive: true }` agli event listener di touch e wheel per uno scroll immediato. Di norma il browser attende che i listener terminino per verificare se viene chiamato `preventDefault()`, e questo ritarda lo scroll.

**Sbagliato:**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  
  document.addEventListener('touchstart', handleTouch)
  document.addEventListener('wheel', handleWheel)
  
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**Corretto:**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  
  document.addEventListener('touchstart', handleTouch, { passive: true })
  document.addEventListener('wheel', handleWheel, { passive: true })
  
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**Usa passive per:** tracking/analytics, logging e qualsiasi listener che non chiama `preventDefault()`.

**Non usare passive per:** gesture di swipe personalizzate, controlli di zoom personalizzati o qualsiasi listener che deve chiamare `preventDefault()`.

---

## Regola 4.3: Usa SWR per la deduplicazione automatica

**Impatto:** MEDIO-ALTO  
**Tag:** client, swr, deduplication, data-fetching  

## Usa SWR per la deduplicazione automatica

SWR offre deduplicazione delle richieste, cache e revalidation condivise tra le istanze dei componenti.

**Sbagliato (nessuna deduplicazione, ogni istanza fa il proprio fetch):**

```tsx
function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => {
    fetch('/api/users')
      .then(r => r.json())
      .then(setUsers)
  }, [])
}
```

**Corretto (più istanze condividono un'unica richiesta):**

```tsx
import useSWR from 'swr'

function UserList() {
  const { data: users } = useSWR('/api/users', fetcher)
}
```

**Per dati immutabili:**

```tsx
import { useImmutableSWR } from '@/lib/swr'

function StaticContent() {
  const { data } = useImmutableSWR('/api/config', fetcher)
}
```

**Per le mutation:**

```tsx
import useSWRMutation from 'swr/mutation'

function UpdateButton() {
  const { trigger } = useSWRMutation('/api/user', updateUser)
  return <button onClick={() => trigger()}>Update</button>
}
```

Riferimento: [https://swr.vercel.app](https://swr.vercel.app)

---

## Regola 4.4: Versiona e riduci al minimo i dati in localStorage

**Impatto:** MEDIO  
**Tag:** client, localStorage, storage, versioning, data-minimization  

## Versiona e riduci al minimo i dati in localStorage

Aggiungi un prefisso di versione alle chiavi e salva solo i campi necessari. Eviti conflitti di schema e il salvataggio accidentale di dati sensibili.

**Sbagliato:**

```typescript
// Nessuna versione, salva tutto, nessuna gestione degli errori
localStorage.setItem('userConfig', JSON.stringify(fullUserObject))
const data = localStorage.getItem('userConfig')
```

**Corretto:**

```typescript
const VERSION = 'v2'

function saveConfig(config: { theme: string; language: string }) {
  try {
    localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify(config))
  } catch {
    // Lancia un'eccezione in navigazione anonima/privata, a quota superata o se disabilitato
  }
}

function loadConfig() {
  try {
    const data = localStorage.getItem(`userConfig:${VERSION}`)
    return data ? JSON.parse(data) : null
  } catch {
    return null
  }
}

// Migrazione da v1 a v2
function migrate() {
  try {
    const v1 = localStorage.getItem('userConfig:v1')
    if (v1) {
      const old = JSON.parse(v1)
      saveConfig({ theme: old.darkMode ? 'dark' : 'light', language: old.lang })
      localStorage.removeItem('userConfig:v1')
    }
  } catch {}
}
```

**Salva solo i campi minimi dalle risposte del server:**

```typescript
// L'oggetto utente ha più di 20 campi: salva solo ciò che serve alla UI
function cachePrefs(user: FullUser) {
  try {
    localStorage.setItem('prefs:v1', JSON.stringify({
      theme: user.preferences.theme,
      notifications: user.preferences.notifications
    }))
  } catch {}
}
```

**Racchiudi sempre in un try-catch:** `getItem()` e `setItem()` lanciano un'eccezione in navigazione anonima/privata (Safari, Firefox), quando la quota è superata o quando lo storage è disabilitato.

**Vantaggi:** evoluzione dello schema tramite il versioning, meno spazio occupato, nessun token, dato personale (PII) o flag interno salvato per errore.
