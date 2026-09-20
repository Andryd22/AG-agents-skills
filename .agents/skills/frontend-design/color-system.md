# Riferimento sistema colori

> Principi di teoria del colore, processo di scelta e linee guida per decidere.
> **Nessun codice hex a memoria: impara a RAGIONARE sul colore.**

---

## 1. Fondamenti di teoria del colore

### La ruota dei colori

```text
                    GIALLO
                      │
           Giallo-    │    Giallo-
           verde      │    arancio
              ╲       │       ╱
               ╲      │      ╱
    VERDE ─────────── ● ─────────── ARANCIONE
               ╱      │      ╲
              ╱       │       ╲
           Blu-       │    Rosso-
           verde      │    arancio
                      │
                    ROSSO
                      │
                    VIOLA
                  ╱       ╲
             Blu-          Rosso-
             viola         viola
                  ╲       ╱
                     BLU
```

### Relazioni tra colori

| Schema | Come crearlo | Quando usarlo |
| --- | --- | --- |
| **Monocromatico** | Scegli UNA sola tonalità e varia solo luminosità/saturazione | Minimal, professionale, coerente |
| **Analogo** | Scegli 2-3 tonalità ADIACENTI sulla ruota | Armonioso, calmo, ispirato alla natura |
| **Complementare** | Scegli tonalità OPPOSTE sulla ruota | Contrasto alto, vivace, attira l'attenzione |
| **Complementare diviso** | Base + i 2 colori adiacenti al suo complementare | Dinamico ma equilibrato |
| **Triadico** | 3 tonalità EQUIDISTANTI sulla ruota | Vivace, giocoso, creativo |

### Come scegliere uno schema

1. **Qual è il mood del progetto?** Calmo → analogo. Deciso → complementare.
2. **Quanti colori servono?** Pochi → monocromatico. Molti → triadico.
3. **Chi è il pubblico?** Conservatore → monocromatico. Giovane → triadico.

---

## 2. La regola 60-30-10

### Principio di distribuzione

```text
┌─────────────────────────────────────────────────┐
│                                                 │
│     60% PRIMARIO (sfondo, aree ampie)           │
│     → Deve essere neutro o rilassante           │
│     → Definisce il tono generale                │
│                                                 │
├────────────────────────────────────┬────────────┤
│                                    │            │
│   30% SECONDARIO                   │ 10% ACCENTO│
│   (card, sezioni, header)          │ (CTA,      │
│   → Supporta senza dominare        │ highlight) │
│                                    │ → Attira   │
│                                    │ attenzione │
└────────────────────────────────────┴────────────┘
```

### Pattern di implementazione

```css
:root {
  /* 60% - Scegli in base a light/dark mode e al mood */
  --color-bg: /* neutro: bianco, bianco sporco o grigio scuro */
  --color-surface: /* leggermente diverso dal bg */
  
  /* 30% - Scegli in base al brand o al contesto */
  --color-secondary: /* versione attenuata del primario o un neutro */
  
  /* 10% - Scegli in base all'azione/emozione che vuoi suscitare */
  --color-accent: /* vivace, cattura l'attenzione */
}
```

---

## 3. Psicologia del colore: significato e scelta

### Come scegliere in base al contesto

| Se il progetto è... | Considera queste tonalità | Perché |
| --- | --- | --- |
| **Finanza, tech, sanità** | Blu, verde acqua | Fiducia, stabilità, calma |
| **Eco, benessere, natura** | Verdi, toni della terra | Crescita, salute, naturalezza |
| **Cibo, energia, giovani** | Arancio, giallo, colori caldi | Appetito, entusiasmo, calore |
| **Lusso, bellezza, creatività** | Verde petrolio scuro, oro, nero | Raffinatezza, premium |
| **Urgenza, saldi, avvisi** | Rosso, arancio | Azione, attenzione, passione |

### Associazioni emotive (per decidere)

| Famiglia di tonalità | Associazioni positive | Attenzione |
| --- | --- | --- |
| **Blu** | Fiducia, calma, professionalità | Può sembrare freddo, aziendale |
| **Verde** | Crescita, natura, successo | Se abusato può annoiare |
| **Rosso** | Passione, urgenza, energia | Molto eccitante, usalo con parsimonia |
| **Arancio** | Calore, cordialità, creatività | Se troppo saturo può sembrare economico |
| **Viola** | ⚠️ **VIETATO**: l'AI lo usa fin troppo! | Usa invece verde petrolio scuro, bordeaux o smeraldo |
| **Giallo** | Ottimismo, attenzione, allegria | Poco leggibile, usalo come accento |
| **Nero** | Eleganza, potere, modernità | Può risultare pesante |
| **Bianco** | Pulizia, minimalismo, apertura | Può sembrare asettico |

### Processo di scelta

1. **Qual è il settore?** → Restringi a 2-3 famiglie di tonalità
2. **Qual è l'emozione?** → Scegli la tonalità primaria
3. **Che contrasto?** → Decidi tra light e dark mode
4. **CHIEDI ALL'UTENTE** → Conferma prima di procedere

---

## 4. Principi per generare una palette

### Da un solo colore (metodo HSL)

Invece di memorizzare codici hex, impara a **manipolare l'HSL**:

```text
HSL = Hue, Saturation, Lightness (tonalità, saturazione, luminosità)

Hue (0-360): la famiglia di colore
  0/360 = rosso
  60 = giallo
  120 = verde
  180 = ciano
  240 = blu
  300 = viola

Saturation (0-100%): intensità del colore
  Bassa = attenuato, raffinato
  Alta = vivace, energico

Lightness (0-100%): luminosità
  0% = nero
  50% = colore puro
  100% = bianco
```

### Generare una palette completa

Partendo da QUALSIASI colore base, crea una scala:

