# 2. Ottimizzare la dimensione del bundle

> **Impatto:** CRITICO
> **Obiettivo:** Ridurre la dimensione del bundle iniziale migliora il Time to Interactive e il Largest Contentful Paint.

---

## Panoramica

Questa sezione contiene **5 regole** per ottimizzare la dimensione del bundle.

---

## Regola 2.1: Evita gli import dai barrel file

**Impatto:** CRITICO  
**Tag:** bundle, imports, tree-shaking, barrel-files, performance  

## Evita gli import dai barrel file

Importa direttamente dai file sorgente invece che dai barrel file, per non caricare migliaia di moduli inutilizzati. I **barrel file** sono entry point che riesportano più moduli (ad es. un `index.js` che fa `export * from './module'`).

Le librerie di icone e componenti più diffuse possono avere **fino a 10.000 riesportazioni** nel loro file di ingresso. Per molti pacchetti React **servono 200-800 ms solo per importarli**, con effetti sia sulla velocità in sviluppo sia sui cold start in produzione.

**Perché il tree-shaking non aiuta:** quando una libreria è marcata come external (non inclusa nel bundle), il bundler non può ottimizzarla. Se la includi nel bundle per abilitare il tree-shaking, le build diventano molto più lente perché analizzano l'intero grafo dei moduli.

**Sbagliato (importa l'intera libreria):**

```tsx
import { Check, X, Menu } from 'lucide-react'
// Carica 1.583 moduli, ~2,8 s in più in sviluppo
// Costo a runtime: 200-800 ms a ogni cold start

import { Button, TextField } from '@mui/material'
// Carica 2.225 moduli, ~4,2 s in più in sviluppo
```

**Corretto (importa solo ciò che serve):**

```tsx
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'
import Menu from 'lucide-react/dist/esm/icons/menu'
// Carica solo 3 moduli (~2 KB invece di ~1 MB)

import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
// Carica solo ciò che usi
```

**Alternativa (Next.js 13.5+):**

```js
// next.config.js - usa optimizePackageImports
module.exports = {
  experimental: {
    optimizePackageImports: ['lucide-react', '@mui/material']
  }
}

// Poi puoi mantenere i comodi import dal barrel file:
import { Check, X, Menu } from 'lucide-react'
// Trasformati automaticamente in import diretti in fase di build
```

Gli import diretti rendono l'avvio in sviluppo più veloce del 15-70%, le build del 28%, i cold start del 40% e l'HMR sensibilmente più rapido.

Librerie spesso coinvolte: `lucide-react`, `@mui/material`, `@mui/icons-material`, `@tabler/icons-react`, `react-icons`, `@headlessui/react`, `@radix-ui/react-*`, `lodash`, `ramda`, `date-fns`, `rxjs`, `react-use`.

Riferimento: [How we optimized package imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)

---

## Regola 2.2: Caricamento condizionale dei moduli

**Impatto:** ALTO  
**Tag:** bundle, conditional-loading, lazy-loading  

## Caricamento condizionale dei moduli

Carica dati o moduli pesanti solo quando una funzionalità viene attivata.

**Esempio (lazy loading dei frame di un'animazione):**

```tsx
function AnimationPlayer({ enabled, setEnabled }: { enabled: boolean; setEnabled: React.Dispatch<React.SetStateAction<boolean>> }) {
  const [frames, setFrames] = useState<Frame[] | null>(null)

  useEffect(() => {
    if (enabled && !frames && typeof window !== 'undefined') {
      import('./animation-frames.js')
        .then(mod => setFrames(mod.frames))
        .catch(() => setEnabled(false))
    }
  }, [enabled, frames, setEnabled])

  if (!frames) return <Skeleton />
  return <Canvas frames={frames} />
}
```

Il controllo `typeof window !== 'undefined'` evita che questo modulo finisca nel bundle per l'SSR, riducendo il bundle del server e velocizzando la build.

---

## Regola 2.3: Rimanda le librerie di terze parti non critiche

**Impatto:** MEDIO  
**Tag:** bundle, third-party, analytics, defer  

## Rimanda le librerie di terze parti non critiche

Analytics, logging ed error tracking non bloccano l'interazione dell'utente. Caricali dopo l'idratazione.

**Sbagliato (blocca il bundle iniziale):**

```tsx
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

**Corretto (si carica dopo l'idratazione):**

```tsx
import dynamic from 'next/dynamic'

const Analytics = dynamic(
  () => import('@vercel/analytics/react').then(m => m.Analytics),
  { ssr: false }
)

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

**Nota:** nell'App Router `ssr: false` non è ammesso nei Server Component (come il root layout di default): metti la chiamata a `dynamic()` in un Client Component (file con `'use client'`) e importa quello nel layout.

---

## Regola 2.4: Import dinamici per i componenti pesanti

**Impatto:** CRITICO  
**Tag:** bundle, dynamic-import, code-splitting, next-dynamic  

## Import dinamici per i componenti pesanti

Usa `next/dynamic` per il lazy loading dei componenti pesanti che non servono al primo render.

**Sbagliato (Monaco finisce nel chunk principale, ~300 KB):**

```tsx
import { MonacoEditor } from './monaco-editor'

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

**Corretto (Monaco si carica su richiesta):**

```tsx
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(
  () => import('./monaco-editor').then(m => m.MonacoEditor),
  { ssr: false }
)

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

---

## Regola 2.5: Precarica in base all'intenzione dell'utente

**Impatto:** MEDIO  
**Tag:** bundle, preload, user-intent, hover  

## Precarica in base all'intenzione dell'utente

Precarica i bundle pesanti prima che servano, per ridurre la latenza percepita.

**Esempio (precaricamento su hover/focus):**

```tsx
function EditorButton({ onClick }: { onClick: () => void }) {
  const preload = () => {
    if (typeof window !== 'undefined') {
      void import('./monaco-editor')
    }
  }

  return (
    <button
      onMouseEnter={preload}
      onFocus={preload}
      onClick={onClick}
    >
      Open Editor
    </button>
  )
}
```

**Esempio (precaricamento quando un feature flag è attivo):**

```tsx
function FlagsProvider({ children, flags }: Props) {
  useEffect(() => {
    if (flags.editorEnabled && typeof window !== 'undefined') {
      void import('./monaco-editor').then(mod => mod.init())
    }
  }, [flags.editorEnabled])

  return <FlagsContext.Provider value={flags}>
    {children}
  </FlagsContext.Provider>
}
```

Il controllo `typeof window !== 'undefined'` evita che i moduli precaricati finiscano nel bundle per l'SSR, riducendo il bundle del server e velocizzando la build.
