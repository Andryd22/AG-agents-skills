---
name: database-design
description: Principi di progettazione dei database e come decidere. Progettazione dello schema, strategia degli indici, scelta dell'ORM, database serverless, migrazioni e ottimizzazione delle query.
---

# Progettazione dei database

> **Impara a RAGIONARE, non a copiare schemi SQL.**

## 🎯 Regola della lettura selettiva

**Leggi SOLO i file che servono alla richiesta!** Guarda la mappa dei contenuti e trova quello che ti serve.

| File | Descrizione | Quando leggerlo |
| --- | --- | --- |
| `database-selection.md` | PostgreSQL, Neon, Turso o SQLite | Scegliere il database |
| `orm-selection.md` | Drizzle, Prisma o Kysely | Scegliere l'ORM |
| `schema-design.md` | Normalizzazione, chiavi primarie, relazioni | Progettare lo schema |
| `indexing.md` | Tipi di indice, indici composti | Ottimizzare le prestazioni |
| `optimization.md` | N+1, EXPLAIN ANALYZE | Ottimizzare le query |
| `migrations.md` | Migrazioni sicure, database serverless | Modificare lo schema |

---

## ⚠️ Principio

- CHIEDI all'utente le sue preferenze sul database quando non sono chiare
- Scegli database e ORM in base al CONTESTO
- Non usare PostgreSQL per tutto senza pensarci

---

## Checklist di decisione

Prima di progettare lo schema:

- [ ] Hai chiesto all'utente che database preferisce?
- [ ] Hai scelto il database per QUESTO contesto?
- [ ] Hai considerato l'ambiente di deploy?
- [ ] Hai pianificato gli indici?
- [ ] Hai definito i tipi di relazione?

---

## Anti-pattern

❌ PostgreSQL per app semplici senza pensarci (può bastare SQLite)
❌ Saltare gli indici
❌ SELECT * in produzione
❌ Salvare JSON quando i dati strutturati sono meglio
❌ Ignorare le query N+1

---

## Script

`python .agents/skills/database-design/scripts/schema_validator.py <cartella_progetto>` controlla gli schema Prisma (nomi, `@id`, `createdAt`, indici sulle foreign key); trova anche gli schema Drizzle, ma per ora non li analizza. I problemi che segnala sono avvisi: esce sempre con 0.
