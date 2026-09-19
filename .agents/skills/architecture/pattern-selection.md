# Come scegliere gli schemi di architettura

> Alberi di decisione per scegliere gli schemi di architettura.

## Albero di decisione principale

```text
INIZIO: qual è la tua preoccupazione PRINCIPALE?

┌─ Complessità dell'accesso ai dati?
│  ├─ ALTA (query complesse, servono test)
│  │  → pattern Repository + Unit of Work
│  │  VERIFICA: la fonte dei dati cambierà spesso?
│  │     ├─ SÌ → il Repository vale l'indirezione
│  │     └─ NO → valuta l'accesso diretto con l'ORM, più semplice
│  └─ BASSA (CRUD semplice, un solo database)
│     → ORM diretto (Prisma, Drizzle)
│     Più semplice = meglio, più veloce
│
├─ Complessità delle regole di business?
│  ├─ ALTA (logica di dominio, regole che cambiano col contesto)
│  │  → Domain-Driven Design
│  │  VERIFICA: nel team ci sono esperti di dominio?
│  │     ├─ SÌ → DDD completo (aggregati, value object)
│  │     └─ NO → DDD parziale (entità ricche, confini chiari)
│  └─ BASSA (quasi solo CRUD, validazioni semplici)
│     → pattern Transaction Script
│     Più semplice = meglio, più veloce
│
├─ Serve scalare le parti separatamente?
│  ├─ SÌ (i componenti scalano in modo diverso)
│  │  → i microservizi VALGONO la complessità
│  │  REQUISITI (devono valere TUTTI):
│  │    - Confini di dominio chiari
│  │    - Team > 10 sviluppatori
│  │    - Esigenze di scala diverse per servizio
│  │  SE NON VALGONO TUTTI → meglio un monolite modulare
│  └─ NO (tutto scala insieme)
│     → monolite modulare
│     I servizi si estraggono dopo, quando serve davvero
│
└─ Requisiti di tempo reale?
   ├─ ALTI (aggiornamenti immediati, sincronizzazione tra utenti)
   │  → architettura guidata dagli eventi
   │  → coda di messaggi (RabbitMQ, Redis, Kafka)
   │  VERIFICA: puoi gestire l'eventual consistency?
   │     ├─ SÌ → gli eventi vanno bene
   │     └─ NO → sincrono con polling
   └─ BASSI (l'eventual consistency è accettabile)
      → sincrono (REST/GraphQL)
      Più semplice = meglio, più veloce
```

## Le 3 domande (prima di QUALSIASI schema)

1. **Problema risolto**: quale problema PRECISO risolve questo schema?
2. **Alternativa più semplice**: c'è una soluzione più semplice?
3. **Complessità rimandata**: si può aggiungere DOPO, quando servirà?

## Campanelli d'allarme (anti-pattern)

| Schema | Anti-pattern | Alternativa più semplice |
| --- | --- | --- |
| Microservizi | Divisione prematura | Parti monolite, estrai dopo |
| Clean/esagonale | Troppa astrazione | Prima il concreto, le interfacce dopo |
| Event sourcing | Sovraingegnerizzazione | Log di audit solo in aggiunta |
| CQRS | Complessità inutile | Un solo modello |
| Repository | YAGNI per il CRUD semplice | Accesso diretto con l'ORM |
