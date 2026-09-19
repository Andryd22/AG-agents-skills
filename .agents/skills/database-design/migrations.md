# Principi delle migrazioni

> Strategia di migrazione sicura per modifiche senza fermare il servizio.

## Migrazioni sicure

```text
Per modifiche senza interruzioni:
│
├── Aggiungere una colonna
│   └── Aggiungila nullable → riempi i dati → aggiungi NOT NULL
│
├── Togliere una colonna
│   └── Smetti di usarla → deploy → togli la colonna
│
├── Aggiungere un indice
│   └── CREATE INDEX CONCURRENTLY (non blocca le scritture)
│
└── Rinominare una colonna
    └── Aggiungi la nuova → migra i dati → deploy → elimina la vecchia
```

## Filosofia delle migrazioni

- Mai modifiche che rompono qualcosa in un passo solo
- Prova prima le migrazioni su una copia dei dati
- Tieni pronto un piano di rollback
- Quando puoi, eseguile in una transazione (non `CREATE INDEX CONCURRENTLY`, che in una transazione non può girare)

## Database serverless

### Neon (PostgreSQL serverless)

| Caratteristica | Vantaggio |
| --- | --- |
| Scala fino a zero | Risparmio |
| Branching istantaneo | Ambienti di sviluppo e anteprima |
| PostgreSQL completo | Compatibilità |
| Autoscaling | Regge i picchi di traffico |

### Turso (SQLite sull'edge)

| Caratteristica | Vantaggio |
| --- | --- |
| Nodi sull'edge | Latenza bassissima |
| Compatibile con SQLite | Semplicità |
| Piano gratuito generoso | Costi |
| Distribuzione globale | Prestazioni |
