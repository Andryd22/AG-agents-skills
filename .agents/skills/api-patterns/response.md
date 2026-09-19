# Principi sul formato delle risposte

> La coerenza è tutto: scegli un formato e mantienilo.

## Schemi comuni

```text
Scegline uno:
├── Envelope ({ success, data, error })
├── Dati diretti (restituisci solo la risorsa)
└── HAL/JSON:API (ipermedia)
```

## Risposta di errore

```text
Includi:
├── Codice di errore (per la gestione nel codice)
├── Messaggio per l'utente (da mostrare)
├── Dettagli (per il debug, errori per campo)
├── ID della richiesta (per l'assistenza)
└── MAI i dettagli interni (sicurezza!)
```

## Tipi di paginazione

| Tipo | Ideale per | Compromessi |
| --- | --- | --- |
| **Offset** | Semplice, si può saltare a una pagina | Prestazioni sui dataset grandi |
| **Cursore** | Dataset grandi | Non si salta a una pagina |
| **Keyset** | Prestazioni critiche | Serve una chiave ordinabile |

### Domande per scegliere

1. Quanto è grande il dataset?
2. Gli utenti devono saltare a pagine precise?
3. I dati cambiano spesso?
