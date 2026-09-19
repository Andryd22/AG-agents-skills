# Principi di progettazione dello schema

> Normalizzazione, chiavi primarie, timestamp, relazioni.

## Normalizzare o no

```text
Quando normalizzare (tabelle separate):
├── Gli stessi dati si ripetono su più righe
├── Un aggiornamento richiederebbe più modifiche
├── Le relazioni sono chiare
└── Le query ne traggono vantaggio

Quando denormalizzare (incorporare/duplicare):
├── Le prestazioni in lettura sono critiche
├── I dati cambiano di rado
├── Si leggono sempre insieme
└── Servono query più semplici
```

## Scelta della chiave primaria

| Tipo | Quando |
| --- | --- |
| **UUID** | Sistemi distribuiti, sicurezza |
| **ULID** | Come UUID, ma ordinabile per tempo |
| **Autoincremento** | App semplici, un solo database |
| **Chiave naturale** | Di rado (ha un significato di business) |

## Timestamp

```text
In ogni tabella:
├── created_at → quando è stato creato
├── updated_at → ultima modifica
└── deleted_at → cancellazione logica (se serve)

Usa TIMESTAMPTZ (con fuso orario), non TIMESTAMP
```

## Tipi di relazione

| Tipo | Quando | Implementazione |
| --- | --- | --- |
| **Uno a uno** | Dati di estensione | Tabella separata con FK |
| **Uno a molti** | Padre e figli | FK nella tabella figlia |
| **Molti a molti** | Molti da entrambe le parti | Tabella di collegamento |

## ON DELETE delle foreign key

```text
├── CASCADE → elimina i figli insieme al padre
├── SET NULL → i figli restano orfani
├── RESTRICT → impedisce l'eliminazione se ci sono figli
└── SET DEFAULT → i figli prendono il valore predefinito
```
