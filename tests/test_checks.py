"""Controlli reali su piccoli progetti temporanei, senza dipendenze da installare."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / ".agents/skills/test/scripts/test_runner.py"


def last_json(output):
    decoder = json.JSONDecoder()
    for index, char in enumerate(output):
        if char == "{":
            try:
                value, end = decoder.raw_decode(output[index:])
                if not output[index + end:].strip():
                    return value
            except ValueError:
                pass
    raise AssertionError(output)


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ag-check-test-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)

    def run_script(self, script, *args):
        env = {**os.environ, "PYTHONUTF8": "1"}
        return subprocess.run([sys.executable, str(script), str(self.project), *args],
                              capture_output=True, text=True, encoding="utf-8", env=env, timeout=30)

    def test_absent_tests_are_skipped(self):
        result = self.run_script(RUNNER)
        report = last_json(result.stdout)
        self.assertIsNot(report.get("passed"), True)
        self.assertEqual(report.get("status"), "skipped")

    def test_python_dependencies_alone_do_not_configure_tests(self):
        (self.project / 'requirements.txt').write_text('pandas\nscikit-learn\n')
        result = self.run_script(RUNNER, '--json')
        report = last_json(result.stdout)
        self.assertEqual(report['status'], 'skipped')

    def test_unknown_test_count_is_not_reported_as_zero(self):
        (self.project / 'package.json').write_text(json.dumps({'scripts': {'test': 'node -e "process.exit(0)"'}}))
        result = self.run_script(RUNNER, '--json')
        report = last_json(result.stdout)
        self.assertIsNone(report.get('tests_run'))

    @unittest.skipUnless(shutil.which("npm") and shutil.which("node"), "Node/npm necessari")
    def test_node_project_executes_on_current_platform(self):
        (self.project / "package.json").write_text(json.dumps({
            "scripts": {"test": 'node -e "process.exit(0)"'}
        }))
        result = self.run_script(RUNNER)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(last_json(result.stdout).get("status"), "passed")

    def test_empty_checklist_does_not_claim_success(self):
        result = self.run_script(ROOT / ".agents/scripts/checklist.py")
        self.assertNotIn("Tutti i controlli SUPERATI", result.stdout)
        self.assertIn("skipped", result.stdout)
        self.assertIn("not_applicable", result.stdout)

    def test_checklist_json_reports_incomplete_verification(self):
        result = self.run_script(ROOT / ".agents/scripts/checklist.py", "--json")
        report = last_json(result.stdout)
        self.assertEqual(report["status"], "incomplete")
        self.assertEqual(report["counts"]["passed"], 0)

    def test_full_suite_accepts_non_web_project(self):
        result = self.run_script(ROOT / ".agents/scripts/verify_all.py", "--json")
        report = last_json(result.stdout)
        self.assertEqual(report["status"], "incomplete")

    def test_invalid_project_fails(self):
        self.project = self.project / "missing"
        result = self.run_script(RUNNER)
        self.assertNotEqual(result.returncode, 0)

    def test_broken_package_json_fails(self):
        (self.project / "package.json").write_text("{broken")
        result = self.run_script(RUNNER)
        self.assertNotEqual(result.returncode, 0)

    def test_latex_project_uses_structural_check(self):
        (self.project / 'latex').mkdir()
        (self.project / 'latex/main.tex').write_text('\\documentclass{book}\n\\begin{document}\nTest\n\\end{document}\n')
        result = self.run_script(ROOT / '.agents/scripts/checklist.py', '--json')
        report = last_json(result.stdout)
        latex = next(item for item in report['results'] if item['name'].startswith('LaTeX'))
        self.assertEqual(latex['status'], 'passed', latex)
        self.assertIn('non compilazione', latex['name'])
        tests = next(item for item in report['results'] if item['name'] == 'Test del progetto')
        self.assertEqual(tests['status'], 'not_applicable')

    def test_latex_subprojects_are_all_checked(self):
        for teacher in ('Alfa', 'Beta'):
            (self.project / 'latex' / teacher).mkdir(parents=True)
            (self.project / 'latex' / teacher / 'main.tex').write_text('\\documentclass{book}\n\\begin{document}\nTest\n\\end{document}\n')
        result = self.run_script(ROOT / '.agents/scripts/checklist.py', '--json')
        report = last_json(result.stdout)
        latex = [item for item in report['results'] if item['name'].startswith('LaTeX')]
        self.assertEqual([item['name'] for item in latex],
                         ['LaTeX latex/Alfa (struttura; non compilazione)', 'LaTeX latex/Beta (struttura; non compilazione)'])
        self.assertTrue(all(item['status'] == 'passed' for item in latex), latex)
        self.assertEqual(report['status'], 'passed')

    def test_listing_labels_are_defined(self):
        (self.project / 'main.tex').write_text(
            '\\documentclass{book}\n\\begin{document}\nVedi il Listato~\\ref{lst:uno} e~\\ref{lst:due}.\n'
            '\\begin{lstlisting}[style=mystyle, caption={Codice [slide 3]},\n  label={lst:uno}]\nx = 1\n\\end{lstlisting}\n'
            '\\lstinputlisting[label=lst:due]{codice.py}\nE~\\ref{lst:tre}.\n\\end{document}\n')
        result = self.run_script(ROOT / '.agents/skills/latex-review/scripts/check_project.py')
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('lst:tre', result.stdout)
        self.assertNotIn("'lst:uno'", result.stdout)
        self.assertNotIn("'lst:due'", result.stdout)

    def test_check_project_finds_every_document_in_latex(self):
        for teacher, body in (('Alfa', 'Test'), ('Beta', 'Vedi~\\ref{sec:manca}.')):
            (self.project / 'latex' / teacher).mkdir(parents=True)
            (self.project / 'latex' / teacher / 'main.tex').write_text(
                '\\documentclass{book}\n\\begin{document}\n' + body + '\n\\end{document}\n')
        result = self.run_script(ROOT / '.agents/skills/latex-review/scripts/check_project.py')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stdout.count('Progetto: '), 2, result.stdout)
        self.assertIn('sec:manca', result.stdout)

    def test_nonzero_exit_cannot_be_overridden_by_child_json(self):
        spec = importlib.util.spec_from_file_location('checks', ROOT / '.agents/scripts/check_support.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        child = self.project / 'child.py'
        child.write_text('import sys\nprint(\'{"status":"success"}\')\nsys.exit(1)\n')
        result = module.run_script('child', child, self.project)
        self.assertEqual(result['status'], 'failed')

    def test_missing_script_is_failed(self):
        spec = importlib.util.spec_from_file_location('checks', ROOT / '.agents/scripts/check_support.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.run_script('missing', self.project / 'missing.py', self.project)
        self.assertEqual(result['status'], 'failed')

    def test_failure_output_is_kept_in_report(self):
        (self.project / 'package.json').write_text(json.dumps({'scripts': {'test': 'node -e "console.log(123456);process.exit(1)"'}}))
        result = self.run_script(ROOT / '.agents/scripts/checklist.py', '--json')
        report = last_json(result.stdout)
        self.assertEqual(report['status'], 'failed')
        self.assertIn('123456', json.dumps(report))

    def test_backups_are_not_audited_as_project_source(self):
        backup = self.project / '.agents.backups/fixture/files/.agents'
        backup.mkdir(parents=True)
        (backup / 'index.html').write_text('<img src="image.png">')
        result = self.run_script(ROOT / '.agents/scripts/checklist.py', '--json')
        report = last_json(result.stdout)
        ux = next(item for item in report['results'] if item['name'].startswith('UX'))
        self.assertEqual(ux['status'], 'not_applicable')


if __name__ == "__main__":
    unittest.main()
