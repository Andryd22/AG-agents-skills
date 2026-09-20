# 8. Pattern avanzati

> **Impatto:** VARIABILE
> **Obiettivo:** Pattern avanzati per casi specifici che richiedono un'implementazione attenta.

---

## Panoramica

Questa sezione contiene **3 regole** dedicate ai pattern avanzati.

---

## Regola 8.1: Inizializza l'app una volta sola, non a ogni mount

**Impatto:** MEDIO-BASSO  
**Tag:** initialization, useEffect, app-startup, side-effects  

## Inizializza l'app una volta sola, non a ogni mount

Non mettere nello `useEffect([])` di un componente un'inizializzazione globale che deve girare una sola volta per caricamento dell'app. I componenti possono essere rimontati e gli effect vengono rieseguiti. Usa invece una guardia a livello di modulo o un'inizializzazione top-level nel modulo di ingresso.

**Sbagliato (in dev gira due volte, si riesegue a ogni remount):**

```tsx
function Comp() {
  useEffect(() => {
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

**Corretto (una volta per caricamento dell'app):**

```tsx
let didInit = false

function Comp() {
  useEffect(() => {
    if (didInit) return
    didInit = true
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

Riferimento: [Initializing the application](https://react.dev/learn/you-might-not-need-an-effect#initializing-the-application)

---

## Regola 8.2: Salva gli event handler nei ref

**Impatto:** BASSO  
**Tag:** advanced, hooks, refs, event-handlers, optimization  

## Salva gli event handler nei ref

Salva le callback nei ref quando le usi in effect che non devono ripetere la sottoscrizione ogni volta che la callback cambia.

**Sbagliato (ripete la sottoscrizione a ogni render):**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}
```

**Corretto (sottoscrizione stabile):**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  const handlerRef = useRef(handler)
  useEffect(() => {
    handlerRef.current = handler
  }, [handler])

  useEffect(() => {
    const listener = (e) => handlerRef.current(e)
    window.addEventListener(event, listener)
    return () => window.removeEventListener(event, listener)
  }, [event])
}
```

**Alternativa: usa `useEffectEvent` se sei su React 19.2 o successivo:**

```tsx
import { useEffectEvent } from 'react'

function useWindowEvent(event: string, handler: (e) => void) {
  const onEvent = useEffectEvent(handler)

  useEffect(() => {
    window.addEventListener(event, onEvent)
    return () => window.removeEventListener(event, onEvent)
  }, [event])
}
```

`useEffectEvent` offre un'API più pulita per lo stesso pattern: crea un riferimento stabile a una funzione che chiama sempre la versione più recente dell'handler.

---

## Regola 8.3: useEffectEvent per riferimenti stabili alle callback

**Impatto:** BASSO  
**Tag:** advanced, hooks, useEffectEvent, refs, optimization  

## useEffectEvent per riferimenti stabili alle callback

Accedi ai valori più recenti nelle callback senza aggiungerli agli array di dipendenze. Eviti che gli effect si rieseguano senza cadere in closure obsolete (stale closure).

**Sbagliato (l'effect si riesegue a ogni cambio della callback):**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')

  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300)
    return () => clearTimeout(timeout)
  }, [query, onSearch])
}
```

**Corretto (con useEffectEvent di React):**

```tsx
import { useEffectEvent } from 'react';

function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')
  const onSearchEvent = useEffectEvent(onSearch)

  useEffect(() => {
    const timeout = setTimeout(() => onSearchEvent(query), 300)
    return () => clearTimeout(timeout)
  }, [query])
}
```
