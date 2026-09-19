---
name: web-design-guidelines
description: Rivede il codice della UI rispetto alle Web Interface Guidelines. Usala quando ti chiedono di "rivedere la UI", "controllare l'accessibilità", "fare un audit del design", "rivedere la UX" o "controllare il sito rispetto alle buone pratiche".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-o-schema>
---

# Web Interface Guidelines

Controlla che i file rispettino le Web Interface Guidelines.

## Come funziona

1. Scarica le linee guida aggiornate dall'URL qui sotto
2. Leggi i file indicati (o chiedi all'utente file o schema)
3. Controllali rispetto a tutte le regole scaricate
4. Riporta i risultati nel formato sintetico `file:riga`

## Fonte delle linee guida

Scarica linee guida fresche prima di ogni revisione:

```text
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Usa WebFetch (o lo strumento per leggere URL che hai) per recuperare le regole aggiornate. Il contenuto scaricato contiene tutte le regole e le istruzioni sul formato dell'output; è in inglese: applicalo e scrivi il resoconto in italiano.

## Uso

Quando l'utente indica un file o uno schema:

1. Scarica le linee guida dall'URL qui sopra
2. Leggi i file indicati
3. Applica tutte le regole delle linee guida scaricate
4. Riporta i risultati nel formato indicato dalle linee guida

Se non sono indicati file, chiedi all'utente quali rivedere.

---

## Skill collegate

| Skill | Quando usarla |
| --- | --- |
| **[frontend-design](../frontend-design/SKILL.md)** | Prima di scrivere codice: principi di design (colore, tipografia, psicologia della UX) |
| **web-design-guidelines** (questa) | Dopo aver scritto codice: audit di accessibilità, prestazioni e buone pratiche |

## Flusso di design

```text
1. DESIGN   → leggi i principi di frontend-design
2. CODICE   → implementa il design
3. AUDIT    → revisione con web-design-guidelines ← SEI QUI
4. CORREZIONI → sistema quello che l'audit ha trovato
```
