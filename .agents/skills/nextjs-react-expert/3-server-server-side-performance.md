# 3. Prestazioni lato server

> **Impatto:** ALTO
> **Obiettivo:** Ottimizzare il rendering lato server e il recupero dei dati elimina i waterfall lato server e riduce i tempi di risposta.

---

## Panoramica

Questa sezione contiene **7 regole** per migliorare le prestazioni lato server.

---

## Regola 3.1: Autentica le Server Action come le API route

**Impatto:** CRITICO  
**Tag:** server, server-actions, authentication, security, authorization  

## Autentica le Server Action come le API route

**Impatto:** CRITICO (impedisce accessi non autorizzati alle mutation lato server)

Le Server Action (funzioni con `"use server"`) sono esposte come endpoint pubblici, proprio come le API route. Verifica sempre autenticazione e autorizzazione **dentro** ogni Server Action: non affidarti solo al middleware (`proxy.ts` da Next.js 16), alle protezioni nei layout o ai controlli a livello di pagina, perché le Server Action possono essere invocate direttamente.

La documentazione di Next.js lo dice esplicitamente: "Treat Server Actions with the same security considerations as public-facing API endpoints, and verify if the user is allowed to perform a mutation."

**Sbagliato (nessun controllo di autenticazione):**

```typescript
'use server'

export async function deleteUser(userId: string) {
  // Chiunque può chiamarla! Nessun controllo di autenticazione
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**Corretto (autenticazione dentro la action):**

```typescript
'use server'

import { verifySession } from '@/lib/auth'
import { unauthorized } from '@/lib/errors'

