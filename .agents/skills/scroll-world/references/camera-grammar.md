# scroll-world — Grammatica della camera

Dettagli per il passo 4 di SKILL.md, architettura A.

"Solo in avanti" è la regola delle *giunture*, non dei *tratti*. La fisica della catena:

- La **continuità di posizione** a una giuntura viene dal passaggio del frame (il tratto
  successivo parte dall'ultimo frame reale del precedente).
- La **continuità di velocità** a una giuntura vuol dire che la camera non deve mai
  *invertire attraverso una giuntura*: è lo scatto da riavvolgimento.
- **Dentro un tratto la camera è libera.** Un tratto è un'unica resa continua: a metà tratto
  non c'è nessuna giuntura da rompere, quindi orbite, salite in gru, carrellate laterali, perfino
  un avvicinamento che poi si allontana sono sicuri *dentro* la clip. Le inversioni sono fatali
  solo *attraverso* le giunture.

Quindi dai a ogni tratto un movimento espressivo scelto dalla logica della scena, sotto un
**contratto di passaggio del movimento**: ogni tratto **finisce assestandosi in una deriva lenta
e costante in avanti** verso la meta successiva (l'ultimo ~1 s), e ogni tratto **comincia
continuando quella stessa deriva**. Tieni identiche entrambe le frasi nei prompt (modelli in
`references/prompts.md`).

Scegli la grammatica dal concept:

| Concept / tono | Movimento a metà tratto |
| --- | --- |
| Prodotto / lusso | mezza orbita lenta intorno all'oggetto protagonista, poi oltre |
| Immobiliare / ospitalità | scivolata in steadicam attraverso le porte; leggera salita in gru negli atri |
| Industria / processi / logistica | carrellata laterale bassa lungo la linea, parallasse in primo piano |
| Viaggi / all'aperto / campus | salita e rivelazione da drone, poi una picchiata in discesa |
| Cibo / artigianato / dettagli | avvicinamento al gesto artigiano, leggero arretramento, poi avanti |
| Miniatura giocosa (arch. B) | tuffi + salti aerei: il connettore È la grammatica |

Costi onesti: i movimenti espressivi a metà tratto aumentano la probabilità di rifacimenti: il
modello può chiudere un movimento elaborato in uno stato che non è una deriva in avanti pulita.
Contromisure: tieni identica la frase dell'assestamento nell'ultimo secondo; **guarda l'ultimo
frame di ogni tratto prima di concatenare il successivo** (deve sembrare un frame di una leggera
scivolata in avanti; se no, rifallo prima di sprecare il tratto dopo); prevedi ~1 rifacimento in
più per ogni tratto espressivo. Una semplice scivolata in avanti resta la scelta predefinita a
rischio zero: usala nei tratti in cui lo spettacolo è la scena stessa.

Nel motore ci sono due manopole del ritmo collegate (passo 7): `scroll` per sezione (più scroll =
sosta più lunga in quella scena) e `linger` (la camera si assesta a metà scena proprio mentre i
testi sono al massimo, poi accelera verso la giuntura). Meglio un movimento espressivo nella
*clip* e sobrietà nella *mappatura dello scrub*: gli effetti si sommano.

E ricorda che lo scroll è una testina: i visitatori possono scorrere **in su**, quindi ogni
movimento si vede anche al contrario. Non costa niente ed è previsto, ma è un motivo in più perché
la velocità alle giunture sia coerente nei due sensi (una giuntura che va bene in avanti scatta
anche all'indietro se la velocità si inverte).
