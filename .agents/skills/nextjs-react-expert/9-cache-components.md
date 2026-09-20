# Cache Components: `use cache` e `cacheLife`

> [!IMPORTANT]
> Questa skill è specifica di Next.js 16+. NON applicare questi pattern a Next.js 15 o precedenti senza aver verificato esplicitamente la compatibilità.

## Filosofia di fondo

Next.js 16 segna il passaggio dal "caching a livello di segmento" al "caching a livello di componente". Non affidarti più a `export const revalidate = 3600`: usa direttive e profili granulari.

## 1. La direttiva `use cache`

La direttiva `use cache` si applica a **Server Component** o a **funzioni**.

### Regola: applicazione granulare

Avvolgi solo la logica di recupero dei dati o il singolo componente che ha bisogno della cache.

```tsx
// Corretto: cache granulare a livello di funzione
async function getProduct(id: string) {
  'use cache'
  return await db.product.findUnique({ where: { id } })
}

// Corretto: cache a livello di componente
export default async function ProductCard({ id }: { id: string }) {
  'use cache'
  const product = await getProduct(id)
  return <div>{product.name}</div>
}
```

## 2. Usare `cacheLife`

`cacheLife` definisce per quanto un elemento in cache resta "fresco" e quando diventa "stale", con profili predefiniti o personalizzati.

### Pattern d'uso

```tsx
import { cacheLife } from 'next/cache'

async function getStockInfo() {
  'use cache'
  cacheLife('minutes') // Usa un profilo predefinito
  return await fetchStocks()
}
```

### Profili disponibili

- `default`: profilo di base (stale 5 minuti, revalidate 15 minuti, expire 1 anno).
- `seconds`: aggiornamenti ad alta frequenza.
- `minutes`: contenuti dinamici standard.
- `hours`: contenuti stabili (es. articoli del blog).
- `days`: contenuti semistatici.
- `weeks`: contenuti quasi statici.
- `max`: cache di durata massima, finché non la invalidi.

## 3. Invalidazione on-demand con `cacheTag`

`cacheTag` ti permette di etichettare i dati in cache per svuotarli in modo selettivo.

### Implementazione

```tsx
import { cacheTag } from 'next/cache'

async function getProfile(user: string) {
  'use cache'
  cacheTag(`profile-${user}`)
  return await db.user.findUnique(...)
}
```

### Revalidation

In una Server Action:

```tsx
import { revalidateTag, updateTag } from 'next/cache'

export async function updateProfile(user: string, data: any) {
  await db.user.update(...)
  
  // Scelta A: revalidation in background (stale-while-revalidate); da Next.js 16 serve un profilo cacheLife come secondo argomento
  revalidateTag(`profile-${user}`, 'max')
  
  // Scelta B: aggiornamento immediato "read-your-writes"
  updateTag(`profile-${user}`)
}
```

## 4. Partial Pre-Rendering (PPR)

Next.js 16 stabilizza il PPR tramite il flag `cacheComponents` in `next.config.ts`.

### Pattern: boundary Suspense

Avvolgi sempre in `<Suspense>` i componenti dinamici (quelli che leggono dati della richiesta o non in cache) per abilitare il PPR.

```tsx
import { Suspense } from 'react'
import { Skeleton } from '@/components/ui/skeleton'

export default function Page() {
  return (
    <main>
      <h1>Static Header</h1>
      <Suspense fallback={<Skeleton />}>
        <DynamicCacheComponent />
      </Suspense>
    </main>
  )
}
```
