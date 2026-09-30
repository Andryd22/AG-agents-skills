"""Regressioni dell'installer: tutti i progetti usati sono temporanei."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
NODE = shutil.which("node")


@unittest.skipUnless(NODE, "Node necessario")
class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ag-kit-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "source"
        self.project = self.base / "project with spaces"
        self.project.mkdir()
        shutil.copytree(ROOT / "bin", self.source / "bin")
        self.write(self.source / "package.json", json.dumps({
            "version": "4.3.0", "repository": {"url": str(self.base / "missing-repository")}
        }))
        self.write(self.source / ".agents/scripts/check.py", "print('original')\n")
        self.write(self.source / ".agents/skills/example/SKILL.md", "example\n")

    def write(self, path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    def run_cli(self, *args, env=None, project=None):
        return subprocess.run([NODE, str(self.source / "bin/install.js"), *args],
                              cwd=project or self.project, env=env, capture_output=True,
                              text=True, encoding="utf-8", timeout=30)

    def install(self):
        result = self.run_cli("init", "-y")
        self.assertEqual(result.returncode, 0, result.stderr)

    def snapshot(self):
        return {p.relative_to(self.project).as_posix(): p.read_bytes()
                for p in self.project.rglob("*") if p.is_file()}

    def test_preserves_personal_file_inside_managed_directory(self):
        personal = self.project / ".agents/scripts/personal.py"
        self.write(personal, "personal\n")
        self.install()
        self.assertTrue(personal.exists(), "L'installer ha cancellato uno script personale")
        self.assertEqual(personal.read_text(), "personal\n")

    def test_download_failure_preserves_existing_installation(self):
        self.install()
        before = self.snapshot()
        result = self.run_cli("update")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_dry_run_does_not_write(self):
        before = self.snapshot()
        result = self.run_cli("init", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_manifest_tracks_hashes_per_file(self):
        self.install()
        manifest = json.loads((self.project / ".agents/.ag-kit.json").read_text())
        expected = hashlib.sha256(b"print('original')\n").hexdigest()
        self.assertEqual(manifest.get("files", {}).get("scripts/check.py"), expected)
        self.assertIn("source", manifest)

    def test_modified_file_blocks_update_without_changing_other_files(self):
        self.install()
        self.write(self.project / ".agents/scripts/check.py", "personal change\n")
        self.write(self.source / ".agents/skills/example/SKILL.md", "new version\n")
        before = self.snapshot()
        result = self.run_cli("init", "-y")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_force_creates_restorable_backup(self):
        self.install()
        self.write(self.project / ".agents/scripts/check.py", "personal change\n")
        result = self.run_cli("init", "-y", "--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        backups = sorted((self.project / ".agents.backups").glob("*/transaction.json"))
        self.assertTrue(backups, "Backup mancante")
        result = self.run_cli("restore", str(backups[-1].parent))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.project / ".agents/scripts/check.py").read_text(), "personal change\n")

    def test_removes_only_unmodified_stale_managed_files(self):
        self.install()
        personal = self.project / ".agents/scripts/personal.py"
        self.write(personal, "personal\n")
        (self.source / ".agents/scripts/check.py").unlink()
        self.install()
        self.assertFalse((self.project / ".agents/scripts/check.py").exists())
        self.assertTrue(personal.exists())

    def test_legacy_manifest_does_not_claim_personal_files(self):
        personal = self.project / ".agents/scripts/personal.py"
        self.write(personal, "personal\n")
        self.write(self.project / ".agents/.ag-kit.json", json.dumps({"entries": ["scripts"]}))
        self.install()
        self.assertTrue(personal.exists())

    def test_legacy_leftovers_are_reported_not_removed(self):
        old = self.project / ".agents/skills/old-kit-skill/SKILL.md"
        self.write(old, "old\n")
        self.write(self.project / ".agents/.ag-kit.json", json.dumps({"entries": ["skills/old-kit-skill", "scripts"]}))
        result = self.run_cli("init", "-y")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(".agents/skills/old-kit-skill", result.stdout)
        self.assertNotIn(".agents/scripts\n", result.stdout)
        self.assertTrue(old.exists())

    def test_npmignore_is_not_installed(self):
        self.write(self.source / ".agents/.npmignore", "**/__pycache__/\n")
        self.install()
        self.assertFalse((self.project / ".agents/.npmignore").exists())

    def test_rejects_manifest_paths_outside_project(self):
        self.write(self.project / ".agents/.ag-kit.json", json.dumps({
            "schemaVersion": 2, "files": {"../../outside": "0" * 64}
        }))
        before = self.snapshot()
        result = self.run_cli("init", "-y", "--force")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_rejects_install_into_source(self):
        before = (self.source / ".agents/scripts/check.py").read_bytes()
        result = self.run_cli("init", "-y", project=self.source)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.source / ".agents/scripts/check.py").read_bytes(), before)

    def test_rollback_after_a_write_failure(self):
        self.install()
        self.write(self.source / ".agents/scripts/check.py", "new script\n")
        self.write(self.source / ".agents/skills/example/SKILL.md", "new skill\n")
        before = {p.relative_to(self.project): p.read_bytes() for p in (self.project / '.agents').rglob('*') if p.is_file()}
        # Simula un errore del filesystem sul secondo file, dopo una scrittura riuscita.
        code = """
