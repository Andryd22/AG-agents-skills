---
name: nextjs-react-expert
description: Ottimizzazione delle prestazioni di React e Next.js secondo Vercel Engineering. Usala quando crei componenti React, ottimizzi le prestazioni, elimini i waterfall, riduci la dimensione del bundle, revisioni il codice per problemi di prestazioni o implementi ottimizzazioni lato server e lato client.
---

# Esperto di prestazioni Next.js e React

> **Da Vercel Engineering**: 58 regole di ottimizzazione ordinate per impatto
> **Filosofia:** prima elimina i waterfall, poi ottimizza i bundle, infine passa alle micro-ottimizzazioni.

---

## 🎯 Regola della lettura selettiva (OBBLIGATORIA)

**Leggi SOLO le sezioni utili al tuo compito!** Guarda la mappa dei contenuti qui sotto e carica quello che ti serve.

> 🔴 **Per le revisioni delle prestazioni: parti dalle sezioni CRITICHE (1-2), poi passa a quelle ALTE e MEDIE.**

---

## 📑 Mappa dei contenuti

| File | Impatto | Regole | Quando leggerlo |
| --- | --- | --- | --- |
| `1-async-eliminating-waterfalls.md` | 🔴 **CRITICO** | 6 regole | Pagine lente da caricare, chiamate API in sequenza, waterfall nel recupero dei dati |
| `2-bundle-bundle-size-optimization.md` | 🔴 **CRITICO** | 5 regole | Bundle grande, Time to Interactive lento, problemi al primo caricamento |
| `3-server-server-side-performance.md` | 🟠 **ALTO** | 7 regole | SSR lento, ottimizzazione delle API route, waterfall lato server |
| `4-client-client-side-data-fetching.md` | 🟡 **MEDIO-ALTO** | 4 regole | Gestione dei dati sul client, pattern SWR, deduplicazione |
| `5-rerender-re-render-optimization.md` | 🟡 **MEDIO** | 12 regole | Troppi re-render, prestazioni di React, memoizzazione |
| `6-rendering-rendering-performance.md` | 🟡 **MEDIO** | 9 regole | Colli di bottiglia nel rendering, liste lunghe, SVG, hydration |
| `7-js-javascript-performance.md` | ⚪ **MEDIO-BASSO** | 12 regole | Micro-ottimizzazioni, cache, prestazioni dei loop, layout thrashing |
| `8-advanced-advanced-patterns.md` | 🔵 **VARIABILE** | 3 regole | Pattern React avanzati, `useEffectEvent`, inizializzazione una tantum |
| `9-cache-components.md` | 🔴 **CRITICO** | 4 sezioni | **Solo Next.js 16+**: `use cache`, `cacheLife`, PPR, `cacheTag` |

**Totale:** 58 regole in 8 categorie, più la guida alle Cache Components

> ℹ️ I file di sezione 1-8 sono una traduzione italiana delle regole react-best-practices di Vercel. Se rilanci `scripts/convert_rules.py` li rigeneri in inglese: dopo vanno tradotti di nuovo.

---

## 🚀 Albero decisionale rapido

**Qual è il tuo problema di prestazioni?**

```text
🐌 Pagine lente da caricare / Time to Interactive lungo
  → Leggi la sezione 1: Eliminare i waterfall
  → Leggi la sezione 2: Ottimizzare la dimensione del bundle

📦 Bundle grande (> 200KB)
  → Leggi la sezione 2: Ottimizzare la dimensione del bundle
  → Controlla: import dinamici, import dai barrel file, tree-shaking

🖥️ Server-Side Rendering lento
  → Leggi la sezione 3: Prestazioni lato server
  → Controlla: fetch dei dati in parallelo, streaming

🔄 Troppi re-render / UI che rallenta
  → Leggi la sezione 5: Ottimizzare i re-render
  → Controlla: React.memo, useMemo, useCallback

🎨 Problemi di prestazioni nel rendering
  → Leggi la sezione 6: Prestazioni del rendering
  → Controlla: content-visibility per le liste lunghe, layout thrashing (sezione 7)

🌐 Problemi nel recupero dei dati lato client
  → Leggi la sezione 4: Recupero dei dati lato client
  → Controlla: deduplicazione con SWR, localStorage

✨ Ti servono pattern avanzati
  → Leggi la sezione 8: Pattern avanzati

🚀 **Prestazioni in Next.js 16+ (caching e PPR)**
  → Leggi la sezione 9: Cache Components: `use cache` e `cacheLife`
```

