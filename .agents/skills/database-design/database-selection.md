# Scegliere il database

> Scegli il database in base al contesto, non per abitudine.

## Albero di decisione

```text
Cosa ti serve?
│
├── Tutte le funzioni relazionali
│   ├── Ospitato da te → PostgreSQL
│   └── Serverless → Neon, Supabase
│
├── Deploy sull'edge / latenza bassissima
│   └── Turso (SQLite sull'edge)
│
├── AI / ricerca vettoriale
│   └── PostgreSQL + pgvector
│
├── Semplice / incorporato / locale
│   └── SQLite
│
└── Distribuzione globale
    └── PlanetScale, CockroachDB, Turso
```

## Confronto

| Database | Ideale per | Compromessi |
| --- | --- | --- |
| **PostgreSQL** | Tutte le funzioni, query complesse | Va ospitato |
| **Neon** | PostgreSQL serverless, branching | La complessità di PostgreSQL |
| **Turso** | Edge, bassa latenza | I limiti di SQLite |
| **SQLite** | Semplice, incorporato, locale | Un solo processo che scrive |
| **PlanetScale** | Scala globale | Servizio a pagamento; verifica piani e vincoli attuali |

## Domande da fare

1. Qual è l'ambiente di deploy?
2. Quanto sono complesse le query?
3. Edge o serverless sono importanti?
4. Serve la ricerca vettoriale?
5. Serve la distribuzione globale?
