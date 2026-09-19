# Riferimento degli schemi di architettura

> Consultazione rapida degli schemi più comuni, con indicazioni d'uso.

## Accesso ai dati

| Schema | Quando usarlo | Quando NON usarlo | Complessità |
| --- | --- | --- | --- |
| **Active Record** | CRUD semplice, prototipi rapidi | Query complesse, più fonti di dati | Bassa |
| **Repository** | Servono test, più fonti di dati | CRUD semplice, un solo database | Media |
| **Unit of Work** | Transazioni complesse | Operazioni semplici | Alta |
| **Data Mapper** | Dominio complesso, prestazioni | CRUD semplice, sviluppo rapido | Alta |

## Logica di dominio

| Schema | Quando usarlo | Quando NON usarlo | Complessità |
| --- | --- | --- | --- |
| **Transaction Script** | CRUD semplice, procedurale | Regole di business complesse | Bassa |
| **Table Module** | Logica basata sui record | Serve un comportamento ricco | Bassa |
| **Domain Model** | Logica di business complessa | CRUD semplice | Media |
| **DDD (completo)** | Dominio complesso, esperti di dominio | Dominio semplice, niente esperti | Alta |

## Sistemi distribuiti

| Schema | Quando usarlo | Quando NON usarlo | Complessità |
| --- | --- | --- | --- |
| **Monolite modulare** | Team piccoli, confini non chiari | Contesti chiari, scale diverse | Media |
| **Microservizi** | Scale diverse, team grandi | Team piccoli, dominio semplice | Molto alta |
| **Guidato dagli eventi** | Tempo reale, accoppiamento debole | Flussi semplici, consistenza forte | Alta |
| **CQRS** | Prestazioni di lettura e scrittura divergono | CRUD semplice, stesso modello | Alta |
| **Saga** | Transazioni distribuite | Un solo database, ACID semplice | Alta |

## API

| Schema | Quando usarlo | Quando NON usarlo | Complessità |
| --- | --- | --- | --- |
| **REST** | CRUD standard, risorse | Tempo reale, query complesse | Bassa |
| **GraphQL** | Query flessibili, più client | CRUD semplice, esigenze di cache | Media |
| **gRPC** | Servizi interni, prestazioni | API pubbliche, client nel browser | Media |
| **WebSocket** | Aggiornamenti in tempo reale | Semplice richiesta/risposta | Media |

---

## Principio di semplicità

> "Parti semplice, aggiungi complessità solo quando è dimostrato che serve."

- Gli schemi si possono sempre aggiungere dopo
- Togliere complessità è MOLTO più difficile che aggiungerla
- Nel dubbio, scegli l'opzione più semplice