---

## 📊 Guida alle priorità per impatto

**Segui questo ordine quando fai un'ottimizzazione completa:**

```text
1️⃣ CRITICO (guadagni maggiori, da fare per primo):
   ├─ Sezione 1: Eliminare i waterfall
   │  └─ Ogni waterfall aggiunge un'intera latenza di rete (100-500ms+)
   └─ Sezione 2: Ottimizzare la dimensione del bundle
      └─ Incide su Time to Interactive e Largest Contentful Paint

2️⃣ ALTO (impatto significativo, da fare per secondo):
   └─ Sezione 3: Prestazioni lato server
      └─ Elimina i waterfall lato server, tempi di risposta più rapidi

3️⃣ MEDIO (guadagni moderati, da fare per terzo):
   ├─ Sezione 4: Recupero dei dati lato client
   ├─ Sezione 5: Ottimizzare i re-render
   └─ Sezione 6: Prestazioni del rendering

4️⃣ BASSO (rifinitura, da fare per ultimo):
   ├─ Sezione 7: Prestazioni di JavaScript
   └─ Sezione 8: Pattern avanzati

🔥 **MODERNO (Next.js 16+):**
   └─ Sezione 9: Cache Components: `use cache` e `cacheLife`
      (sostituisce gran parte della revalidation tradizionale)
```

---

## 🔗 Skill collegate

| Serve | Skill |
| --- | --- |
| Pattern di progettazione delle API | `@[skills/api-patterns]` |
| Ottimizzazione del database | `@[skills/database-design]` |
| Strategie di test | `@[skills/test]` |
| Principi di design UI/UX | `@[skills/frontend-design]` |

---

## ✅ Checklist per la revisione delle prestazioni

Prima di andare in produzione:

**Critico (da correggere per forza):**

- [ ] Nessun recupero dei dati in sequenza (waterfall eliminati)
- [ ] Bundle principale < 200KB
- [ ] Nessun import dai barrel file nel codice dell'app
- [ ] Import dinamici per i componenti grandi
- [ ] Recupero dei dati in parallelo dove possibile

**Priorità alta:**

- [ ] Server Component usati dove ha senso
- [ ] API route ottimizzate (niente query N+1)
- [ ] Boundary Suspense per il recupero dei dati
- [ ] Generazione statica usata dove possibile

**Priorità media:**

- [ ] Calcoli costosi memoizzati
- [ ] Liste lunghe virtualizzate (oltre i 100 elementi)
- [ ] Immagini ottimizzate con next/image
- [ ] Nessun re-render superfluo

**Priorità bassa (rifinitura):**

- [ ] Loop negli hot path ottimizzati
- [ ] RegExp spostate fuori dal render
- [ ] Accessi alle proprietà messi in cache nei loop

---

## ❌ Anti-pattern (errori comuni)

**NON:**

- ❌ Usare `await` in sequenza per operazioni indipendenti
- ❌ Importare intere librerie quando ti serve una sola funzione
- ❌ Usare i barrel export (re-export da `index.ts`) nel codice dell'app
- ❌ Rinunciare agli import dinamici per componenti o librerie grandi
- ❌ Recuperare i dati in useEffect senza deduplicazione
- ❌ Dimenticare di memoizzare i calcoli costosi
- ❌ Usare Client Component quando basta un Server Component

**SÌ:**

- ✅ Recuperare i dati in parallelo con `Promise.all()`
- ✅ Usare gli import dinamici: `const Comp = dynamic(() => import('./Heavy'))`
- ✅ Importare direttamente: `import { specific } from 'library/specific'`
- ✅ Usare i boundary Suspense per una UX migliore
- ✅ Sfruttare i React Server Components
- ✅ Misurare le prestazioni prima di ottimizzare
- ✅ Usare le ottimizzazioni integrate di Next.js (next/image, next/font)

---

## 🎯 Come usare questa skill

### Per le nuove funzionalità

1. Consulta le **sezioni 1 e 2** mentre sviluppi (previeni i waterfall, tieni piccolo il bundle)
2. Usa i Server Component come default (sezione 3)
3. Applica la memoizzazione alle operazioni costose (sezione 5)

