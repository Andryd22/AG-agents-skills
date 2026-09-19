# Raccogliere il contesto

> Prima di proporre un'architettura, raccogli il contesto.

## Domande in ordine (chiedile PRIMA all'utente)

1. **Scala**
   - Quanti utenti? (10, 1K, 100K, 1M+)
   - Quanti dati? (MB, GB, TB)
   - Quante transazioni? (al secondo/al minuto)

2. **Team**
   - Sviluppatore singolo o team?
   - Dimensione e competenze del team?
   - Distribuito o nella stessa sede?

3. **Tempi**
   - MVP/prototipo o prodotto a lungo termine?
   - Fretta di arrivare sul mercato?

4. **Dominio**
   - Tanto CRUD o logica di business complessa?
   - Requisiti di tempo reale?
   - Normative da rispettare?

5. **Vincoli**
   - Limiti di budget?
   - Sistemi esistenti da integrare?
   - Preferenze sullo stack?

## Classificazione del progetto

```text
                    MVP              SaaS             Enterprise
┌───────────────────────────────────────────────────────────────┐
│ Scala        │ <1K           │ 1K-100K        │ 100K+        │
│ Team         │ Una persona   │ 2-10           │ 10+          │
│ Tempi        │ Rapidi (sett.)│ Medi (mesi)    │ Lunghi (anni)│
│ Architettura │ Semplice      │ Modulare       │ Distribuita  │
│ Schemi       │ Il minimo     │ Selezionati    │ Completi     │
│ Esempio      │ API Next.js   │ NestJS         │ Microservizi │
└───────────────────────────────────────────────────────────────┘
```
