# Scegliere lo stile dell'API

> REST, GraphQL o tRPC: quale usare e quando?

## Albero di decisione

```text
Chi usa l'API?
│
├── API pubblica / più piattaforme
│   └── REST + OpenAPI (la compatibilità più ampia)
│
├── Dati complessi / più frontend
│   └── GraphQL (query flessibili)
│
├── Frontend + backend in TypeScript (monorepo)
│   └── tRPC (tipi garantiti da un capo all'altro)
│
├── Tempo reale / guidata dagli eventi
│   └── WebSocket + AsyncAPI
│
└── Microservizi interni
    └── gRPC (prestazioni) o REST (semplicità)
```

## Confronto

| Fattore | REST | GraphQL | tRPC |
| --- | --- | --- | --- |
| **Ideale per** | API pubbliche | App complesse | Monorepo TS |
| **Curva di apprendimento** | Bassa | Media | Bassa (se usi TS) |
| **Dati in eccesso o in difetto** | Frequenti | Risolto | Risolto |
| **Tipi garantiti** | A mano (OpenAPI) | Dallo schema | Automatici |
| **Cache** | Nativa di HTTP | Complessa | Lato client |

## Domande per scegliere

1. Chi usa l'API?
2. Il frontend è in TypeScript?
3. Quanto sono complesse le relazioni tra i dati?
4. La cache è critica?
5. API pubblica o interna?
