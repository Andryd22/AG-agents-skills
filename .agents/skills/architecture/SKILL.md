---
name: architecture
description: Metodo per prendere decisioni di architettura. Analisi dei requisiti, valutazione dei compromessi, documentazione con ADR. Usala quando prendi decisioni di architettura o analizzi la progettazione di un sistema.
---

# Metodo per le decisioni di architettura

> "I requisiti guidano l'architettura. I compromessi guidano le decisioni. Gli ADR ne conservano le ragioni."

## 🎯 Regola della lettura selettiva

**Leggi SOLO i file che servono alla richiesta!** Guarda la mappa dei contenuti e trova quello che ti serve.

| File | Descrizione | Quando leggerlo |
| --- | --- | --- |
| `context-discovery.md` | Domande da fare, classificazione del progetto | All'inizio della progettazione |
| `trade-off-analysis.md` | Modelli di ADR, metodo per i compromessi | Documentare le decisioni |
| `pattern-selection.md` | Alberi di decisione, anti-pattern | Scegliere gli schemi |
| `examples.md` | Esempi MVP, SaaS, enterprise | Implementazioni di riferimento |
| `patterns-reference.md` | Consultazione rapida degli schemi | Confrontare gli schemi |

---

## 🔗 Skill collegate

| Skill | Per cosa |
| --- | --- |
| `@[skills/database-design]` | Progettazione dello schema del database |
| `@[skills/api-patterns]` | Schemi di progettazione delle API |

---

## Principio

> "La semplicità è la massima raffinatezza."

- Parti semplice
- Aggiungi complessità SOLO quando è dimostrato che serve
- Gli schemi si possono sempre aggiungere dopo
- Togliere complessità è MOLTO più difficile che aggiungerla

---

## Checklist di validazione

Prima di chiudere l'architettura:

- [ ] Requisiti capiti con chiarezza
- [ ] Vincoli individuati
- [ ] Ogni decisione ha l'analisi dei compromessi
- [ ] Alternative più semplici considerate
- [ ] ADR scritti per le decisioni importanti
- [ ] Le competenze del team sono adatte agli schemi scelti
