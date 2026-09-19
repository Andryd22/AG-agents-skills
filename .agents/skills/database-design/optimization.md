# Ottimizzare le query

> Problema N+1, EXPLAIN ANALYZE, priorità di ottimizzazione.

## Il problema N+1

```text
Cos'è N+1?
├── 1 query per leggere i record padre
├── N query per leggere i record collegati
└── Lentissimo!

Soluzioni:
├── JOIN → una sola query con tutti i dati
├── Eager loading → la JOIN la fa l'ORM
├── DataLoader → batch e cache (GraphQL)
└── Subquery → i dati collegati in una query
```

## Come analizzare una query

```text
Prima di ottimizzare:
├── EXPLAIN ANALYZE sulla query
├── Cerca i Seq Scan (lettura di tutta la tabella)
├── Confronta le righe reali con quelle stimate
└── Individua gli indici mancanti
```

## Priorità di ottimizzazione

1. **Aggiungi gli indici mancanti** (il problema più comune)
2. **Seleziona solo le colonne che servono** (niente SELECT *)
3. **Usa le JOIN giuste** (evita le subquery quando puoi)
4. **Limita presto** (paginazione nel database)
5. **Cache** (quando ha senso)
