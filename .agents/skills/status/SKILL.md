---
name: status
description: 'Mostra lo stato del progetto e degli agenti: stack, funzionalità, lavoro in sospeso e conteggio dei file. Usala quando l''utente lancia /status o chiede a che punto è il progetto.'
---

# /status - Stato del progetto

La richiesta è il testo che segue `/status`.

---

## Compito

Mostra lo stato attuale del progetto e degli agenti.

### Cosa mostra

1. **Informazioni sul progetto**
   - Nome e percorso del progetto
   - Stack tecnologico
   - Funzionalità presenti

2. **Tabella degli agenti**
   - Quali agenti stanno lavorando
   - Quali compiti sono finiti
   - Lavoro in sospeso

3. **Statistiche sui file**
   - Numero di file creati
   - Numero di file modificati

---

## Esempio di output

```text
=== Stato del progetto ===

📁 Progetto: my-ecommerce
📂 Percorso: C:/projects/my-ecommerce
🏷️ Tipo: nextjs-ecommerce
📊 Stato: attivo

🔧 Stack:
   Framework: next.js
   Database: postgresql
   Auth: clerk
   Pagamenti: stripe

✅ Funzionalità (5):
   • elenco prodotti
   • carrello
   • checkout
   • autenticazione
   • storico ordini

⏳ In sospeso (2):
   • pannello di amministrazione
   • notifiche email

📄 File: 73 creati, 12 modificati

=== Stato degli agenti ===

✅ backend-specialist → finito
🔄 frontend-specialist → componenti della dashboard (60%)
⏳ test-engineer → in attesa
```

---

## Dettagli tecnici

Lo stato usa questo script:

- `python .agents/scripts/session_manager.py status`