export async function deleteUser(userId: string) {
  // Controlla sempre l'autenticazione dentro la action
  const session = await verifySession()
  
  if (!session) {
    throw unauthorized('Must be logged in')
  }
  
  // Controlla anche l'autorizzazione
  if (session.user.role !== 'admin' && session.user.id !== userId) {
    throw unauthorized('Cannot delete other users')
  }
  
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**Con validazione dell'input:**

```typescript
'use server'

import { verifySession } from '@/lib/auth'
import { z } from 'zod'

const updateProfileSchema = z.object({
  userId: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email()
})

export async function updateProfile(data: unknown) {
  // Prima valida l'input
  const validated = updateProfileSchema.parse(data)
  
  // Poi autentica
  const session = await verifySession()
  if (!session) {
    throw new Error('Unauthorized')
  }
  
  // Poi autorizza
  if (session.user.id !== validated.userId) {
    throw new Error('Can only update own profile')
  }
  
  // Infine esegui la mutation
  await db.user.update({
    where: { id: validated.userId },
    data: {
      name: validated.name,
      email: validated.email
    }
  })
  
  return { success: true }
}
```

Riferimento: [https://nextjs.org/docs/app/guides/authentication](https://nextjs.org/docs/app/guides/authentication)

---

## Regola 3.2: Evita la serializzazione duplicata nelle prop RSC

**Impatto:** BASSO  
**Tag:** server, rsc, serialization, props, client-components  

## Evita la serializzazione duplicata nelle prop RSC

**Impatto:** BASSO (riduce il payload di rete evitando la serializzazione duplicata)

La serializzazione RSC→client deduplica per riferimento dell'oggetto, non per valore. Stesso riferimento = serializzato una volta; nuovo riferimento = serializzato di nuovo. Fai le trasformazioni (`.toSorted()`, `.filter()`, `.map()`) sul client, non sul server.

**Sbagliato (duplica l'array):**

```tsx
// RSC: invia 6 stringhe (2 array × 3 elementi)
<ClientList usernames={usernames} usernamesOrdered={usernames.toSorted()} />
```

**Corretto (invia 3 stringhe):**

```tsx
// RSC: invia una sola volta
<ClientList usernames={usernames} />

// Client: trasforma qui
'use client'
const sorted = useMemo(() => [...usernames].sort(), [usernames])
```

**Deduplicazione dei dati annidati:**

La deduplicazione funziona in modo ricorsivo. L'impatto varia in base al tipo di dato:

- `string[]`, `number[]`, `boolean[]`: **impatto ALTO**: l'array e tutti i valori primitivi vengono duplicati per intero
- `object[]`: **impatto BASSO**: l'array viene duplicato, ma gli oggetti annidati sono deduplicati per riferimento

```tsx
// string[] - duplica tutto
usernames={['a','b']} sorted={usernames.toSorted()} // invia 4 stringhe

// object[] - duplica solo la struttura dell'array
users={[{id:1},{id:2}]} sorted={users.toSorted()} // invia 2 array + 2 oggetti unici (non 4)
```

**Operazioni che rompono la deduplicazione (creano nuovi riferimenti):**

- Array: `.toSorted()`, `.filter()`, `.map()`, `.slice()`, `[...arr]`
- Oggetti: `{...obj}`, `Object.assign()`, `structuredClone()`, `JSON.parse(JSON.stringify())`

**Altri esempi:**

```tsx
// ❌ Sbagliato
<C users={users} active={users.filter(u => u.active)} />
<C product={product} productName={product.name} />

// ✅ Corretto
<C users={users} />
<C product={product} />
// Filtra/destruttura sul client
```

**Eccezione:** passa dati derivati quando la trasformazione è costosa o il client non ha bisogno dell'originale.

---

## Regola 3.3: Cache LRU tra richieste

**Impatto:** ALTO  
**Tag:** server, cache, lru, cross-request  

## Cache LRU tra richieste

`React.cache()` funziona solo all'interno di una singola richiesta. Per i dati condivisi tra richieste successive (l'utente clicca il pulsante A e poi il pulsante B), usa una cache LRU.

**Implementazione:**

```typescript
import { LRUCache } from 'lru-cache'

const cache = new LRUCache<string, any>({
  max: 1000,
  ttl: 5 * 60 * 1000  // 5 minuti
})

export async function getUser(id: string) {
  const cached = cache.get(id)
  if (cached) return cached

  const user = await db.user.findUnique({ where: { id } })
  cache.set(id, user)
  return user
}

// Richiesta 1: query al DB, risultato in cache
// Richiesta 2: cache hit, nessuna query al DB
```

Usala quando azioni successive dell'utente chiamano più endpoint che, nel giro di pochi secondi, hanno bisogno degli stessi dati.

**Con [Fluid Compute](https://vercel.com/docs/fluid-compute) di Vercel:** la cache LRU è particolarmente efficace, perché più richieste concorrenti possono condividere la stessa istanza della funzione e la stessa cache. La cache quindi persiste tra le richieste senza bisogno di uno storage esterno come Redis.

**Nel serverless tradizionale:** ogni invocazione gira isolata, quindi valuta Redis per una cache condivisa tra processi.

Riferimento: [https://github.com/isaacs/node-lru-cache](https://github.com/isaacs/node-lru-cache)

---

## Regola 3.4: Riduci al minimo la serializzazione ai confini RSC

**Impatto:** ALTO  
**Tag:** server, rsc, serialization, props  

## Riduci al minimo la serializzazione ai confini RSC

Il confine tra Server e Client di React serializza tutte le proprietà degli oggetti in stringhe e le incorpora nella risposta HTML e nelle successive richieste RSC. Questi dati serializzati pesano direttamente sulla dimensione della pagina e sui tempi di caricamento, quindi **la dimensione conta molto**. Passa solo i campi che il client usa davvero.

**Sbagliato (serializza tutti i 50 campi):**

```tsx
async function Page() {
  const user = await fetchUser()  // 50 campi
  return <Profile user={user} />
}

'use client'
function Profile({ user }: { user: User }) {
  return <div>{user.name}</div>  // usa 1 campo
}
```

**Corretto (serializza un solo campo):**

```tsx
async function Page() {
  const user = await fetchUser()
  return <Profile name={user.name} />
}

'use client'
function Profile({ name }: { name: string }) {
  return <div>{name}</div>
}
```

---

## Regola 3.5: Fetch dei dati in parallelo con la composizione dei componenti

**Impatto:** CRITICO  
**Tag:** server, rsc, parallel-fetching, composition  

## Fetch dei dati in parallelo con la composizione dei componenti

I React Server Component vengono eseguiti in sequenza all'interno di un albero. Ristruttura con la composizione per parallelizzare il fetch dei dati.

**Sbagliato (Sidebar attende la fine del fetch di Page):**

```tsx
export default async function Page() {
  const header = await fetchHeader()
  return (
    <div>
      <div>{header}</div>
      <Sidebar />
    </div>
  )
}

async function Sidebar() {
  const items = await fetchSidebarItems()
  return <nav>{items.map(renderItem)}</nav>
}
```

**Corretto (i due fetch partono insieme):**

```tsx
async function Header() {
  const data = await fetchHeader()
  return <div>{data}</div>
}

async function Sidebar() {
  const items = await fetchSidebarItems()
  return <nav>{items.map(renderItem)}</nav>
}

export default function Page() {
  return (
    <div>
      <Header />
      <Sidebar />
    </div>
  )
}
```

**Alternativa con la prop children:**

```tsx
async function Header() {
  const data = await fetchHeader()
  return <div>{data}</div>
}

async function Sidebar() {
  const items = await fetchSidebarItems()
  return <nav>{items.map(renderItem)}</nav>
}

function Layout({ children }: { children: ReactNode }) {
  return (
    <div>
      <Header />
      {children}
    </div>
  )
}

export default function Page() {
  return (
    <Layout>
      <Sidebar />
    </Layout>
  )
}
```

---

## Regola 3.6: Deduplicazione per richiesta con React.cache()

**Impatto:** MEDIO  
**Tag:** server, cache, react-cache, deduplication  

## Deduplicazione per richiesta con React.cache()

Usa `React.cache()` per la deduplicazione delle richieste lato server. Ne traggono il maggior beneficio l'autenticazione e le query al database.

**Uso:**

```typescript
import { cache } from 'react'

export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({
    where: { id: session.user.id }
  })
})
```

All'interno di una singola richiesta, più chiamate a `getCurrentUser()` eseguono la query una sola volta.

**Evita oggetti inline come argomenti:**

`React.cache()` usa l'uguaglianza superficiale (`Object.is`) per decidere se c'è un cache hit. Gli oggetti inline creano un nuovo riferimento a ogni chiamata e impediscono i cache hit.

**Sbagliato (sempre cache miss):**

```typescript
const getUser = cache(async (params: { uid: number }) => {
  return await db.user.findUnique({ where: { id: params.uid } })
})

// Ogni chiamata crea un nuovo oggetto, nessun cache hit
getUser({ uid: 1 })
getUser({ uid: 1 })  // Cache miss, riesegue la query
```

**Corretto (cache hit):**

```typescript
const getUser = cache(async (uid: number) => {
  return await db.user.findUnique({ where: { id: uid } })
})

// Gli argomenti primitivi sono confrontati per valore
getUser(1)
getUser(1)  // Cache hit, restituisce il risultato in cache
```

Se devi per forza passare oggetti, passa lo stesso riferimento:

```typescript
const params = { uid: 1 }
getUser(params)  // Esegue la query
getUser(params)  // Cache hit (stesso riferimento)
```

**Nota specifica per Next.js:**

In Next.js l'API `fetch` è estesa automaticamente con la request memoization. Le richieste con stesso URL e stesse opzioni vengono deduplicate automaticamente all'interno di una singola richiesta, quindi per le chiamate `fetch` non serve `React.cache()`. `React.cache()` resta però essenziale per gli altri task asincroni:

- Query al database (Prisma, Drizzle, ecc.)
- Calcoli pesanti
- Controlli di autenticazione
- Operazioni sul file system
- Qualsiasi lavoro asincrono diverso da fetch

Usa `React.cache()` per deduplicare queste operazioni in tutto l'albero dei componenti.

Riferimento: [React.cache documentation](https://react.dev/reference/react/cache)

---

## Regola 3.7: Usa after() per le operazioni non bloccanti

**Impatto:** MEDIO  
**Tag:** server, async, logging, analytics, side-effects  

## Usa after() per le operazioni non bloccanti

Usa `after()` di Next.js per pianificare il lavoro da eseguire dopo l'invio della risposta. Così logging, analytics e altri side effect non bloccano la risposta.

**Sbagliato (blocca la risposta):**

```tsx
import { logUserAction } from '@/app/utils'

export async function POST(request: Request) {
  // Esegue la mutation
  await updateDatabase(request)
  
  // Il logging blocca la risposta
  const userAgent = request.headers.get('user-agent') || 'unknown'
  await logUserAction({ userAgent })
  
  return new Response(JSON.stringify({ status: 'success' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  })
}
```

**Corretto (non bloccante):**

```tsx
import { after } from 'next/server'
import { headers, cookies } from 'next/headers'
import { logUserAction } from '@/app/utils'

export async function POST(request: Request) {
  // Esegue la mutation
  await updateDatabase(request)
  
  // Log dopo l'invio della risposta
  after(async () => {
    const userAgent = (await headers()).get('user-agent') || 'unknown'
    const sessionCookie = (await cookies()).get('session-id')?.value || 'anonymous'
    
    logUserAction({ sessionCookie, userAgent })
  })
  
  return new Response(JSON.stringify({ status: 'success' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  })
}
```

La risposta parte subito, mentre il logging avviene in background.

**Casi d'uso comuni:**

- Tracciamento analytics
- Audit log
- Invio di notifiche
- Invalidazione della cache
- Operazioni di pulizia

**Note importanti:**

- `after()` viene eseguito anche se la risposta fallisce o fa un redirect
- Funziona in Server Action, Route Handler e Server Component

Riferimento: [https://nextjs.org/docs/app/api-reference/functions/after](https://nextjs.org/docs/app/api-reference/functions/after)
