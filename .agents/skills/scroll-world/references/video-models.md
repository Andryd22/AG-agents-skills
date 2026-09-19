# scroll-world — Modelli video

Dettagli per il passo 4 di SKILL.md. Gli schemi sono stati verificati con la CLI di Higgsfield.

**Questa skill produce solo risultati senza giunture**, quindi si possono usare solo i modelli
che agganciano i frame di una giuntura: ogni clip della catena deve accettare `--start-image`,
e i connettori anche `--end-image`. È questa capacità, non la preferenza, a decidere. Controlla
qualsiasi modello con `higgsfield model get <job_type>` e **scarta quelli in cui i media in
ingresso sono solo di riferimento** (niente immagine iniziale/finale): possono solo
*condizionare* una generazione, non *continuare* un'inquadratura, quindi fisicamente non tengono
una giuntura. Gli schemi qui sotto sono stati verificati con la CLI:

| Modello | Immagine iniziale/finale | Note |
| --- | --- | --- |
| `seedance_2_0` (predefinito) | ✓ / ✓ | Catena completa (tratti + connettori). `--mode std --resolution 1080p`. Il suo filtro NSFW è quello permaloso (vedi Trappole). |
| `kling3_0` | ✓ / ✓ | Catena completa — provato: `--mode std --sound off --duration 5` con immagini iniziale e finale accettate, le giunture si agganciano pulite. **Nessun parametro `--resolution`** (non passarlo; `--mode std` restituisce **720p nativo**: codifica quello che dice ffprobe, mai ingrandire). Il suono è **attivo** di default → `--sound off`. `--duration` predefinita 5, prova 10 per i tratti. Filtro dei contenuti diverso da Seedance: il ripiego ufficiale per l'NSFW. |
| `seedance_2_0_mini` | ✓ / ✓ | Livello di bozza economico che continua ad agganciare i frame (720p). Il livello previz: fai qui prima tutta la catena, poi rigenera i tratti finali con il modello completo; resta senza giunture, quindi si traduce direttamente. |

Questi tre sono l'elenco: tutti fanno entrambe le architetture. (Anche `kling3_0_turbo` aggancia
i frame con `--start-image`, ma non ha `--end-image`, quindi va bene solo per l'architettura A e
non può fare connettori; ha anche un altro insieme di flag — niente `--mode`, c'è `--resolution` —
quindi non entra nella pipeline così com'è. Non è nell'elenco predefinito; usalo, collegandolo a
mano, solo se il tempo di resa in sequenza dell'architettura A è un collo di bottiglia dimostrato
e hai misurato che è davvero più veloce.)

**Prima la previz (predefinita, non un extra facoltativo).** A meno che la corsa non sia piccola
(≤4 scene), rendi prima tutta la catena con `seedance_2_0_mini`. Aggancia i frame, quindi tutto
quello che conta — ordine del viaggio, grammatica della camera, continuità delle giunture, ritmo dei
testi rispetto allo scrub — si convalida al costo di una bozza; monta la pagina con le clip di
previz e rivedila con l'utente prima di spendere un solo credito del modello completo. Poi togli
le clip di bozza, cambia `$VMODEL` e rigenera la versione finale (le immagini si riusano;
l'idempotenza della pipeline rende meccanico il secondo passaggio: `references/pipeline.md`,
blocco di configurazione).

Regole:

- **Un solo modello per tutte le clip della catena.** Ogni modello ha il suo carattere di
  movimento, colore e grana; mescolare modelli a metà catena mantiene la continuità di *posizione*
  (i frame si passano comunque) ma il cambio di carattere si legge come un piccolo scatto. L'unica
  eccezione ammessa è il ripiego per l'NSFW su una singola clip ostinata (Trappole): un leggero
  cambio di carattere su un connettore di 5 s è meglio di un connettore mancante.
- Predefinito `seedance_2_0`; rispetta la preferenza dell'utente **solo se il modello ha i
  requisiti** (aggancio dei frame). Se non li ha, dillo e usa un modello supportato: mai consegnare
  un lavoro con giunture per accontentare la richiesta di un modello.
- Gli script della pipeline prendono il modello come `$VMODEL`, con i flag di ogni modello già
  gestiti (`references/pipeline.md`).
