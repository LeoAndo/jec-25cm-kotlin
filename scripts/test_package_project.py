"""完成版ZIPの生成条件と、配布対象の選別を検証する。"""

from pathlib import Path
import os
from shutil import copy2, which
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile


SCRIPT = Path(__file__).with_name("package-project.py")
GIT = which("git")


@unittest.skipUnless(GIT, "テスト用リポジトリの作成にはGitが必要です。")
class PackageProjectTest(unittest.TestCase):
    """実際のGitと一時フォルダで、配布用スクリプトを実行する。"""

    def setUp(self):
        """各テスト専用のソースと既存ZIPを用意する。"""
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.parent = Path(temporary.name)
        self.root = self.parent / "source"
        (self.root / "scripts").mkdir(parents=True)
        copy2(SCRIPT, self.root / "scripts" / SCRIPT.name)
        self.output = self.root / "docs/hello-kotlin/downloads/K01HelloKotlin.zip"
        self.output.parent.mkdir(parents=True)
        self.output.write_bytes(b"previous archive")

    def git(self, *args, cwd=None):
        """指定フォルダでGitを実行し、失敗はテストエラーにする。"""
        return subprocess.run(
            [GIT, *args], cwd=cwd or self.root, check=True,
            capture_output=True, text=True,
        )

    def run_package(self, *args, env=None):
        """独立したPythonプロセスで配布スクリプトを実行する。"""
        if not args:
            args = ("--project", "K01HelloKotlin", "--output", str(self.output))
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / SCRIPT.name), *args],
            cwd=self.root, env=env, capture_output=True, text=True,
        )

    def assert_rejected(self, result, message):
        """日本語の案内を返し、既存ZIPを保持することを確認する。"""
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.output.read_bytes(), b"previous archive")

    def test_no_git_metadata(self):
        """GitHubのDownload ZIPに相当するフォルダを拒否する。"""
        self.assert_rejected(self.run_package(), "git clone")

    def test_source_inside_another_repository(self):
        """上位フォルダのGit管理情報を誤って使用しない。"""
        self.git("init", cwd=self.parent)
        self.assert_rejected(self.run_package(), "ルートではありません")

    def test_git_not_installed(self):
        """Gitが見つからない場合にインストールを案内する。"""
        env = dict(os.environ, PATH="")
        self.assert_rejected(self.run_package(env=env), "Gitが見つかりません")

    def test_no_tracked_project_files(self):
        """配布対象がない場合に既存ZIPを維持する。"""
        self.git("init")
        self.assert_rejected(self.run_package(), "プロジェクトが見つかりません")

    def test_project_and_output_are_required(self):
        """既定の単元を持たない。引数なしでは何も作り直さない。

        単元が増えたときに、既定の単元だけを静かに作り直す事故を防ぐための確認。
        """
        self.git("init")
        result = self.run_package("--project", "K01HelloKotlin")
        self.assert_rejected(result, "--output")
        self.assert_rejected(self.run_package("--output", str(self.output)), "--project")

    def test_tracked_sources_only_and_repeatable_archive(self):
        """編集済みの管理対象と実行権限を保持し、ローカル状態を除外する。"""
        self.git("init")
        project = self.root / "K01HelloKotlin"
        for name in [
            "src/ex01/main.kt", "run.sh", "local.properties",
            ".idea/misc.xml", ".gradle/cache", ".kotlin/cache", "build/classes",
            "out/production/K01HelloKotlin/ex01/MainKt.class",
        ]:
            path = project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("original")
        (project / "run.sh").chmod(0o744)
        (project / "src/ex01/main.kt").chmod(0o600)
        self.git("add", "K01HelloKotlin")
        (project / "src/ex01/main.kt").write_text("edited")
        (project / "untracked.txt").write_text("not for distribution")
        result = self.run_package()
        self.assertEqual(result.returncode, 0, result.stderr)
        with ZipFile(self.output) as archive:
            self.assertEqual(archive.namelist(), [
                "K01HelloKotlin/run.sh",
                "K01HelloKotlin/src/ex01/main.kt",
            ])
            self.assertEqual(archive.read("K01HelloKotlin/src/ex01/main.kt"), b"edited")
            mode = archive.getinfo("K01HelloKotlin/run.sh").external_attr >> 16
            self.assertEqual(mode, 0o100755)
            source_mode = archive.getinfo("K01HelloKotlin/src/ex01/main.kt").external_attr >> 16
            self.assertEqual(source_mode, 0o100644)
        first = self.output.read_bytes()
        self.assertEqual(self.run_package().returncode, 0)
        self.assertEqual(self.output.read_bytes(), first)

    def test_intellij_output_folder_is_excluded(self):
        """IntelliJ IDEAの out フォルダが誤ってcommitされていても配らない。

        純Kotlin系はGradleを使わないので、ビルド出力は build ではなく out に出る。
        """
        self.git("init")
        project = self.root / "K01HelloKotlin"
        for name in ["src/ex01/main.kt", "out/production/K01HelloKotlin/ex01/MainKt.class"]:
            path = project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("original")
        self.git("add", "-f", "K01HelloKotlin")
        self.assertEqual(self.run_package().returncode, 0)
        with ZipFile(self.output) as archive:
            self.assertEqual(archive.namelist(), ["K01HelloKotlin/src/ex01/main.kt"])


if __name__ == "__main__":
    unittest.main()
