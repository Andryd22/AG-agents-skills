/* ============================================================================
   scroll-world — motore portabile di voli di camera guidati dallo scroll
   ----------------------------------------------------------------------------
   Indipendente dal framework. JavaScript puro, zero dipendenze. Costruisce il suo DOM
   e inietta il suo CSS (con prefisso) in un contenitore che gli passi, quindi va in
   HTML semplice, Next.js (chiamalo da un ref/useEffect), Vue (onMounted), una pagina
   renderizzata dal server, qualsiasi cosa.

   USO
     mountScrollWorld(document.getElementById('world'), {
       brand: { name: 'Pearl & Co.', href: '#top' },
       diveScroll: 1.3,   // altezze di viewport di scroll per ogni clip di tuffo
       connScroll: 0.9,   // ...per ogni clip connettore
       hint: 'scorri per entrare in volo',
       nav: true,         // mostra la navigazione delle sezioni in alto
       atmosphere: true,  // leggero gradiente + particelle in deriva dietro le clip
       scrollMobileFactor: 1.2,  // scroll in più per segmento su mobile (nei viewport
                                 // piccoli lo stesso volo sembra più veloce; la pratica
                                 // del settore è uno scroll mobile PIÙ LUNGO)
       sections: [
         { id, label, still, poster, posterMobile, clip, clipMobile, accent,
                          // `poster` = il PRIMO FRAME ESTRATTO dalla clip codificata
                          // (pipeline.md §5b). Si vede mentre la clip carica, così il
                          // passaggio da immagine a video è identico al pixel (niente scatti).
                          // `posterMobile` = lo stesso, estratto dalla codifica mobile/verticale
                          // (collegalo ogni volta che clipMobile ha un'inquadratura diversa).
                          // Se manca si usa `still`; `still` resta la grafica della
                          // modalità immagini / senza clip.
           scroll: 1.6,   // facoltativo, sostituisce diveScroll per questa sezione: più
                          // scroll = sosta più lenta e lunga in questa scena
           linger: 0.5,   // facoltativo 0..1: rimappa il tempo in modo che la camera si
                          // assesti a metà scena (proprio dove i testi sono al massimo) e
                          // vada più veloce ai bordi. 0 = lineare (predefinito). Tienilo ≤ 0.6; 1 = pausa piena.
           eyebrow, title, body, tags:[…],
           cta:{ primary:{label,href}, secondary:{label,href} } }, // solo l'ultima sezione
         …
       ],
       connectors: [clipUrl, …],          // lunghezza = sections.length - 1 (null ammessi)
       connectorsMobile: [clipUrl, …],    // facoltativi, connettori più leggeri per i telefoni (stessa lunghezza)

   MOBILE (le varianti clipMobile/connectorsMobile sono le fasce mobile facoltative;
   il resto della gestione dei telefoni qui sotto è sempre attivo)
     Due assi indipendenti, separati di proposito:
     - LIVELLO DELLE CLIP (quale file): lo decide la classe del dispositivo — lato corto
       dello schermo ≤600 px CSS = telefono → `clipMobile`/`posterMobile`; tablet (iPad Pro
       compreso) e desktop ricevono il master completo. NON lo decide il tipo di puntatore:
       iPadOS dichiara un puntatore grossolano e uno user agent da Mac, ma ha schermo e
       decoder da desktop.
     - PROTEZIONI (come si comporta): con puntatore grossolano / viewport ≤860 px il motore
       raggruppa i seek (non imposta mai un nuovo currentTime mentre il decoder è ancora in
       `seeking`: gli scorrimenti veloci non si accumulano e non congelano), usa un passo di
       seek più largo, tiene il poster finché la clip non disegna davvero, prepara ogni video
       (play→pause muto) al primo tocco (correzione del video vuoto su iOS), allunga lo scroll
       (`scrollMobileFactor`), toglie le particelle e ignora i resize dovuti solo alla barra
       degli indirizzi (niente salti dello scroll).
     MODALITÀ IMMAGINI (ripiego automatico, mai da configurare): la pagina passa alle
     immagini che si dissolvono l'una nell'altra mentre scorri — nessun caricamento o
     decodifica di video — quando l'utente lo ha chiesto (`prefers-reduced-motion`,
     risparmio dati) o il sistema blocca il video a runtime (il Risparmio energetico di iOS
     rifiuta perfino un play() muto; rilevato al primo tocco).
     I segnali di rete solo di Chromium (`navigator.connection.saveData`/`effectiveType`)
     servono solo a ridurre: saveData → modalità immagini, 2g/3g → finestra di
     precaricamento delle clip più stretta. iOS non espone niente di tutto questo, quindi la
     base resta prudente (prima i poster, download pigro dei blob vicino al viewport) per tutti.
     Niente di questo è obbligatorio: una configurazione con solo `clip`/`connectors`
     funziona anche sui telefoni; le varianti mobile la rendono solo più leggera e fluida.

   TEMA (proprietà CSS personalizzate; impostale sul contenitore o su :root)
     --sw-bg         sfondo della pagina (uguale allo sfondo delle scene per poster senza giunture)
     --sw-ink        testo principale
     --sw-ink-soft   testo secondario
     --sw-accent     accent predefinito (ogni sezione lo cambia con il suo `accent`)
     --sw-font-display / --sw-font-body

   SEO / TESTI STATICI
     Il motore costruisce il DOM lato client, quindi da sola la pagina non ha testo
     indicizzabile. Metti una versione in markup semplice dei testi (h1 + h2/p per sezione,
     link veri) dentro il contenitore, in un blocco marcato `data-sw-seo`: il motore lo
     nasconde al montaggio e non disturba mai il livello visivo, ma esiste nell'HTML servito
     per crawler, anteprime dei link e visitatori senza JS (vedi index-template.html).

   REQUISITI DEL MATERIALE
     - clip codificate alla risoluzione nativa, crf~20, -g 8, +faststart, senza audio (vedi pipeline.md)
     - gli estremi dei connettori sono i frame REALI dei tuffi vicini (vedi il passo 5 di SKILL)
     - poster estratti dal primo frame delle clip CODIFICATE (pipeline.md §5b)
     - (facoltative) varianti mobile a ~720p, -g 4 per uno scrub più fluido sui telefoni
   Il motore carica ogni clip come Blob (seek sempre possibile) e fa lo scrub di currentTime;
   NON dipende dal supporto HTTP per gli intervalli di byte.
   ========================================================================== */

