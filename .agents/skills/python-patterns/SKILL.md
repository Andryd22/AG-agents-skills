---
name: python-patterns
description: Principi di sviluppo in Python e come decidere. Scelta del framework web, schemi asincroni, type hint, struttura del progetto. Insegna a ragionare, non a copiare.
---

# Schemi per Python

> Principi e decisioni per lo sviluppo in Python.
> **Impara a RAGIONARE, non a memorizzare schemi.**

Questa skill riguarda applicazioni e API. Per analisi dei dati e machine learning con pandas e scikit-learn usa `classic-ml`.

---

## ⚠️ Come usare questa skill

Questa skill insegna **principi per decidere**, non codice fisso da copiare.

- CHIEDI all'utente che framework preferisce quando non è chiaro
- Scegli tra async e sync in base al CONTESTO
- Non usare ogni volta lo stesso framework

---

## 1. Scelta del framework

### Albero di decisione

```text
Cosa stai costruendo?
│
├── Prima le API / microservizi
│   └── FastAPI (async, moderno, veloce)
│
├── Web full-stack / CMS / pannello di amministrazione
│   └── Django (tutto incluso)
│
├── Semplice / script / per imparare
│   └── Flask (minimale, flessibile)
│
├── Servire modelli AI/ML via API
│   └── FastAPI (Pydantic, async, uvicorn)
│
└── Lavori in background
    └── Celery + qualsiasi framework
```

### Confronto

| Fattore | FastAPI | Django | Flask |
| --- | --- | --- | --- |
| **Ideale per** | API, microservizi | Full-stack, CMS | Cose semplici, imparare |
| **Async** | Nativo | Django 5.0+ | Con estensioni |
| **Pannello admin** | A mano | Integrato | Con estensioni |
| **ORM** | A scelta | Django ORM | A scelta |
| **Curva di apprendimento** | Bassa | Media | Bassa |

### Domande per scegliere

1. Solo API o full-stack?
2. Serve un pannello di amministrazione?
3. Il team conosce l'async?
4. C'è un'infrastruttura esistente?

---

## 2. Async o sync

### Quando usare l'async

```text
async def è meglio quando:
├── Operazioni legate all'I/O (database, HTTP, file)
├── Tante connessioni contemporanee
├── Funzionalità in tempo reale
├── Comunicazione tra microservizi
└── FastAPI/Starlette/Django ASGI

def (sync) è meglio quando:
├── Operazioni legate alla CPU
├── Script semplici
├── Codebase esistenti
├── Il team non conosce l'async
└── Librerie bloccanti (senza versione async)
```

### La regola d'oro

```text
Legato all'I/O → async (si aspetta qualcosa da fuori)
Legato alla CPU → sync + multiprocessing (si calcola)

Da non fare:
├── Mescolare sync e async senza attenzione
├── Usare librerie sync nel codice async
└── Forzare l'async per il lavoro di CPU
```

### Librerie async

| Serve | Libreria async |
| --- | --- |
| Client HTTP | httpx |
| PostgreSQL | asyncpg |
| Redis | redis-py (`redis.asyncio`; aioredis è confluito lì) |
| I/O su file | aiofiles |
| ORM | SQLAlchemy 2.0 async, Tortoise |

---

## 3. Type hint

### Cosa annotare

```text
Annota sempre:
├── Parametri delle funzioni
├── Tipi di ritorno
├── Attributi delle classi
├── API pubbliche

Si può evitare:
├── Variabili locali (lascia fare all'inferenza)
├── Script usa e getta
├── Test (di solito)
```

### Schemi di tipi comuni

```python
# Sono schemi da capire, non da copiare:

# Può essere None
def find_user(id: int) -> User | None: ...

# Uno tra più tipi
def process(data: str | dict) -> None: ...

# Collezioni generiche
def get_items() -> list[Item]: ...
def get_mapping() -> dict[str, int]: ...

# Funzioni come parametro
from collections.abc import Callable
def apply(fn: Callable[[int], str]) -> str: ...
```

### Pydantic per la validazione

```text
Quando usare Pydantic:
├── Modelli di richiesta e risposta delle API
├── Configurazione e impostazioni
├── Validazione dei dati
├── Serializzazione

Vantaggi:
├── Validazione a runtime
├── JSON schema generato da solo
├── Funziona nativamente con FastAPI
└── Messaggi di errore chiari
```

---

## 4. Struttura del progetto

### Quale struttura

```text
Progetto piccolo / script:
├── main.py
├── utils.py
└── requirements.txt

API media:
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── schemas/
├── tests/
└── pyproject.toml

Applicazione grande:
├── src/
│   └── myapp/
│       ├── core/
│       ├── api/
│       ├── services/
│       ├── models/
│       └── ...
├── tests/
└── pyproject.toml
```

### Struttura di un progetto FastAPI

```text
Organizza per funzionalità o per livello:

Per livello:
├── routes/ (endpoint delle API)
├── services/ (logica di business)
├── models/ (modelli del database)
├── schemas/ (modelli Pydantic)
└── dependencies/ (dipendenze condivise)

Per funzionalità:
├── users/
│   ├── routes.py
│   ├── service.py
│   └── schemas.py
└── products/
    └── ...
```

