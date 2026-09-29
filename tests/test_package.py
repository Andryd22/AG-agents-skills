"""Il pacchetto distribuito contiene le risorse necessarie, non gli output locali."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('npm'), 'npm necessario')
    def test_pack_excludes_generated_files_and_includes_runtime(self):
        result = subprocess.run([shutil.which('npm'), 'pack', '--dry-run', '--json'],
                                cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        paths = {item['path'] for item in json.loads(result.stdout)[0]['files']}
        self.assertIn('.agents/scripts/check_support.py', paths)
        self.assertIn('.agents/skills/kit-plan/SKILL.md', paths)
        self.assertIn('docs/ANTIGRAVITY-COMPATIBILITY.md', paths)
        self.assertNotIn('.agents/skills/plan/SKILL.md', paths)
        generated = [name for name in paths if '__pycache__' in name or name.endswith('.pyc')
                     or (name.startswith('.agents/skills/latex-tutor/assets/') and not name.endswith('.tex'))]
        self.assertEqual(generated, [])