function mountScrollWorld(container, config) {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Le PROTEZIONI (passo di seek, preparazione, particelle, filtro dei resize) dipendono dal
  // tipo di input e dal viewport: `coarse` si legge una volta (il tipo di input non cambia a
  // metà sessione); la query ≤860px si legge dal vivo con isMobile(), così un resize su desktop
  // o il pulsante di DevTools cambiano il comportamento dei seek senza ricaricare.
  const coarse = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
  const smallMQ = window.matchMedia('(max-width: 860px)');
  const isMobile = () => coarse || smallMQ.matches;
  // Il LIVELLO DELLE CLIP dipende dalla classe del dispositivo, NON dal tipo di input: un iPad Pro
  // ha il puntatore grossolano ma schermo e decoder da desktop, quindi riceve il master a 1080p,
  // con le protezioni touch qui sopra sempre attive. screen.* non cambia con la rotazione né con
  // il resize della finestra; il lato corto di un telefono è ≤ ~500 px CSS, i tablet partono da 744.
  const phoneClass = Math.min(screen.width, screen.height) <= 600;
  // I segnali di rete ci sono solo in Chromium (iOS/Safari/Firefox non espongono niente):
  // usali solo come segnale per *ridurre* sopra un'impostazione prudente, mai come
  // condizione per dare l'esperienza migliore.
  const conn = navigator.connection;
  const dataSaver = !!(conn && conn.saveData);
  const slowNet = !!(conn && /^(slow-2g|2g|3g)$/.test(conn.effectiveType || ''));
  // Modalità immagini: la pagina diventa le immagini che si dissolvono l'una nell'altra mentre
  // scorri, senza caricare né decodificare video. Si attiva subito con prefers-reduced-motion e
  // il risparmio dati, e a runtime quando il Risparmio energetico di iOS blocca il video
  // (vedi enterStillsMode/primeVideo).
  let stillsOnly = reduce || dataSaver;
  const SECTIONS = config.sections || [];
  const CONNECTORS = config.connectors || [];
  const CONNECTORS_M = config.connectorsMobile || [];
  const DIVE_W = config.diveScroll || 1.3;
  const CONN_W = config.connScroll || 0.9;
  const CROSSFADE = (config.crossfade != null) ? config.crossfade : 0.12;  // larghezza della dissolvenza alla giuntura (vh)
  const N = SECTIONS.length;
  if (!N) return;

  injectCSS();
  container.classList.add('sw-root');
  // Testi SEO renderizzati dal server (crawler e visitatori senza JS li leggono dall'HTML);
  // quando il motore si monta, subentra il livello visivo e il blocco statico si nasconde.
  container.querySelectorAll('[data-sw-seo]').forEach(n => { n.hidden = true; });

  // ---- costruisce la catena alternata dei segmenti: dive0, conn0, dive1, … diveN-1 ----
  const SEGMENTS = [];
  SECTIONS.forEach((s, i) => {
    const dive = { kind: 'dive', si: i, clip: s.clip, clipM: s.clipMobile, still: s.still,
                   poster: s.poster, posterM: s.posterMobile,
                   accent: s.accent, w: s.scroll || DIVE_W, linger: s.linger || 0 };
    SEGMENTS.push(dive);
    s._seg = dive;
    // Un connettore è facoltativo: se connectors[i] è falsy, i due tuffi si dissolvono
    // direttamente (senza sorvolo). Così la pagina resta completa anche quando un connettore
    // non si riesce a generare (es. un falso positivo del filtro dei contenuti).
    if (i < N - 1 && CONNECTORS[i]) {
      SEGMENTS.push({ kind: 'conn', si: i, clip: CONNECTORS[i], clipM: CONNECTORS_M[i],
                      still: SECTIONS[i + 1].still, poster: SECTIONS[i + 1].poster,
                      posterM: SECTIONS[i + 1].posterMobile,
                      accent: SECTIONS[i + 1].accent, w: CONN_W });
    }
  });
  const NSEG = SEGMENTS.length;

  // ---- DOM ----
  const sky = el('div', 'sw-sky');
  if (config.atmosphere !== false) {
    sky.appendChild(el('div', 'sw-sky__grad'));
    sky.appendChild(el('div', 'sw-sky__glow'));
  }
  const particles = el('div', 'sw-particles'); sky.appendChild(particles);

  const scrollbar = el('div', 'sw-scrollbar');
  const scrollbarFill = el('span'); scrollbar.appendChild(scrollbarFill);

  const topbar = el('div', 'sw-topbar');
  if (config.brand) {
    const brand = el('a', 'sw-brand'); brand.href = (config.brand.href || '#');
    brand.appendChild(el('span', 'sw-brand__mark'));
    const nm = el('span', 'sw-brand__name'); nm.textContent = config.brand.name || ''; brand.appendChild(nm);
    topbar.appendChild(brand);
  }
  const nav = el('nav', 'sw-nav'); if (config.nav !== false) topbar.appendChild(nav);
  if (config.cta && config.cta.label) {
    const c = el('a', 'sw-topcta'); c.href = config.cta.href || '#'; c.textContent = config.cta.label;
    topbar.appendChild(c);
  }

  const stage = el('div', 'sw-stage');
  const copylayer = el('div', 'sw-copylayer');
  const route = el('div', 'sw-route');
  const hint = el('div', 'sw-hint');
  const hintText = el('span'); hintText.textContent = config.hint || 'scorri'; hint.appendChild(hintText);
  hint.appendChild(el('i'));
  const track = el('div', 'sw-track');

  [sky, scrollbar, topbar, stage, copylayer, route, hint, track].forEach(n => container.appendChild(n));

  // scene dei segmenti
  SEGMENTS.forEach(s => {
    const scene = el('div', 'sw-scene'); scene.style.setProperty('--sw-accent', s.accent || '');
    const img = el('img', 'sw-scene__still'); img.alt = ''; img.decoding = 'async'; img.loading = 'lazy';
    // Meglio il poster dal frame estratto (identico al pixel al primo frame della clip, così
    // il passaggio da immagine a video non scatta), quello della codifica che il dispositivo
    // riceverà. In modalità immagini la clip non si carica mai, quindi l'immagine sorgente,
    // più fedele, è la scelta migliore come immagine fissa.
    const pref = phoneClass ? (s.posterM || s.poster) : s.poster;
    const posterSrc = (!stillsOnly && pref) ? pref : s.still;
    if (posterSrc) img.src = posterSrc;
    scene.appendChild(img); stage.appendChild(scene);
    s.el = scene; s.img = img; s.video = null; s.hasClip = false;
    s.loading = false; s.ready = false; s.cur = 0; s.target = 0; s.visible = false;
  });

  // testi, percorso e navigazione per sezione
  const copies = [], dots = [];
  SECTIONS.forEach((s, i) => {
    const c = el('article', 'sw-copy'); c.style.setProperty('--sw-accent', s.accent || '');
    c.innerHTML =
      `<span class="sw-copy__num">${pad(i + 1)} / ${pad(N)}</span>` +
      (s.eyebrow ? `<span class="sw-copy__eyebrow">${esc(s.eyebrow)}</span>` : '') +
      (s.title ? `<h2 class="sw-copy__title">${esc(s.title)}</h2>` : '') +
      (s.body ? `<p class="sw-copy__body">${esc(s.body)}</p>` : '') +
      (s.tags && s.tags.length ? `<ul class="sw-copy__tags">${s.tags.map(t => `<li>${esc(t)}</li>`).join('')}</ul>` : '') +
      (s.cta ? `<div class="sw-copy__cta">${ctaBtns(s.cta)}</div>` : '');
    copylayer.appendChild(c); copies.push(c);

    const dot = el('button', 'sw-route__dot'); dot.style.setProperty('--sw-accent', s.accent || '');
    dot.innerHTML = `<span class="sw-route__label">${esc(s.label || '')}</span><i></i>`;
    dot.addEventListener('click', () => jumpTo(i)); route.appendChild(dot); dots.push(dot);

    if (config.nav !== false) {
      const b = el('button', 'sw-nav__item'); b.textContent = s.label || '';
      b.addEventListener('click', () => jumpTo(i)); nav.appendChild(b);
    }
  });

  // ---- calcoli ----
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const smooth = x => { x = clamp(x); return x * x * (3 - 2 * x); };
  // Sosta per sezione: rimappatura monotona scroll→tempo, così la camera si assesta a metà
  // scena (dove i testi sono al massimo) e va più veloce vicino alle giunture. L=0 lineare,
  // L=1 pausa piena a metà scena. Sempre f(0)=0, f(1)=1, quindi i frame delle giunture non cambiano.
  const lingerEase = (x, L) => { L = clamp(L); const c = x - 0.5; return (1 - L) * x + L * (4 * c * c * c + 0.5); };
  let vh = window.innerHeight, stageX = 0, totalW = 0, activeIndex = -1, ticking = false;
  let laidOutW = window.innerWidth;   // larghezza con cui è stato calcolato il layout attuale (vedi onResize)

  function layout() {
    vh = window.innerHeight;
    laidOutW = window.innerWidth;
    stageX = window.innerWidth > 860 ? 4 : 0;
    // Nei viewport piccoli un volo di camera sembra più veloce che in quelli grandi, quindi su
    // mobile ogni segmento ha più scroll (pratica del settore: a parità di sequenza, lo scroll
    // mobile è PIÙ LUNGO di quello desktop). Si cambia con scrollMobileFactor.
    const wf = isMobile() ? (config.scrollMobileFactor != null ? config.scrollMobileFactor : 1.2) : 1;
    let off = 0;
    SEGMENTS.forEach(s => { s.start = off * vh; off += s.w * wf; s.end = off * vh; });
    totalW = off;
    track.style.height = (totalW * vh + vh) + 'px';   // +1vh perché l'ultimo volo arrivi in fondo
    read();
  }

  function jumpTo(i) {
    const seg = SECTIONS[i]._seg;
    window.scrollTo({ top: seg.start + (seg.end - seg.start) * 0.5, behavior: reduce ? 'auto' : 'smooth' });
  }

  function enterStillsMode() {
    if (stillsOnly) return;
    stillsOnly = true;
    SEGMENTS.forEach(s => {
      if (s.video) {
        try { s.video.pause(); } catch (e) {}
        try { URL.revokeObjectURL(s.video.src); } catch (e) {}
        s.video.remove();
      }
      s.el.classList.remove('has-clip');
      s.video = null; s.hasClip = false; s.ready = false; s.loading = false;
    });
    read();
  }

  function loadClip(s) {
    if (stillsOnly || s.loading || !s.clip) return;
    s.loading = true;
    // Ai dispositivi di classe telefono servi la codifica mobile più leggera, se c'è
    // (tablet e desktop ricevono il master completo: vedi phoneClass sopra).
    const url = (phoneClass && s.clipM) ? s.clipM : s.clip;
    fetch(url).then(r => r.ok ? r.blob() : Promise.reject(new Error('404')))
      .then(blob => {
        const v = document.createElement('video');
        v.className = 'sw-scene__video';
        v.muted = true; v.playsInline = true; v.preload = 'auto';
        v.setAttribute('muted', ''); v.setAttribute('playsinline', '');
        v.src = URL.createObjectURL(blob);
        v.addEventListener('loadedmetadata', () => { s.ready = true; read(); });
        // Mostra il video (nascondi il poster) solo quando un frame vero è stato disegnato:
        // su iOS un video muto con un seek ma mai riprodotto resta vuoto, quindi nascondere
        // l'immagine già ai metadati farebbe lampeggiare una scena vuota.
        v.addEventListener('seeked', () => { s.el.classList.add('has-clip'); }, { once: true });
        v.addEventListener('loadeddata', () => { try { v.pause(); } catch (e) {} if (userReady) primeVideo(v); });
        s.el.appendChild(v); s.video = v; s.hasClip = true;
      }).catch(() => { s.loading = false; });
  }

  function read() {
    const y = window.scrollY || window.pageYOffset;
    const fade = CROSSFADE * vh;
    let ci = 0;
    for (let i = 0; i < NSEG; i++) if (y >= SEGMENTS[i].start) ci = i;

    // Con una connessione lenta (segnale solo di Chromium) restringi la finestra di
    // precaricamento: scarica la clip in cui sei, non quelle vicine. Tutti gli altri
    // precaricano ±1.6 viewport.
    const lookahead = slowNet ? 0.4 : 1.6;
    for (let i = 0; i < NSEG; i++) {
      const s = SEGMENTS[i];
      if (y > s.start - lookahead * vh && y < s.end + lookahead * vh) loadClip(s);
      const local = clamp((y - s.start) / (s.end - s.start), 0, 1);
      s.target = s.linger ? lingerEase(local, s.linger) : local;
      let outside = 0;
      if (y < s.start) outside = s.start - y; else if (y > s.end) outside = y - s.end;
      const op = smooth(1 - outside / fade);
      s.el.style.opacity = op; s.visible = op > 0.001;
      s.el.style.zIndex = (i === ci) ? '120' : String(100 + Math.round(op * 10));
      if (!s.hasClip || !s.ready) {
        const sc = reduce ? 1 : 1.03 + local * 0.14;
        s.img.style.transform = `translateX(${stageX - 2}vw) scale(${sc.toFixed(3)})`;
      }
    }

    for (let i = 0; i < N; i++) {
      const seg = SECTIONS[i]._seg;
      const pr = clamp((y - seg.start) / (seg.end - seg.start), 0, 1);
      const before = y < seg.start, after = y > seg.end;
      let cop;
      if (i === 0) cop = after ? 0 : smooth(1 - pr / 0.62);            // accoglie all'arrivo
      else if (i === N - 1) cop = before ? 0 : smooth(pr / 0.4);       // tiene la CTA alla fine
      else cop = (before || after) ? 0 : smooth(1 - Math.abs(pr - 0.5) / 0.5);
      const c = copies[i];
      c.style.opacity = cop;
      c.style.transform = reduce ? 'none' : `translateY(${(0.5 - pr) * 4}vh)`;
      c.style.pointerEvents = cop > 0.5 ? 'auto' : 'none';
    }

    const cur = SEGMENTS[ci];
    const near = clamp(cur.kind === 'dive' ? cur.si
      : (((y - cur.start) / (cur.end - cur.start)) > 0.5 ? cur.si + 1 : cur.si), 0, N - 1);
    if (near !== activeIndex) {
      activeIndex = near;
      dots.forEach((d, k) => d.classList.toggle('is-active', k === near));
      nav.querySelectorAll('.sw-nav__item').forEach((n, k) => n.classList.toggle('is-active', k === near));
      container.style.setProperty('--sw-accent', SECTIONS[near].accent || '');
    }
    scrollbarFill.style.transform = `scaleX(${clamp(y / (totalW * vh))})`;
    hint.style.opacity = clamp(1 - y / (0.5 * vh));
    if (particles) particles.style.transform = `translate3d(0, ${-y * 0.05}px, 0)`;
    ticking = false;
  }

  function raf() {
    const eps = isMobile() ? 0.02 : 0.008;   // passo di seek più largo sui telefoni = meno decodifiche
    for (let i = 0; i < NSEG; i++) {
      const s = SEGMENTS[i];
      if (!s.hasClip || !s.ready || !s.video) continue;
      // Mai accodare un seek mentre il decoder sta ancora risolvendo il precedente.
      // Sui telefoni uno scorrimento veloce accumulerebbe i seek e congelerebbe la clip;
      // cur continua a interpolare, quindi appena il decoder è libero si salta all'ultimo obiettivo.
      if (s.video.seeking) continue;
      if (!s.visible && Math.abs(s.cur - s.target) < 0.002) continue;
      s.cur += (s.target - s.cur) * (reduce ? 1 : 0.18);
      const dur = s.video.duration || 1;
      const t = clamp(s.cur, 0, 0.999) * dur;
      if (Math.abs(s.video.currentTime - t) > eps) { try { s.video.currentTime = t; } catch (e) {} }
    }
    requestAnimationFrame(raf);
  }

  // iOS vuole un gesto dell'utente prima che un video muto decodifichi e disegni in modo
  // affidabile. Al primo tocco prepariamo ogni clip caricata (play→pause muto), così il primo
  // seek è immediato invece di mostrare un frame vuoto. `userReady` fa preparare da sole anche
  // le clip caricate dopo (vedi loadClip).
  let userReady = false;
  function primeVideo(v) {
    if (!isMobile() || !v) return;
    // Un play() muto e playsinline che viene RIFIUTATO dopo un gesto dell'utente vuol dire che
    // il sistema blocca il video: in pratica il Risparmio energetico di iOS, in cui non funziona
    // nemmeno lo scrub con currentTime. Passa alle immagini per tutta la pagina invece di
    // mostrare scene congelate o vuote.
    try { const p = v.play(); if (p && p.then) p.then(() => { try { v.pause(); } catch (e) {} }).catch(() => { enterStillsMode(); }); }
    catch (e) {}
  }
  function onFirstGesture() {
    if (userReady) return;
    userReady = true;
    SEGMENTS.forEach(s => primeVideo(s.video));
  }
  window.addEventListener('pointerdown', onFirstGesture, { once: true, passive: true });
  window.addEventListener('touchstart', onFirstGesture, { once: true, passive: true });

  // Le particelle costano a ogni frame: su un telefono, insieme allo scrub del video, non ce le possiamo permettere.
  seedParticles(particles, reduce || coarse);
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(read); } }, { passive: true });
  // I browser mobile lanciano `resize` ogni volta che la barra degli indirizzi entra o esce.
  // Rifare lì layout() ricostruisce l'altezza della traccia e fa saltare la posizione dello
  // scroll, quindi sui dispositivi touch ignoriamo i cambi solo in altezza e rifacciamo il
  // layout solo quando cambia davvero la larghezza (la rotazione passa comunque da
  // orientationchange). layout() si segna la larghezza con cui ha calcolato.
  function onResize() {
    if (coarse && window.innerWidth === laidOutW) return;
    layout();
  }
  window.addEventListener('resize', onResize);
  window.addEventListener('orientationchange', layout);
  window.addEventListener('load', layout);
  layout();
  requestAnimationFrame(raf);

  // ---- funzioni di supporto ----
  function el(tag, cls) { const n = document.createElement(tag); if (cls) n.className = cls; return n; }
  function pad(n) { return String(n).padStart(2, '0'); }
  function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
  function ctaBtns(cta) {
    let h = '';
    if (cta.primary) h += `<a class="sw-btn sw-btn--primary" href="${esc(cta.primary.href || '#')}">${esc(cta.primary.label)}</a>`;
    if (cta.secondary) h += `<a class="sw-btn sw-btn--ghost" href="${esc(cta.secondary.href || '#')}">${esc(cta.secondary.label)}</a>`;
    return h;
  }
}