const fs = require('fs');
const path = require('path');
const installer = require(process.argv[1]);
const rename = fs.renameSync;
let failed = false;
fs.renameSync = (source, dest) => {
  if (!failed && dest === path.join(process.cwd(), '.agents/skills/example/SKILL.md')) {
    failed = true;
    throw new Error('Errore disco simulato');
  }
  return rename(source, dest);
};
try { installer.main(['init', '-y']); } catch (error) { console.error(error.message); process.exitCode = 1; }
"""
        result = subprocess.run([NODE, '-e', code, str(self.source / 'bin/install.js')],
                                cwd=self.project, capture_output=True, text=True, encoding='utf-8')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('File originali ripristinati', result.stderr)
        after = {p.relative_to(self.project): p.read_bytes() for p in (self.project / '.agents').rglob('*') if p.is_file()}
        self.assertEqual(after, before)

    def test_restore_refuses_changes_made_after_install(self):
        self.install()
        backup = next((self.project / '.agents.backups').glob('*/transaction.json')).parent
        self.write(self.project / '.agents/scripts/check.py', 'later change\n')
        before = self.snapshot()
        result = self.run_cli('restore', str(backup))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_existing_lock_is_preserved(self):
        self.write(self.project / '.agents.install.lock', 'other-installer')
        before = self.snapshot()
        result = self.run_cli('init', '-y')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_symlink_destination_is_rejected(self):
        outside = self.base / 'outside'
        outside.mkdir()
        try:
            (self.project / '.agents').symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('Creazione symlink non consentita su questa macchina')
        result = self.run_cli('init', '-y', '--force')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])

    @unittest.skipUnless(shutil.which('git'), 'Git necessario')
    def test_successful_update_records_source_commit(self):
        def git(*args):
            return subprocess.run(['git', '-C', str(self.source), *args], check=True,
                                  capture_output=True, text=True).stdout.strip()
        git('init')
        git('config', 'user.email', 'test@example.invalid')
        git('config', 'user.name', 'Installer Test')
        self.write(self.source / 'package.json', json.dumps({'version': '4.3.0', 'repository': {'url': str(self.source)}}))
        git('add', '.')
        git('commit', '-m', 'fixture')
        commit = git('rev-parse', 'HEAD')
        result = self.run_cli('update')
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((self.project / '.agents/.ag-kit.json').read_text())
        self.assertEqual(manifest['source']['commit'], commit)


if __name__ == "__main__":
    unittest.main()
