#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const command = args[0];

if (!command || command === 'help' || command === '--help') {
  console.log(`
  Antigravity Kit (Andryd22 fork) — v2.1.0
  25 agents | 48 skills | 13 workflows | Caveman Mode

  Usage:
    npx github:Andryd22/AG-agents-skills init [options]

  Commands:
    init       Install .agent/ folder into current project
    update     Update to the latest version (overwrites .agent/)
    status     Show what would be installed
    help       Show this help

  Options:
    --force    Overwrite existing .agent/ folder
    --path     Target directory (default: current directory)
    --quiet    Suppress output
    --dry-run  Preview without writing files
  `);
  process.exit(0);
}

if (command === 'status') {
  console.log('Antigravity Kit (Andryd22 fork) v2.1.0');
  console.log('  Agents:    25 (incl. AI/ML, IoT, LaTeX, API designer)');
  console.log('  Skills:    48 (incl. caveman-mode, prompt-engineering, embedded-systems, html-it)');
  console.log('  Workflows: 13 (incl. /caveman, /html-it)');
  console.log('  Features:  Caveman Mode, Next.js 16 support, academic LaTeX');
  process.exit(0);
}

if (command !== 'init' && command !== 'update') {
  console.error(`Unknown command: ${command}`);
  console.error('Usage: ag-kit-andryd init');
  process.exit(1);
}

let force = args.includes('--force') || command === 'update';
const dryRun = args.includes('--dry-run');
const quiet = args.includes('--quiet');

const pathIdx = args.indexOf('--path');
const targetDir = pathIdx !== -1 ? path.resolve(args[pathIdx + 1] || '.') : process.cwd();

const sourceDir = path.resolve(__dirname, '..', '.agent');
const destDir = path.join(targetDir, '.agent');

if (!fs.existsSync(sourceDir)) {
  console.error(`Error: Source .agent/ not found at ${sourceDir}`);
  process.exit(1);
}

if (fs.existsSync(destDir) && !force && !dryRun) {
  console.error(`Error: .agent/ already exists in ${targetDir}`);
  console.error('Use --force to overwrite, or --dry-run to preview.');
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
      if (!dryRun) fs.copyFileSync(srcPath, destPath);
    }
  }
}

if (dryRun) {
  let count = 0;
  function countFiles(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isDirectory()) {
        countFiles(path.join(dir, entry.name));
      } else {
        count++;
      }
    }
  }
  countFiles(sourceDir);
  console.log(`[DRY RUN] Would install ${count} files to ${destDir}`);
  console.log('  25 agents, 48 skills, 13 workflows');
  console.log('  Includes: Caveman Mode, AI/ML, IoT, LaTeX, Data Engineering');
} else {
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

  if (!quiet) {
    console.log(`Installed .agent/ to ${targetDir}`);
    console.log(`  ${count} files — 25 agents, 48 skills, 13 workflows`);
    console.log(`  Try /caveman on in your IDE to enable Caveman Mode`);
  }
}
