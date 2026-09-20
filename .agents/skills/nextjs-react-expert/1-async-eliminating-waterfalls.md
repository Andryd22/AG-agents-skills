# 1. Eliminare i waterfall

> **Impatto:** CRITICO
> **Obiettivo:** I waterfall sono il nemico numero uno delle prestazioni. Ogni await sequenziale aggiunge un'intera latenza di rete. Eliminarli porta i guadagni maggiori.

---

## Panoramica

Questa sezione contiene **6 regole** per eliminare i waterfall, compresi i pattern `after()` e `connection()` di Next.js.

---

## Regola 1.1: Rimanda l'await finché non serve

**Impatto:** ALTO  
**Tag:** async, await, conditional, optimization  

## Rimanda l'await finché non serve

Sposta le operazioni `await` nei rami in cui vengono davvero usate, così non blocchi i percorsi di codice che non ne hanno bisogno.

**Sbagliato (blocca entrambi i rami):**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  const userData = await fetchUserData(userId)
  
  if (skipProcessing) {
    // Esce subito, ma ha comunque atteso userData
    return { skipped: true }
  }
  
  // Solo questo ramo usa userData
  return processUserData(userData)
}
```

**Corretto (blocca solo quando serve):**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  if (skipProcessing) {
    // Esce subito senza attendere
    return { skipped: true }
  }
  
  // Fetch solo quando serve
  const userData = await fetchUserData(userId)
  return processUserData(userData)
}
```

**Altro esempio (ottimizzazione con early return):**

```typescript
// Sbagliato: recupera sempre i permessi
async function updateResource(resourceId: string, userId: string) {
  const permissions = await fetchPermissions(userId)
  const resource = await getResource(resourceId)
  
  if (!resource) {
    return { error: 'Not found' }
  }
  
  if (!permissions.canEdit) {
    return { error: 'Forbidden' }
  }
  
  return await updateResourceData(resource, permissions)
}

// Corretto: recupera i permessi solo quando servono
async function updateResource(resourceId: string, userId: string) {
  const resource = await getResource(resourceId)
  
  if (!resource) {
    return { error: 'Not found' }
  }
  
  const permissions = await fetchPermissions(userId)
  
  if (!permissions.canEdit) {
    return { error: 'Forbidden' }
  }
  
  return await updateResourceData(resource, permissions)
}
```

Questa ottimizzazione è particolarmente utile quando il ramo che salta l'operazione viene percorso spesso, o quando l'operazione rimandata è costosa.

---

## Regola 1.2: Parallelizzazione basata sulle dipendenze

**Impatto:** CRITICO  
**Tag:** async, parallelization, dependencies, better-all  

## Parallelizzazione basata sulle dipendenze

Per operazioni con dipendenze parziali, usa `better-all` per massimizzare il parallelismo: avvia automaticamente ogni task il prima possibile.

**Sbagliato (profile attende config senza motivo):**

```typescript
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig()
])
const profile = await fetchProfile(user.id)
```