```text
Scala di luminosità:
  50  (più chiaro) → L: 97%
  100              → L: 94%
  200              → L: 86%
  300              → L: 74%
  400              → L: 66%
  500 (base)       → L: 50-60%
  600              → L: 48%
  700              → L: 38%
  800              → L: 30%
  900 (più scuro)  → L: 20%
```

### Regolare la saturazione

| Contesto | Livello di saturazione |
| --- | --- |
| **Professionale/aziendale** | Più bassa (40-60%) |
| **Giocoso/giovane** | Più alta (70-90%) |
| **Dark mode** | Riducila del 10-20% |
| **Accessibilità** | Garantisci il contrasto, potrebbe servire qualche ritocco |

---

## 5. Guida alla scelta in base al contesto

### Invece di copiare palette, segui questo processo

#### Passo 1: identifica il contesto

```text
Che tipo di progetto è?
├── E-commerce → Serve equilibrio tra fiducia e urgenza
├── SaaS/Dashboard → Serve poca fatica visiva, focus sui dati
├── Salute/benessere → Serve un'atmosfera calma e naturale
├── Lusso/premium → Serve un'eleganza sobria
├── Creativo/portfolio → Serve personalità, deve restare impresso
└── Altro → CHIEDI all'utente
```

##### Passo 2: scegli la famiglia di tonalità primaria

```text
In base al contesto, scegline UNA:
- Famiglia dei blu (fiducia)
- Famiglia dei verdi (crescita)
- Famiglia dei caldi (energia)
- Famiglia dei neutri (eleganza)
- OPPURE chiedi la preferenza all'utente
```

###### Passo 3: scegli tra light e dark mode

```text
Valuta:
- Preferenza dell'utente?
- Standard del settore?
- Tipo di contenuto? (molto testo = meglio light)
- Momento d'uso? (app serale = opzione dark)
```

###### Passo 4: genera la palette seguendo i principi

- Manipola l'HSL
- Segui la regola 60-30-10
- Controlla il contrasto (WCAG)
- Prova con contenuti reali

---

## 6. Principi della dark mode

### Regole chiave (nessun codice fisso)

1. **Mai nero puro** → Usa un grigio molto scuro con una leggera tonalità
2. **Mai testo bianco puro** → Usa una luminosità dell'87-92%
3. **Riduci la saturazione** → In dark mode i colori vivaci affaticano la vista
4. **Elevazione = luminosità** → Gli elementi più in alto sono un po' più chiari

### Contrasto in dark mode

```text
Livelli di sfondo (da più scuro a più chiaro man mano che sale l'elevazione):
Livello 0 (base)    → Il più scuro
Livello 1 (card)    → Un po' più chiaro
Livello 2 (modali)  → Ancora più chiaro
Livello 3 (popup)   → Lo scuro più chiaro
```

### Adattare i colori alla dark mode

| Light mode | Adattamento per la dark mode |
| --- | --- |
| Accento molto saturo | Riduci la saturazione del 10-20% |
| Sfondo bianco puro | Grigio scuro con una sfumatura della tonalità del brand |
| Testo nero | Grigio chiaro (non bianco puro) |
| Sfondi colorati | Versioni desaturate e più scure |

---

## 7. Linee guida di accessibilità

### Requisiti di contrasto (WCAG)

| Livello | Testo normale | Testo grande |
| --- | --- | --- |
| AA (minimo) | 4.5:1 | 3:1 |
| AAA (avanzato) | 7:1 | 4.5:1 |

### Come verificare il contrasto

1. **Converti i colori in luminanza relativa**
2. **Calcola il rapporto**: (più chiaro + 0.05) / (più scuro + 0.05)
3. **Regola finché il rapporto non soddisfa il requisito**

### Pattern sicuri

| Caso d'uso | Linea guida |
| --- | --- |
| **Testo su sfondo chiaro** | Usa una luminosità del 35% o meno |
| **Testo su sfondo scuro** | Usa una luminosità dell'85% o più |
| **Primario su bianco** | Assicurati che la variante sia abbastanza scura |
| **Pulsanti** | Contrasto alto tra sfondo e testo |

---

## 8. Checklist per la scelta dei colori

Prima di confermare qualsiasi scelta di colore, verifica:

- [ ] **Hai chiesto la preferenza dell'utente?** (se non è specificata)
- [ ] **È adatta al contesto del progetto?** (settore, pubblico)
- [ ] **Rispetta la regola 60-30-10?** (distribuzione corretta)
- [ ] **È conforme alle WCAG?** (contrasto verificato)
- [ ] **Funziona in entrambe le modalità?** (se serve la dark mode)
- [ ] **NON è la tua scelta predefinita/preferita?** (verifica la varietà)
- [ ] **È diversa dall'ultimo progetto?** (evita le ripetizioni)

---

## 9. Anti-pattern da evitare

### ❌ NON FARE

- Copiare gli stessi codici hex in ogni progetto
- Ripiegare sul viola (tendenza tipica dell'AI)
- Ripiegare su dark mode + neon (tendenza tipica dell'AI)
- Usare sfondi nero puro (#000000)
- Usare testo bianco puro (#FFFFFF) su sfondo scuro
- Ignorare il settore dell'utente
- Saltare la domanda sulle preferenze dell'utente

### ✅ FAI

- Genera una palette nuova per ogni progetto
- Chiedi all'utente le sue preferenze di colore
- Tieni conto di settore e pubblico
- Usa l'HSL per manipolare i colori con flessibilità
- Verifica contrasto e accessibilità
- Proponi opzioni light E dark

---

> **Ricorda**: i colori sono decisioni, non impostazioni predefinite. Ogni progetto merita una scelta ponderata in base al suo contesto specifico.
