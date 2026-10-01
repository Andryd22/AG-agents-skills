#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');
const pkg = require('../package.json');

const KIT = '.agents';
const MANIFEST = '.ag-kit.json';
const BACKUPS = '.agents.backups';
const localRoot = path.resolve(__dirname, '..');
const repoUrl = (pkg.repository?.url || 'https://github.com/Andryd22/AG-agents-skills.git').replace(/^git\+/, '');
const hash = content => content === null ? null : crypto.createHash('sha256').update(content).digest('hex');

function safePath(root, relative) {
  if (typeof relative !== 'string' || !/^[\w.-]+(?:\/[\w.-]+)*$/.test(relative) ||
      relative.split('/').some(part => part === '.' || part === '..')) {
    throw new Error(`Percorso non valido: ${relative}`);
  }
  let current = root;
  for (const part of ['', ...relative.split('/')]) {
    current = path.join(current, part);
    try {
      if (fs.lstatSync(current).isSymbolicLink()) throw new Error(`Link non supportato: ${current}`);
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
    }
  }
  return current;
}

function readFile(root, relative) {
  const filename = safePath(root, relative);
  try {
    if (!fs.statSync(filename).isFile()) throw new Error(`Atteso un file, trovato altro: ${filename}`);
    return fs.readFileSync(filename);
  } catch (error) {
    if (error.code === 'ENOENT') return null;
    throw error;
  }
}

function sourceFiles(root, prefix = '') {
  const files = {};
  for (const entry of fs.readdirSync(path.join(root, prefix), { withFileTypes: true })) {
    if (['__pycache__', '.DS_Store', '.npmignore', MANIFEST].includes(entry.name) || entry.name.endsWith('.pyc')) continue;
    const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (/^skills\/latex-tutor\/assets\/main\.(aux|fdb_latexmk|fls|log|out|pdf|synctex\.gz|toc)$/.test(relative)) continue;
    safePath(root, relative);
    if (entry.isDirectory()) Object.assign(files, sourceFiles(root, relative));
    else files[relative] = readFile(root, relative);
  }
  return files;
}

function readManifest(root) {
  const content = readFile(root, MANIFEST);
  if (!content) return { files: {} };
  const data = JSON.parse(content.toString('utf8'));
  if (data.schemaVersion === undefined && Array.isArray(data.entries)) {
    console.log('Manifest precedente senza hash: i file non identificabili restano; le collisioni richiedono --force.');
    return { version: data.version, files: {}, legacy: data.entries };
  }
  if (data.schemaVersion !== 2 || !data.files || Array.isArray(data.files) || typeof data.files !== 'object') {
    throw new Error('Manifest non valido o versione non supportata: installazione invariata.');
  }
  for (const [relative, digest] of Object.entries(data.files)) {
    safePath(root, relative);
    if (relative === MANIFEST || !/^[a-f0-9]{64}$/.test(digest)) throw new Error(`Hash o voce non validi: ${relative}`);
  }
  return data;
}

function gitOutput(root, args) {
  return execFileSync('git', ['-C', root, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], timeout: 60000 }).trim();
}

function sourceInfo(root, repository) {
  let commit = null;
  let dirty = null;
  // Non attribuire il commit di un repository padre a un pacchetto npm estratto.
  if (fs.existsSync(path.join(root, '.git'))) {
    try {
      commit = gitOutput(root, ['rev-parse', 'HEAD']);
      dirty = Boolean(gitOutput(root, ['status', '--porcelain', '--', KIT, 'package.json']));
    } catch { /* init funziona anche senza Git; l'origine resta esplicitamente sconosciuta */ }
  }
  return { repository, commit, dirty };
}

