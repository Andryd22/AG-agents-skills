---
name: test
description: Genera test, esegue la suite di test del progetto (scripts/test_runner.py) e riporta la copertura. Usala quando l'utente lancia /test o chiede di scrivere, eseguire o correggere dei test.
---

# /test - Generare ed eseguire test

La richiesta è il testo che segue `/test`.

---

## Scopo

Questo comando genera test, esegue quelli esistenti o controlla la copertura.

---

## Eseguire la suite

`python .agents/skills/test/scripts/test_runner.py . [--coverage]` riconosce il framework (Jest, Vitest, pytest, ...), esegue la suite ed esce con un codice diverso da zero se qualcosa fallisce. Lo usano anche `checklist.py` e `verify_all.py`.

---

## Sottocomandi

```text
/test                  - Esegue tutti i test
/test [file/funzione]  - Genera i test per un obiettivo preciso
/test coverage         - Mostra il report di copertura
/test watch            - Esegue i test in modalità watch
```

---

## Comportamento

### Generare i test

Quando ti chiedono di testare un file o una funzionalità:

1. **Analizza il codice**
   - Individua funzioni e metodi
   - Trova i casi limite
   - Individua le dipendenze da simulare (mock)

2. **Genera i casi di test**
   - Percorso felice
   - Casi di errore
   - Casi limite
   - Test di integrazione (se servono)

3. **Scrivi i test**
   - Usa il framework di test del progetto (Jest, Vitest, ...)
   - Segui gli schemi dei test esistenti
   - Simula le dipendenze esterne

---

## Formato dell'output

### Per la generazione dei test

```markdown
## 🧪 Test: [obiettivo]

### Piano dei test
| Caso di test | Tipo | Copertura |
|--------------|------|-----------|
| Crea l'utente | Unit | Percorso felice |
| Rifiuta un'email non valida | Unit | Validazione |
| Gestisce un errore del database | Unit | Caso di errore |

### Test generati

`tests/[file].test.ts`

[blocco di codice con i test]

---

Esegui con: `npm test`
```

### Per l'esecuzione dei test

```text
🧪 Esecuzione dei test...

✅ auth.test.ts (5 superati)
✅ user.test.ts (8 superati)
❌ order.test.ts (2 superati, 1 fallito)

Falliti:
  ✗ calcola il totale con lo sconto
    Atteso: 90
    Ottenuto: 100

Totale: 15 test (14 superati, 1 fallito)
```

---

## Esempi

```text
/test src/services/auth.service.ts
/test flusso di registrazione dell'utente
/test coverage
/test correggi i test falliti
```

---

## Schemi di test

### Struttura di un test unitario

```typescript
describe('AuthService', () => {
  describe('login', () => {
    it('restituisce il token con credenziali valide', async () => {
      // Prepara
      const credentials = { email: 'test@test.com', password: 'pass123' };

      // Esegui
      const result = await authService.login(credentials);

      // Verifica
      expect(result.token).toBeDefined();
    });

    it('lancia un errore con una password sbagliata', async () => {
      // Prepara
      const credentials = { email: 'test@test.com', password: 'sbagliata' };

      // Esegui e verifica
      await expect(authService.login(credentials)).rejects.toThrow('Credenziali non valide');
    });
  });
});
```

---

## Principi chiave

- **Testa il comportamento, non l'implementazione**
- **Una verifica per test** (quando è pratico)
- **Nomi dei test descrittivi**, in italiano
- **Schema Arrange-Act-Assert** (prepara, esegui, verifica)
- **Simula le dipendenze esterne**
