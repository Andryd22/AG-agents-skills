# Schemi di autenticazione

> Scegli lo schema di autenticazione in base al caso d'uso.

## Guida alla scelta

| Schema | Ideale per |
| --- | --- |
| **JWT** | Senza stato, microservizi |
| **Sessione** | Web tradizionale, semplice |
| **OAuth 2.0** | Integrazione con terze parti |
| **API key** | Da server a server, API pubbliche |
| **Passkey** | Accesso moderno senza password |

## Principi dei JWT

```text
Importante:
├── Verifica sempre la firma
├── Controlla la scadenza
├── Metti il minimo di claim
├── Scadenza breve + refresh token
└── Mai dati sensibili dentro un JWT
```
