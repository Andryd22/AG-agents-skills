# scroll-world — Checklist di QA nel browser

Dettagli per il passo 8 di SKILL.md. Eseguila dopo che il controllo SSIM delle giunture
(`pipeline.md` §5c) è verde.

Poi guida la pagina in un browser headless e **verifica la continuità dei frame alle giunture**
da cima a fondo:

- Fai screenshot alle posizioni di scroll appena prima e appena dopo ogni giuntura. I due frame
  devono essere quasi identici (l'ultimo frame del tuffo == il primo frame del connettore). Se
  scattano, hai usato l'immagine del diorama invece del frame reale renderizzato (rifai il passo
  5), oppure la fascia di dissolvenza è troppo corta.
- Controlla che il primo disegno sia pulito: il poster (frame estratto) compare subito, e quando
  il video subentra al poster l'immagine non si sposta (se si sposta, `poster` manca o punta
  all'immagine: passo 6).
- Controlla gli errori in console, verifica che `video.seekable.end(0) > 0` (il blob funziona) e
  che `currentTime` segua lo scroll lungo la fascia di ogni clip.
- **Ripieghi sulle immagini (in ogni lavoro, costa poco controllarli):**
  - Risparmio dati: emula `navigator.connection.saveData = true` (override di DevTools o uno
    script di avvio): la pagina deve mostrarsi come immagini con dissolvenze, zero download di
    clip nel pannello Network.
  - Risparmio energetico: il più difficile da emulare. Su un iPhone vero attivalo e verifica che
    al primo tocco la pagina passi alle immagini invece di un video congelato. Surrogato emulato:
    fai restituire a `HTMLMediaElement.play` una promise rifiutata, tocca, verifica la modalità immagini.
  - Fascia tablet: il viewport dell'iPad (834×1194, touch) deve scaricare la clip **desktop**
    (pannello Network), non la `-m.mp4`, pur comportandosi da dispositivo touch.
- **Mobile — checklist completa solo se l'utente ha scelto una fascia mobile (passo 1.6).**
  Per un lavoro con ritaglio sicuro basta un controllo veloce in un viewport da telefono: la
  pagina si carica, i poster si vedono, niente si sovrappone; le protezioni del motore coprono il
  degrado. Per le fasce mobile (su un telefono vero o emulato, in verticale e in orizzontale):
  - Emula un viewport da telefono **con la CPU rallentata 4-6×** e scorri veloce: la clip deve
    seguire senza congelarsi (sono i seek raggruppati + le codifiche `-m.mp4` a farla tenere).
  - Verifica che la prima scena si veda subito (la sua immagine è il poster) e che il video subentri
    appena scorri: nessuna scena vuota o nera (la correzione della preparazione per iOS). Prova in
    particolare Safari su iOS: è quello che torna vuoto se la correzione si rompe.
  - Verifica che su mobile venga servita davvero la variante `-m.mp4` (pannello Network), e su
    desktop il master pesante a 1080p.
  - Scorri piano in modo che la barra degli indirizzi si chiuda: la pagina **non deve saltare** (i
    resize solo in altezza vengono ignorati sui dispositivi touch). Ruota il dispositivo: il layout
    deve ricomporsi pulito.
  - In verticale una clip 16:9 viene ritagliata al centro; verifica che il soggetto principale si
    legga ancora. Se il soggetto di una scena hero sta fuori centro e viene tagliato, ricomponilo
    (prompts.md) o genera una variante 9:16 per quella scena.
- Controlla il movimento ridotto (deve passare alle immagini: niente video, niente particelle).
