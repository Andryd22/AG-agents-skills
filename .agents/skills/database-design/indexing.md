# Principi degli indici

> Quando e come creare indici che servono davvero.

## Quando creare un indice

```text
Indicizza:
├── Le colonne nelle clausole WHERE
├── Le colonne nelle condizioni di JOIN
├── Le colonne in ORDER BY
├── Le colonne di foreign key
└── I vincoli di unicità

Non esagerare:
├── Tabelle con molte scritture (insert più lenti)
├── Colonne a bassa cardinalità
├── Colonne interrogate di rado
```

## Scelta del tipo di indice

| Tipo | Per cosa |
| --- | --- |
| **B-tree** | Uso generale, uguaglianza e intervalli |
| **Hash** | Solo uguaglianza, più veloce |
| **GIN** | JSONB, array, testo completo |
| **GiST** | Tipi geometrici e di intervallo |
| **HNSW/IVFFlat** | Similarità vettoriale (pgvector) |

## Indici composti

```text
Negli indici composti l'ordine conta:
├── Prima le colonne con uguaglianza
├── Per ultime quelle con intervalli
├── Prima le più selettive
└── Segui la forma della query
```
