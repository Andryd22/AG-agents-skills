# Riferimento di psicologia UX

> Approfondimento su leggi UX, design emotivo, costruzione della fiducia e psicologia comportamentale.

---

## 1. Leggi UX fondamentali

### Legge di Hick

**Principio:** il tempo necessario per prendere una decisione cresce in modo logaritmico con il numero di scelte.

```text
Tempo di decisione = a + b × log₂(n + 1)
Dove n = numero di scelte
```

**Applicazione:**

- Navigazione: massimo 5-7 voci di primo livello
- Form: suddividili in step (progressive disclosure)
- Opzioni: selezioni predefinite quando possibile
- Filtri: dai priorità a quelli più usati, nascondi quelli avanzati

**Esempio:**

```text
❌ Male: 15 voci di menu in una sola nav
✅ Bene: 5 categorie principali + "Altro"

❌ Male: 20 campi del form tutti insieme
✅ Bene: wizard in 3 step con 5-7 campi ciascuno
```

---

### Legge di Fitts

**Principio:** il tempo per raggiungere un target è funzione della sua distanza e della sua dimensione.

```text
MT = a + b × log₂(1 + D/W)
Dove D = distanza, W = larghezza
```

**Applicazione:**

- CTA: rendi più grandi i pulsanti primari (altezza minima 44px)
- Touch target: minimo 44×44px su mobile
- Posizionamento: azioni importanti vicino alla posizione naturale del cursore
- Angoli: "angoli magici" (bordo infinito = facili da colpire)

**Dimensionamento dei pulsanti:**

```css
/* Dimensiona in base all'importanza */
.btn-primary { height: 48px; padding: 0 24px; }
.btn-secondary { height: 40px; padding: 0 16px; }
.btn-tertiary { height: 36px; padding: 0 12px; }

/* Touch target su mobile */
@media (hover: none) {
  .btn { min-height: 44px; min-width: 44px; }
}
```

---

### Legge di Miller

**Principio:** una persona media riesce a tenere 7±2 blocchi (chunk) nella memoria di lavoro.

**Applicazione:**

- Liste: raggruppa in blocchi da 5-7 elementi
- Navigazione: massimo 7 voci di menu
- Contenuti: spezza i testi lunghi con i titoli
- Numeri di telefono: 555-123-4567 (a blocchi)

**Esempio di chunking:**

```text
❌ 5551234567
✅ 555-123-4567

❌ Un lungo paragrafo di testo senza interruzioni
✅ Paragrafi brevi
   Con elenchi puntati
   E sottotitoli
```

---

### Effetto Von Restorff (effetto di isolamento)

**Principio:** un elemento che spicca ha più probabilità di essere ricordato.

**Applicazione:**

- Pulsanti CTA: colore distinto dagli altri elementi
- Pricing: evidenzia il piano consigliato
- Informazioni importanti: differenziazione visiva
- Nuove funzionalità: badge o callout

**Esempio:**

```css
/* Tutti i pulsanti grigi, il primario spicca */
.btn { background: #E5E7EB; }
.btn-primary { background: #3B82F6; }

/* Piano consigliato evidenziato */
.pricing-card { border: 1px solid #E5E7EB; }
.pricing-card.popular {
  border: 2px solid #3B82F6;
  box-shadow: var(--shadow-lg);
}
```

---

### Effetto di posizione seriale

**Principio:** gli elementi all'inizio (primacy) e alla fine (recency) di una lista sono quelli ricordati meglio.

**Applicazione:**

- Navigazione: le voci più importanti per prime e per ultime
- Liste: informazioni chiave in cima e in fondo
- Form: i campi più critici all'inizio
- CTA: ripetile in cima e in fondo alle pagine lunghe

**Esempio:**

```text
Navigazione: Home | [voci chiave] | Contatti

Landing page lunga:
- CTA nella hero (in alto)
- Sezioni di contenuto
- CTA ripetuta in fondo
```

### Legge di Jakob

**Principio:** gli utenti passano la maggior parte del tempo su altri siti. Preferiscono che il tuo sito funzioni come tutti gli altri siti che già conoscono.

**Applicazione:**

