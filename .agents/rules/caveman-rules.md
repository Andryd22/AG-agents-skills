---
trigger: model_decision
description: Da applicare quando la modalità caveman è attiva (l'utente ha lanciato /caveman on, lite, full o ultra). Mantiene la modalità caveman uguale in tutti gli agenti.
---

# Regole caveman

## 🔧 Linee guida generali

1. **Coerenza**: quando è attiva, tutti gli agenti seguono le regole della skill `caveman`.
2. **L'utente decide**: l'utente può scavalcare la modalità caveman con una richiesta esplicita (es. "spiegami nel dettaglio").
3. **Precisione tecnica**: mai sacrificare la precisione per la brevità.
4. **Ripiego**: se la modalità caveman rende ambigua una risposta, torna alla modalità normale per quella risposta.

## 📝 Note di implementazione

- La modalità caveman dura per tutta la sessione.
- Gli agenti controllano se la modalità caveman è attiva prima di rispondere.
- Lo stato della modalità caveman va indicato nell'output di debug, per trasparenza.
