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

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
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
const forceFlag = args.includes('--force') || args.includes('-f');

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
    init       Install .agent/ folder into current project
    update     Fetch latest .agent/ from GitHub and overwrite the local copy
    status     Show what would be installed
    force      Force overwrite existing .agent/ folder
    help       Show this help

  Options:
    -y, --yes  Auto-complete installation automatically
    --force    Overwrite existing .agent/ folder
  `);
  process.exit(0);
}

if (command === 'status') {
  const { agents, skills, workflows } = getCounts(localAgentDir);
  console.log(`Antigravity Kit (Andryd22 fork) ${version}`);
  console.log(`  Agents:    ${agents} (incl. AI/ML, IoT, LaTeX, API designer)`);
  console.log(`  Skills:    ${skills} (incl. caveman-mode, scroll-film-studio, embedded-systems, html-it)`);
  console.log(`  Workflows: ${workflows} (incl. /caveman, /html-it, /scroll-film)`);
  console.log('  Features:  Caveman Mode, Scroll-Film Studio, Next.js 16 support, academic LaTeX');
  process.exit(0);
}

if (command === 'force') {
  command = 'init';
}

if (command !== 'init' && command !== 'update') {
  console.error(`Unknown command: ${command}`);
  console.error('Usage: npx github:Andryd22/AG-agents-skills [init|update|status|force] [-y]');
  process.exit(1);
}

const force = autoYes || forceFlag || command === 'update';
const targetDir = process.cwd();
const destDir = path.join(targetDir, '.agent');

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

if (!fs.existsSync(sourceDir)) {
  console.error(`Error: Source .agent/ not found at ${sourceDir}`);
  process.exit(1);
}

if (force && fs.existsSync(destDir)) {
  fs.rmSync(destDir, { recursive: true, force: true });
}
copyDir(sourceDir, destDir);

// Count installed files
let count = 0;
function countInstalled(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory()) countInstalled(path.join(dir, entry.name));
    else count++;
  }
}
countInstalled(destDir);

const { agents, skills, workflows } = getCounts(sourceDir);
console.log(`Installed .agent/ to ${targetDir}`);
console.log(`  ${count} files — ${agents} agents, ${skills} skills, ${workflows} workflows`);
console.log(`  Try /caveman in your IDE to enable Caveman Mode`);

if (fetched) {
  fetched.cleanup();
}
