---
name: prompt-engineering
description: Progettazione di prompt per LLM, architettura RAG e schemi di integrazione dell'AI. Template di prompt, few-shot, chain-of-thought, strategie di embedding e pipeline di retrieval.
---

# Prompt engineering e RAG

> Progetta prompt che funzionano. Costruisci pipeline RAG che recuperano. Integra LLM che reggono il carico.

## Schemi di prompt

### Few-shot

```text
Classifica il sentiment: Positivo, Negativo o Neutro.

Testo: "Questo prodotto ha superato le mie aspettative." → Sentiment: Positivo
Testo: "La spedizione è arrivata con due settimane di ritardo." → Sentiment: Negativo
Testo: "È arrivato in tempo, niente di speciale." → Sentiment: Neutro
Testo: "{USER_INPUT}" → Sentiment:
```

### Chain-of-thought (CoT)

```text
Domanda: una panetteria ha venduto 120 cornetti lunedì e il 30% in più martedì.
Quanti ne ha venduti martedì?

Ragioniamo passo per passo:
1. Vendite di lunedì = 120
2. Il 30% di 120 = 0,30 × 120 = 36
3. Martedì = 120 + 36 = 156
Risposta: 156
```

### Output strutturato (modalità JSON)

```typescript
const prompt = `
Estrai dal testo qui sotto:
- Nome dell'azienda
- Ruolo
- Fascia di stipendio (min/max)
- Modalità di lavoro (remote/hybrid/onsite)

Rispondi solo in JSON:
Testo: "Acme Corp cerca un Senior Engineer, 120K-160K €, completamente da remoto."
`;

// Output atteso:
{
  "company": "Acme Corp",
  "title": "Senior Engineer",
  "salary": { "min": 120000, "max": 160000 },
  "remote": "remote"
}
```

## Architettura RAG

### Pipeline

```text
Query dell'utente → riscrittura della query → embedding → ricerca vettoriale → reranking → generazione con l'LLM → risposta
```

### Strategie di chunking

| Strategia | Quando | Esempio |
| --- | --- | --- |
| **Dimensione fissa** | Documenti semplici | 512 token, 64 di sovrapposizione |
| **Per frase** | Domande e risposte su articoli | Divisione ai confini delle frasi |
| **Semantica** | Documenti tecnici lunghi | Divisione per titolo/sezione |
| **Ricorsiva** | Uso generale | Parti grande, dividi di più se serve |

### Scelta del modello di embedding

| Modello | Dimensioni | Ideale per |
| --- | --- | --- |
| `text-embedding-3-small` | 512/1536 | Costi contenuti, grandi volumi |
| `text-embedding-3-large` | 256/1024/3072 | Quando l'accuratezza è critica |
| `bge-large-en-v1.5` | 1024 | Self-hosted, open source, solo inglese |
| `bge-m3` | 1024 | Self-hosted, open source, multilingue (testi in italiano) |

### Ottimizzare il retrieval

```python
# Ricerca ibrida: vettoriale + parole chiave
# LangChain v1: pip install langchain-classic langchain-community rank_bm25
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
bm25_retriever = BM25Retriever.from_documents(docs)
ensemble = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6]
)
```

## Function calling / uso di strumenti

```python
tools = [{
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "description": "Cerca nei documenti interni le informazioni pertinenti",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Testo da cercare"},
                "top_k": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    }
}]
```

## Protezioni

| Rischio | Contromisura |
| --- | --- |
| Allucinazioni | Ancorare ai documenti recuperati, citare le fonti |
| Prompt injection | Ripulire l'input, validare l'output strutturato |
| Fuga di dati | Mai fare embedding di dati personali, filtrare prima di indicizzare |
| Amplificazione dei bias | Esempi few-shot vari, controlli sull'output |
| Esplosione dei costi in token | Cache degli embedding, chiamate API in batch |

## Anti-pattern

| ❌ Da non fare | ✅ Da fare |
| --- | --- |
| Un solo passo per compiti complessi | Chain-of-thought o tree-of-thought |
| `max_tokens` troppo basso | Abbastanza alto per un output completo |
| Indicizzare tutto come un solo chunk | Chunk per unità semantiche con sovrapposizione |
| Ricalcolare gli embedding a ogni query | Cache degli embedding, aggiornamenti incrementali |
| Nessun ripiego se il retrieval fallisce | Degrado controllato: "Non lo so" |
| Ignorare i limiti della finestra di contesto | Conta i token, tronca, dai priorità ai più recenti |

## Checklist

- [ ] Prompt provato con più input (3+ casi limite)
- [ ] Output strutturato validato contro lo schema
- [ ] Pipeline RAG: dimensione dei chunk ottimizzata per il modello di embedding
- [ ] Il retrieval include un passo di reranking
- [ ] Protezione dalle allucinazioni: fonti citate nel testo
- [ ] Budget dei token calcolato (prompt + risposta + contesto)
- [ ] Gestione degli errori: API che falliscono, rate limit, timeout
