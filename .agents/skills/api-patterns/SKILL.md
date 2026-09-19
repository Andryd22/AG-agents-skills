---
name: api-patterns
description: Principi di progettazione delle API e come decidere. Scelta tra REST, GraphQL e tRPC, formato delle risposte, versioning, paginazione, autenticazione, rate limiting e test di sicurezza.
---

# Schemi per le API

> Principi di progettazione delle API e come decidere.
> **Impara a RAGIONARE, non a copiare schemi fissi.**

## 🎯 Regola della lettura selettiva

**Leggi SOLO i file che servono alla richiesta!** Guarda la mappa dei contenuti e trova quello che ti serve.

---

## 📑 Mappa dei contenuti

| File | Descrizione | Quando leggerlo |
| --- | --- | --- |
| `api-style.md` | Albero di decisione REST, GraphQL o tRPC | Scegliere il tipo di API |
| `rest.md` | Nomi delle risorse, metodi HTTP, codici di stato | Progettare un'API REST |
| `response.md` | Envelope, formato degli errori, paginazione | Struttura delle risposte |
| `graphql.md` | Progettare lo schema, quando usarlo, sicurezza | Se valuti GraphQL |
| `trpc.md` | Monorepo TypeScript, tipi garantiti | Progetti fullstack in TS |
| `versioning.md` | Versioning nell'URI, nell'header o nella query | Pianificare l'evoluzione dell'API |
| `auth.md` | JWT, OAuth, passkey, API key | Scegliere l'autenticazione |
| `rate-limiting.md` | Token bucket, finestra scorrevole | Proteggere l'API |
| `documentation.md` | Buone pratiche di OpenAPI/Swagger | Documentazione |
| `security-testing.md` | OWASP API Top 10, test di autenticazione e autorizzazione | Audit di sicurezza |

---

## 🔗 Skill collegate

| Serve | Skill |
| --- | --- |
| Implementare l'API | `@[skills/nodejs-best-practices]`, `@[skills/python-patterns]` |
| Struttura dei dati | `@[skills/database-design]` |
| Dettagli di sicurezza | `security-testing.md` in questa skill |

---

## ✅ Checklist di decisione

Prima di progettare un'API:

- [ ] **Hai chiesto all'utente chi userà l'API?**
- [ ] **Hai scelto lo stile di API per QUESTO contesto?** (REST/GraphQL/tRPC)
- [ ] **Hai definito un formato di risposta coerente?**
- [ ] **Hai pianificato il versioning?**
- [ ] **Hai considerato le esigenze di autenticazione?**
- [ ] **Hai previsto il rate limiting?**
- [ ] **Hai deciso come documentarla?**

---

## ❌ Anti-pattern

**NON:**

- Usare REST per tutto senza pensarci
- Mettere verbi negli endpoint REST (/getUsers)
- Restituire risposte in formati diversi
- Mostrare ai client gli errori interni
- Saltare il rate limiting

**SÌ:**

- Scegliere lo stile di API in base al contesto
- Chiedere quali sono le esigenze dei client
- Documentare a fondo
- Usare i codici di stato giusti

---

## Script

| Script | Scopo | Comando |
| --- | --- | --- |
| `scripts/api_validator.py` | Controlla gli endpoint e le specifiche OpenAPI | `python .agents/skills/api-patterns/scripts/api_validator.py <cartella_progetto>` |