function nested(a, b) {
  const canonical = p => fs.existsSync(p) ? fs.realpathSync(p) : path.resolve(p);
  const relative = path.relative(canonical(a), canonical(b));
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function planInstall(project, source, metadata) {
  const destination = safePath(project, KIT);
  const previous = readManifest(destination);
  const incoming = sourceFiles(source);
  if (!Object.keys(incoming).length) throw new Error('Il kit sorgente è vuoto.');
  const changes = {};
  const conflicts = [];
  for (const relative of new Set([...Object.keys(previous.files), ...Object.keys(incoming)])) {
    const current = readFile(destination, relative);
    const next = incoming[relative] ?? null;
    if (hash(current) === hash(next)) continue;
    if (hash(current) !== (previous.files[relative] ?? null)) conflicts.push(`${KIT}/${relative}`);
    changes[`${KIT}/${relative}`] = next;
  }
  const files = Object.fromEntries(Object.entries(incoming).sort().map(([name, content]) => [name, hash(content)]));
  const manifest = Buffer.from(JSON.stringify({ schemaVersion: 2, ...metadata, files }, null, 2) + '\n');
  if (hash(readFile(destination, MANIFEST)) !== hash(manifest)) changes[`${KIT}/${MANIFEST}`] = manifest;
  // Le voci del vecchio manifest che il kit non ha più restano su disco: vanno segnalate.
  const stale = (previous.legacy || []).filter(entry => {
    try {
      return !Object.keys(incoming).some(name => name === entry || name.startsWith(`${entry}/`)) &&
        fs.existsSync(safePath(destination, entry));
    } catch { return false; }
  });
  return { changes, conflicts, files, stale };
}

function writeFile(root, relative, content) {
  const filename = safePath(root, relative);
  if (content === null) {
    if (fs.existsSync(filename)) fs.unlinkSync(filename);
    return;
  }
  fs.mkdirSync(path.dirname(filename), { recursive: true });
  const temporary = `${filename}.agkit-${crypto.randomUUID()}`;
  try {
    fs.writeFileSync(temporary, content, { flag: 'wx' });
    fs.renameSync(temporary, filename);
  } finally {
    if (fs.existsSync(temporary)) fs.unlinkSync(temporary);
  }
}

function applyChanges(project, changes, keepBackup) {
  const names = Object.keys(changes);
  if (!names.length) return null;
  // Gli originali restano in memoria per il rollback; su disco solo se serve un backup da ripristinare.
  const originals = Object.fromEntries(names.map(name => [name, readFile(project, name)]));
  let backup = null;
  if (keepBackup) {
    const backupName = `${BACKUPS}/${new Date().toISOString().replace(/[:.]/g, '-')}-${crypto.randomBytes(3).toString('hex')}`;
    backup = safePath(project, backupName);
    fs.mkdirSync(backup, { recursive: true });
    const records = names.map(name => ({ path: name, before: hash(originals[name]), after: hash(changes[name]) }));
    for (const name of names) {
      if (originals[name] !== null) writeFile(backup, `files/${name}`, originals[name]);
    }
    const transaction = { schemaVersion: 1, project: fs.realpathSync(project), records };
    writeFile(backup, 'transaction.json', Buffer.from(JSON.stringify(transaction, null, 2) + '\n'));
  }
  const attempted = [];
  try {
    for (const name of names) {
      attempted.push(name);
      writeFile(project, name, changes[name]);
    }
  } catch (error) {
    const failures = [];
    for (const name of attempted.reverse()) {
      try { writeFile(project, name, originals[name]); } catch (rollbackError) { failures.push(rollbackError.message); }
    }
    throw new Error(`${error.message}\n${failures.length ? `Ripristino incompleto: ${failures.join('; ')}` : 'File originali ripristinati.'}${backup ? `\nBackup: ${backup}` : ''}`);
  }
  return backup;
}

function planRestore(project, input) {
  const backup = path.resolve(project, input);
  const relative = path.relative(project, backup).split(path.sep).join('/');
  if (!relative.startsWith(`${BACKUPS}/`) || relative.split('/').length !== 2) throw new Error('Scegli un backup nella .agents.backups/ di questo progetto.');
  safePath(project, relative);
  const transaction = JSON.parse(readFile(backup, 'transaction.json')?.toString('utf8') || 'null');
  if (transaction?.schemaVersion !== 1 || transaction.project !== fs.realpathSync(project) || !Array.isArray(transaction.records)) {
    throw new Error('Backup non valido o appartenente a un altro progetto.');
  }
  const changes = {};
  const conflicts = [];
  for (const record of transaction.records) {
    if (!record.path?.startsWith(`${KIT}/`) ||
        ![record.before, record.after].every(digest => digest === null || /^[a-f0-9]{64}$/.test(digest))) {
      throw new Error('Voce del backup non valida.');
    }
    const original = record.before === null ? null : readFile(backup, `files/${record.path}`);
    if (hash(original) !== record.before) throw new Error(`Backup alterato: ${record.path}`);
    const current = hash(readFile(project, record.path));
    if (current === record.before) continue;
    if (current !== record.after) conflicts.push(record.path);
    changes[record.path] = original;
  }
  return { changes, conflicts };
}

function executePlan(project, plan, options) {
  for (const [name, content] of Object.entries(plan.changes)) console.log(`  ${content === null ? 'rimuovi' : 'scrivi'} ${name}`);
  if (plan.conflicts.length) console.log(`Conflitti locali:\n${plan.conflicts.map(name => `  ${name}`).join('\n')}`);
  if (plan.stale?.length) console.log(`Voci della versione precedente non più nel kit, da controllare e togliere a mano:\n${plan.stale.map(name => `  ${KIT}/${name}`).join('\n')}`);
  if (options.dryRun) {
    console.log('Anteprima: nessun file del progetto modificato.');
    if (plan.conflicts.length && !options.force) process.exitCode = 1;
    return;
  }
  if (plan.conflicts.length && !options.force) throw new Error('Modifiche locali o file non gestiti: confrontali e usa --force solo per sostituirli (gli originali finiscono in un backup).');
  // Il backup si fa solo con --backup, oppure quando --force sostituisce file cambiati a mano.
  const backup = applyChanges(project, plan.changes, options.backup || plan.conflicts.length > 0);
  if (backup) console.log(`Backup ripristinabile: ${backup}`);
  else if (!Object.keys(plan.changes).length) console.log('Nessuna modifica necessaria.');
}

function main(args = process.argv.slice(2)) {
  const options = { dryRun: args.includes('--dry-run'), force: args.includes('--force'), backup: args.includes('--backup') };
  const positional = args.filter(arg => !arg.startsWith('-'));
  const yes = args.includes('-y') || args.includes('--yes');
  const command = positional[0] || (yes ? 'init' : 'help');
  if (command === 'help' || args.includes('--help') || args.includes('-h')) {
    console.log(`Antigravity Kit v${pkg.version}\n\nComandi:\n  init -y                 Installa i file del kit\n  update                  Scarica da GitHub (un errore lascia tutto invariato)\n  restore <backup>        Ripristina un backup creato con --backup o --force\n\nOpzioni:\n  --dry-run               Mostra modifiche e conflitti senza applicarli\n  --force                 Sostituisce i file in conflitto, salvandoli in un backup\n  --backup                Conserva in .agents.backups/ i file sostituiti, per restore\n  -y, --yes               Conferma init (non scavalca i conflitti)\n`);
    return;
  }
  const known = new Set(['--dry-run', '--force', '--backup', '-y', '--yes']);
  if (args.some(arg => arg.startsWith('-') && !known.has(arg))) throw new Error('Opzione sconosciuta. Usa help.');
  if (!['init', 'update', 'restore'].includes(command)) throw new Error(`Comando sconosciuto: ${command}`);
  if (positional.length !== (command === 'restore' ? 2 : 1) && !(command === 'init' && positional.length === 0)) throw new Error('Argomenti non validi. Usa help.');
  if (command === 'init' && !yes && !options.dryRun) throw new Error('init richiede -y oppure --dry-run.');
  const project = fs.realpathSync(process.cwd());
  const localKit = path.join(localRoot, KIT);
  const destination = safePath(project, KIT);
  if (nested(localKit, destination) || nested(destination, localKit)) throw new Error('Sorgente e destinazione coincidono: esegui dal progetto destinatario.');
  let fetched = null;
  let lock = null;
  try {
    // Una sola transazione alla volta; l'anteprima non crea file nel progetto.
    if (!options.dryRun) {
      const lockPath = safePath(project, '.agents.install.lock');
      try {
        fs.writeFileSync(lockPath, String(process.pid), { flag: 'wx' });
      } catch (error) {
        if (error.code === 'EEXIST') throw new Error('Installazione bloccata da .agents.install.lock: verifica che nessun installer sia attivo prima di rimuovere un lock residuo.');
        throw error;
      }
      lock = lockPath;
    }
    if (command === 'restore') {
      executePlan(project, planRestore(project, positional[1]), options);
      return;
    }
    let sourceRoot = localRoot;
    if (command === 'update') {
      fetched = fs.mkdtempSync(path.join(os.tmpdir(), 'ag-kit-download-'));
      sourceRoot = path.join(fetched, 'repo');
      console.log(`Scarico il kit da ${repoUrl} ...`);
      execFileSync('git', ['clone', '--depth', '1', '--', repoUrl, sourceRoot], { stdio: 'pipe', timeout: 60000 });
    }
    const sourcePackage = JSON.parse(fs.readFileSync(path.join(sourceRoot, 'package.json'), 'utf8'));
    if (typeof sourcePackage.version !== 'string') throw new Error('Versione del kit sorgente mancante.');
    const metadata = { version: sourcePackage.version, source: sourceInfo(sourceRoot, repoUrl) };
    const plan = planInstall(project, path.join(sourceRoot, KIT), metadata);
    executePlan(project, plan, options);
    if (!options.dryRun) console.log(`Kit v${metadata.version} installato in ${destination} (${Object.keys(plan.files).length} file).`);
    if (fs.existsSync(path.join(project, '.agent'))) console.log('La vecchia .agent/ resta intatta: controlla eventuali regole duplicate prima di rimuoverla.');
  } finally {
    if (fetched) fs.rmSync(fetched, { recursive: true, force: true });
    if (lock) fs.unlinkSync(lock);
  }
}

if (require.main === module) {
  try { main(); } catch (error) { console.error(`Errore: ${error.message}`); process.exitCode = 1; }
}
module.exports = { applyChanges, planInstall, planRestore, main };
