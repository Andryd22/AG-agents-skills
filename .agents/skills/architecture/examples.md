# Esempi di architettura

> Decisioni di architettura reali, per tipo di progetto.

---

## Esempio 1: e-commerce MVP (sviluppatore singolo)

```yaml
Requisiti:
  - <1000 utenti all'inizio
  - Uno sviluppatore
  - Sul mercato in fretta (8 settimane)
  - Budget ridotto

Decisioni di architettura:
  Struttura dell'app: monolite (più semplice per una persona)
  Framework: Next.js (full-stack, veloce)
  Accesso ai dati: Prisma diretto (niente astrazioni in eccesso)
  Autenticazione: JWT (più semplice di OAuth)
  Pagamenti: Stripe (soluzione ospitata)
  Database: PostgreSQL (ACID per gli ordini)

Compromessi accettati:
  - Monolite → le parti non scalano separatamente (il team non lo giustifica)
  - Niente Repository → meno testabile (il CRUD semplice non ne ha bisogno)
  - JWT → niente login social all'inizio (si aggiunge dopo)

Evoluzione prevista:
  - Utenti > 10K → estrarre il servizio dei pagamenti
  - Team > 3 → aggiungere il pattern Repository
  - Richiesto il login social → aggiungere OAuth
```

---

## Esempio 2: prodotto SaaS (5-10 sviluppatori)

```yaml
Requisiti:
  - 1K-100K utenti
  - 5-10 sviluppatori
  - Lungo termine (12+ mesi)
  - Più domini (fatturazione, utenti, nucleo)

Decisioni di architettura:
  Struttura dell'app: monolite modulare (ottimale per questo team)
  Framework: NestJS (modulare per costruzione)
  Accesso ai dati: pattern Repository (test, flessibilità)
  Modello di dominio: DDD parziale (entità ricche)
  Autenticazione: OAuth + JWT
  Cache: Redis
  Database: PostgreSQL

Compromessi accettati:
  - Monolite modulare → un po' di accoppiamento tra moduli (i microservizi non sono giustificati)
  - DDD parziale → niente aggregati completi (mancano esperti di dominio)
  - RabbitMQ più avanti → all'inizio tutto sincrono (si aggiunge quando serve davvero)

Evoluzione prevista:
  - Team > 10 → valutare i microservizi
  - Domini in conflitto → estrarre i bounded context
  - Problemi di prestazioni in lettura → aggiungere CQRS
```

---

## Esempio 3: enterprise (100K+ utenti)

```yaml
Requisiti:
  - 100K+ utenti
  - 10+ sviluppatori
  - Più domini di business
  - Esigenze di scala diverse
  - Disponibilità 24/7

Decisioni di architettura:
  Struttura dell'app: microservizi (scala indipendente)
  API gateway: Kong/AWS API Gateway
  Modello di dominio: DDD completo
  Consistenza: guidata dagli eventi (eventual consistency accettabile)
  Bus di messaggi: Kafka
  Autenticazione: OAuth + SAML (SSO aziendale)
  Database: poliglotta (lo strumento giusto per ogni lavoro)
  CQRS: solo in alcuni servizi

Requisiti operativi:
  - Service mesh (Istio/Linkerd)
  - Tracing distribuito (Jaeger/Tempo)
  - Log centralizzati (ELK/Loki)
  - Circuit breaker (Resilience4j)
  - Kubernetes/Helm
```
