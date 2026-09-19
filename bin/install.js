#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execSync } = require('child_process');
const pkg = require('../package.json');
const version = `v${pkg.version}`;

const KIT = '.agents';
const MANIFEST = '.ag-kit.json'; // dentro .agents/: le voci installate dal kit, tolte all'aggiornamento successivo
const localKitDir = path.resolve(__dirname, '..', KIT);
const repoUrl = (pkg.repository && pkg.repository.url || 'https://github.com/Andryd22/AG-agents-skills.git').replace(/^git\+/, '');

// Conta il contenuto reale di .agents/ invece di scrivere i numeri nel codice
function countMdFiles(dir) {
  if (!fs.existsSync(dir)) return 0;
  return fs.readdirSync(dir, { withFileTypes: true }).filter(e => e.isFile() && e.name.endsWith('.md')).length;
}
function countDirs(dir) {
  if (!fs.existsSync(dir)) return 0;
  return fs.readdirSync(dir, { withFileTypes: true }).filter(e => e.isDirectory()).length;
}
function getCounts(kitDir) {
  return {
    agents: countMdFiles(path.join(kitDir, 'agents')),
    skills: countDirs(path.join(kitDir, 'skills')),
  };
}

const SKIP = new Set(['__pycache__', '.DS_Store', MANIFEST]);

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (SKIP.has(entry.name) || entry.name.endsWith('.pyc')) continue;
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) copyDir(srcPath, destPath);
    else fs.copyFileSync(srcPath, destPath);
  }
}

function countFiles(dir) {
  if (!fs.existsSync(dir)) return 0;
  let n = 0;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    n += entry.isDirectory() ? countFiles(path.join(dir, entry.name)) : 1;
  }
  return n;
}

// Cosa appartiene al kit dentro .agents/: ogni agente, skill e regola uno per uno,
// ogni altra voce al primo livello (ARCHITECTURE.md, scripts/) per intero.
// Tutto il resto nella .agents/ del progetto è dell'utente e non si tocca.
const SPLIT = new Set(['agents', 'skills', 'rules']);
function kitEntries(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory() && SPLIT.has(entry.name)) {
      for (const child of fs.readdirSync(path.join(dir, entry.name))) out.push(`${entry.name}/${child}`);
    } else {
      out.push(entry.name);
    }
  }
  return out.sort();
}

function readManifest(dir) {
  try {
    const data = JSON.parse(fs.readFileSync(path.join(dir, MANIFEST), 'utf8'));
    // solo voci semplici "nome" o "cartella/nome": mai un percorso fuori da .agents/
    const safe = e => typeof e === 'string' && /^[\w.-]+(\/[\w.-]+)?$/.test(e) && !e.split('/').some(s => s === '.' || s === '..');
    return Array.isArray(data.entries) ? data.entries.filter(safe) : [];
  } catch {
    return [];
  }
}

// Clona direttamente da GitHub l'ultima .agents/
function fetchLatestFromGitHub() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'ag-agents-skills-'));
  try {
    execSync(`git clone --depth 1 "${repoUrl}" "${path.join(tmp, 'repo')}"`, { stdio: 'pipe' });
    const fetched = path.join(tmp, 'repo', KIT);
    if (!fs.existsSync(fetched)) throw new Error(`${KIT}/ non trovata nel repository clonato`);
    return { dir: fetched, cleanup: () => fs.rmSync(tmp, { recursive: true, force: true }) };
  } catch (err) {
    fs.rmSync(tmp, { recursive: true, force: true });
    throw err;
  }
}

const args = process.argv.slice(2);
const autoYes = args.includes('-y') || args.includes('--yes');
const positionalArgs = args.filter(a => !a.startsWith('-'));
let command = positionalArgs[0];
if (!command && autoYes) command = 'init';

if (!command || command === 'help' || command === '--help' || args.includes('-h')) {
  const { agents, skills } = getCounts(localKitDir);
  console.log(`
  Antigravity Kit (fork di Andryd22) — ${version}
  ${agents} agenti | ${skills} skill | modalità caveman

  Uso:
    npx github:Andryd22/AG-agents-skills [comando] [opzioni]

  Comandi:
    init -y    Installa il kit in .agents/ del progetto corrente
    update     Scarica da GitHub l'ultima versione del kit e la installa
    help       Mostra questo aiuto

  I tuoi agenti, skill e regole in .agents/ restano; quelli del kit vengono sostituiti.

  Opzioni:
    -y, --yes  Conferma l'installazione
  `);
  process.exit(0);
}