**Corretto (config e profile vanno in parallelo):**

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  }
})
```

**Alternativa senza dipendenze aggiuntive:**

Puoi anche creare prima tutte le promise e fare `Promise.all()` alla fine.

```typescript
const userPromise = fetchUser()
const profilePromise = userPromise.then(user => fetchProfile(user.id))

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(),
  profilePromise
])
```

Riferimento: [https://github.com/shuding/better-all](https://github.com/shuding/better-all)

---

## Regola 1.3: Evita catene di waterfall nelle API route

**Impatto:** CRITICO  
**Tag:** api-routes, server-actions, waterfalls, parallelization  

## Evita catene di waterfall nelle API route

Nelle API route e nelle Server Action avvia subito le operazioni indipendenti, anche se non le attendi ancora.

**Sbagliato (config attende auth, data attende entrambi):**

```typescript
export async function GET(request: Request) {
  const session = await auth()
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return Response.json({ data, config })
}
```

**Corretto (auth e config partono subito):**

```typescript
export async function GET(request: Request) {
  const sessionPromise = auth()
  const configPromise = fetchConfig()
  const session = await sessionPromise
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id)
  ])
  return Response.json({ data, config })
}
```

Per catene di dipendenze più complesse, usa `better-all` per massimizzare automaticamente il parallelismo (vedi Parallelizzazione basata sulle dipendenze).

---

## Regola 1.4: Promise.all() per le operazioni indipendenti

**Impatto:** CRITICO  
**Tag:** async, parallelization, promises, waterfalls  

## Promise.all() per le operazioni indipendenti

Quando le operazioni asincrone non dipendono l'una dall'altra, eseguile in parallelo con `Promise.all()`.

**Sbagliato (esecuzione sequenziale, 3 round trip):**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**Corretto (esecuzione parallela, 1 round trip):**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

---

## Regola 1.5: Boundary Suspense strategici

**Impatto:** ALTO  
**Tag:** async, suspense, streaming, layout-shift  

## Boundary Suspense strategici

Invece di attendere i dati nei componenti async prima di restituire il JSX, usa boundary Suspense per mostrare prima la UI contenitore mentre i dati si caricano.

**Sbagliato (contenitore bloccato dal fetch dei dati):**

```tsx
async function Page() {
  const data = await fetchData() // Blocca l'intera pagina
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <DataDisplay data={data} />
      </div>
      <div>Footer</div>
    </div>
  )
}
```

L'intero layout attende i dati anche se solo la sezione centrale ne ha bisogno.

**Corretto (il contenitore compare subito, i dati arrivano in streaming):**

```tsx
function Page() {
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <Suspense fallback={<Skeleton />}>
          <DataDisplay />
        </Suspense>
      </div>
      <div>Footer</div>
    </div>
  )
}

async function DataDisplay() {
  const data = await fetchData() // Blocca solo questo componente
  return <div>{data.content}</div>
}
```

Sidebar, Header e Footer vengono renderizzati subito. Solo DataDisplay attende i dati.

**Alternativa (condividi la promise tra componenti):**

```tsx
function Page() {
  // Avvia subito il fetch, ma senza await
  const dataPromise = fetchData()
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay dataPromise={dataPromise} />
        <DataSummary dataPromise={dataPromise} />
      </Suspense>
      <div>Footer</div>
    </div>
  )
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // Estrae il valore dalla promise
  return <div>{data.content}</div>
}

function DataSummary({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // Riusa la stessa promise
  return <div>{data.summary}</div>
}
```

Entrambi i componenti condividono la stessa promise, quindi il fetch avviene una sola volta. Il layout viene renderizzato subito mentre i due componenti attendono insieme.

**Quando NON usare questo pattern:**

- Dati critici per le decisioni di layout (influenzano il posizionamento)
- Contenuti above the fold importanti per la SEO
- Query piccole e veloci, per cui l'overhead di Suspense non vale la pena
- Quando vuoi evitare il layout shift (salto da caricamento a contenuto)

**Compromesso:** first paint più rapido contro possibile layout shift. Scegli in base alle priorità della tua UX.

---

## Regola 1.6: Usa `after()` e `connection()` (Next.js 15+)

**Impatto:** ALTO  
**Tag:** nextjs16, async, runtime, performance

Next.js (dalla versione 15) offre API per non bloccare la risposta con lavoro secondario e per dichiarare esplicitamente il rendering dinamico.

### 1. `after()` per la logica non bloccante

Non usare `await` per la logica che non influisce sulla UI iniziale (logging, analytics, email): spostala in `after()`.

```tsx
import { after } from 'next/server'

export default async function Page() {
  const data = await fetchData() // CRITICO
  
  after(() => {
    // ESEGUITO DOPO L'INVIO DELLA RISPOSTA
    logTrack(data) 
  })

  return <View data={data} />
}
```

### 2. `connection()` per l'intento dinamico

Usa `connection()` per segnalare che un componente è dinamico e non va prerenderizzato come statico: avvolto in un boundary `<Suspense>`, lascia che le altre parti della pagina vadano in streaming in modo indipendente.

```tsx
import { connection } from 'next/server'

async function DynamicData() {
  await connection() // Segnala l'intento dinamico
  return await fetchFreshData()
}
```
