# Test di sicurezza delle API

> Principi per testare la sicurezza di un'API: OWASP API Top 10, test di autenticazione e autorizzazione.

---

## OWASP API Security Top 10

| Vulnerabilità | Cosa testare |
| --- | --- |
| **API1: BOLA** | Accesso alle risorse di altri utenti |
| **API2: Broken Auth** | JWT, sessioni, credenziali |
| **API3: Property Auth** | Mass assignment, esposizione di dati |
| **API4: Resource Consumption** | Rate limiting, DoS |
| **API5: Function Auth** | Endpoint di amministrazione, aggirare i ruoli |
| **API6: Business Flow** | Abuso della logica, automazione |
| **API7: SSRF** | Accesso alla rete interna |
| **API8: Misconfiguration** | Endpoint di debug, CORS |
| **API9: Inventory** | API nascoste, versioni vecchie |
| **API10: Unsafe Consumption** | Fiducia nelle API di terze parti |

---

## Test dell'autenticazione

### JWT

| Controllo | Cosa testare |
| --- | --- |
| Algoritmo | None, confusione di algoritmo |
| Segreto | Segreti deboli, forza bruta |
| Claim | Scadenza, issuer, audience |
| Firma | Manipolazione, iniezione di chiavi |

### Sessioni

| Controllo | Cosa testare |
| --- | --- |
| Generazione | Prevedibilità |
| Conservazione | Sicurezza lato client |
| Scadenza | Il timeout viene applicato |
| Invalidazione | Il logout funziona davvero |

---

## Test dell'autorizzazione

| Tipo di test | Approccio |
| --- | --- |
| **Orizzontale** | Accedere ai dati di altri utenti dello stesso livello |
| **Verticale** | Accedere a funzioni con privilegi più alti |
| **Contesto** | Accedere fuori dal perimetro permesso |

### Test BOLA/IDOR

1. Individua gli ID delle risorse nelle richieste
2. Cattura una richiesta con la sessione dell'utente A
3. Ripetila con la sessione dell'utente B
4. Controlla se c'è un accesso non autorizzato

---

## Test della validazione degli input

| Tipo di iniezione | Cosa testare |
| --- | --- |
| SQL | Manipolazione delle query |
| NoSQL | Query sui documenti |
| Comandi | Comandi di sistema |
| LDAP | Query sulle directory |

**Approccio:** testa tutti i parametri, prova la conversione dei tipi, testa i valori limite, controlla i messaggi di errore.

---

## Test del rate limiting

| Aspetto | Controllo |
| --- | --- |
| Esistenza | C'è un limite? |
| Aggiramento | Header, rotazione degli IP |
| Ambito | Per utente, per IP, globale |

**Tecniche di aggiramento:** X-Forwarded-For, metodi HTTP diversi, variazioni di maiuscole e minuscole, versioni dell'API.

---

## Sicurezza di GraphQL

| Test | Cosa guardare |
| --- | --- |
| Introspection | Esposizione dello schema |
| Batching | DoS con le query |
| Annidamento | DoS sulla profondità |
| Autorizzazione | Accesso per singolo campo |

---

## Checklist dei test di sicurezza

**Autenticazione:**

- [ ] Prova ad aggirarla
- [ ] Controlla la robustezza delle credenziali
- [ ] Verifica la sicurezza dei token

**Autorizzazione:**

- [ ] Testa BOLA/IDOR
- [ ] Controlla l'escalation dei privilegi
- [ ] Verifica l'accesso alle funzioni

**Input:**

- [ ] Testa tutti i parametri
- [ ] Cerca le iniezioni

**Configurazione:**

- [ ] Controlla il CORS
- [ ] Verifica gli header
- [ ] Testa la gestione degli errori

---

> **Ricorda:** le API sono la spina dorsale delle app moderne. Testale come le attaccherebbe un aggressore.
