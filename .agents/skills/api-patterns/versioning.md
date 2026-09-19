# Strategie di versioning

> Prevedi l'evoluzione dell'API fin dal primo giorno.

## Fattori di decisione

| Strategia | Implementazione | Compromessi |
| --- | --- | --- |
| **URI** | /v1/users | Chiara, cache facile |
| **Header** | Accept-Version: 1 | URL più puliti, meno facile da scoprire |
| **Query** | ?version=1 | Facile da aggiungere, disordinata |
| **Nessuna** | Evolvere con cautela | Ottima per API interne, rischiosa per quelle pubbliche |

## Filosofia del versioning

```text
Valuta:
├── API pubblica? → versione nell'URI
├── Solo interna? → forse il versioning non serve
├── GraphQL? → di solito niente versioni (lo schema evolve)
├── tRPC? → sono i tipi a garantire la compatibilità
```
