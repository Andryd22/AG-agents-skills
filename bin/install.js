#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execSync } = require('child_process');
const pkg = require('../package.json');
const version = `v${pkg.version}`;

const localAgentDir = path.resolve(__dirname, '..', '.agent');
const repoUrl = (pkg.repository && pkg.repository.url || 'https://github.com/Andryd22/AG-agents-skills.git').replace(/^git\+/, '');

// Count real content of .agent/ instead of hardcoding numbers
function countMdFiles(dir) {
  if (!fs.existsSync(dir)) return 0;
  return fs.readdirSync(dir, { withFileTypes: true }).filter(e => e.isFile() && e.name.endsWith('.md')).length;
}
function countDirs(dir) {
  if (!fs.existsSync(dir)) return 0;
  return fs.readdirSync(dir, { withFileTypes: true }).filter(e => e.isDirectory()).length;
}
function getCounts(agentDir) {
  return {
    agents: countMdFiles(path.join(agentDir, 'agents')),
    skills: countDirs(path.join(agentDir, 'skills')),
    workflows: countMdFiles(path.join(agentDir, 'workflows')),
  };
}

const SKIP = new Set(['__pycache__', '.DS_Store']);

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    if (SKIP.has(entry.name) || entry.name.endsWith('.pyc')) continue;
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Clone the latest .agent/ straight from GitHub
function fetchLatestFromGitHub() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'ag-agents-skills-'));
  try {
    execSync(`git clone --depth 1 "${repoUrl}" "${path.join(tmp, 'repo')}"`, { stdio: 'pipe' });
    const fetched = path.join(tmp, 'repo', '.agent');
    if (!fs.existsSync(fetched)) {
      throw new Error('.agent/ not found in cloned repo');
    }
    return {
      dir: fetched,
      cleanup: () => fs.rmSync(tmp, { recursive: true, force: true }),
    };
  } catch (err) {
    fs.rmSync(tmp, { recursive: true, force: true });
    throw err;
  }
}

const args = process.argv.slice(2);
const autoYes = args.includes('-y') || args.includes('--yes');

// Filter out flag args to find positional command
const positionalArgs = args.filter(a => !a.startsWith('-'));
let command = positionalArgs[0];

// If -y is provided without explicit command, default to init
if (!command && autoYes) {
  command = 'init';
}

if (!command || command === 'help' || command === '--help' || args.includes('-h')) {
  const { agents, skills, workflows } = getCounts(localAgentDir);
  console.log(`
  Antigravity Kit (Andryd22 fork) — ${version}
  ${agents} agents | ${skills} skills | ${workflows} workflows | Caveman Mode

  Usage:
    npx github:Andryd22/AG-agents-skills [command] [options]

  Commands:
    init -y    Install .agent/ folder into current project (overwrites)
    update     Fetch latest .agent/ from GitHub and overwrite the local copy
    help       Show this help

  Options:
    -y, --yes  Auto-complete installation automatically
  `);
  process.exit(0);
}

if (command === 'init' && !autoYes) {
  console.error('Error: init requires -y (overwrites existing .agent/).');
  console.error('Usage: npx github:Andryd22/AG-agents-skills init -y');
  process.exit(1);
}

if (command !== 'init' && command !== 'update') {
  console.error(`Unknown command: ${command}`);
  console.error('Usage: npx github:Andryd22/AG-agents-skills [init -y|update]');
  process.exit(1);
}

const targetDir = process.cwd();
const destDir = path.join(targetDir, '.agent');

function countFiles(dir) {
  if (!fs.existsSync(dir)) return 0;
  let n = 0;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    n += entry.isDirectory() ? countFiles(path.join(dir, entry.name)) : 1;
  }
  return n;
}

// Throws so that the finally block below still removes the temporary GitHub clone.
function fail(msg) {
  throw new Error(msg);
}

// Refuse to install the kit onto itself (e.g. running init/update from the kit repo):
// removing the destination would delete the source too.
function realOrResolved(p) {
  return fs.existsSync(p) ? fs.realpathSync(p) : path.resolve(p);
}
function sameOrNested(a, b) {
  const rel = path.relative(realOrResolved(a), realOrResolved(b));
  return rel === '' || (!rel.startsWith('..') && !path.isAbsolute(rel));
}

// update: pull the latest version straight from GitHub, fall back to local copy
let sourceDir = localAgentDir;
let fetched = null;
if (command === 'update') {
  console.log(`Fetching latest .agent/ from ${repoUrl} ...`);
  try {
    fetched = fetchLatestFromGitHub();
    sourceDir = fetched.dir;
  } catch (err) {
    console.error(`Warning: could not fetch from GitHub (${err.message.trim()})`);
    console.error('Falling back to the locally installed version.');
    sourceDir = localAgentDir;
  }
}

try {
  if (!fs.existsSync(sourceDir)) fail(`source .agent/ not found at ${sourceDir}`);
  if (sameOrNested(sourceDir, destDir) || sameOrNested(destDir, sourceDir)) {
    fail(`source and destination are the same .agent/ (${destDir}).\n` +
      'Run this command from the project you want to install into, not from the kit itself.');
  }

  // Copy into a staging folder first: the existing .agent/ is replaced only if the copy succeeded.
  const staging = path.join(targetDir, `.agent.tmp-${process.pid}`);
  const previous = path.join(targetDir, `.agent.old-${process.pid}`);
  fs.rmSync(staging, { recursive: true, force: true });
  copyDir(sourceDir, staging);
  const count = countFiles(staging);
  if (count === 0) {
    fs.rmSync(staging, { recursive: true, force: true });
    fail(`nothing copied from ${sourceDir}`);
  }

  const hadPrevious = fs.existsSync(destDir);
  if (hadPrevious) fs.renameSync(destDir, previous);
  try {
    fs.renameSync(staging, destDir);
  } catch (err) {
    if (hadPrevious) fs.renameSync(previous, destDir);
    fs.rmSync(staging, { recursive: true, force: true });
    throw err;
  }
  if (hadPrevious) fs.rmSync(previous, { recursive: true, force: true });

  const { agents, skills, workflows } = getCounts(destDir);
  console.log(`Installed .agent/ to ${targetDir}`);
  console.log(`  ${count} files — ${agents} agents, ${skills} skills, ${workflows} workflows`);
  if (hadPrevious) console.log('  The previous .agent/ was replaced (local edits to it are not kept).');
  console.log('  Try /caveman in your IDE to enable Caveman Mode');
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exitCode = 1;
} finally {
  if (fetched) fetched.cleanup();
}