if (command === 'init' && !autoYes) {
  console.error(`Errore: init richiede -y (sostituisce i file del kit in ${KIT}/).`);
  console.error('Uso: npx github:Andryd22/AG-agents-skills init -y');
  process.exit(1);
}

if (command !== 'init' && command !== 'update') {
  console.error(`Comando sconosciuto: ${command}`);
  console.error('Uso: npx github:Andryd22/AG-agents-skills [init -y|update]');
  process.exit(1);
}

const targetDir = process.cwd();
const destDir = path.join(targetDir, KIT);

function fail(msg) {
  throw new Error(msg); // lanciato così il blocco finally toglie comunque il clone temporaneo
}

function realOrResolved(p) {
  return fs.existsSync(p) ? fs.realpathSync(p) : path.resolve(p);
}
function sameOrNested(a, b) {
  const rel = path.relative(realOrResolved(a), realOrResolved(b));
  return rel === '' || (!rel.startsWith('..') && !path.isAbsolute(rel));
}

let sourceDir = localKitDir;
let fetched = null;
if (command === 'update') {
  console.log(`Scarico l'ultima ${KIT}/ da ${repoUrl} ...`);
  try {
    fetched = fetchLatestFromGitHub();
    sourceDir = fetched.dir;
  } catch (err) {
    console.error(`Avviso: impossibile scaricare da GitHub (${err.message.trim()})`);
    console.error('Uso la versione installata in locale.');
  }
}

const staging = path.join(targetDir, `${KIT}.tmp-${process.pid}`);
try {
  if (!fs.existsSync(sourceDir)) fail(`sorgente ${KIT}/ non trovata in ${sourceDir}`);
  // Installare il kit su se stesso (es. dal repository del kit) cancellerebbe la sorgente.
  if (sameOrNested(sourceDir, destDir) || sameOrNested(destDir, sourceDir)) {
    fail(`sorgente e destinazione sono la stessa ${KIT}/ (${destDir}).\n` +
      'Lancia il comando dal progetto in cui vuoi installare, non dal kit stesso.');
  }

  // Prima la copia: la .agents/ del progetto si tocca solo se la copia è riuscita.
  fs.rmSync(staging, { recursive: true, force: true });
  copyDir(sourceDir, staging);
  const count = countFiles(staging);
  if (count === 0) fail(`niente copiato da ${sourceDir}`);

  const entries = kitEntries(staging);
  const previous = readManifest(destDir);
  const stale = previous.filter(e => !entries.includes(e));
  const replaced = entries.filter(e => fs.existsSync(path.join(destDir, e)));

  // Toglie quello che aveva installato la versione precedente e quello che questa sostituisce, poi sposta dentro i file nuovi.
  for (const e of new Set([...previous, ...entries])) {
    fs.rmSync(path.join(destDir, e), { recursive: true, force: true });
  }
  for (const e of entries) {
    fs.mkdirSync(path.dirname(path.join(destDir, e)), { recursive: true });
    fs.renameSync(path.join(staging, e), path.join(destDir, e));
  }
  fs.writeFileSync(path.join(destDir, MANIFEST), JSON.stringify({ version: pkg.version, entries }, null, 2) + '\n');

  // Le versioni vecchie del kit stavano in .agent/: Antigravity ne legge ancora le regole, quindi la sposta da parte.
  const legacy = path.join(targetDir, '.agent');
  let legacyMoved = null;
  if (fs.existsSync(path.join(legacy, 'ARCHITECTURE.md'))) {
    legacyMoved = path.join(targetDir, fs.existsSync(path.join(targetDir, '.agent.bak')) ? `.agent.bak-${Date.now()}` : '.agent.bak');
    fs.renameSync(legacy, legacyMoved);
  }

  const { agents, skills } = getCounts(destDir);
  console.log(`Kit installato in ${destDir}`);
  console.log(`  ${count} file — ${agents} agenti, ${skills} skill (compresi i tuoi)`);
  if (replaced.length) console.log(`  ${replaced.length} voci del kit sostituite (le modifiche locali a quelle voci non restano)`);
  if (stale.length) console.log(`  Tolte dalla versione precedente: ${stale.join(', ')}`);
  if (legacyMoved) console.log(`  La vecchia cartella del kit .agent/ è stata spostata in ${path.basename(legacyMoved)}/: cancellala dopo averla controllata.`);
  console.log('  Prova /caveman nel tuo IDE per attivare la modalità caveman');
} catch (err) {
  console.error(`Errore: ${err.message}`);
  process.exitCode = 1;
} finally {
  fs.rmSync(staging, { recursive: true, force: true });
  if (fetched) fetched.cleanup();
}