### Per le revisioni delle prestazioni

1. Parti dalla **sezione 1** (waterfall = impatto maggiore)
2. Poi la **sezione 2** (dimensione del bundle)
3. Poi la **sezione 3** (lato server)
4. Infine le altre sezioni, se servono

### Per il debug delle prestazioni lente

1. Individua il sintomo (caricamento lento, lag, ecc.)
2. Usa l'albero decisionale rapido qui sopra
3. Leggi la sezione pertinente
4. Applica le correzioni in ordine di priorità

---

## 📚 Percorso di apprendimento

**Principiante (concentrati sulle criticità):**
→ Sezione 1: Eliminare i waterfall
→ Sezione 2: Ottimizzare la dimensione del bundle

**Intermedio (aggiungi la priorità alta):**
→ Sezione 3: Prestazioni lato server
→ Sezione 5: Ottimizzare i re-render

**Avanzato (ottimizzazione completa):**
→ Tutte le sezioni + sezione 8: Pattern avanzati

---

## 🔍 Script di verifica

| Script | Scopo | Comando |
| --- | --- | --- |
| `scripts/react_performance_checker.py` | Audit automatico: waterfall (critici, uscita 1), barrel file, fetch in useEffect, memo, `next/image` | `python .agents/skills/nextjs-react-expert/scripts/react_performance_checker.py <cartella>` |

---

## 📖 Dettagli delle sezioni

### Sezione 1: Eliminare i waterfall (CRITICO)

**Impatto:** Ogni waterfall aggiunge 100-500ms+ di latenza
**Concetti chiave:** Fetch in parallelo, Promise.all(), boundary Suspense, precaricamento, `after()` e `connection()`

### Sezione 2: Ottimizzare la dimensione del bundle (CRITICO)

**Impatto:** Incide direttamente su Time to Interactive e Largest Contentful Paint
**Concetti chiave:** Import dinamici, tree-shaking, niente import dai barrel file

### Sezione 3: Prestazioni lato server (ALTO)

**Impatto:** Risposte del server più rapide, SEO migliore
**Concetti chiave:** Fetch in parallelo sul server, streaming, ottimizzazione delle API route

### Sezione 4: Recupero dei dati lato client (MEDIO-ALTO)

**Impatto:** Meno richieste ridondanti, UX migliore
**Concetti chiave:** Deduplicazione con SWR, cache in localStorage, event listener

### Sezione 5: Ottimizzare i re-render (MEDIO)

**Impatto:** UI più fluida, meno calcoli sprecati
**Concetti chiave:** React.memo, useMemo, useCallback, struttura dei componenti

### Sezione 6: Prestazioni del rendering (MEDIO)

**Impatto:** Rendering più efficiente
**Concetti chiave:** content-visibility per le liste lunghe, SVG, hydration mismatch, Activity, useTransition

### Sezione 7: Prestazioni di JavaScript (MEDIO-BASSO)

**Impatto:** Miglioramenti incrementali negli hot path
**Concetti chiave:** Ottimizzazione dei loop, cache, RegExp fuori dal render, layout thrashing

### Sezione 8: Pattern avanzati (VARIABILE)

**Impatto:** Casi d'uso specifici
**Concetti chiave:** `useEffectEvent`, inizializzazione una tantum, event handler nei ref

---

## 🎓 Riepilogo delle buone pratiche

**Regole d'oro:**

1. **Prima misura**: usa React DevTools Profiler e Chrome DevTools
2. **Prima l'impatto maggiore**: waterfall → bundle → server → micro
3. **Non ottimizzare troppo**: concentrati sui colli di bottiglia reali
4. **Sfrutta la piattaforma**: Next.js ha ottimizzazioni integrate
5. **Pensa agli utenti**: contano le condizioni d'uso reali

**Mentalità orientata alle prestazioni:**

- Ogni `await` in sequenza = potenziale waterfall
- Ogni `import` = potenziale bundle gonfio
- Ogni re-render = calcolo sprecato (se non serve)
- Server Component = meno JavaScript da inviare al client
- Misura, non tirare a indovinare

---

**Fonte:** Vercel Engineering
**Data:** gennaio 2026
**Versione:** 1.0.0
**Regole totali:** 58 in 8 categorie
