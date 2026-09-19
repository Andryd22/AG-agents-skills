---
name: prompt-engineering
description: LLM prompt design, RAG architecture, and AI integration patterns. Prompt templates, few-shot, chain-of-thought, embedding strategies, and retrieval pipelines.
---

# Prompt Engineering & RAG

> Design prompts that work. Build RAG pipelines that retrieve. Integrate LLMs that scale.

## Prompt Patterns

### Few-Shot Prompting

```text
Classify the sentiment: Positive, Negative, or Neutral.

Text: "This product exceeded my expectations." → Sentiment: Positive
Text: "The shipping was delayed by two weeks." → Sentiment: Negative
Text: "It arrived on time, nothing special." → Sentiment: Neutral
Text: "{USER_INPUT}" → Sentiment:
```

### Chain-of-Thought (CoT)

```text
Question: A bakery sold 120 croissants on Monday and 30% more on Tuesday.
How many were sold on Tuesday?

Let's think step by step:
1. Monday sales = 120
2. 30% of 120 = 0.30 × 120 = 36
3. Tuesday = 120 + 36 = 156
Answer: 156
```

### Structured Output (JSON Mode)

```typescript
const prompt = `
Extract from the text below:
- Company name
- Job title
- Salary range (min/max)
- Remote policy (remote/hybrid/onsite)

Output as JSON only:
Text: "Acme Corp is hiring a Senior Engineer, $120K-$160K, fully remote."
`;

// Expected output:
{
  "company": "Acme Corp",
  "title": "Senior Engineer",
  "salary": { "min": 120000, "max": 160000 },
  "remote": "remote"
}
```

## RAG Architecture

### Pipeline

```text
User Query → Query Rewriting → Embedding → Vector Search → Reranking → LLM Generation → Response
```

### Chunking Strategies

| Strategy | Use Case | Example |
| ---------- | ---------- | --------- |
| **Fixed-size** | Simple docs | 512 tokens, 64 overlap |
| **Sentence** | QA on articles | Split by sentence boundary |
| **Semantic** | Long technical docs | Split by heading/section |
| **Recursive** | General purpose | Start big, split smaller if needed |

### Embedding Model Selection

| Model | Dimensions | Best For |
| ------- | ------------ | ---------- |
| `text-embedding-3-small` | 512/1536 | Cost-sensitive, high volume |
| `text-embedding-3-large` | 256/1024/3072 | Accuracy-critical |
| `bge-large-en-v1.5` | 1024 | Self-hosted, open source |

### Retrieval Optimization

```python
# Hybrid search: combine vector + keyword
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

## Function Calling / Tool Use

```python
tools = [{
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "description": "Search internal docs for relevant information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "top_k": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    }
}]
```

## Guardrails

| Risk | Mitigation |
| ------ | ------------ |
| Hallucination | Ground in retrieved docs, cite sources |
| Prompt injection | Strip input, validate structured output |
| Data leakage | Never embed PII, filter before indexing |
| Bias amplification | Diverse few-shot examples, output audits |
| Token cost explosion | Cache embeddings, batch API calls |

## Anti-Patterns

| ❌ Don't | ✅ Do |
| ---------- | ------- |
| Single-shot for complex tasks | Chain-of-thought or tree-of-thought |
| `max_tokens` too low | Set high enough for complete output |
| Index everything as one chunk | Chunk by semantic units with overlap |
| Re-embed on every query | Cache embeddings, use incremental updates |
| No fallback if retrieval fails | Graceful degradation: "I don't know" |
| Ignore context window limits | Count tokens, truncate, prioritize recency |

## Checklist

- [ ] Prompt tested with multiple inputs (3+ edge cases)
- [ ] Structured output validated against schema
- [ ] RAG pipeline: chunk size optimized for embedding model
- [ ] Retrieval includes reranking step
- [ ] Hallucination guard: sources cited inline
- [ ] Token budget calculated (prompt + completion + context)
- [ ] Error handling: API failures, rate limits, timeouts
