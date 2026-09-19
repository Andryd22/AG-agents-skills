# Principi REST

> API basate sulle risorse: nomi, non verbi.

## Nomi delle risorse

```text
Principi:
├── NOMI, non verbi (risorse, non azioni)
├── Al PLURALE (/users, non /user)
├── Minuscole con trattini (/user-profiles)
├── Annidamento per le relazioni (/users/123/posts)
└── Poco profondi (massimo 3 livelli)
```

## Scelta del metodo HTTP

| Metodo | Scopo | Idempotente? | Corpo? |
| --- | --- | --- | --- |
| **GET** | Leggere una o più risorse | Sì | No |
| **POST** | Creare una risorsa | No | Sì |
| **PUT** | Sostituire tutta la risorsa | Sì | Sì |
| **PATCH** | Aggiornamento parziale | No | Sì |
| **DELETE** | Eliminare la risorsa | Sì | No |

## Scelta del codice di stato

| Situazione | Codice | Perché |
| --- | --- | --- |
| Successo (lettura) | 200 | Successo standard |
| Creata | 201 | Nuova risorsa creata |
| Nessun contenuto | 204 | Successo, niente da restituire |
| Richiesta errata | 400 | Richiesta malformata |
| Non autenticato | 401 | Autenticazione mancante o non valida |
| Vietato | 403 | Autenticato, ma senza permesso |
| Non trovata | 404 | La risorsa non esiste |
| Conflitto | 409 | Conflitto di stato (duplicato) |
| Errore di validazione | 422 | Sintassi valida, dati non validi |
| Troppe richieste | 429 | Limite superato |
| Errore del server | 500 | Colpa nostra |
