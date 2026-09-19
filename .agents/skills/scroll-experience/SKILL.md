---
name: scroll-experience
description: Costruisce un'esperienza immersiva guidata dallo scroll coordinando three-js, scroll-film e scroll-world (WebGL scritto in codice, sezioni cinematiche in codice o video pre-renderizzati, scelti con l'intervista iniziale). Usala per unire più tecniche di scroll in un'unica narrazione continua e quando l'utente lancia /scroll-experience.
---

# /scroll-experience

Usa questo comando quando vuoi un'esperienza completa guidata dallo scroll, che può mescolare più tecniche (scene 3D in WebGL, codice cinematico con camera continua, clip video pre-renderizzate) in un'unica narrazione continua.

## Procedura

1. **Passo 0 — Intervista**: argomento, momenti della storia, brand kit, fascia di budget, fascia mobile. Decidi il motore: codice 3D (three-js), video (scroll-world), codice cinematico (scroll-film) o ibrido.
2. **Passo 1 — Proposta di concept**: 2-3 concept con un nome, ciascuno con il percorso della camera e il motore di ogni sezione.
3. **Passo 2 — Costruzione**: passa il lavoro alla skill del motore scelto e seguine le regole d'oro e la procedura. Per l'ibrido, costruisci una sezione alla volta, rispettando la regola del driver unico.
4. **Passo 3 — Controllo delle giunture**: verifica le transizioni. Video↔video: controllo SSIM delle giunture (`references/pipeline.md` §5c di scroll-world; `knockout.py` rimuove solo gli sfondi). 3D↔video↔codice: controllo visivo della continuità — la posizione finale dell'inquadratura N deve coincidere con l'inizio della N+1; nessuno scatto della camera.
5. **Passo 4 — Verifica e deploy**: test di jank + budget della GPU (verification.md di three-js), poi, se l'utente lo vuole, deploy su Vercel.

## Uso

```text
/scroll-experience mondo 3D da attraversare in volo per un marchio di caffè
/scroll-experience scrollytelling ibrido: hero in 3D + sezioni video
/scroll-experience landing a diorama con livelli di parallasse in WebGL
```
