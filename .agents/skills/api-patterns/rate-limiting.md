# Principi del rate limiting

> Proteggi l'API da abusi e sovraccarichi.

## Perché limitare

```text
Proteggi da:
├── Attacchi a forza bruta
├── Esaurimento delle risorse
├── Costi fuori controllo (se paghi a consumo)
└── Uso sleale
```

## Scelta della strategia

| Tipo | Come funziona | Quando |
| --- | --- | --- |
| **Token bucket** | Permette picchi, si ricarica nel tempo | La maggior parte delle API |
| **Finestra scorrevole** | Distribuzione uniforme | Limiti rigidi |
| **Finestra fissa** | Semplici contatori per finestra | Esigenze di base |

## Header della risposta

```text
Metti negli header:
├── X-RateLimit-Limit (richieste massime)
├── X-RateLimit-Remaining (richieste rimaste)
├── X-RateLimit-Reset (quando si azzera il limite)
└── Rispondi 429 quando il limite è superato
```
