"""提出APKの証拠収集が原本・既存結果を壊さず、未確認を正しく残すことを確かめる。"""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
from shutil import copy2, which
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile


SCRIPT = Path(__file__).with_name("student-apk-review.py")


@unittest.skipUnless(which("git"), "検証用リポジトリにはGitが必要です。")
class StudentApkReviewTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.parent = Path(temporary.name).resolve()
        self.root = self.parent / "repository"
        (self.root / "scripts").mkdir(parents=True)
        self.script = self.root / "scripts" / SCRIPT.name
        copy2(SCRIPT, self.script)
        (self.root / "config").mkdir()
        config = {"projects": [
            {"name": name, "kind": "android", "root": name,
             "package": "jp.ac.jec.reference",
             "docs": [f"docs/{slug}/index.html", f"teacher/{slug}/index.html"]}
            for name, slug in (("A01HelloAndroid", "hello-android"),
                               ("A02CalcGame", "calc-game"),
                               ("A03GithubSearch", "github-search"),
                               ("A04FunnyCamera", "funny-camera"))
        ]}
        config["projects"].extend([
            {"name": "K01HelloKotlin", "kind": "kotlin-console"},
            {"name": "UnknownKind", "kind": "future-kind"},
            {"name": "MissingKind"},
        ])
        self.config = self.root / "config/teaching-materials.json"
        self.config.write_text(json.dumps(config), encoding="utf-8")
        self.git("init")
        self.git("add", "scripts/student-apk-review.py", "config/teaching-materials.json")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-m", "検証用の教材")
        self.git("tag", "materials-test")
        self.commit = self.git("rev-parse", "HEAD").stdout.strip()
        self.apk = self.parent / "submission.apk"
        with ZipFile(self.apk, "w") as archive:
            archive.writestr("AndroidManifest.xml", "fixture manifest")
            archive.writestr("classes.dex", "fixture dex")
            archive.writestr("res/layout/activity_main.xml", "fixture layout")
        self.original = self.apk.read_bytes()
        self.output = self.parent / "results"
        self.analyzer = self.parent / "fake-apkanalyzer"
        self.analyzer.write_text(
            f"#!{sys.executable}\n"
            "import sys, time\n"
            "if 'manifest' in sys.argv:\n"
            " print('<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\" '"
            "'package=\"student.changed\" android:versionCode=\"1\">'"
            "'<uses-sdk android:minSdkVersion=\"24\" android:targetSdkVersion=\"36\"/>'"
            "'<application><activity-alias android:name=\".Entry\" '"
            "'android:targetActivity=\"custom.feature.MainActivity\">"
            "<intent-filter><category android:name=\"android.intent.category.LAUNCHER\"/>"
            "</intent-filter></activity-alias></application>'"
            "'</manifest>')\n"
            "elif 'dex' in sys.argv:\n"
            " print('C d 1\t1\t32\tstudent.changed.MainActivity')\n"
            "else:\n"
            " print('<TextView/>')\n",
            encoding="utf-8",
        )
        self.analyzer.chmod(0o755)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              capture_output=True, text=True)

    def run_review(self, *extra, output=None, ref="materials-test", analyzer=None):
        return subprocess.run(
            [sys.executable, str(self.script), "inspect", "--apk", str(self.apk),
             "--project", "A01HelloAndroid", "--baseline-ref", ref,
             "--output", str(output or self.output), "--apkanalyzer",
             str(analyzer or self.analyzer), *extra],
            cwd=self.root, capture_output=True, text=True,
        )

    def evidence(self):
        return json.loads((self.output / "evidence.json").read_text(encoding="utf-8"))

    def test_collects_exact_baseline_and_does_not_grade_changed_package(self):
        self.config.write_text('{"projects": []}', encoding="utf-8")
        result = self.run_review("--resource", "/res/layout/activity_main.xml")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = self.evidence()
        self.assertEqual(data["baseline"]["commit"], self.commit)
        self.assertEqual(data["baseline"]["project"]["kind"], "android")
        self.assertEqual(data["apk"]["sha256"], hashlib.sha256(self.original).hexdigest())
        self.assertEqual(data["manifest"]["application_id"], "student.changed")
        self.assertEqual(data["manifest"]["target_sdk"], "36")
        self.assertEqual(data["dynamic_review"], "not_run")
        self.assertEqual(data["status"], "complete")
        self.assertEqual(len(data["commands"]), 3)
        self.assertEqual(self.apk.read_bytes(), self.original)
        report = (self.output / "report.md").read_text(encoding="utf-8")
        feedback = (self.output / "feedback.md").read_text(encoding="utf-8")
        self.assertIn("未評価", report)
        self.assertIn("動作確認：未確認", report)
        self.assertIn("未評価・教員確認前", feedback)
        self.assertIn("未記入", feedback)

    def replace_dex_output(self, body):
        script = self.analyzer.read_text(encoding="utf-8")
        start = script.index("elif 'dex' in sys.argv:\n")
        end = script.index("else:\n", start)
        self.analyzer.write_text(
            script[:start] + "elif 'dex' in sys.argv:\n" + body + script[end:],
            encoding="utf-8",
        )

    def test_dex_classes_after_output_limit_are_saved_separately(self):
        self.replace_dex_output(
            " sys.stdout.write('C d 1\\t1\\t32\\tdependency.pkg.Class\\n' * 350000)\n"
            " sys.stdout.write('M d 1\\t1\\t32\\t' + 'x' * 140000 + '\\n')\n"
            " print('C d 1\\t1\\t32\\tstudent.changed.MainActivity')\n"
            " print('C d 1\\t1\\t32\\tstudent.changedlib.Lookalike')\n"
            " print('C r 0\\t1\\t32\\tstudent.changed.ReferenceOnly')\n"
            " print('C d 1\\t1\\t32\\tcustom.feature.ExtraClass')\n"
            " print('C d 1\\t1\\t32\\tjp.ac.jec.reference.Fallback', end='')\n"
        )
        result = self.run_review()
        self.assertEqual(result.returncode, 2, result.stderr)
        dex = self.evidence()["commands"]["dex-packages"]
        self.assertEqual(dex["status"], "truncated")
        self.assertEqual(dex["exit_code"], 0)
        self.assertEqual((self.output / dex["stdout"]).stat().st_size, 10 * 1024 * 1024)
        classes = dex["app_classes"]
        self.assertEqual(classes["status"], "ok")
        self.assertEqual(classes["class_count"], 3)
        self.assertEqual(classes["package_prefixes"],
                         ["custom.feature", "jp.ac.jec.reference", "student.changed"])
        rows = (self.output / classes["file"]).read_text(encoding="utf-8").splitlines()
        self.assertEqual([row.split()[-1] for row in rows],
                         ["student.changed.MainActivity", "custom.feature.ExtraClass",
                          "jp.ac.jec.reference.Fallback"])

    def test_no_dex_package_matches_keeps_result_partial(self):
        self.replace_dex_output(" print('C d 1\\t1\\t32\\tdependency.pkg.Class')\n")
        result = self.run_review()
        self.assertEqual(result.returncode, 2, result.stderr)
        dex = self.evidence()["commands"]["dex-packages"]
        self.assertEqual(dex["status"], "ok")
        self.assertEqual(dex["app_classes"]["status"], "not_found")
        self.assertEqual(dex["app_classes"]["class_count"], 0)
        self.assertTrue(self.evidence()["warnings"])

    def test_app_classes_file_is_capped_without_cutting_class_rows(self):
        module = self.load_module()
        self.output.mkdir()
        rows = b"C d 1\t1\t32\tstudent.changed.MainActivity\n"
        with patch.object(module, "MAX_TOOL_BYTES", len(rows) + 1):
            result = module.collect(
                [sys.executable, "-c", f"import sys; sys.stdout.buffer.write({rows * 4!r})"],
                self.output, "dex-packages", 5, dex_packages=("student.changed",),
            )
        self.assertEqual(result["app_classes"]["status"], "truncated")
        self.assertEqual(result["app_classes"]["class_count"], 1)
        self.assertEqual((self.output / result["app_classes"]["file"]).read_bytes(), rows)

    def test_dex_timeout_does_not_report_candidates_as_complete(self):
        self.replace_dex_output(
            " print('C d 1\\t1\\t32\\tstudent.changed.MainActivity', flush=True)\n"
            " time.sleep(10)\n"
        )
        result = self.run_review("--timeout", "0.8")
        self.assertEqual(result.returncode, 2, result.stderr)
        dex = self.evidence()["commands"]["dex-packages"]
        self.assertEqual(dex["status"], "timeout")
        self.assertEqual(dex["app_classes"]["status"], "incomplete")
        self.assertEqual(dex["app_classes"]["class_count"], 1)

    def test_all_four_android_projects_are_accepted(self):
        for name in ("A01HelloAndroid", "A02CalcGame", "A03GithubSearch", "A04FunnyCamera"):
            with self.subTest(project=name):
                output = self.parent / name
                result = self.run_review("--project", name, output=output)
                self.assertEqual(result.returncode, 0, result.stderr)
                data = json.loads((output / "evidence.json").read_text(encoding="utf-8"))
                self.assertEqual(data["baseline"]["project"]["name"], name)

    def test_non_android_or_missing_kind_is_rejected_before_apk_collection(self):
        # 無効なAPKでもkindのエラーが先に出て、出力を作らない。
        self.apk.write_bytes(b"not an apk")
        for name in ("K01HelloKotlin", "UnknownKind", "MissingKind"):
            with self.subTest(project=name):
                result = self.run_review("--project", name)
                self.assertEqual(result.returncode, 1)
                self.assertIn("kind が android", result.stderr)
                self.assertFalse(self.output.exists())

    def test_kind_is_read_from_requested_commit_not_current_worktree(self):
        config = json.loads(self.config.read_text(encoding="utf-8"))
        config["projects"][0]["kind"] = "kotlin-console"
        # 現在の版でandroidに変えても、比較版で対象外なら受理しない。
        config["projects"][4]["kind"] = "android"
        self.config.write_text(json.dumps(config), encoding="utf-8")
        self.git("add", "config/teaching-materials.json")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-m", "現在の版のkindを変更")
        result = self.run_review("--project", "K01HelloKotlin")
        self.assertEqual(result.returncode, 1)
        self.assertIn("kind が android", result.stderr)
        self.assertFalse(self.output.exists())
        self.assertEqual(self.run_review().returncode, 0)
        self.assertEqual(self.evidence()["baseline"]["commit"], self.commit)
        self.assertEqual(self.evidence()["baseline"]["project"]["kind"], "android")

    def test_missing_analyzer_is_partial_not_success(self):
        result = self.run_review(analyzer=self.parent / "missing")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(self.evidence()["status"], "partial")
        self.assertNotIn("manifest", self.evidence())
        self.assertTrue(self.evidence()["warnings"])
        self.assertEqual(self.evidence()["dynamic_review"], "not_run")

    def test_failed_tool_retains_stderr_and_other_evidence(self):
        self.analyzer.write_text(f"#!{sys.executable}\nimport sys\n"
                                 "print('bad dex', file=sys.stderr)\nsys.exit(7)\n")
        result = self.run_review()
        self.assertEqual(result.returncode, 2)
        data = self.evidence()
        self.assertEqual(data["commands"]["dex-packages"]["exit_code"], 7)
        self.assertIn("bad dex", (self.output / "dex-packages.stderr.txt").read_text())
        self.assertEqual(data["apk"]["sha256"], hashlib.sha256(self.original).hexdigest())

    def test_timeout_is_partial(self):
        self.analyzer.write_text(f"#!{sys.executable}\nimport time\ntime.sleep(2)\n")
        result = self.run_review("--timeout", "0.05")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.evidence()["commands"]["manifest"]["status"], "timeout")

    def test_malformed_successful_manifest_is_not_accepted(self):
        self.analyzer.write_text(f"#!{sys.executable}\nprint('not XML')\n")
        result = self.run_review()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.evidence()["commands"]["manifest"]["status"], "invalid_output")

    def test_existing_output_and_input_are_never_overwritten(self):
        self.output.mkdir()
        marker = self.output / "marker.txt"
        marker.write_text("prior review")
        result = self.run_review()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(marker.read_text(), "prior review")
        self.assertEqual(self.apk.read_bytes(), self.original)
        self.assertEqual(self.run_review(output=self.apk).returncode, 1)

    def test_output_inside_repo_or_symlink_to_repo_is_rejected(self):
        self.assertEqual(self.run_review(output=self.root / "results").returncode, 1)
        alias = self.parent / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        self.assertEqual(self.run_review(output=alias / "results").returncode, 1)
        self.assertFalse((self.root / "results").exists())

    def test_output_inside_another_worktree_is_rejected(self):
        other = self.parent / "another-worktree"
        self.git("worktree", "add", "--detach", str(other), "HEAD")
        result = self.run_review(output=other / "results")
        self.assertEqual(result.returncode, 1)
        self.assertFalse((other / "results").exists())

    def test_output_inside_unrelated_git_repository_is_rejected(self):
        other = self.parent / "unrelated-repository"
        other.mkdir()
        subprocess.run(["git", "init", str(other)], check=True, capture_output=True)
        result = self.run_review(output=other / "results")
        self.assertEqual(result.returncode, 1)
        self.assertFalse((other / "results").exists())

    def test_dangling_output_symlink_is_rejected(self):
        target = self.parent / "not-created"
        self.output.symlink_to(target, target_is_directory=True)
        self.assertEqual(self.run_review().returncode, 1)
        self.assertTrue(self.output.is_symlink())
        self.assertFalse(target.exists())

    def test_unknown_baseline_and_project_create_no_output(self):
        result = self.run_review(ref="unknown-version")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.output.exists())
        result = self.run_review("--project", "A99Unknown")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.output.exists())

    def test_head_requires_provisional_and_records_it(self):
        self.assertEqual(self.run_review(ref="HEAD").returncode, 1)
        self.assertFalse(self.output.exists())
        self.assertEqual(self.run_review("--provisional", ref="HEAD").returncode, 0)
        self.assertTrue(self.evidence()["baseline"]["provisional"])

    def test_invalid_apk_creates_no_output(self):
        self.apk.write_bytes(b"not an apk")
        result = self.run_review()
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.output.exists())

    def test_zip_paths_cannot_escape_output(self):
        with ZipFile(self.apk, "a") as archive:
            archive.writestr("../escaped.xml", "not allowed")
        result = self.run_review()
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.output.exists())
        self.assertFalse((self.parent / "escaped.xml").exists())

    def test_missing_manifest_duplicate_entries_and_unknown_resource_are_rejected(self):
        with ZipFile(self.apk, "w") as archive:
            archive.writestr("classes.dex", "fixture dex")
        self.assertEqual(self.run_review().returncode, 1)
        self.assertFalse(self.output.exists())
        self.apk.write_bytes(self.original)
        with ZipFile(self.apk, "a") as archive:
            with self.assertWarns(UserWarning):
                archive.writestr("AndroidManifest.xml", "duplicate")
        self.assertEqual(self.run_review().returncode, 1)
        self.assertFalse(self.output.exists())
        self.apk.write_bytes(self.original)
        self.assertEqual(self.run_review("--resource", "/res/layout/missing.xml").returncode, 1)
        self.assertFalse(self.output.exists())

    def load_module(self):
        spec = importlib.util.spec_from_file_location("student_apk_review", self.script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_apk_and_uncompressed_size_limits_are_enforced(self):
        module = self.load_module()
        with patch.object(module, "MAX_APK_BYTES", len(self.original) - 1):
            with self.assertRaisesRegex(ValueError, "1 GiB"):
                module.apk_inventory(self.apk)
        with patch.object(module, "MAX_UNCOMPRESSED_BYTES", 1):
            with self.assertRaisesRegex(ValueError, "展開サイズ"):
                module.apk_inventory(self.apk)

    def test_large_tool_output_is_bounded_and_marked_unconfirmed(self):
        module = self.load_module()
        self.output.mkdir()
        with patch.object(module, "MAX_TOOL_BYTES", 128):
            result = module.collect(
                [sys.executable, "-c", "import sys; print('x' * 256); print('y' * 256, file=sys.stderr)"],
                self.output, "large-output", 5,
            )
        self.assertEqual(result["status"], "truncated")
        self.assertEqual(result["limit_bytes"], 128)
        self.assertEqual((self.output / result["stdout"]).stat().st_size, 128)
        self.assertEqual((self.output / result["stderr"]).stat().st_size, 128)

    def test_invalid_timeout_is_cli_error_without_evidence(self):
        for timeout in ("0", "-1", "301", "nan", "inf", "invalid"):
            with self.subTest(timeout=timeout):
                result = self.run_review("--timeout", timeout)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(self.output.exists())

    def test_sdk_analyzer_uses_numeric_version_order(self):
        module = self.load_module()
        sdk = self.parent / "sdk"
        for version in ("9.0", "21.0"):
            executable = sdk / "cmdline-tools" / version / "bin/apkanalyzer"
            executable.parent.mkdir(parents=True)
            executable.write_text("fake executable")
            executable.chmod(0o755)
        with patch.object(module.shutil, "which", return_value=None), patch.dict(
                os.environ, {"ANDROID_HOME": str(sdk)}):
            self.assertEqual(module.find_analyzer(None),
                             str(sdk / "cmdline-tools/21.0/bin/apkanalyzer"))


if __name__ == "__main__":
    unittest.main()