- **Pattern:** usa le posizioni standard per barra di ricerca e carrello.
- **Modelli mentali:** sfrutta icone familiari (per es. la lente d'ingrandimento).
- **Lessico:** usa "Accedi" invece di "Entra nel portale".
- **Layout:** tieni il logo in alto a sinistra come link alla "Home".
- **Interazione:** lo swipe a destra per tornare indietro o andare avanti deve sembrare nativo.
- **Feedback:** colori standard (rosso = errore, verde = successo).

**Esempio:**

```text
❌ Male: un sito in cui il clic sul logo porta alla pagina "Chi siamo".
✅ Bene: il clic sul logo riporta sempre l'utente alla homepage.

❌ Male: usare un'icona "stella" per indicare "Elimina".
✅ Bene: usare un'icona "cestino" per indicare "Elimina".
```

---

### Legge di Tesler (conservazione della complessità)

**Principio:** in ogni sistema c'è una quota di complessità che non si può ridurre, ma solo spostare dall'utente al software.

**Applicazione:**

- **Backend:** lascia che sia il sistema a gestire la formattazione (per es. la valuta).
- **Rilevamento:** rileva in automatico il tipo di carta, o la città dal CAP.
- **Automazione:** precompila i dati degli utenti che tornano.
- **Personalizzazione:** mostra solo i campi pertinenti in base alle risposte precedenti.
- **Default:** valori predefiniti intelligenti per le impostazioni comuni.
- **Integrazione:** usa l'SSO (social login) per togliere attrito alla registrazione.

**Esempio:**

```text
❌ Male: costringere gli utenti a digitare "USD $" prima di ogni campo prezzo del form.
✅ Bene: l'app antepone da sola il "$" in base alla posizione dell'utente.

❌ Male: costringere gli utenti a scegliere a mano il "tipo di carta" (Visa/Mastercard).
✅ Bene: rilevare il tipo di carta in automatico dalle prime quattro cifre inserite.
```

---

### Legge di Parkinson

**Principio:** ogni attività si dilata fino a occupare tutto il tempo disponibile.

**Applicazione:**

- **Efficienza:** usa il salvataggio automatico ("Auto-save") per ridurre il tempo di completamento.
- **Velocità:** limita gli step di un funnel di conversione.
- **Chiarezza:** usa etichette chiare, così l'utente non deve andare a tentoni con l'hover per capirne il significato.
- **Feedback:** validazione in tempo reale, così l'utente non perde tempo sugli errori.
- **Onboarding:** configurazione rapida ("Express") per gli utenti esperti.
- **Vincoli:** imposta limiti di caratteri sugli input per far concentrare i pensieri.

**Esempio:**

```text
❌ Male: un form di registrazione di 10 pagine che lascia uscire dalla pagina e perdere i dati.
✅ Bene: un "accesso con un tocco" tramite Google o Apple ID.

❌ Male: dare all'utente un tempo illimitato per scrivere una bio.
✅ Bene: offrire una funzione di "bio suggerite" che aiuta a finire in pochi secondi.
```

---

### Soglia di Doherty

**Principio:** la produttività schizza in alto quando computer e utenti interagiscono a un ritmo (<400ms) tale che nessuno dei due debba aspettare l'altro.

**Applicazione:**

- **Feedback:** usa segnali visivi immediati per i clic.
- **Caricamento:** usa gli skeleton screen per migliorare la performance percepita.
- **Ottimismo:** aggiorna la UI prima che risponda il server (Optimistic UI).
- **Motion:** usa micro-animazioni per mascherare piccoli ritardi.
- **Caching:** precarica in background le pagine o gli asset successivi.
- **Priorità:** carica il testo prima delle immagini pesanti ad alta risoluzione.

**Esempio:**

```text
❌ Male: un pulsante che per 2 secondi dopo il clic non fa nulla.
✅ Bene: un pulsante che cambia subito colore e mostra uno spinner di caricamento.

❌ Male: una schermata bianca vuota mentre i dati vengono caricati.
✅ Bene: uno skeleton screen con le sagome grigie dei punti in cui apparirà il contenuto.
```

---

### Legge di Postel (principio di robustezza)

**Principio:** sii rigoroso in ciò che fai e tollerante in ciò che accetti dagli altri.

**Applicazione:**

- **Gestione degli errori:** non dare errore per uno spazio o un trattino mancante.
- **Formattazione:** accetta le date sia in GG/MM/AAAA sia in MM/GG/AAAA.
- **Input:** elimina in automatico gli spazi iniziali e finali.
- **Fallback:** usa avatar predefiniti se l'utente non ha caricato una foto.
- **Ricerca:** tollera i refusi e proponi suggerimenti del tipo "Forse cercavi...?".
- **Accessibilità:** assicurati che il sito funzioni su tutti i browser e dispositivi.

**Esempio:**

```text
❌ Male: rifiutare un numero di telefono perché l'utente ci ha messo uno spazio.
✅ Bene: accettare l'input ed eliminare gli spazi in automatico.

❌ Male: costringere gli utenti a scrivere "gennaio" invece di "01" o "gen".
✅ Bene: un campo data che capisce tutti e tre i formati.
```

---

### Rasoio di Occam

**Principio:** tra ipotesi concorrenti con la stessa capacità predittiva va scelta quella con meno assunzioni. La soluzione più semplice di solito è la migliore.

**Applicazione:**

- **Logica:** elimina i clic inutili.
- **Aspetto visivo:** usa solo i font e i colori strettamente necessari.
- **Funzione:** se un campo può fare il lavoro di due, uniscili.
- **Copy:** usa il testo più breve possibile per trasmettere il significato.
- **Layout:** elimina gli elementi decorativi che non servono a uno scopo.
- **Flusso:** evita i percorsi ramificati se non sono indispensabili.

**Esempio:**

```text
❌ Male: un pulsante "Accedi" che apre una nuova pagina, poi l'email, poi la password.
✅ Bene: un'unica modale di login che chiede entrambe in una sola schermata.

❌ Male: usare 5 dimensioni di font diverse e 4 colori in una sola card.
✅ Bene: usare 2 dimensioni di font e 1 colore d'accento.
```

---

## 2. Percezione visiva (principi della Gestalt)

### Legge di prossimità

**Principio:** gli oggetti vicini tra loro tendono a essere percepiti come un gruppo.

**Applicazione:**

- **Raggruppamento:** tieni le etichette fisicamente vicine ai campi di input.
- **Spaziatura:** margini più ampi tra blocchi di contenuto non correlati.
- **Card:** il testo in una card deve stare più vicino alla sua immagine che al bordo.
- **Footer:** raggruppa i link legali, lontano dai link social.
- **Navigazione:** tieni le impostazioni "Utente" separate da quelle "App".
- **Form:** raggruppa i campi dell'indirizzo, separati da quelli della carta di credito.

**Esempio:**

```text
❌ Male: spazi ampi e uguali tra tutte le righe di testo di un form.
✅ Bene: spaziatura stretta tra etichetta e input, con spazi più ampi tra una coppia e l'altra.

❌ Male: un pulsante "Invia" che fluttua a metà pagina, lontano dal form.
✅ Bene: il pulsante "Invia" subito sotto l'ultimo campo di input.
```

---

### Legge di somiglianza

**Principio:** l'occhio umano tende a percepire gli elementi simili di un design come un'unica immagine, forma o gruppo, anche se sono separati.

**Applicazione:**

- **Coerenza:** colori coerenti per tutti i link cliccabili.
- **Iconografia:** tutte le icone di un set devono avere lo stesso spessore del tratto.
- **Pulsanti:** stessa forma e dimensione per pulsanti della stessa importanza.
- **Tipografia:** usa lo stesso stile H2 per tutti i titoli di sezione.
- **Feedback:** tutte le azioni "Elimina" devono usare lo stesso colore (per es. rosso).
- **Stati:** gli stati hover e active devono essere coerenti in tutta l'app.

**Esempio:**

```text
❌ Male: alcuni link sono blu, altri verdi, altri semplicemente neri in grassetto.
✅ Bene: ogni testo cliccabile dell'app ha la stessa tonalità di blu.

❌ Male: usare lo stesso "pulsante blu" sia per "Invia" sia per "Annulla".
✅ Bene: "Invia" è blu pieno; "Annulla" ha solo il contorno blu (ghost button).
```

---

### Legge della regione comune

**Principio:** gli elementi tendono a essere percepiti come gruppo se condividono un'area con un confine ben definito.

**Applicazione:**

- **Contenitori:** usa le card per raggruppare immagini e titoli.
- **Bordi:** usa delle linee per separare la sidebar dal feed principale.
- **Sfondi:** usa un colore di sfondo diverso per il footer.
- **Modali:** usa un riquadro distinto per separare i pop-up dalla pagina.
- **Liste:** colori di sfondo alternati per le righe (zebra striping).
- **Header:** una barra piena in alto per raggruppare le voci di navigazione.

**Esempio:**

```text
❌ Male: un elenco di notizie in cui testo e immagini di articoli diversi si sovrappongono.
✅ Bene: ogni articolo sta nella sua card bianca su sfondo grigio chiaro.

❌ Male: un footer con lo stesso colore di sfondo del corpo della pagina.
✅ Bene: un footer scuro che separa chiaramente i link legali dal contenuto della pagina.
```

---

### Legge della connessione uniforme

**Principio:** gli elementi collegati visivamente (per es. da linee o frecce) vengono percepiti come più correlati di quelli non collegati.

**Applicazione:**

- **Flusso:** usa delle linee per collegare gli step di un wizard.
- **Menu:** dropdown che "toccano" il pulsante da cui partono o vi si collegano.
- **Grafici:** linee che collegano i punti dati di un grafico.
- **Relazione:** collega un interruttore (toggle) al testo che controlla.
- **Gerarchia:** strutture ad albero per le cartelle dei file.
- **Form:** collega il radio button "Carta di credito" al fieldset sottostante.

**Esempio:**

```text
❌ Male: una configurazione in 3 step in cui i numeri "1", "2" e "3" sono sparsi.
✅ Bene: una linea orizzontale che collega "1", "2" e "3" per mostrare la sequenza.

❌ Male: menu dropdown fluttuanti che non toccano il pulsante che li ha aperti.
✅ Bene: un menu dropdown che si "aggancia" visivamente al pulsante da cui parte.
```

---

### Legge della Prägnanz (semplicità)

**Principio:** le persone percepiscono e interpretano le immagini ambigue o complesse nella forma più semplice possibile, perché è l'interpretazione che richiede il minimo sforzo cognitivo.

**Applicazione:**

- **Chiarezza:** usa icone chiare e geometriche per la navigazione.
- **Riduzione:** elimina texture 3D e ombre non necessarie.
- **Forme:** preferisci rettangoli e cerchi standard ai poligoni complessi.
- **Focus:** usa sagome ad alto contrasto per le azioni primarie.
- **Logo:** marchi semplici, riconoscibili anche a dimensioni ridotte.
- **UX:** un solo obiettivo principale per pagina, per mantenere semplice la "forma mentale".

**Esempio:**

```text
❌ Male: un'illustrazione 3D iperrealistica di una cartella come icona "File".
✅ Bene: il semplice contorno 2D di una cartella.

❌ Male: un logo complesso e multicolore usato come spinner di caricamento.
✅ Bene: un semplice anello circolare di un solo colore.
```

---

### Legge figura/sfondo

**Principio:** l'occhio distingue un oggetto dall'area che lo circonda. Una forma o una sagoma viene percepita come figura (oggetto), mentre l'area intorno viene percepita come sfondo.

**Applicazione:**

- **Focus:** usa overlay (scrim) per le modali, così il contenuto risalta.
- **Profondità:** ombre esterne per suggerire che la "figura" sta sopra lo "sfondo".
- **Contrasto:** testo chiaro su sfondo scuro (o viceversa).
- **Sfocatura:** usa il blur dello sfondo per dare risalto al testo in primo piano.
- **Navigazione:** header sticky fluttuanti che restano sopra il contenuto della pagina.
- **Hover:** solleva leggermente le card all'hover per definirle come figura.

**Esempio:**

```text
❌ Male: un popup senza ombra né bordo, che si confonde con la pagina.
✅ Bene: una modale con ombra e un overlay che scurisce lo sfondo.

❌ Male: testo bianco messo direttamente sopra una foto affollata e multicolore.
✅ Bene: testo bianco sopra uno "scrim" scuro semitrasparente.
```

---

### Legge del punto focale

**Principio:** ciò che risalta visivamente cattura e trattiene per primo l'attenzione di chi guarda.

**Applicazione:**

- **Ingresso:** metti la value proposition principale nel punto focale.
- **Colore:** usa un solo "colore d'azione" molto acceso su una UI neutra.
- **Movimento:** usa un'animazione discreta sulla CTA per attirare lo sguardo.
- **Dimensione:** il dato più importante deve avere il font più grande.
- **Tipografia:** pesi bold per i titoli e pesi normali per il corpo del testo.
- **Direzione:** usa frecce o lo sguardo (immagini di persone che guardano un pulsante).

**Esempio:**

```text
❌ Male: una homepage con 5 pulsanti della stessa dimensione e dello stesso colore.
✅ Bene: un solo grande pulsante "Inizia" in un colore acceso.

❌ Male: una dashboard in cui "Fatturato totale" ha la stessa dimensione di "Versione di sistema".
✅ Bene: "Fatturato totale" mostrato con numeri enormi in grassetto, in alto al centro.
```

---

## 3. Bias cognitivi e comportamento

### Effetto Zeigarnik

**Principio:** le persone ricordano le attività incompiute o interrotte meglio di quelle completate.

**Applicazione:**

- **Gamification:** usa barre del tipo "Profilo completo al 60%".
- **Engagement:** anticipa il modulo successivo di un percorso di apprendimento.
- **Retention:** mostra una lista "Da fare" delle funzionalità ancora da esplorare.
- **Feedback:** badge persistenti per i messaggi non letti.
- **Slancio:** mostra i passi "Successivi" subito dopo averne completato uno.
- **Shopping:** promemoria "Completa l'ordine" nel carrello.

**Esempio:**

```text
❌ Male: un onboarding silenzioso che non dà alcuna indicazione di cosa manca.
✅ Bene: una checklist che mostra "3 step su 5 completati".

❌ Male: un'app di e-learning che mostra la spunta anche se il video è stato visto a metà.
✅ Bene: un anello di avanzamento che resta pieno a metà finché il video non è finito.
```

### Effetto del gradiente dell'obiettivo (goal gradient)

**Principio:** la spinta verso un obiettivo aumenta man mano che ci si avvicina.

**Applicazione:**

- **Slancio:** dai agli utenti un "avanzamento artificiale" (per es. 2 timbri omaggio).
- **Avanzamento:** dividi un form da 10 campi in due step da 5.
- **Feedback:** festeggia i traguardi a metà di un'attività.
- **Motivazione:** mostra all'utente quanto è vicino a un premio o a un nuovo status.
- **Navigazione:** usa i breadcrumb per mostrare quanto manca alla fine.
- **Caricamento:** accelera l'animazione di caricamento quando si avvicina al 100%.

**Esempio:**

```text
❌ Male: una barra di avanzamento che parte da 0% e sembra una lunga salita.
✅ Bene: una barra che parte dal 20% perché l'utente ha "iniziato" aprendo l'app.

❌ Male: un checkout in cui il "Riepilogo finale" sembra un 5° step a sorpresa.
✅ Bene: step etichettati chiaramente: "Spedizione > Pagamento > Quasi fatto!"
```

### Regola del picco-fine (peak-end rule)

**Principio:** le persone giudicano un'esperienza soprattutto in base a come si sono sentite nel momento di picco (il più intenso) e alla fine, non in base alla somma o alla media di tutti i momenti.

**Applicazione:**

- **Successo:** rendi memorabile la schermata "Ordine confermato".
- **Delight:** aggiungi coriandoli o un'animazione unica nel momento in cui arriva il valore.
- **Supporto:** assicurati che l'ultima interazione con un chatbot sia utile.
- **Offboarding:** anche quando un utente se ne va, rendi pulita l'uscita finale.
- **Onboarding:** chiudi la prima sessione con una "vittoria" chiara.
- **Gestione degli errori:** trasforma una pagina 404 in un'interazione divertente e utile.

**Esempio:**

```text
❌ Male: dopo 20 minuti di dichiarazione dei redditi, l'app dice solo "Inviato".
✅ Bene: una schermata "Complimenti!" con il riepilogo dell'importo del rimborso.

❌ Male: un gioco che finisce con un semplice "Game Over" in un font anonimo.
✅ Bene: una schermata di riepilogo con i punteggi migliori e musica celebrativa.
```

### Effetto estetica-usabilità

**Principio:** gli utenti tendono a percepire un design esteticamente gradevole come più usabile.

**Applicazione:**

- **Trust:** una grafica curata fa guadagnare "credito di fiducia" per i bug minori.
- **Branding:** immagini coerenti e di qualità trasmettono professionalità.
- **Engagement:** le interfacce belle tengono gli utenti a esplorare più a lungo.
- **Pazienza:** gli utenti perdonano di più i tempi di caricamento se la UI è bella.
- **Sicurezza:** un design pulito fa sembrare più gestibili gli strumenti complessi.
- **Fedeltà:** le persone creano legami emotivi con i prodotti belli.

**Esempio:**

```text
❌ Male: un'app bancaria con testo disallineato e colori anni '90 che stridono.
✅ Bene: un'app bancaria elegante e moderna con animazioni fluide.

❌ Male: usare foto stock pixelate a bassa risoluzione.
✅ Bene: usare illustrazioni di brand personalizzate in alta definizione.
```

### Bias di ancoraggio

**Principio:** per decidere, gli utenti si basano molto sulla prima informazione che ricevono (l'"ancora").

**Applicazione:**

- **Pricing:** mostra il prezzo originale barrato.
- **Piani:** metti il piano "Enterprise", il più costoso, all'estrema sinistra.
- **Ordinamento:** metti in evidenza "Il più popolare" come prima raccomandazione.
- **Sconti:** indica "Risparmi il 20%" prima di mostrare il prezzo finale.
- **Limiti:** "Massimo 12 per cliente" ancora l'idea che il prodotto valga molto.
- **Default:** parti da un importo alto di "donazione suggerita".

**Esempio:**

```text
❌ Male: mostrare solo il prezzo "$49".
✅ Bene: mostrare "~~$99~~ $49 (-50%)".

❌ Male: ordinare una lista di laptop dal più economico al più costoso.
✅ Bene: mostrare per primo un modello "Pro" di fascia alta, così gli altri sembrano economici.
```

### Riprova sociale (social proof)

**Principio:** le persone copiano le azioni degli altri per capire come comportarsi in una data situazione.

**Applicazione:**

- **Conferma:** mostra "Unisciti a oltre 50.000 persone".
- **Recensioni:** valutazioni a stelle e testimonianze di clienti verificati.
- **Logo:** sezione "Scelto da" con i brand partner.
- **Feed live:** notifiche del tipo "Sara l'ha comprato 5 minuti fa".
- **Attività:** "300 persone stanno guardando questo articolo".
- **Certificati:** premi di settore e badge di sicurezza.

**Esempio:**

```text
❌ Male: una pagina di registrazione con solo un form.
✅ Bene: una pagina di registrazione che dice "Unisciti a 2 milioni di designer".

❌ Male: recensioni anonime, senza nomi né foto.
✅ Bene: recensioni con un volto, un nome e l'etichetta "Acquirente verificato".
```

### Principio di scarsità

**Principio:** le persone danno più valore a ciò che è scarso e meno a ciò che è abbondante.

**Applicazione:**

- **Urgenza:** "Solo 2 articoli rimasti in magazzino".
- **Tempo:** timer con conto alla rovescia per le offerte.
- **Accesso:** beta "solo su invito" o piani esclusivi.
- **Stagionalità:** prodotti "Summer Edition".
- **Scorte basse:** "Presto di nuovo disponibile: preordina ora".
- **Domanda:** "Molto richiesto: 10 persone lo hanno nel carrello".

**Esempio:**

```text
❌ Male: una promozione che non finisce mai e non ha conto alla rovescia.
✅ Bene: un'"Offerta del giorno" con il timer che scorre.

❌ Male: mostrare che un prodotto è disponibile senza indicare la quantità.
✅ Bene: "Solo 3 rimasti a questo prezzo!"
```

### Bias di autorità

**Principio:** la tendenza ad attribuire maggiore accuratezza all'opinione di una figura autorevole e a lasciarsene influenzare di più.

**Applicazione:**

- **Competenza:** usa diciture come "Verificato da esperti" o foto professionali.
- **Certificazioni:** sigilli di fiducia (Norton, ISO, HIPAA).
- **Media:** loghi "Visto su TechCrunch/Forbes".
- **Endorsement:** testimonianze di leader di settore o influencer.
- **Linguaggio:** copy sicuro, professionale e accurato.
- **Storia:** "Dal 1950" per suggerire longevità e affidabilità.

**Esempio:**

```text
❌ Male: un blog sulla salute scritto da "Admin".
✅ Bene: un articolo sulla salute "Revisionato dalla dott.ssa Jane Smith, cardiologa".

❌ Male: un'app di sicurezza che non cita alcuna certificazione.
✅ Bene: mostrare i loghi "Certificato ISO 27001" e "Norton Secured".
```

### Avversione alla perdita

**Principio:** in genere le persone preferiscono evitare una perdita piuttosto che ottenere un guadagno equivalente. Non perdere 5 $ conta più che trovarne 5.

**Applicazione:**

- **Messaggi:** "Non perdere il tuo sconto".
- **Prove gratuite:** "La tua prova gratuita sta per scadere: conserva i tuoi dati ora".
- **Scarsità:** "Quando finisce, è finito per sempre".
- **Carrello:** "Non lasciarti sfuggire gli articoli nel carrello".
- **Fedeltà:** "Hai accumulato 500 punti: non lasciarli scadere".
- **Rischio:** "Soddisfatti o rimborsati entro 30 giorni" (riduce la "perdita" di denaro).

**Esempio:**

```text
❌ Male: "Clicca qui per ricevere un coupon da 10 $".
✅ Bene: "Hai un credito di 10 $ che ti aspetta. Usalo prima che scada stanotte!"

❌ Male: "Annulla l'abbonamento".
✅ Bene: "Se annulli, perderai l'accesso ai tuoi 50 progetti salvati".
```

### Effetto falso consenso

**Principio:** le persone tendono a sopravvalutare quanto le proprie opinioni, convinzioni, preferenze, valori e abitudini siano normali e condivisi dagli altri.

**Applicazione:**

- **Test:** tu non sei l'utente: testa con il vero pubblico di riferimento.
- **Ricerca:** usa dati qualitativi (interviste) e quantitativi (analytics).
- **Bias:** usa le "design review alla cieca" per evitare favoritismi personali.
- **Persona:** attieniti alle User Persona definite invece che alle intuizioni personali.
- **Varietà:** testa con utenti di fasce demografiche e abilità diverse.
- **Oggettività:** usa le heatmap per vedere il comportamento reale degli utenti.

**Esempio:**

```text
❌ Male: un designer che decide che una funzionalità è "intuitiva" senza testarla.
✅ Bene: fare un A/B test per vedere quale versione preferiscono gli utenti.

❌ Male: costruire un'app interamente in inglese perché "tutti sanno l'inglese".
✅ Bene: aggiungere la localizzazione in base ai dati reali sulla posizione degli utenti.
```

### Maledizione della conoscenza

**Principio:** un bias cognitivo per cui chi comunica con altre persone dà per scontato, senza rendersene conto, che abbiano le conoscenze di base per capire.

**Applicazione:**

- **Copy:** evita il gergo e usa un linguaggio semplice.
- **Onboarding:** tutorial che partono dal presupposto che l'utente non sappia nulla.
- **Tooltip:** spiega i termini complessi all'hover.
- **Struttura:** progressive disclosure (nascondi le impostazioni avanzate).
- **Etichette:** usa icone + etichette di testo per la navigazione (non affidarti alle sole icone).
- **Supporto:** FAQ complete per chi usa il prodotto per la prima volta.

**Esempio:**

```text
❌ Male: un messaggio di errore che dice "Exception: Null Pointer at 0x0045".
✅ Bene: un messaggio di errore che dice "Qualcosa è andato storto. Prova ad aggiornare la pagina".

❌ Male: far navigare un'app cloud con termini come "S3 Bucket Instances".
✅ Bene: usare termini semplici come "Archivio file".
```

### Effetto trampolino (foot-in-the-door)

**Principio:** gli utenti si impegnano in attività grandi se cominciano da quelle piccole.

**Applicazione:**

- **Funnel:** chiedi l'email prima della carta di credito.
- **Engagement:** chiedi una sola preferenza (per es. "Dark mode?") prima della registrazione.
- **Onboarding:** usa una serie di domande rapide "Sì/No".
- **Trust:** offri un PDF o uno strumento gratuito prima di chiedere un abbonamento.
- **Profilo:** chiedi prima di caricare una foto e solo dopo di compilare la bio.
- **Vendite:** offri un prodotto "tripwire" a basso costo prima del servizio principale.

**Esempio:**

```text
❌ Male: un pulsante "Inizia la prova gratuita" che chiede subito i dati della carta.
✅ Bene: chiedere prima email e password, poi offrire la prova.

❌ Male: un sondaggio che mostra tutte le 50 domande in una sola pagina.
✅ Bene: un sondaggio che inizia con una semplice domanda "Sì/No".
```

---

## 4. Design emotivo (Don Norman)

### I tre livelli di elaborazione

```text
┌─────────────────────────────────────────────────────────────┐
│  VISCERALE (cervello rettiliano)                            │
│  ───────────────────────────────                            │
│  • Reazione immediata e automatica                          │
│  • Prime impressioni (primi 50ms)                           │
│  • Estetica: colori, forme, immagini                        │
│  • "Wow, che bello!"                                        │
├─────────────────────────────────────────────────────────────┤
│  COMPORTAMENTALE (cervello funzionale)                      │
│  ─────────────────────────────────────                      │
│  • Usabilità e funzione                                     │
│  • Piacere di un uso efficace                               │
│  • Performance, affidabilità, facilità                      │
│  • "Funziona esattamente come mi aspettavo!"                │
├─────────────────────────────────────────────────────────────┤
│  RIFLESSIVO (cervello conscio)                              │
│  ─────────────────────────────                              │
│  • Pensiero consapevole e significato                       │
│  • Identità e valori personali                              │
│  • Memoria a lungo termine e fedeltà                        │
│  • "Questo brand rappresenta chi sono"                      │
└─────────────────────────────────────────────────────────────┘
```

### Progettare per ciascun livello

**Viscerale:**

```css
/* Una prima impressione bellissima */
.hero {
  background: linear-gradient(135deg, #0ea5e9 0%, #14b8a6 100%);
  color: white;
}

/* Microinterazioni piacevoli */
.button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

**Comportamentale:**

```javascript
// Feedback immediato
button.onclick = () => {
  button.disabled = true;
  button.textContent = 'Saving...';

  save().then(() => {
    showSuccess('Saved!');  // Conferma immediata
  });
};
```

**Riflessivo:**

```html
<!-- Storia e valori del brand -->
<section class="about">
  <h2>Why We Exist</h2>
  <p>We believe technology should empower, not complicate...</p>
</section>

<!-- Riprova sociale legata all'identità -->
<blockquote>
  "This tool helped me become the designer I wanted to be."
</blockquote>
```

---

## 5. Sistema per costruire la fiducia

### Categorie di segnali di fiducia

| Categoria | Elementi | Implementazione |
| --- | --- | --- |
| **Sicurezza** | SSL, badge, crittografia | Lucchetto visibile, loghi di sicurezza sui form |
| **Riprova sociale** | Recensioni, testimonianze, loghi | Valutazioni a stelle, foto dei clienti, loghi dei brand |
| **Trasparenza** | Policy, prezzi, contatti | Link chiari, nessun costo nascosto, indirizzo reale |
| **Professionalità** | Qualità del design, coerenza | Nessun elemento rotto, branding coerente |
| **Autorità** | Certificazioni, premi, media | "Visto su...", certificazioni di settore |

### Dove posizionare i segnali di fiducia

```text
┌──────────────────────────────────────────────────────┐
│  HEADER: banner di fiducia ("Spedizione gratuita |   │
│          Reso entro 30 giorni | Checkout sicuro")    │
├──────────────────────────────────────────────────────┤
│  HERO: riprova sociale ("Scelto da oltre 10.000")    │
├──────────────────────────────────────────────────────┤
│  PRODOTTO: recensioni visibili, badge di sicurezza   │
├──────────────────────────────────────────────────────┤
│  CHECKOUT: icone di pagamento, badge SSL, garanzia   │
├──────────────────────────────────────────────────────┤
│  FOOTER: contatti, policy, certificazioni            │
└──────────────────────────────────────────────────────┘
```

### Pattern CSS per costruire fiducia

```css
/* Stile del badge di fiducia */
.trust-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #F0FDF4;  /* Verde chiaro = sicurezza */
  border-radius: 2px; /* Angoli netti per la fiducia = senso di precisione */
  font-size: 14px;
  color: #166534;
}

/* Indicatore di form sicuro */
.secure-form::before {
  content: '🔒 Secure form';
  display: block;
  font-size: 12px;
  color: #166534;
  margin-bottom: 8px;
}

/* Card della testimonianza */
.testimonial {
  display: flex;
  gap: 16px;
  padding: 24px;
  background: white;
  border-radius: 16px; /* Amichevole = raggio più ampio */
  box-shadow: var(--shadow-sm);
}

.testimonial-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;  /* Foto reali > iniziali */
}
```

---

## 6. Gestione del carico cognitivo

### I tre tipi di carico cognitivo

| Tipo | Definizione | Ruolo del designer |
| --- | --- | --- |
| **Intrinseco** | Complessità propria dell'attività | Suddividila in step più piccoli |
| **Estraneo** | Carico dovuto a un design scadente | Eliminalo! |
| **Pertinente** (germane) | Sforzo dedicato all'apprendimento | Sostienilo e incoraggialo |

### Strategie di riduzione

#### 1. Semplifica (riduci il carico estraneo)

```css
/* Rumore visivo → pulizia */
.card-busy {
  border: 2px solid red;
  background: linear-gradient(...);
  box-shadow: 0 0 20px ...;
  /* Troppo! */
}

.card-clean {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px -10px rgba(0,0,0,0.1);
  /* Calmo, focalizzato */
}
```

#### 2. Suddividi le informazioni in blocchi

```html
<!-- Opprimente -->
<form>
  <!-- 15 campi tutti insieme -->
</form>

<!-- A blocchi -->
<form>
  <fieldset>
    <legend>Step 1: Personal Info</legend>
    <!-- 3-4 campi -->
  </fieldset>
  <fieldset>
    <legend>Step 2: Shipping</legend>
    <!-- 3-4 campi -->
  </fieldset>
</form>
```

#### 3. Progressive disclosure

```html
<!-- Nascondi la complessità finché non serve -->
<div class="filters">
  <div class="filters-basic">
    <!-- Filtri comuni visibili -->
  </div>
  <button onclick="toggleAdvanced()">
    Advanced Options ▼
  </button>
  <div class="filters-advanced" hidden>
    <!-- Filtri complessi nascosti -->
  </div>
</div>
```

#### 4. Usa pattern familiari

```text
✅ Posizione standard della navigazione
✅ Significati delle icone che l'utente si aspetta (🔍 = ricerca)
✅ Layout dei form convenzionali
✅ Gesture comuni (swipe, pinch)
```

#### 5. Alleggerisci la memoria dell'utente

```html
<!-- Non costringere gli utenti a ricordare -->
<label>
  Card Number
  <input type="text" inputmode="numeric"
         autocomplete="cc-number"
         placeholder="1234 5678 9012 3456">
</label>

<!-- Mostra cosa hanno inserito -->
<div class="order-summary">
  <p>Shipping to: <strong>John Doe, 123 Main St...</strong></p>
  <a href="#">Edit</a>
</div>
```

---

## 7. Design persuasivo (etico)

### Tecniche di persuasione etica

| Tecnica | Uso etico | Dark pattern (da evitare) |
| --- | --- | --- |
| **Scarsità** | Scorte reali | Timer con conto alla rovescia finti |
| **Riprova sociale** | Recensioni autentiche | Testimonianze false |
| **Autorità** | Credenziali reali | Badge ingannevoli |
| **Urgenza** | Scadenze reali | FOMO artificiale |
| **Impegno** | Salvataggio dei progressi | Far sentire in colpa l'utente |

### Pattern di nudge

**Default intelligenti:**

```html
<!-- Preseleziona l'opzione consigliata -->
<input type="radio" name="plan" value="monthly">
<input type="radio" name="plan" value="annual" checked>
  Annual (Save 20%)
```

**Ancoraggio:**

```html
<!-- Mostra il prezzo originale per inquadrare lo sconto -->
<div class="price">
  <span class="original">$99</span>
  <span class="current">$79</span>
  <span class="savings">Save 20%</span>
</div>
```

**Riprova sociale:**

```html
<!-- Attività in tempo reale -->
<div class="activity">
  <span class="avatar">👤</span>
  <span>Sarah from NYC just purchased</span>
</div>

<!-- Riprova aggregata -->
<p>Join 50,000+ designers who use our tool</p>
```

**Avanzamento e impegno:**

```html
<!-- Mostra l'avanzamento per incoraggiare il completamento -->
<div class="progress">
  <div class="progress-bar" style="width: 60%"></div>
  <span>60% complete - almost there!</span>
</div>
```

---

## 8. Guida rapida alle User Persona

### Gen Z (nati nel 1997-2012)

```text
CARATTERISTICHE:
- Nativi digitali, mobile-first
- Danno valore ad autenticità e diversità
- Soglia di attenzione breve
- Apprendono soprattutto per immagini

APPROCCIO DI DESIGN:
├── Colori: vivaci, ipercolori, gradienti decisi
├── Tipografia: grande, variabile, sperimentale
├── Layout: scroll verticale, nativo per mobile
├── Interazioni: veloci, gamificate, basate su gesture
├── Contenuti: video brevi, meme, stories
└── Trust: recensioni dei pari > autorità
```

### Millennial (nati nel 1981-1996)

```text
CARATTERISTICHE:
- Preferiscono le esperienze agli oggetti
- Si informano prima di comprare
- Attenti alle questioni sociali
- Sensibili al prezzo ma attenti alla qualità

APPROCCIO DI DESIGN:
├── Colori: pastelli tenui, toni terra
├── Tipografia: sans-serif pulito e leggibile
├── Layout: responsive, basato su card
├── Interazioni: animazioni fluide e motivate
├── Contenuti: orientati ai valori, trasparenti
└── Trust: recensioni, sostenibilità, valori
```

### Gen X (nati nel 1965-1980)

```text
CARATTERISTICHE:
- Indipendenti, autosufficienti
- Danno valore all'efficienza
- Scettici verso il marketing
- Discreta dimestichezza con la tecnologia

APPROCCIO DI DESIGN:
├── Colori: professionali, affidabili
├── Tipografia: familiare, conservativa
├── Layout: gerarchia chiara, tradizionale
├── Interazioni: funzionali, non appariscenti
├── Contenuti: diretti, basati sui fatti
└── Trust: competenza, risultati comprovati
```

### Baby Boomer (nati nel 1946-1964)

```text
CARATTERISTICHE:
- Attenti ai dettagli
- Fedeli quando si fidano
- Apprezzano il servizio personale
- Meno sicuri con la tecnologia

APPROCCIO DI DESIGN:
├── Colori: alto contrasto, palette semplice
├── Tipografia: grande (18px+), alto contrasto
├── Layout: semplice, lineare, arioso
├── Interazioni: minime, feedback chiaro
├── Contenuti: completi, dettagliati
└── Trust: numeri di telefono, persone reali
```

---

## 9. Mappa emozioni-colori

```text
┌────────────────────────────────────────────────────┐
│  EMOZIONE      │  COLORI             │  USO        │
├────────────────┼─────────────────────┼─────────────┤
│  Fiducia       │  Blu, verde         │  Finanza    │
│  Eccitazione   │  Rosso, arancione   │  Saldi      │
│  Calma         │  Blu, verde tenue   │  Benessere  │
│  Lusso         │  Nero, oro          │  Premium    │
│  Creatività    │  Verde acqua, rosa  │  Arte       │
│  Energia       │  Giallo, arancione  │  Sport      │
│  Natura        │  Verde, marrone     │  Eco        │
│  Felicità      │  Giallo, arancione  │  Bambini    │
│  Raffinatezza  │  Grigio, blu navy   │  Corporate  │
│  Urgenza       │  Rosso              │  Errori     │
└────────────────┴─────────────────────┴─────────────┘
```

---

## 10. Checklist di psicologia

### Prima del lancio

- [ ] **Legge di Hick:** non più di 7 scelte nella navigazione. Hai ridotto le scelte per limitare l'affaticamento decisionale?
- [ ] **Legge di Fitts:** le CTA primarie sono grandi e raggiungibili. I pulsanti più importanti sono facili da toccare su mobile?
- [ ] **Legge di Miller:** i contenuti sono suddivisi in blocchi adeguati. Le informazioni sono raggruppate in unità digeribili da 5-7?
- [ ] **Legge di Jakob:** il sito segue le convenzioni web standard che gli utenti già conoscono?
- [ ] **Soglia di Doherty:** il sistema dà un feedback entro 400ms? Ci sono gli skeleton screen?
- [ ] **Legge di Tesler:** dove possibile, la complessità è stata spostata dall'utente al sistema?
- [ ] **Legge di Parkinson:** ci sono funzionalità come il "checkout con un clic" per ridurre al minimo il tempo di completamento?
- [ ] **Von Restorff:** la CTA primaria risalta visivamente rispetto a tutti gli altri elementi?
- [ ] **Posizione seriale:** le informazioni più critiche sono proprio all'inizio o alla fine delle liste?
- [ ] **Leggi della Gestalt:** gli elementi correlati sono raggruppati fisicamente (prossimità) o dentro una card (regione comune)?
- [ ] **Effetto Zeigarnik:** ci sono indicatori visivi (come le barre di avanzamento) per le attività incompiute?
- [ ] **Gradiente dell'obiettivo:** l'utente riceve un "vantaggio iniziale" (per es. 20% di avanzamento) che lo incoraggi a completare?
- [ ] **Regola del picco-fine:** la schermata finale di "successo" crea un momento di delight?
- [ ] **Rasoio di Occam:** sono stati eliminati gli elementi visivi o funzionali non necessari?
- [ ] **Estetica-usabilità:** la UI è abbastanza curata da conquistare la fiducia iniziale dell'utente?
- [ ] **Fiducia e autorità:** badge di sicurezza, recensioni e certificazioni di esperti sono visibili?
- [ ] **Riprova sociale:** numeri reali di utenti o testimonianze sono visibili nei punti di decisione?
- [ ] **Scarsità e urgenza:** se le usi, la scarsità è reale ed etica (per es. scorte davvero basse)?
- [ ] **Avversione alla perdita:** il copy mette in risalto ciò che l'utente può conservare, non solo ciò che può guadagnare?
- [ ] **Ancoraggio:** i prezzi sono presentati in modo che la scelta desiderata sembri un ottimo affare?
- [ ] **Legge di Postel:** il sistema è abbastanza flessibile da accettare vari formati di input senza dare errore?
- [ ] **Falso consenso:** il design è stato testato con utenti reali e non solo con il team interno?
- [ ] **Maledizione della conoscenza:** il copy è privo di gergo tecnico e facile da capire per un principiante?
- [ ] **Effetto trampolino:** il funnel parte da attività con poco attrito (per es. solo l'email)?
- [ ] **Carico cognitivo:** il rumore visivo estraneo è ridotto al minimo, così l'interfaccia resta pulita?
- [ ] **Design emotivo:** palette e immagini suscitano la reazione viscerale voluta?
- [ ] **Feedback:** tutti gli elementi interattivi hanno stati hover, active e di successo immediati?
- [ ] **Accessibilità:** il rapporto di contrasto è sufficiente e il sito si naviga da tastiera e con lo screen reader?
- [ ] **Prägnanz:** icone e forme sono abbastanza semplici da essere riconosciute a colpo d'occhio?
- [ ] **Figura/sfondo:** è chiaro quale elemento è in primo piano (per es. con ombre o scrim per le modali)?
