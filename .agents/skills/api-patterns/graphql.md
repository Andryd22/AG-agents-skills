# Principi di GraphQL

> Query flessibili per dati complessi e collegati tra loro.

## Quando usarlo

```text
✅ Adatto:
├── Dati complessi e collegati tra loro
├── Più piattaforme frontend
├── I client hanno bisogno di query flessibili
├── Requisiti sui dati che cambiano
└── Conta ridurre i dati scaricati in eccesso

❌ Poco adatto:
├── Semplici operazioni CRUD
├── Tanti upload di file
├── La cache HTTP è importante
└── Il team non conosce GraphQL
```

## Progettare lo schema

```text
Principi:
├── Ragiona a grafo, non a endpoint
├── Progetta per evolvere (niente versioni)
├── Usa le connection per la paginazione
├── Tipi precisi (non un generico "data")
└── Gestisci con attenzione i valori null
```

## Sicurezza

```text
Proteggiti da:
├── Attacchi sulla profondità delle query → imposta una profondità massima
├── Complessità delle query → calcola il costo
├── Abuso del batching → limita la dimensione dei batch
├── Introspection → disattivala in produzione
```