---

## 5. Django

### Django async (Django 5.0+)

```text
Django supporta l'async:
├── View async
├── Middleware async
├── ORM async (con limiti)
└── Deploy ASGI

Quando usare l'async in Django:
├── Chiamate ad API esterne
├── WebSocket (Channels)
├── View con molta concorrenza
└── Avvio di task in background
```

### Buone pratiche

```text
Modelli:
├── Modelli ricchi, view sottili
├── Manager per le query comuni
├── Classi base astratte per i campi condivisi

View:
├── Basate su classi per il CRUD complesso
├── Basate su funzioni per gli endpoint semplici
├── Viewset con DRF

Query:
├── select_related() per le FK
├── prefetch_related() per le M2M
├── Evita le query N+1
└── .only() per scegliere i campi
```

---

## 6. FastAPI

### async def o def in FastAPI

```text
Usa async def quando:
├── Usi driver di database async
├── Fai chiamate HTTP async
├── Operazioni legate all'I/O
└── Vuoi gestire la concorrenza

Usa def quando:
├── Operazioni bloccanti
├── Driver di database sync
├── Lavoro di CPU
└── FastAPI lo esegue da solo in un threadpool
```

### Dependency injection

```text
Usa le dipendenze per:
├── Sessioni del database
├── Utente corrente / autenticazione
├── Configurazione
├── Risorse condivise

Vantaggi:
├── Testabilità (dipendenze simulate)
├── Separazione pulita
├── Pulizia automatica (yield)
```

### Integrazione con Pydantic v2

```python
# FastAPI e Pydantic sono strettamente integrati:

# Validazione della richiesta
@app.post("/users")
async def create(user: UserCreate) -> UserResponse:
    # user è già validato
    ...

# Serializzazione della risposta:
# il tipo di ritorno diventa lo schema della risposta
```

---

## 7. Task in background

### Guida alla scelta

| Soluzione | Ideale per |
| --- | --- |
| **BackgroundTasks** | Task semplici nello stesso processo |
| **Celery** | Flussi distribuiti e complessi |
| **ARQ** | Async, basato su Redis |
| **RQ** | Coda Redis semplice |
| **Dramatiq** | Basato su attori, più semplice di Celery |

### Quando usare cosa

```text
BackgroundTasks di FastAPI:
├── Operazioni veloci
├── Non serve persistenza
├── Lanci e dimentichi
└── Stesso processo

Celery/ARQ:
├── Task lunghi
├── Serve la logica dei tentativi
├── Worker distribuiti
├── Coda persistente
└── Flussi complessi
```

---

## 8. Gestione degli errori

### Strategia delle eccezioni

```text
In FastAPI:
├── Crea classi di eccezione personalizzate
├── Registra gli exception handler
├── Restituisci sempre lo stesso formato di errore
└── Scrivi nei log senza esporre i dettagli interni

Schema:
├── Lancia eccezioni di dominio nei servizi
├── Catturale e trasformale negli handler
└── Il client riceve una risposta di errore pulita
```

### Cosa mettere nella risposta di errore

```text
Includi:
├── Codice di errore (per il codice)
├── Messaggio (leggibile da una persona)
├── Dettagli (per campo, quando serve)
└── MAI gli stack trace (sicurezza)
```

---

## 9. Test

### Strategia

| Tipo | Scopo | Strumenti |
| --- | --- | --- |
| **Unitari** | Logica di business | pytest |
| **Integrazione** | Endpoint delle API | pytest + httpx/TestClient |
| **E2E** | Flussi completi | pytest + DB |

### Test async

```python
# Per i test async usa pytest-asyncio

import pytest
from httpx import ASGITransport, AsyncClient

@pytest.mark.asyncio
async def test_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/users")
        assert response.status_code == 200
```

### Fixture

```text
Fixture comuni:
├── db_session → connessione al database
├── client → client di test
├── authenticated_user → utente con token
└── sample_data → dati di prova
```

---

## 10. Checklist di decisione

Prima di implementare:

- [ ] **Hai chiesto all'utente che framework preferisce?**
- [ ] **Hai scelto il framework per QUESTO contesto?** (non per abitudine)
- [ ] **Hai deciso tra async e sync?**
- [ ] **Hai deciso come usare i type hint?**
- [ ] **Hai definito la struttura del progetto?**
- [ ] **Hai pianificato la gestione degli errori?**
- [ ] **Hai considerato i task in background?**

---

## 11. Anti-pattern da evitare

### ❌ NON

- Usare Django per API semplici senza pensarci (FastAPI può andare meglio)
- Usare librerie sync nel codice async
- Saltare i type hint nelle API pubbliche
- Mettere la logica di business nelle route o nelle view
- Ignorare le query N+1
- Mescolare async e sync senza attenzione

### ✅ SÌ

- Scegliere il framework in base al contesto
- Chiedere dei requisiti di async
- Usare Pydantic per la validazione
- Separare le responsabilità (route → servizi → repository)
- Testare i percorsi critici

---

> **Ricorda**: gli schemi di Python servono a decidere per il TUO contesto. Non copiare codice: pensa a cosa serve davvero alla tua applicazione.
