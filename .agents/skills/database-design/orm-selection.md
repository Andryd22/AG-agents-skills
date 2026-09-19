# Scegliere l'ORM

> Scegli l'ORM in base al deploy e all'esperienza di sviluppo che serve.

## Albero di decisione

```text
Qual è il contesto?
│
├── Deploy sull'edge / conta la dimensione del bundle
│   └── Drizzle (il più leggero, simile a SQL)
│
├── Migliore esperienza di sviluppo / prima lo schema
│   └── Prisma (migrazioni, Prisma Studio)
│
├── Massimo controllo
│   └── SQL diretto con un query builder
│
└── Ecosistema Python
    └── SQLAlchemy 2.0 (supporta async)
```

## Confronto

| ORM | Ideale per | Compromessi |
| --- | --- | --- |
| **Drizzle** | Edge, TypeScript | Più giovane, meno esempi |
| **Prisma** | Esperienza di sviluppo, gestione dello schema | Più pesante; verifica il supporto all'edge della versione che usi |
| **Kysely** | Query builder SQL con tipi garantiti | Migrazioni a mano |
| **SQL diretto** | Query complesse, controllo | Tipi da garantire a mano |
