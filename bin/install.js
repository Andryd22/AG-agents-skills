#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execSync } = require('child_process');
const pkg = require('../package.json');
const version = `v${pkg.version}`;

const KIT = '.agents';
const MANIFEST = '.ag-kit.json'; // inside .agents/: the entries the kit installed, removed on the next update
const localKitDir = path.resolve(__dirname, '..', KIT);
const repoUrl = (pkg.repository && pkg.repository.url || 'https://github.com/Andryd22/AG-agents-skills.git').replace(/^git\+/, '');

// Count real content of .agents/ instead of hardcoding numbers
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

// What the kit owns inside .agents/: every agent, skill and rule on its own,
// every other top-level item (ARCHITECTURE.md, scripts/) as a whole.
// Anything else in the project's .agents/ belongs to the user and is left alone.
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
    // only plain "name" or "folder/name" entries: never a path outside .agents/
    const safe = e => typeof e === 'string' && /^[\w.-]+(\/[\w.-]+)?$/.test(e) && !e.split('/').some(s => s === '.' || s === '..');
    return Array.isArray(data.entries) ? data.entries.filter(safe) : [];
  } catch {
    return [];
  }
}

// Clone the latest .agents/ straight from GitHub
function fetchLatestFromGitHub() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'ag-agents-skills-'));
  try {
    execSync(`git clone --depth 1 "${repoUrl}" "${path.join(tmp, 'repo')}"`, { stdio: 'pipe' });
    const fetched = path.join(tmp, 'repo', KIT);
    if (!fs.existsSync(fetched)) throw new Error(`${KIT}/ not found in cloned repo`);
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
  Antigravity Kit (Andryd22 fork) — ${version}
  ${agents} agents | ${skills} skills | Caveman Mode

  Usage:
    npx github:Andryd22/AG-agents-skills [command] [options]

  Commands:
    init -y    Install the kit into .agents/ of the current project
    update     Fetch the latest kit from GitHub and install it
    help       Show this help

  Your own agents, skills and rules in .agents/ are kept; the kit's are replaced.

  Options:
    -y, --yes  Confirm the installation
  `);
  process.exit(0);
}

if (command === 'init' && !autoYes) {
  console.error(`Error: init requires -y (replaces the kit's files in ${KIT}/).`);
  console.error('Usage: npx github:Andryd22/AG-agents-skills init -y');
  process.exit(1);
}

if (command !== 'init' && command !== 'update') {
  console.error(`Unknown command: ${command}`);
  console.error('Usage: npx github:Andryd22/AG-agents-skills [init -y|update]');
  process.exit(1);
}

const targetDir = process.cwd();
const destDir = path.join(targetDir, KIT);

function fail(msg) {
  throw new Error(msg); // thrown so that the finally block still removes the temporary clone
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
  console.log(`Fetching latest ${KIT}/ from ${repoUrl} ...`);
  try {
    fetched = fetchLatestFromGitHub();
    sourceDir = fetched.dir;
  } catch (err) {
    console.error(`Warning: could not fetch from GitHub (${err.message.trim()})`);
    console.error('Falling back to the locally installed version.');
  }
}

const staging = path.join(targetDir, `${KIT}.tmp-${process.pid}`);
try {
  if (!fs.existsSync(sourceDir)) fail(`source ${KIT}/ not found at ${sourceDir}`);
  // Installing the kit onto itself (e.g. from the kit repo) would delete the source.
  if (sameOrNested(sourceDir, destDir) || sameOrNested(destDir, sourceDir)) {
    fail(`source and destination are the same ${KIT}/ (${destDir}).\n` +
      'Run this command from the project you want to install into, not from the kit itself.');
  }

  // Copy first: the project's .agents/ is touched only if the copy succeeded.
  fs.rmSync(staging, { recursive: true, force: true });
  copyDir(sourceDir, staging);
  const count = countFiles(staging);
  if (count === 0) fail(`nothing copied from ${sourceDir}`);

  const entries = kitEntries(staging);
  const previous = readManifest(destDir);
  const stale = previous.filter(e => !entries.includes(e));
  const replaced = entries.filter(e => fs.existsSync(path.join(destDir, e)));

  // Remove what the previous version installed and what this one replaces, then move the new files in.
  for (const e of new Set([...previous, ...entries])) {
    fs.rmSync(path.join(destDir, e), { recursive: true, force: true });
  }
  for (const e of entries) {
    fs.mkdirSync(path.dirname(path.join(destDir, e)), { recursive: true });
    fs.renameSync(path.join(staging, e), path.join(destDir, e));
  }
  fs.writeFileSync(path.join(destDir, MANIFEST), JSON.stringify({ version: pkg.version, entries }, null, 2) + '\n');

  // Older versions of the kit lived in .agent/: Antigravity still reads its rules, so move it aside.
  const legacy = path.join(targetDir, '.agent');
  let legacyMoved = null;
  if (fs.existsSync(path.join(legacy, 'ARCHITECTURE.md'))) {
    legacyMoved = path.join(targetDir, fs.existsSync(path.join(targetDir, '.agent.bak')) ? `.agent.bak-${Date.now()}` : '.agent.bak');
    fs.renameSync(legacy, legacyMoved);
  }

  const { agents, skills } = getCounts(destDir);
  console.log(`Installed the kit in ${destDir}`);
  console.log(`  ${count} files — ${agents} agents, ${skills} skills (your own ones included)`);
  if (replaced.length) console.log(`  ${replaced.length} kit entries replaced (local edits to them are not kept)`);
  if (stale.length) console.log(`  Removed from the previous version: ${stale.join(', ')}`);
  if (legacyMoved) console.log(`  The old kit folder .agent/ was moved to ${path.basename(legacyMoved)}/: delete it once you have checked it.`);
  console.log('  Try /caveman in your IDE to enable Caveman Mode');
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exitCode = 1;
} finally {
  fs.rmSync(staging, { recursive: true, force: true });
  if (fetched) fetched.cleanup();
}
