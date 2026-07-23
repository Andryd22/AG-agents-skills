#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const pkg = require('../package.json');
const version = `v${pkg.version}`;

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
  console.log(`
  Antigravity Kit (Andryd22 fork) — ${version}
  25 agents | 48 skills | 13 workflows | Caveman Mode

  Usage:
    npx github:Andryd22/AG-agents-skills [command] [options]

  Commands:
    init       Install .agent/ folder into current project
    update     Update to the latest version (overwrites .agent/)
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
  console.log(`Antigravity Kit (Andryd22 fork) ${version}`);
  console.log('  Agents:    25 (incl. AI/ML, IoT, LaTeX, API designer)');
  console.log('  Skills:    49 (incl. caveman-mode, scroll-film-studio, embedded-systems, html-it)');
  console.log('  Workflows: 14 (incl. /caveman, /html-it, /scroll-film)');
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
const sourceDir = path.resolve(__dirname, '..', '.agent');
const destDir = path.join(targetDir, '.agent');

if (!fs.existsSync(sourceDir)) {
  console.error(`Error: Source .agent/ not found at ${sourceDir}`);
  process.exit(1);
}

if (fs.existsSync(destDir) && !force) {
  console.error(`Error: .agent/ already exists in ${targetDir}`);
  console.error('Use -y or --force to overwrite existing files.');
  process.exit(1);
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

console.log(`Installed .agent/ to ${targetDir}`);
console.log(`  ${count} files — 25 agents, 48 skills, 13 workflows`);
console.log(`  Try /caveman in your IDE to enable Caveman Mode`);

