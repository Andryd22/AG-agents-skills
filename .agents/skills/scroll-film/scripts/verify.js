#!/usr/bin/env node
/*
 * verify.js — lo strumento di verifica visiva (lavoro meccanico, nessun modello).
 *
 *   node verify.js shot   <url> <file.png> [larghezza] [altezza]   # screenshot alla posizione ?jump
 *   node verify.js jank   <url>                                    # test di jank scorrendo tutta la pagina
 *
 * Usa puppeteer-core + il Chrome di sistema (le anteprime dell'host rallentano le schede nascoste,
 * congelano il rAF e restituiscono screenshot vecchi: questa strada no). La pagina sotto test deve
 * implementare il contratto di sviluppo di references/engine.md: ?jump=<scrollY> apre la pagina già
 * scrollata e assestata, e window.__ready === true scatta quando la pagina è davvero pronta.
 * Se __ready non scatta mai, lo strumento FALLISCE: lo screenshot di una pagina non pronta non prova niente.
 *
 * Da fare una volta:  npm i puppeteer-core   (e avere Google Chrome installato)
 * Il percorso di Chrome è trovato da solo su macOS/Linux/Windows; per cambiarlo CHROME_PATH=/percorso.
 */
const puppeteer = require('puppeteer-core');

function chromePath() {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const p = process.platform;
  if (p === 'darwin') return '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  if (p === 'win32') return 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  return '/usr/bin/google-chrome';
}

async function withBrowser(fn) {
  const b = await puppeteer.launch({
    executablePath: chromePath(),
    headless: 'new',
    args: ['--hide-scrollbars', '--no-sandbox'],
  });
  try { return await fn(b); }
  finally { await b.close().catch(() => {}); }
}

async function ready(page) {
  await page.waitForFunction('window.__ready === true', { timeout: 45000 })
    .catch(() => { throw new Error('window.__ready non è mai scattato — pagina non pronta, niente cattura (implementa il contratto di sviluppo)'); });
}

async function shot(url, out, w = 1440, h = 900) {
  await withBrowser(async b => {
    const page = await b.newPage();
    await page.setViewport({ width: +w, height: +h, deviceScaleFactor: 1 });
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
    await ready(page);
    await new Promise(r => setTimeout(r, 1200)); // lascia assestare interpolazioni e animazioni di ingresso
    await page.screenshot({ path: out });
    console.log('catturato', out);
  });
}

async function jank(url) {
  await withBrowser(async b => {
    const page = await b.newPage();
    await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
    await ready(page);
    const stats = await page.evaluate(() => new Promise(res => {
      const end = Math.max(0, (document.scrollingElement || document.documentElement).scrollHeight - innerHeight);
      const deltas = []; let last = performance.now(), y = 0;
      const tick = () => {
        const now = performance.now(); deltas.push(now - last); last = now;
        y += 13; window.scrollTo(0, Math.min(y, end));
        if (y < end) requestAnimationFrame(tick);
        else {
          deltas.sort((a, b) => a - b);
          const p = q => deltas[Math.floor(deltas.length * q)];
          res({
            frames: deltas.length, scrolled: end,
            avg: +(deltas.reduce((a, b) => a + b, 0) / deltas.length).toFixed(1),
            p95: +p(0.95).toFixed(1), max: +deltas[deltas.length - 1].toFixed(1),
            over50: deltas.filter(d => d > 50).length,
          });
        }
      };
      requestAnimationFrame(tick);
    }));
    console.log(JSON.stringify(stats));
    console.log(stats.max < 50 ? 'SUPERATO (max < 50 ms)' : 'JANK — controlla la finestra di bitmap, il DPR e il peso dei frame');
    if (stats.max >= 50) process.exitCode = 2;
  });
}

const [mode, url, out, w, h] = process.argv.slice(2);
(async () => {
  if (mode === 'shot') await shot(url, out, w, h);
  else if (mode === 'jank') await jank(url);
  else { console.error('uso: node verify.js shot <url> <file.png> [larg] [alt]  |  node verify.js jank <url>'); process.exit(1); }
})().catch(e => { console.error(e.message); process.exit(1); });