function seedParticles(host, reduce) {
  if (!host || reduce) return;
  const kinds = ['dot', 'dot', 'ring'];
  const seeds = [7, 23, 41, 58, 71, 88, 12, 34, 52, 66, 83, 95, 18, 29, 47, 63, 77, 91, 5, 38, 55, 69, 82, 97];
  for (let k = 0; k < 20; k++) {
    const s = document.createElement('span');
    s.className = 'sw-pt sw-pt--' + kinds[k % kinds.length];
    s.style.left = seeds[k % seeds.length] + 'vw';
    s.style.top = ((seeds[(k * 3) % seeds.length] * 1.3) % 100) + 'vh';
    s.style.setProperty('--sw-sc', (0.5 + ((seeds[(k * 5) % seeds.length] % 60) / 60) * 1.1).toFixed(2));
    const dur = 14 + (seeds[(k * 7) % seeds.length] % 22);
    s.style.animationDuration = dur + 's';
    s.style.animationDelay = (-(seeds[(k * 2) % seeds.length] % dur)) + 's';
    host.appendChild(s);
  }
}

function injectCSS() {
  if (document.getElementById('sw-css')) return;
  const css = `
  .sw-root{--sw-bg:#F5EDE0;--sw-ink:#241d2b;--sw-ink-soft:#6a6072;--sw-accent:#8a7bb5;
    --sw-font-display:ui-rounded,"SF Pro Rounded","Segoe UI",system-ui,sans-serif;
    --sw-font-body:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,system-ui,sans-serif;
    color:var(--sw-ink);font-family:var(--sw-font-body);}
  html,body{margin:0;background:var(--sw-bg,#F5EDE0);overflow-x:hidden;}
  .sw-sky{position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none;background:var(--sw-bg);}
  .sw-sky__grad{position:absolute;inset:-10%;background:linear-gradient(178deg,color-mix(in srgb,var(--sw-accent) 12%,var(--sw-bg)) 0%,var(--sw-bg) 55%,color-mix(in srgb,var(--sw-accent) 6%,var(--sw-bg)) 100%);}
  .sw-sky__glow{position:absolute;inset:0;background:radial-gradient(60% 42% at 74% 16%,color-mix(in srgb,var(--sw-accent) 22%,transparent),transparent 70%),radial-gradient(46% 34% at 50% 50%,color-mix(in srgb,#fff 45%,transparent),transparent 70%);}
  .sw-particles{position:absolute;inset:-6% -2%;will-change:transform;}
  .sw-pt{position:absolute;width:13px;height:13px;transform:scale(var(--sw-sc,1));opacity:0;animation:sw-drift linear infinite;}
  .sw-pt::before{content:"";position:absolute;inset:0;border-radius:50%;}
  .sw-pt--dot::before{background:radial-gradient(circle at 34% 30%,color-mix(in srgb,var(--sw-accent) 60%,#000),#000 82%);}
  .sw-pt--ring::before{background:transparent;border:2px solid color-mix(in srgb,var(--sw-accent) 55%,transparent);}
  @keyframes sw-drift{0%{opacity:0;transform:scale(var(--sw-sc)) translate(0,12vh) rotate(0)}12%{opacity:.5}88%{opacity:.45}100%{opacity:0;transform:scale(var(--sw-sc)) translate(4vw,-22vh) rotate(210deg)}}
  .sw-scrollbar{position:fixed;top:0;left:0;right:0;height:3px;z-index:60;background:color-mix(in srgb,var(--sw-accent) 14%,transparent);}
  .sw-scrollbar span{display:block;height:100%;width:100%;transform-origin:0 50%;transform:scaleX(0);background:var(--sw-accent);}
  .sw-topbar{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:clamp(14px,2.4vw,26px) clamp(18px,5vw,64px);}
  .sw-brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--sw-ink);}
  .sw-brand__mark{width:24px;height:28px;border-radius:7px 7px 10px 10px;background:linear-gradient(160deg,var(--sw-accent),color-mix(in srgb,var(--sw-accent) 60%,#000));box-shadow:0 6px 14px color-mix(in srgb,var(--sw-accent) 40%,transparent);}
  .sw-brand__name{font-family:var(--sw-font-display);font-weight:700;font-size:1.1rem;}
  .sw-nav{display:flex;gap:4px;padding:5px;background:color-mix(in srgb,#fff 55%,transparent);backdrop-filter:blur(10px);border:1px solid color-mix(in srgb,var(--sw-accent) 16%,transparent);border-radius:999px;}
  .sw-nav__item{font:inherit;font-size:.82rem;color:var(--sw-ink-soft);border:0;background:transparent;cursor:pointer;padding:7px 14px;border-radius:999px;transition:color .25s,background .25s;}
  .sw-nav__item:hover{color:var(--sw-ink);} .sw-nav__item.is-active{color:#fff;background:var(--sw-accent);}
  .sw-topcta{text-decoration:none;font-weight:600;font-size:.9rem;color:#fff;background:var(--sw-ink);padding:10px 20px;border-radius:999px;white-space:nowrap;}
  .sw-stage{position:fixed;inset:0;z-index:10;pointer-events:none;}
  .sw-scene{position:absolute;inset:0;opacity:0;overflow:hidden;will-change:opacity;}
  .sw-scene__video,.sw-scene__still{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 42%;}
  .sw-scene__still{will-change:transform;} .sw-scene.has-clip .sw-scene__still{opacity:0;} .sw-scene__video{z-index:1;}
  .sw-copylayer{position:fixed;inset:0;z-index:20;pointer-events:none;}
  .sw-copylayer::before{content:"";position:absolute;inset:0;width:min(58vw,780px);background:linear-gradient(90deg,var(--sw-bg) 0%,color-mix(in srgb,var(--sw-bg) 82%,transparent) 34%,color-mix(in srgb,var(--sw-bg) 40%,transparent) 62%,transparent 100%);}
  .sw-copy{position:absolute;left:clamp(18px,5vw,64px);top:50%;transform:translateY(-50%);width:min(42vw,460px);opacity:0;will-change:opacity,transform;}
  .sw-copy__num{font-family:ui-monospace,Menlo,monospace;font-size:.74rem;letter-spacing:.12em;color:var(--sw-ink-soft);}
  .sw-copy__eyebrow{display:block;margin-top:18px;font-family:var(--sw-font-display);font-weight:700;font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;color:var(--sw-accent);}
  .sw-copy__title{font-family:var(--sw-font-display);font-weight:700;color:var(--sw-ink);font-size:clamp(2rem,4.4vw,3.5rem);line-height:1.03;margin:12px 0 0;letter-spacing:-.01em;text-shadow:0 2px 20px color-mix(in srgb,var(--sw-bg) 70%,transparent);}
  .sw-copy__body{margin-top:18px;font-size:clamp(1rem,1.25vw,1.14rem);line-height:1.55;color:color-mix(in srgb,var(--sw-ink) 78%,var(--sw-ink-soft));max-width:40ch;text-shadow:0 1px 12px color-mix(in srgb,var(--sw-bg) 90%,transparent);}
  .sw-copy__tags{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 0;padding:0;}
  .sw-copy__tags li{font-size:.82rem;font-weight:600;color:color-mix(in srgb,var(--sw-accent) 70%,#000);padding:7px 14px;border-radius:999px;background:color-mix(in srgb,var(--sw-accent) 14%,#fff);border:1px solid color-mix(in srgb,var(--sw-accent) 30%,transparent);}
  .sw-copy__cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px;pointer-events:auto;}
  .sw-btn{text-decoration:none;font-weight:600;font-size:.95rem;padding:13px 24px;border-radius:999px;transition:transform .2s;}
  .sw-btn--primary{color:#fff;background:var(--sw-ink);} .sw-btn--primary:hover{transform:translateY(-2px);}
  .sw-btn--ghost{color:var(--sw-ink);border:1.5px solid color-mix(in srgb,var(--sw-ink) 25%,transparent);} .sw-btn--ghost:hover{transform:translateY(-2px);}
  .sw-route{position:fixed;right:clamp(14px,2.4vw,30px);top:50%;z-index:40;transform:translateY(-50%);display:flex;flex-direction:column;gap:22px;padding:18px 10px;}
  .sw-route::before{content:"";position:absolute;left:50%;top:22px;bottom:22px;width:2px;transform:translateX(-50%);background:var(--sw-accent);opacity:.28;}
  .sw-route__dot{position:relative;border:0;background:transparent;cursor:pointer;width:14px;height:14px;display:grid;place-items:center;}
  .sw-route__dot i{width:9px;height:9px;border-radius:50%;background:color-mix(in srgb,var(--sw-accent) 40%,transparent);transition:transform .3s,background .3s,box-shadow .3s;}
  .sw-route__dot:hover i{transform:scale(1.25);background:var(--sw-accent);}
  .sw-route__dot.is-active i{background:var(--sw-accent);transform:scale(1.4);box-shadow:0 0 0 5px color-mix(in srgb,var(--sw-accent) 22%,transparent);}
  .sw-route__label{position:absolute;right:24px;top:50%;transform:translateY(-50%) translateX(6px);white-space:nowrap;font-size:.78rem;font-weight:600;color:var(--sw-ink);background:color-mix(in srgb,#fff 85%,transparent);backdrop-filter:blur(6px);padding:5px 11px;border-radius:999px;opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;border:1px solid color-mix(in srgb,var(--sw-accent) 14%,transparent);}
  .sw-route__dot:hover .sw-route__label,.sw-route__dot.is-active .sw-route__label{opacity:1;transform:translateY(-50%) translateX(0);}
  .sw-hint{position:fixed;left:50%;bottom:26px;z-index:30;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:10px;font-size:.76rem;letter-spacing:.14em;text-transform:uppercase;color:var(--sw-ink-soft);transition:opacity .3s;}
  .sw-hint i{width:22px;height:34px;border-radius:12px;border:2px solid color-mix(in srgb,var(--sw-ink) 28%,transparent);position:relative;}
  .sw-hint i::after{content:"";position:absolute;left:50%;top:7px;width:4px;height:7px;border-radius:2px;background:var(--sw-accent);transform:translateX(-50%);animation:sw-wheel 1.7s ease-in-out infinite;}
  @keyframes sw-wheel{0%{opacity:0;top:6px}40%{opacity:1}100%{opacity:0;top:17px}}
  .sw-track{position:relative;z-index:1;width:100%;pointer-events:none;}
  @media (max-width:860px){
    .sw-nav{display:none;}
    .sw-copylayer::before{width:100%;height:60%;top:auto;bottom:0;background:linear-gradient(0deg,var(--sw-bg) 8%,color-mix(in srgb,var(--sw-bg) 70%,transparent) 46%,transparent 100%);}
    /* Testi ancorati in basso, lontani dall'indicatore home e dalla barra degli indirizzi che si chiude.
       dvh + env() sono progressivi: i browser che non li hanno tengono la riga di ripiego in vh. */
    .sw-copy{left:clamp(18px,5vw,64px);right:clamp(18px,5vw,64px);top:auto;bottom:clamp(64px,14vh,120px);transform:none;width:auto;max-width:560px;}
    .sw-copy{bottom:calc(clamp(56px,12dvh,110px) + env(safe-area-inset-bottom));}
    .sw-copy__title{font-size:clamp(1.9rem,7.5vw,2.7rem);}
    .sw-copy__body{max-width:none;font-size:clamp(.98rem,3.6vw,1.1rem);} .sw-scene__video,.sw-scene__still{object-position:center 46%;}
    .sw-hint{bottom:calc(20px + env(safe-area-inset-bottom));}
    .sw-route{gap:16px;right:6px;} .sw-route__label{display:none;}
  }
  /* I telefoni in verticale tagliano molto una clip 16:9; tieni l'inquadratura centrata così
     il soggetto principale (verso cui si tuffa la camera) resta visibile. */
  @media (max-width:860px) and (orientation:portrait){
    .sw-scene__video,.sw-scene__still{object-position:center 44%;}
  }
  /* Touch: ai punti del percorso un'area di tocco grande come un dito, senza ingrandire il punto visibile. */
  @media (hover:none) and (pointer:coarse){
    .sw-route{padding:14px 6px;}
    .sw-route__dot{width:28px;height:28px;}
    .sw-btn{padding:15px 26px;}
  }
  @media (prefers-reduced-motion:reduce){ .sw-hint i::after{animation:none;} .sw-pt{display:none;} }
  `;
  // Racchiude tutto in un cascade layer, così i valori del tema della pagina (fuori dai layer,
  // :root / .sw-root { --sw-bg / --sw-ink / --sw-accent … }) vincono sempre su questi
  // predefiniti, qualunque sia l'ordine di iniezione. Permette temi scuri puliti.
  const style = document.createElement('style'); style.id = 'sw-css';
  style.textContent = '@layer sw {\n' + css + '\n}';
  document.head.appendChild(style);
}

// Esposto sia come modulo sia come globale.
if (typeof module !== 'undefined' && module.exports) module.exports = { mountScrollWorld };
if (typeof window !== 'undefined') window.mountScrollWorld = mountScrollWorld;
