# Verifica

## Test di jank (a mano, 10 secondi)

1. DevTools → Performance → avvia la registrazione
2. Scorri dall'alto in basso e di nuovo in alto a velocità costante, una volta
3. Ferma e leggi il grafico dei frame: qualsiasi frame > 16,7 ms con i segni rossi dei long task = FALLITO
4. Ripeti a velocità doppia (scatti della rotella) su desktop

SUPERATO = frame massimo sotto i 24 ms, nessun long task > 50 ms, mai più di 3 frame persi di fila.

## Controlli in console

- `THREE.WebGLRenderer: Context Lost` — manca l'handler di ripristino → FALLITO
- `[.WebGL-0000] GL_INVALID_OPERATION` — uso sbagliato di geometria/materiali → FALLITO
- `Uniform buffers overflow` — troppe luci o materiali → FALLITO
- Avviso `THREE.ColorManagement` sul colorSpace — correggi l'SRGB delle texture

## Soglia delle statistiche della GPU

Eseguilo una volta dopo la build e scrivi il risultato in console, per memoria:

```js
console.table({
  drawCalls: renderer.info.render.calls,
  triangles: renderer.info.render.triangles,
  geometries: renderer.info.memory.geometries,
  textures: renderer.info.memory.textures,
});
```

Confronta con i budget di performance.md. Fuori budget → correggi prima del deploy: mai rilasciare con un budget in rosso.

## Checklist funzionale

- [ ] La scena si vede al primo disegno (nessun lampo di canvas vuoto)
- [ ] Tutte le sezioni data-scene si raggiungono con lo scroll; nessuna bloccata fuori percorso
- [ ] La camera non attraversa mai la geometria (sposta i punti di passaggio)
- [ ] Il resize funziona (aspect e dimensioni aggiornati, niente distorsioni)
- [ ] Mobile: niente ombre, pixel ratio ≤ 1.5, budget < 50 draw call
- [ ] Scheda nascosta → animazione in pausa; di nuovo visibile → riparte senza salti
- [ ] Navigando avanti e indietro la memoria non cresce (grafico della memoria di Performance monitor piatto)

## Smoke test automatico

Se il progetto ha un test runner: verifica che `renderer.info.render.calls < budget` dopo il montaggio della scena e il primo scatto di scroll, e che la differenza di `performance.memory.usedJSHeapSize` sia < 50 MB dopo 10 cicli di navigazione.
