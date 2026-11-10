"""教材整合性検査の回帰テスト。

このリポジトリの単元は2系統ある。純Kotlin系（kind: kotlin-console。IntelliJ IDEAの
コンソールアプリ）と、Android系（kind: android）である。どちらも検査できることを確かめる。

ここで確かめるのは検査そのものの動きで、tempfile で仮のリポジトリを組み立てて試す。
このリポジトリ自身が整合しているかは `python3 scripts/check-teaching-materials.py` が見る
（CIの validate ジョブとREADMEの検証コマンドに入っている）ので、ここでは重ねて見ない。
"""

import contextlib
import html
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


SCRIPT = Path(__file__).with_name("check-teaching-materials.py")
SPEC = importlib.util.spec_from_file_location("check_teaching_materials", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class TeachingMaterialsCheckTest(unittest.TestCase):
    AVD = "jec_25cm_kotlin_Pixel 9a"
    KOTLIN_SOURCE = 'package ex01\n\nfun main() {\n    println("こんにちは")\n}\n'
    ANDROID_SOURCE = (
        "package jp.ac.jec.a01helloandroid\n\n"
        "class MainActivity : AppCompatActivity() {\n}\n"
    )
    GRADLE = (
        "android {\n"
        '    namespace = "jp.ac.jec.a01helloandroid"\n'
        "    defaultConfig {\n"
        '        applicationId = "jp.ac.jec.a01helloandroid"\n'
        "    }\n"
        "}\n"
    )
    LAYOUT = '<?xml version="1.0" encoding="utf-8"?>\n<FrameLayout />\n'
    # 純Kotlin系はIntelliJ IDEA、Android系はGradleなので、無視するものが違う。
    KOTLIN_IGNORE = "out/\n.idea/\n.kotlin\n"
    ANDROID_IGNORE = "build/\n.gradle/\n.idea/\nlocal.properties\n"

    # ------------------------------------------------------------------
    # 仮のリポジトリを組み立てる道具
    # ------------------------------------------------------------------

    def _write(self, root: Path, name: str, text: str) -> Path:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def _write_config(self, root: Path, config: dict) -> None:
        """検査に必要な設定ファイルを書き出す。"""
        (root / "config").mkdir(exist_ok=True)
        (root / "config/teaching-materials.json").write_text(
            json.dumps(config, ensure_ascii=False), encoding="utf-8"
        )

    def _minimal_config(self, root: Path, projects: list[dict], **extra) -> None:
        """見たい検査だけが動く、最小の設定を書き出す。

        course も registration も project_layout も書かないので、それらの検査は動かない。
        """
        config = {"scan_roots": [], "terms": [], "projects": projects}
        config.update(extra)
        self._write_config(root, config)

    def _project(self, **overrides) -> dict:
        """単元の設定。既定は第1単元（純Kotlin系）の形。

        純Kotlin系は packages（配列）、Android系は package（文字列）を持つ。
        package を渡した呼び出しはAndroid系の単元なので、既定の packages は落とす。
        """
        project = {
            "name": "K01HelloKotlin",
            "kind": "kotlin-console",
            "root": "K01HelloKotlin",
            "packages": ["ex01"],
            "sessions": 1,
            "docs": ["docs/hello-kotlin/index.html", "teacher/hello-kotlin/index.html"],
            "sources": ["K01HelloKotlin/src/ex01/main.kt"],
            "snippets": [],
            "archive": "docs/hello-kotlin/downloads/K01HelloKotlin.zip",
        }
        project.update(overrides)
        if "package" in overrides:
            project.pop("packages", None)
        return project

    def _git_add(self, root: Path, *paths: str) -> None:
        """完成プロジェクトZIPの検査は git ls-files を使うので、Gitの索引を作る。"""
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "add", *paths], cwd=root, check=True, capture_output=True)

    def _archive(self, root: Path, name: str, members: list[str]) -> Path:
        """完成プロジェクトZIPを、scripts/package-project.py と同じ形で作る。"""
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
            for member in members:
                source = root / member
                info = ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                executable = bool(source.stat().st_mode & 0o100)
                info.external_attr = (0o100755 if executable else 0o100644) << 16
                info.compress_type = ZIP_DEFLATED
                archive.writestr(info, source.read_bytes())
        return path

    def _textbook(self, name: str, units: list[tuple[str, str]], current: str,
                  snippet: tuple[str, str] | None = None) -> str:
        """教科書HTMLのうち、検査に関わる部分だけを持つページを作る。

        units は (フォルダ名, 単元名) の一覧。current はいま開いている単元のフォルダ名。
        """
        entries = []
        for folder, unit_name in units:
            shown = f"{unit_name[:3]}：{unit_name[3:]}"
            if folder == current:
                entries.append(f'<span aria-current="page">{shown}</span>')
            else:
                entries.append(f'<a href="../{folder}/index.html">{shown}</a>')
        code = ""
        if snippet:
            snippet_id, source = snippet
            code = f'<pre id="{snippet_id}"><code>{html.escape(source)}</code></pre>'
        return (
            '<!doctype html><html lang="ja"><body>'
            f"<main><h1>{name}</h1><p>エミュレータは {self.AVD} を使います。</p>{code}</main>"
            '<aside class="sidebar"><div class="resources"><a href="#help">困ったとき</a>'
            + "".join(entries)
            + f'<a href="../common/setup.html?from={current}">共通：はじめの準備</a>'
            "</div></aside></body></html>"
        )

    def _teacher_doc(self, name: str) -> str:
        return (
            '<!doctype html><html lang="ja"><body><main>'
            f"<h1>{name} 教員用ガイド</h1>"
            f"<p>エミュレータは {self.AVD} を使います。</p>"
            "</main></body></html>"
        )

    def _readme(self, *paths: str) -> str:
        """コマ数の表記と、単元へのリンクを持つREADMEを作る。"""
        body = "".join(f"- {path}\n" for path in paths)
        return (
            "# Kotlin演習 — 授業用教材\n\n"
            "全15コマ・1コマ90分（計画は仮）。\n\n" + body
        )

    def _kotlin_console_repository(self, root: Path) -> dict:
        """純Kotlin系の、検査を通る最小のリポジトリを作る。"""
        self._write(root, "K01HelloKotlin/.gitignore", self.KOTLIN_IGNORE)
        self._write(root, "K01HelloKotlin/src/ex01/main.kt", self.KOTLIN_SOURCE)
        self._git_add(root, "K01HelloKotlin")
        self._write(root, "docs/hello-kotlin/index.html", self._textbook(
            "K01HelloKotlin", [("hello-kotlin", "K01HelloKotlin")], "hello-kotlin",
            snippet=("code-final-kotlin", self.KOTLIN_SOURCE)))
        self._write(root, "teacher/hello-kotlin/index.html", self._teacher_doc("K01HelloKotlin"))
        self._archive(root, "docs/hello-kotlin/downloads/K01HelloKotlin.zip",
                      ["K01HelloKotlin/.gitignore", "K01HelloKotlin/src/ex01/main.kt"])
        self._write(root, "README.md", self._readme(
            "docs/hello-kotlin/index.html",
            "teacher/hello-kotlin/index.html",
            "docs/hello-kotlin/downloads/K01HelloKotlin.zip"))
        config = {
            "course": {"name": "Kotlin演習", "total_sessions": 15, "minutes_per_session": 90},
            "scan_roots": ["README.md", "docs", "teacher", "K01HelloKotlin"],
            "terms": [{
                "name": "指定AVD名",
                "canonical": self.AVD,
                "forbidden": ["jec_25cm_kotlin_Pixel_9a"],
                "required_in": [
                    "docs/hello-kotlin/index.html",
                    "teacher/hello-kotlin/index.html",
                ],
            }],
            "registration": {"targets": [
                {"path": "README.md", "requires": ["student_doc", "teacher_doc", "archive"]},
            ]},
            "project_layout": {
                "gitignore_reference": {"kotlin-console": "K01HelloKotlin/.gitignore"},
                "untracked_parts": [".idea", ".gradle", ".kotlin", "build", "out"],
                "untracked_names": ["local.properties"],
            },
            "projects": [self._project(snippets=[{
                "html": "docs/hello-kotlin/index.html",
                "id": "code-final-kotlin",
                "source": "K01HelloKotlin/src/ex01/main.kt",
            }])],
        }
        self._write_config(root, config)
        return config

    def _android_repository(self, root: Path, gradle: str | None = None) -> dict:
        """Android系の、検査を通る最小のリポジトリを作る。"""
        sources = "A01HelloAndroid/app/src/main/java/jp/ac/jec/a01helloandroid/MainActivity.kt"
        layout = "A01HelloAndroid/app/src/main/res/layout/activity_main.xml"
        self._write(root, "A01HelloAndroid/.gitignore", self.ANDROID_IGNORE)
        self._write(root, "A01HelloAndroid/app/build.gradle.kts", gradle or self.GRADLE)
        self._write(root, sources, self.ANDROID_SOURCE)
        self._write(root, layout, self.LAYOUT)
        self._git_add(root, "A01HelloAndroid")
        self._write(root, "docs/hello-android/index.html", self._textbook(
            "A01HelloAndroid（jp.ac.jec.a01helloandroid）",
            [("hello-android", "A01HelloAndroid")], "hello-android"))
        self._write(root, "teacher/hello-android/index.html", self._teacher_doc(
            "A01HelloAndroid（jp.ac.jec.a01helloandroid）"))
        self._archive(root, "docs/hello-android/downloads/A01HelloAndroid.zip", [
            "A01HelloAndroid/.gitignore",
            "A01HelloAndroid/app/build.gradle.kts",
            sources,
            layout,
        ])
        self._write(root, "README.md", self._readme(
            "docs/hello-android/index.html",
            "teacher/hello-android/index.html",
            "docs/hello-android/downloads/A01HelloAndroid.zip"))
        config = {
            "course": {"name": "Kotlin演習", "total_sessions": 15, "minutes_per_session": 90},
            "scan_roots": ["README.md", "docs", "teacher", "A01HelloAndroid"],
            "terms": [{
                "name": "指定AVD名",
                "canonical": self.AVD,
                "forbidden": ["jec_25cm_kotlin_Pixel_9a"],
                "required_in": [
                    "docs/hello-android/index.html",
                    "teacher/hello-android/index.html",
                ],
            }],
            "registration": {"targets": [
                {"path": "README.md", "requires": ["student_doc", "teacher_doc", "archive"]},
            ]},
            "project_layout": {
                "gitignore_reference": {"android": "A01HelloAndroid/.gitignore"},
                "untracked_parts": [".idea", ".gradle", ".kotlin", "build", "out"],
                "untracked_names": ["local.properties"],
            },
            "projects": [self._project(
                name="A01HelloAndroid",
                kind="android",
                root="A01HelloAndroid",
                package="jp.ac.jec.a01helloandroid",
                sessions=2,
                docs=["docs/hello-android/index.html", "teacher/hello-android/index.html"],
                sources=[sources],
                layout=layout,
                archive="docs/hello-android/downloads/A01HelloAndroid.zip",
            )],
        }
        self._write_config(root, config)
        return config

    # ------------------------------------------------------------------
    # 純Kotlin系（kind: kotlin-console）
    # ------------------------------------------------------------------

    def test_kotlin_console_project_is_accepted(self):
        """純Kotlin系の単元が、ひと通りそろっていれば何も言わない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._kotlin_console_repository(root)
            self.assertEqual(CHECKER.validate(root), [])

    def test_kotlin_console_source_with_wrong_package_is_rejected(self):
        """完成コードのpackage宣言が、packagesのどれとも違えば検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt", "package ex02\n\nfun main() {}\n")
            self._minimal_config(root, [self._project()])
            errors = [error for error in CHECKER.validate(root) if "package宣言" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("K01HelloKotlin/src/ex01/main.kt:1", errors[0])
            self.assertIn("K01HelloKotlinのpackagesにありません: 'ex02'（packagesはex01）", errors[0])

    def test_kotlin_console_source_without_package_is_rejected(self):
        """package宣言そのものが無い場合も検出する。IntelliJ IDEAで実行できなくなる。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt", "fun main() {}\n")
            self._minimal_config(root, [self._project()])
            errors = [error for error in CHECKER.validate(root) if "package宣言" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("K01HelloKotlin/src/ex01/main.kt:1", errors[0])
            self.assertIn("Kotlinのpackage宣言がありません", errors[0])
            self.assertIn("K01HelloKotlinのpackages（ex01）", errors[0])

    def test_kotlin_console_source_outside_package_folder_is_rejected(self):
        """完成コードが src/<パッケージ>/ の直下になければ検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/main.kt", self.KOTLIN_SOURCE)
            self._minimal_config(root, [self._project(sources=["K01HelloKotlin/src/main.kt"])])
            errors = [error for error in CHECKER.validate(root) if "置き場所" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("K01HelloKotlin/src/main.kt:1", errors[0])
            self.assertIn("完成コードの置き場所がK01HelloKotlin/src/ex01/ではありません", errors[0])

    def test_kotlin_console_source_in_subfolder_of_package_is_rejected(self):
        """src/<パッケージ>/ の下にフォルダを作って置いた状態も検出する。

        Gradleを使わないIntelliJ IDEAのプロジェクトなので、宣言したパッケージの
        フォルダの直下にないと、学生が実行ボタンを押したときに動かない。
        """
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/sub/main.kt", self.KOTLIN_SOURCE)
            self._minimal_config(root, [self._project(
                sources=["K01HelloKotlin/src/ex01/sub/main.kt"])])
            errors = [error for error in CHECKER.validate(root) if "置き場所" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("完成コードの置き場所がK01HelloKotlin/src/ex01/ではありません", errors[0])

    def test_kotlin_console_document_does_not_require_package(self):
        """ex01 のような短い語は本文に偶然現れるので、純Kotlin系では表記を求めない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._kotlin_console_repository(root)
            document = root / "teacher/hello-kotlin/index.html"
            self.assertNotIn("ex01", document.read_text(encoding="utf-8"))
            self.assertEqual(CHECKER.validate(root), [])

    def test_empty_sources_is_rejected(self):
        """完成コードを1つも登録していない単元は、何も検査できないので検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._minimal_config(root, [self._project(sources=[])])
            errors = [error for error in CHECKER.validate(root) if "sources" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])

    # ------------------------------------------------------------------
    # 純Kotlin系の packages（配列）
    #
    # 1コマで複数の演習（exNN）を扱う単元があるので、純Kotlin系のパッケージは
    # 配列で書く。Android系は、アプリのパッケージが1つなので文字列のまま。
    # ------------------------------------------------------------------

    def _packages_errors(self, root: Path, project: dict) -> list[str]:
        """packages と、その置き場所についてのエラーだけを返す。"""
        self._minimal_config(root, [project])
        return [error for error in CHECKER.validate(root)
                if "package" in error or "置き場所" in error]

    def test_kotlin_console_with_two_packages_is_accepted(self):
        """1つの単元で2つの演習を扱う形。どちらの完成コードもそろっていれば何も言わない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt", self.KOTLIN_SOURCE)
            self._write(root, "K01HelloKotlin/src/ex02/main.kt",
                        self.KOTLIN_SOURCE.replace("package ex01", "package ex02"))
            errors = self._packages_errors(root, self._project(
                name="K03FunctionAndFlow",
                packages=["ex01", "ex02"],
                sources=["K01HelloKotlin/src/ex01/main.kt", "K01HelloKotlin/src/ex02/main.kt"]))
            self.assertEqual(errors, [])

    def test_kotlin_console_package_without_source_is_rejected(self):
        """packages に書いたのに、その演習の完成コードを足し忘れた状態を検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt", self.KOTLIN_SOURCE)
            errors = self._packages_errors(root, self._project(
                name="K03FunctionAndFlow",
                packages=["ex01", "ex02"],
                sources=["K01HelloKotlin/src/ex01/main.kt"]))
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])
            self.assertIn("K03FunctionAndFlowのpackagesに書いたex02の完成コードが、"
                          "sourcesにありません", errors[0])

    def test_kotlin_console_source_outside_packages_is_rejected(self):
        """packages に無いパッケージを宣言した完成コードを検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt", self.KOTLIN_SOURCE)
            self._write(root, "K01HelloKotlin/src/ex03/main.kt",
                        self.KOTLIN_SOURCE.replace("package ex01", "package ex03"))
            errors = self._packages_errors(root, self._project(
                name="K03FunctionAndFlow",
                packages=["ex01", "ex02"],
                sources=["K01HelloKotlin/src/ex01/main.kt", "K01HelloKotlin/src/ex03/main.kt"]))
            self.assertEqual(len(errors), 2, errors)
            self.assertIn("K01HelloKotlin/src/ex03/main.kt:1", errors[0])
            self.assertIn("K03FunctionAndFlowのpackagesにありません: 'ex03'"
                          "（packagesはex01、ex02）", errors[0])
            # ex02 は、これで完成コードが1つも無いことになる。
            self.assertIn("packagesに書いたex02の完成コードが、sourcesにありません", errors[1])

    def test_kotlin_console_empty_packages_is_rejected(self):
        """packages が空配列なら、何も検査できないので設定エラーにする。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = self._packages_errors(root, self._project(packages=[]))
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])
            self.assertIn("K01HelloKotlinのpackagesは、パッケージ名を1つ以上並べた"
                          "配列で書いてください: []", errors[0])

    def test_kotlin_console_packages_as_string_is_rejected(self):
        """packages を文字列で書いたら設定エラーにする。1件でも配列で書く。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = self._packages_errors(root, self._project(packages="ex01"))
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("パッケージ名を1つ以上並べた配列で書いてください: 'ex01'", errors[0])

    def test_kotlin_console_packages_with_non_string_element_is_rejected(self):
        """packages の要素が文字列でなければ設定エラーにする。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = self._packages_errors(root, self._project(packages=["ex01", 2]))
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("K01HelloKotlinのpackagesには、パッケージ名を文字列で"
                          "書いてください: [2]", errors[0])

    def test_kotlin_console_with_package_is_rejected(self):
        """純Kotlin系に package（単数）を書いたら設定エラーにする。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt", self.KOTLIN_SOURCE)
            project = self._project(package="ex01")
            self.assertNotIn("packages", project)
            errors = self._packages_errors(root, project)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])
            self.assertIn("K01HelloKotlinはkotlin-consoleなので、packageではなく"
                          "packagesに配列で書いてください", errors[0])

    def test_android_with_packages_is_rejected(self):
        """Android系に packages（複数）を書いたら設定エラーにする。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._android_repository(root)
            config = json.loads(
                (root / "config/teaching-materials.json").read_text(encoding="utf-8"))
            project = config["projects"][0]
            project.pop("package")
            project["packages"] = ["jp.ac.jec.a01helloandroid"]
            self._write_config(root, config)
            errors = [error for error in CHECKER.validate(root) if "packages" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])
            self.assertIn("A01HelloAndroidはandroidなので、packagesではなく"
                          "packageに文字列で書いてください", errors[0])

    # ------------------------------------------------------------------
    # Android系（kind: android）
    # ------------------------------------------------------------------

    def test_android_project_is_accepted(self):
        """Android系の単元が、ひと通りそろっていれば何も言わない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._android_repository(root)
            self.assertEqual(CHECKER.validate(root), [])

    def test_android_package_mismatch_is_rejected(self):
        """namespace と applicationId が設定のpackageと違えば検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._android_repository(root, gradle=self.GRADLE.replace(
                "jp.ac.jec.a01helloandroid", "jp.ac.jec.hello"))
            errors = CHECKER.validate(root)
            self.assertEqual(len(errors), 2, errors)
            self.assertIn("A01HelloAndroid/app/build.gradle.kts:2", errors[0])
            self.assertIn("namespaceが一致しません", errors[0])
            self.assertIn("applicationIdが一致しません", errors[1])

    def test_android_missing_layout_is_rejected(self):
        """layout に書いたXMLが無ければ検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = self._android_repository(root)
            config["projects"][0]["layout"] = "A01HelloAndroid/app/src/main/res/layout/activity_sub.xml"
            self._write_config(root, config)
            errors = [error for error in CHECKER.validate(root) if "レイアウトXML" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("activity_sub.xml:1", errors[0])

    def test_android_document_requires_package(self):
        """Android系の教材には、単元名とpackageの両方の表記を求める。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._android_repository(root)
            self._write(root, "teacher/hello-android/index.html",
                        self._teacher_doc("A01HelloAndroid"))
            errors = [error for error in CHECKER.validate(root) if "必要な表記" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("教材に必要な表記がありません: jp.ac.jec.a01helloandroid", errors[0])

    def test_unknown_kind_is_rejected(self):
        """kind は android か kotlin-console のどちらかだけ。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._minimal_config(root, [self._project(kind="gradle")])
            errors = [error for error in CHECKER.validate(root) if "kind" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])
            self.assertIn("K01HelloKotlinのkindが不正です: 'gradle'", errors[0])

    # ------------------------------------------------------------------
    # コマ数（check_course）
    # ------------------------------------------------------------------

    def _course_errors(self, root: Path) -> list[str]:
        return [error for error in CHECKER.validate(root) if "コマ" in error or "sessions" in error]

    def _course_root(self, root: Path, sessions: list[int], readme: str,
                     total=15, minutes=90) -> None:
        self._write(root, "README.md", readme)
        projects = [
            self._project(
                name=f"K0{index}Unit",
                packages=[f"ex0{index}"],
                sessions=value,
                sources=[f"K01HelloKotlin/src/ex0{index}/main.kt"],
                docs=[f"docs/u{index}/index.html", f"teacher/u{index}/index.html"],
                archive=f"docs/u{index}/downloads/K01HelloKotlin.zip",
            )
            for index, value in enumerate(sessions, 1)
        ]
        self._minimal_config(root, projects, course={
            "name": "Kotlin演習", "total_sessions": total, "minutes_per_session": minutes,
        })

    def test_sessions_within_total_are_accepted(self):
        """合計が全コマ数に足りないのは、まだ単元にしていないだけなので許す。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._course_root(root, [1, 2], self._readme())
            self.assertEqual(self._course_errors(root), [])

    def test_sessions_over_total_are_rejected(self):
        """単元のコマ数の合計が、決めた全コマ数を超えたら検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._course_root(root, [10, 6], self._readme())
            errors = self._course_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])
            self.assertIn("course.total_sessionsの15コマを超えています: 16コマ", errors[0])

    def test_sessions_must_be_positive_integer(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._course_root(root, [0], self._readme())
            errors = self._course_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("K01Unitのsessionsは正の整数で書いてください: 0", errors[0])

    def test_total_sessions_must_be_positive_integer(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._course_root(root, [1], self._readme(), total=0)
            errors = self._course_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("course.total_sessionsは正の整数で書いてください: 0", errors[0])

    def test_readme_without_session_notation_is_rejected(self):
        """設定だけ直して、READMEの「全15コマ」「1コマ90分」を書き換え忘れた状態を検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._course_root(root, [1], "# Kotlin演習\n\n授業の分量はここに書く。\n")
            errors = self._course_errors(root)
            self.assertEqual(len(errors), 2, errors)
            self.assertIn("README.md:1", errors[0])
            self.assertIn("授業の分量の表記がありません: 全15コマ", errors[0])
            self.assertIn("授業の分量の表記がありません: 1コマ90分", errors[1])

    def test_readme_notation_follows_the_configured_numbers(self):
        """コマ数を変えたら、READMEに求める表記もそれに合わせて変わる。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._course_root(root, [1], self._readme(), total=30, minutes=45)
            errors = self._course_errors(root)
            self.assertEqual(len(errors), 2, errors)
            self.assertIn("全30コマ", errors[0])
            self.assertIn("1コマ45分", errors[1])

    # ------------------------------------------------------------------
    # 登録（check_registration）と表記揺れ（check_terms）
    # ------------------------------------------------------------------

    def _registration_root(self, root: Path, readme: str, requires: list[str]) -> None:
        self._write(root, "README.md", readme)
        self._minimal_config(
            root,
            [self._project()],
            scan_roots=["README.md", "K01HelloKotlin"],
            terms=[{"name": "t", "canonical": "Kotlin演習", "forbidden": [], "required_in": [
                "docs/hello-kotlin/index.html", "teacher/hello-kotlin/index.html"]}],
            registration={"targets": [{"path": "README.md", "requires": requires}]},
        )

    def test_missing_registration_is_reported(self):
        """READMEから単元のリンクが1つでも抜けたら検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/.gitignore", self.KOTLIN_IGNORE)
            # 完成プロジェクトZIPへのリンクだけ書いていない。
            self._registration_root(root, self._readme(
                "docs/hello-kotlin/index.html", "teacher/hello-kotlin/index.html"),
                ["student_doc", "teacher_doc", "archive"])
            errors = [error for error in CHECKER.validate(root) if "への参照がありません" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("README.md:1", errors[0])
            self.assertIn("docs/hello-kotlin/downloads/K01HelloKotlin.zip", errors[0])

    def test_guidance_line_is_no_longer_required(self):
        """配布スクリプトは単元一覧をconfigから読むので、案内文の1行は求めない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/.gitignore", self.KOTLIN_IGNORE)
            readme = self._readme(
                "docs/hello-kotlin/index.html",
                "teacher/hello-kotlin/index.html",
                "docs/hello-kotlin/downloads/K01HelloKotlin.zip")
            self.assertNotIn("K01 HelloKotlin：", readme)
            self._registration_root(root, readme, ["student_doc", "teacher_doc", "archive"])
            errors = [error for error in CHECKER.validate(root) if "への参照がありません" in error]
            self.assertEqual(errors, [])

    def test_unknown_requires_is_reported(self):
        """requires に、もう無い項目（guidance_line など）を書いたら検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._registration_root(root, self._readme(), ["guidance_line"])
            errors = [error for error in CHECKER.validate(root) if "知らない項目" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])
            self.assertIn("guidance_line", errors[0])

    def test_forbidden_spelling_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "README.md", "jec_25cm_kotlin_Pixel_9a\n")
            self._write_config(root, {
                "scan_roots": ["README.md"],
                "terms": [{
                    "name": "指定AVD名",
                    "canonical": self.AVD,
                    "forbidden": ["jec_25cm_kotlin_Pixel_9a"],
                    "required_in": [],
                }],
                "projects": [],
            })
            errors = CHECKER.validate(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("README.md:1", errors[0])
            self.assertIn("禁止表記", errors[0])

    def test_kotlin_source_is_scanned_for_spelling(self):
        """表記揺れの検査は .kt も見る。純Kotlin系の完成コードは scan_roots の中にある。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt",
                        '// jec_25cm_kotlin_Pixel_9a で動かす\nfun main() {}\n')
            self._write_config(root, {
                "scan_roots": ["K01HelloKotlin"],
                "terms": [{
                    "name": "指定AVD名",
                    "canonical": self.AVD,
                    "forbidden": ["jec_25cm_kotlin_Pixel_9a"],
                    "required_in": [],
                }],
                "projects": [],
            })
            errors = CHECKER.validate(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("K01HelloKotlin/src/ex01/main.kt:1", errors[0])

    def test_missing_scan_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(root, {"scan_roots": ["missing"], "terms": [], "projects": []})

            errors = CHECKER.validate(root)

            self.assertEqual(len(errors), 1, errors)
            self.assertIn("missing:1", errors[0])
            self.assertIn("検査対象のパスがありません", errors[0])

    # ------------------------------------------------------------------
    # 完成プロジェクトZIP
    # ------------------------------------------------------------------

    def test_archive_executable_bit_is_rejected(self):
        """gradlew の実行権限がZIPで落ちていたら検出する。学生が ./gradlew を実行できない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._android_repository(root)
            gradlew = self._write(root, "A01HelloAndroid/gradlew", "#!/bin/sh\n")
            self._git_add(root, "A01HelloAndroid")
            self._archive(root, "docs/hello-android/downloads/A01HelloAndroid.zip", [
                "A01HelloAndroid/.gitignore",
                "A01HelloAndroid/app/build.gradle.kts",
                "A01HelloAndroid/app/src/main/java/jp/ac/jec/a01helloandroid/MainActivity.kt",
                "A01HelloAndroid/app/src/main/res/layout/activity_main.xml",
                "A01HelloAndroid/gradlew",
            ])
            # ZIPを作ったあとで実行権限を付けた。中身は同じでも、権限だけがずれる。
            gradlew.chmod(0o755)
            errors = CHECKER.validate(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("実行権限が一致しません: A01HelloAndroid/gradlew", errors[0])

    def test_archive_contents_must_match_the_sources(self):
        """ZIPを作り直さずに完成コードを直した状態を検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._kotlin_console_repository(root)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt",
                        self.KOTLIN_SOURCE.replace("こんにちは", "おはよう"))
            errors = [error for error in CHECKER.validate(root) if "ZIP" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("内容が一致しません: K01HelloKotlin/src/ex01/main.kt", errors[0])

    def test_snippet_must_match_the_source(self):
        """教科書に貼った完成コードが、実際のファイルと1バイトでも違えば検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._kotlin_console_repository(root)
            self._write(root, "docs/hello-kotlin/index.html", self._textbook(
                "K01HelloKotlin", [("hello-kotlin", "K01HelloKotlin")], "hello-kotlin",
                snippet=("code-final-kotlin", self.KOTLIN_SOURCE.replace("こんにちは", "おはよう"))))
            errors = [error for error in CHECKER.validate(root) if "code-final-kotlin" in error]
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("K01HelloKotlin/src/ex01/main.ktが一致しません", errors[0])

    # ------------------------------------------------------------------
    # 教材のフォルダから学生がコピーするファイル（check_downloads）
    # ------------------------------------------------------------------

    PNG = b"\x89PNG\r\n\x1a\n" + bytes(range(64))
    # 置き場所とファイル名を、同じSTEP（<section>）に書いた教科書。
    GUIDE = ('<section id="step-2"><ol><li>教材のフォルダの <code>docs → x → downloads</code> を開きます。</li>'
             "<li><code>title.png</code> をコピーします。</li></ol></section>")

    def _download_root(self, root: Path, download: bytes, textbook: str,
                       download_name: str = "title.png") -> None:
        """配布ファイルの検査に必要な最小限のリポジトリを作る。"""
        source = root / "Sample/app/src/main/res/drawable/title.png"
        source.parent.mkdir(parents=True)
        source.write_bytes(self.PNG)
        (root / "docs/x/downloads").mkdir(parents=True)
        (root / "docs/x/downloads" / download_name).write_bytes(download)
        (root / "docs/x/index.html").write_text(textbook, encoding="utf-8")
        self._git_add(root, "Sample")
        self._minimal_config(root, [self._project(
            name="Sample", kind="android", root="Sample", package="jp.example.sample",
            docs=["docs/x/index.html", "teacher/x/index.html"],
            sources=["Sample/app/src/main/java/MainActivity.kt"],
            archive="docs/x/downloads/Sample.zip",
            downloads=[{
                "download": f"docs/x/downloads/{download_name}",
                "source": "Sample/app/src/main/res/drawable/title.png",
            }],
        )])

    def _download_errors(self, root: Path) -> list[str]:
        return [error for error in CHECKER.validate(root) if "配布ファイル" in error]

    def test_download_identical_to_source_is_accepted(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._download_root(root, self.PNG, self.GUIDE)
            self.assertEqual(self._download_errors(root), [])

    def test_download_folder_written_as_separate_codes_is_accepted(self):
        """置き場所は、フォルダ名を1つずつ <code> で囲んでも、途中で改行しても通る。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._download_root(
                root, self.PNG,
                "<section><p><code>docs</code> →\n  <code>x</code> → <code>downloads</code> の title.png をコピーします。</p></section>")
            self.assertEqual(self._download_errors(root), [])

    def test_download_differing_by_one_byte_is_rejected(self):
        """配布ファイルが、完成プロジェクトのソースと1バイトでも違えば検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            changed = bytearray(self.PNG)
            changed[-1] ^= 0x01
            self._download_root(root, bytes(changed), self.GUIDE)
            errors = self._download_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("docs/x/downloads/title.png:1", errors[0])
            self.assertIn("内容が一致しません: Sample/app/src/main/res/drawable/title.png", errors[0])

    def test_download_without_folder_guidance_is_rejected(self):
        """置き場所の案内が教科書から消えたら検出する。学生はファイルを見つけられない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._download_root(root, self.PNG, "<section><p>先生から配られた title.png を使います。</p></section>")
            errors = self._download_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("docs/x/index.html:1", errors[0])
            self.assertIn("置き場所の案内がありません: docs → x → downloads", errors[0])

    def test_download_button_is_not_guidance(self):
        """ダウンロードボタンだけでは通らない。file:// で開いた教科書では、押しても保存されない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._download_root(
                root, self.PNG,
                '<section><a class="button-link" href="downloads/title.png" download>title.png</a></section>')
            errors = self._download_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("置き場所の案内がありません: docs → x → downloads", errors[0])

    def test_download_without_file_name_is_rejected(self):
        """ファイル名の案内が消えたら検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._download_root(root, self.PNG, "<section><p><code>docs → x → downloads</code> を開きます。</p></section>")
            errors = self._download_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("ファイル名の案内がありません: title.png", errors[0])

    def test_download_guided_only_in_another_step_is_rejected(self):
        """置き場所が別のSTEPにしか書かれていなければ検出する。

        同じフォルダのファイルを別々のSTEPで使うとき、片方のSTEPから置き場所の案内が消えても、
        教科書全体で探すと見つかってしまう。
        """
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._download_root(
                root, self.PNG,
                '<section id="step-2"><p>title.png をdrawableに入れます。</p></section>'
                '<section id="step-7"><p><code>docs → x → downloads</code> の Other.kt をコピーします。</p></section>')
            errors = self._download_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("ファイル名の案内がありません: title.png", errors[0])
            self.assertIn("同じSTEP", errors[0])

    def test_download_renamed_from_source_is_rejected(self):
        """学生はコピーしたファイルをそのままdrawableに入れるので、名前の違いも検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._download_root(root, self.PNG, self.GUIDE.replace("title.png", "Title.png"),
                                download_name="Title.png")
            errors = self._download_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("ファイル名が一致しません", errors[0])

    def test_download_source_outside_archive_is_rejected(self):
        """元ファイルがGit管理されていなければ、完成プロジェクトZIPにも入らない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._download_root(root, self.PNG, self.GUIDE)
            subprocess.run(["git", "rm", "--cached", "-q", "Sample/app/src/main/res/drawable/title.png"],
                           cwd=root, check=True, capture_output=True)
            errors = self._download_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("完成プロジェクトZIPに入るファイルではありません", errors[0])

    # ------------------------------------------------------------------
    # サイドバー（check_sidebar_units）
    # ------------------------------------------------------------------

    # 純Kotlin系2単元 → Android系1単元。K系はどれも K01HelloKotlin プロジェクトを共有する。
    SIDEBAR_UNITS = [("K01One", "one"), ("K02Two", "two"), ("A01Three", "three")]

    def _sidebar(self, current: str, order: list[str] | None = None, link_self: bool = False) -> str:
        """3単元ぶんのサイドバーを作る。current はいま開いている単元のフォルダ名。"""
        names = dict((folder, name) for name, folder in self.SIDEBAR_UNITS)
        entries = []
        for folder in order or [folder for _, folder in self.SIDEBAR_UNITS]:
            label = f"{names[folder][:3]}：{names[folder][3:]}"
            if folder == current and not link_self:
                entries.append(f'<span aria-current="page">{label}</span>')
            else:
                entries.append(f'<a href="../{folder}/index.html">{label}</a>')
        return ('<aside class="sidebar"><div class="progress"><span>0 / 3</span></div>\n'
                '<div class="resources"><a href="#help">困ったとき</a>' + "".join(entries)
                + f'<a href="../common/setup.html?from={current}">共通：はじめの準備</a></div></aside>')

    def _sidebar_project(self, name: str, folder: str) -> dict:
        """サイドバーの検査に必要なだけの単元設定を作る。"""
        if name.startswith("K"):
            return self._project(
                name=name, kind="kotlin-console", root="K01HelloKotlin",
                packages=[f"ex{name[1:3]}"],
                sources=[f"K01HelloKotlin/src/ex{name[1:3]}/main.kt"],
                docs=[f"docs/{folder}/index.html", f"teacher/{folder}/index.html"],
                archive=f"docs/{folder}/downloads/K01HelloKotlin.zip")
        return self._project(
            name=name, kind="android", root=name, package=f"jp.ac.jec.{name.lower()}",
            sources=[f"{name}/app/src/main/java/MainActivity.kt"],
            docs=[f"docs/{folder}/index.html", f"teacher/{folder}/index.html"],
            archive=f"docs/{folder}/downloads/{name}.zip")

    def _sidebar_errors(self, root: Path, textbooks: dict[str, str]) -> list[str]:
        """教科書を書き出して検査し、サイドバーについてのエラーだけを返す。"""
        for folder, content in textbooks.items():
            (root / "docs" / folder).mkdir(parents=True)
            (root / "docs" / folder / "index.html").write_text(content, encoding="utf-8")
        self._minimal_config(root, [
            self._sidebar_project(name, folder) for name, folder in self.SIDEBAR_UNITS
        ])
        return [error for error in CHECKER.validate(root) if "サイドバー" in error]

    def test_sidebar_listing_every_unit_is_accepted(self):
        """どの単元でも全単元が並び、いま開いている単元だけが現在地になっている。"""
        with tempfile.TemporaryDirectory() as temporary:
            errors = self._sidebar_errors(Path(temporary), {
                folder: self._sidebar(folder) for _, folder in self.SIDEBAR_UNITS
            })
            self.assertEqual(errors, [])

    def test_sidebar_missing_later_unit_is_rejected(self):
        """単元を足したのに、前の単元のサイドバーを直し忘れた状態を検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            textbooks = {folder: self._sidebar(folder) for _, folder in self.SIDEBAR_UNITS}
            textbooks["one"] = self._sidebar("one", order=["one", "two"])
            errors = self._sidebar_errors(Path(temporary), textbooks)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("docs/one/index.html:2", errors[0])
            self.assertIn('単元へのリンクがありません: <a href="../three/index.html">A01：Three</a>', errors[0])

    def test_sidebar_linking_current_unit_is_rejected(self):
        """いま開いている単元は、リンクではなく現在地として示す。"""
        with tempfile.TemporaryDirectory() as temporary:
            textbooks = {folder: self._sidebar(folder) for _, folder in self.SIDEBAR_UNITS}
            textbooks["two"] = self._sidebar("two", link_self=True)
            errors = self._sidebar_errors(Path(temporary), textbooks)
            self.assertEqual(len(errors), 2, errors)
            self.assertIn('現在地がありません: <span aria-current="page">K02：Two</span>', errors[0])
            self.assertIn("いま開いている単元がリンクになっています: K02：Two", errors[1])

    def test_sidebar_in_wrong_order_is_rejected(self):
        """過不足がなくても、projects の順に並んでいなければ検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            textbooks = {folder: self._sidebar(folder) for _, folder in self.SIDEBAR_UNITS}
            textbooks["three"] = self._sidebar("three", order=["two", "one", "three"])
            errors = self._sidebar_errors(Path(temporary), textbooks)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("projectsの順に並んでいません: K02：Two、K01：One、A01：Three", errors[0])

    def test_sidebar_with_unregistered_unit_is_rejected(self):
        """projects にない単元へのリンクが残っている状態を検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            textbooks = {folder: self._sidebar(folder) for _, folder in self.SIDEBAR_UNITS}
            textbooks["one"] = textbooks["one"].replace(
                '<a href="../common/', '<a href="../four/index.html">A02：Four</a><a href="../common/', 1)
            errors = self._sidebar_errors(Path(temporary), textbooks)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("登録のない単元があります: A02：Four（../four/index.html）", errors[0])

    def test_sidebar_with_duplicated_unit_is_rejected(self):
        """単元を足すときのコピーで、同じ単元が2回並んだ状態を検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            textbooks = {folder: self._sidebar(folder) for _, folder in self.SIDEBAR_UNITS}
            textbooks["two"] = self._sidebar("two", order=["one", "one", "two", "three"])
            errors = self._sidebar_errors(Path(temporary), textbooks)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("projectsの順に並んでいません: K01：One、K01：One、K02：Two、A01：Three", errors[0])

    def test_sidebar_with_link_around_current_unit_is_rejected(self):
        """現在地をリンクで包むと、リンクにしない決まりをすり抜けるので検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            textbooks = {folder: self._sidebar(folder) for _, folder in self.SIDEBAR_UNITS}
            textbooks["two"] = textbooks["two"].replace(
                '<span aria-current="page">K02：Two</span>',
                '<a href="../two/index.html"><span aria-current="page">K02：Two</span></a>', 1)
            errors = self._sidebar_errors(Path(temporary), textbooks)
            self.assertTrue(any("単元の中に、別のタグがあります: <span>" in error for error in errors), errors)
            self.assertTrue(any("いま開いている単元がリンクになっています: K02：Two" in error for error in errors), errors)

    def test_sidebar_ignores_topbar_and_nested_div(self):
        """topbarの単元リンクは検査しない。resources の中の <div> は、サイドバーの終わりと取り違えない。"""
        with tempfile.TemporaryDirectory() as temporary:
            textbooks = {folder: self._sidebar(folder) for _, folder in self.SIDEBAR_UNITS}
            textbooks["two"] = (
                '<header class="topbar"><a href="../one/index.html">K01 One</a></header>\n'
                + textbooks["two"].replace(
                    '<a href="../one/index.html">K01：One</a>',
                    '<div class="group"><a href="../one/index.html">K01：One</a></div>', 1))
            errors = self._sidebar_errors(Path(temporary), textbooks)
            self.assertEqual(errors, [])

    def test_textbook_without_sidebar_is_rejected(self):
        """サイドバーそのものがない教科書は、並びを確かめようがないので検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            textbooks = {folder: self._sidebar(folder) for _, folder in self.SIDEBAR_UNITS}
            textbooks["two"] = "<main><h1>Two</h1></main>"
            errors = self._sidebar_errors(Path(temporary), textbooks)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("docs/two/index.html:1", errors[0])
            self.assertIn("サイドバー（<div class=\"resources\">）がありません", errors[0])

    # ------------------------------------------------------------------
    # projects の並び（2系統）
    # ------------------------------------------------------------------

    def _order_errors(self, root: Path, names: list[str]) -> list[str]:
        self._minimal_config(root, [
            self._sidebar_project(name, name.lower()) for name in names
        ])
        return [error for error in CHECKER.validate(root) if "単元番号順" in error]

    def test_projects_in_kotlin_then_android_order_are_accepted(self):
        """純Kotlin系をひと通り終えてからAndroid系に入るのが、この授業の進み方。"""
        with tempfile.TemporaryDirectory() as temporary:
            errors = self._order_errors(Path(temporary), ["K01One", "K02Two", "A01Three"])
            self.assertEqual(errors, [])

    def test_projects_out_of_unit_number_order_are_rejected(self):
        """サイドバーは projects の順と照合するので、番号が戻っていたら検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = self._order_errors(root, ["K01One", "K03Three", "K02Two"])
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])
            self.assertIn("K03ThreeのあとにK02Twoがあります", errors[0])

    def test_projects_returning_to_kotlin_after_android_are_rejected(self):
        """いちどAndroid系に移ったあとで純Kotlin系に戻る並びは検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = self._order_errors(root, ["K01One", "A01Three", "K02Two"])
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("A01ThreeのあとにK02Twoがあります", errors[0])

    # ------------------------------------------------------------------
    # .gitignore と追跡してはいけないファイル（check_project_layout）
    # ------------------------------------------------------------------

    def _layout_root(self, root: Path, reference, gitignores: dict[str, str],
                     projects: list[dict]) -> None:
        for project_root, content in gitignores.items():
            self._write(root, f"{project_root}/.gitignore", content)
        self._git_add(root, *gitignores)
        self._minimal_config(root, projects, project_layout={
            "gitignore_reference": reference,
            "untracked_parts": [".idea", ".gradle", ".kotlin", "build", "out"],
            "untracked_names": ["local.properties"],
        })

    def _layout_errors(self, root: Path) -> list[str]:
        return [error for error in CHECKER.validate(root)
                if ".gitignore" in error or "Git管理" in error]

    def test_gitignore_reference_dictionary_is_applied_per_kind(self):
        """kind ごとに .gitignore の基準を変えられる。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._layout_root(
                root,
                {"kotlin-console": "K01HelloKotlin/.gitignore",
                 "android": "A01HelloAndroid/.gitignore"},
                {"K01HelloKotlin": self.KOTLIN_IGNORE,
                 "A01HelloAndroid": self.ANDROID_IGNORE,
                 # Android系なのに、純Kotlin系の .gitignore をコピーしてしまった。
                 "A02CalcGame": self.KOTLIN_IGNORE},
                [self._project(),
                 self._sidebar_project("A01HelloAndroid", "hello-android"),
                 self._sidebar_project("A02CalcGame", "calc-game")])
            errors = self._layout_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("A02CalcGame/.gitignore:1", errors[0])
            self.assertIn("A01HelloAndroid/.gitignoreと内容が異なります", errors[0])

    def test_gitignore_reference_string_is_common_to_every_kind(self):
        """文字列で書かれていたら、参照リポジトリと同じく全kind共通の基準とみなす。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._layout_root(
                root,
                "A01HelloAndroid/.gitignore",
                {"K01HelloKotlin": self.KOTLIN_IGNORE,
                 "A01HelloAndroid": self.ANDROID_IGNORE},
                [self._project(), self._sidebar_project("A01HelloAndroid", "hello-android")])
            errors = self._layout_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("K01HelloKotlin/.gitignore:1", errors[0])
            self.assertIn("A01HelloAndroid/.gitignoreと内容が異なります", errors[0])

    def test_missing_gitignore_reference_for_kind_is_rejected(self):
        """使っている kind の基準を書き忘れたら検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._layout_root(
                root,
                {"android": "A01HelloAndroid/.gitignore"},
                {"K01HelloKotlin": self.KOTLIN_IGNORE, "A01HelloAndroid": self.ANDROID_IGNORE},
                [self._project(), self._sidebar_project("A01HelloAndroid", "hello-android")])
            errors = self._layout_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])
            self.assertIn("kotlin-consoleの基準がありません", errors[0])

    def test_untracked_file_is_reported_once_per_project(self):
        """純Kotlin系は複数の単元が1つのプロジェクトを共有する。同じ指摘を単元の数だけ出さない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/local.properties", "sdk.dir=/dev/null\n")
            self._layout_root(
                root,
                {"kotlin-console": "K01HelloKotlin/.gitignore"},
                {"K01HelloKotlin": self.KOTLIN_IGNORE},
                [self._project(name="K01One", packages=["ex01"],
                               sources=["K01HelloKotlin/src/ex01/main.kt"]),
                 self._project(name="K02Two", packages=["ex02"],
                               sources=["K01HelloKotlin/src/ex02/main.kt"])])
            errors = self._layout_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("K01HelloKotlin/local.properties:1", errors[0])
            self.assertIn("Git管理してはいけないファイルです", errors[0])

    # ------------------------------------------------------------------
    # 用語をどの系統に求めるか（terms[].applies_to）
    #
    # 指定AVD名のように、Android系でしか使わない用語がある。それを純Kotlin系の
    # 教科書にまで required_in で求めると、書きようのない表記を迫ることになる。
    # applies_to を書かない用語は、これまでどおり両方の系統に求める。
    # ------------------------------------------------------------------

    KOTLIN_DOCS = ["docs/hello-kotlin/index.html", "teacher/hello-kotlin/index.html"]
    ANDROID_DOCS = ["docs/hello-android/index.html", "teacher/hello-android/index.html"]

    def _term(self, required_in: list[str], **extra) -> dict:
        term = {"name": "指定AVD名", "canonical": self.AVD, "forbidden": [],
                "required_in": required_in}
        term.update(extra)
        return term

    def _applies_to_errors(self, root: Path, terms: list[dict]) -> list[str]:
        """純Kotlin系とAndroid系を1単元ずつ置いて、required_in の不足だけを返す。"""
        self._minimal_config(
            root,
            [self._project(), self._sidebar_project("A01HelloAndroid", "hello-android")],
            terms=terms,
            registration={"targets": []},
        )
        return [error for error in CHECKER.validate(root)
                if "terms.required_inにありません" in error]

    def test_term_for_android_requires_android_documents(self):
        """applies_to がAndroid系なら、Android単元の教材を required_in に求める。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = self._applies_to_errors(
                root, [self._term(self.KOTLIN_DOCS, applies_to=["android"])])
            self.assertEqual(len(errors), 2, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])
            self.assertIn("A01HelloAndroidのdocs/hello-android/index.htmlが", errors[0])
            self.assertIn("A01HelloAndroidのteacher/hello-android/index.htmlが", errors[1])

    def test_term_for_android_does_not_require_kotlin_documents(self):
        """同じ設定でも、純Kotlin系の教材は required_in に無くてよい。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = self._applies_to_errors(
                root, [self._term(self.ANDROID_DOCS, applies_to=["android"])])
            self.assertEqual(errors, [])

    def test_term_without_applies_to_requires_every_kind(self):
        """applies_to を書かない用語は、両方の系統に求める（後方互換）。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = self._applies_to_errors(root, [self._term(self.ANDROID_DOCS)])
            self.assertEqual(len(errors), 2, errors)
            self.assertIn("K01HelloKotlinのdocs/hello-kotlin/index.htmlが", errors[0])
            self.assertIn("K01HelloKotlinのteacher/hello-kotlin/index.htmlが", errors[1])

    def test_term_with_empty_applies_to_requires_no_kind(self):
        """applies_to が空配列なら、どの系統にも求めない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = self._applies_to_errors(root, [self._term([], applies_to=[])])
            self.assertEqual(errors, [])

    def test_terms_are_judged_one_by_one(self):
        """用語が2つあるとき、applies_to は用語ごとに効く。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = self._applies_to_errors(root, [
                # Android系にだけ求める用語。Android単元の教材は required_in にある。
                self._term(self.ANDROID_DOCS, applies_to=["android"]),
                # 両方の系統に求める用語。純Kotlin系の教材が required_in にない。
                self._term(self.ANDROID_DOCS, name="授業名"),
            ])
            self.assertEqual(len(errors), 2, errors)
            self.assertTrue(all("K01HelloKotlin" in error for error in errors), errors)

    # ------------------------------------------------------------------
    # 教材に置いた複製コード（check_mirrors）
    #
    # teacher/<スラッグ>/code/ は完成プロジェクトのソースの複製。完成コードだけを
    # 直すと複製が古いまま静かに残るので、バイト単位で照合する。
    # ------------------------------------------------------------------

    MIRROR = [{"source": "K01HelloKotlin/src/ex01/main.kt",
               "copy": "teacher/hello-kotlin/code/01-main.kt"}]

    def _mirror_errors(self, root: Path, **overrides) -> list[str]:
        """複製コードについてのエラーだけを返す。"""
        self._minimal_config(root, [self._project(**overrides)])
        return [error for error in CHECKER.validate(root) if "複製コード" in error]

    def test_mirror_identical_to_the_source_is_accepted(self):
        """複製コードが元ファイルと1バイトも違わなければ、何も言わない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt", self.KOTLIN_SOURCE)
            self._write(root, "teacher/hello-kotlin/code/01-main.kt", self.KOTLIN_SOURCE)
            self.assertEqual(self._mirror_errors(root, mirrors=self.MIRROR), [])

    def test_mirror_differing_by_one_byte_is_rejected(self):
        """完成コードだけ直して、複製コードが古いまま残った状態を検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt", self.KOTLIN_SOURCE)
            self._write(root, "teacher/hello-kotlin/code/01-main.kt",
                        self.KOTLIN_SOURCE.replace("こんにちは", "おはよう"))
            errors = self._mirror_errors(root, mirrors=self.MIRROR)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("teacher/hello-kotlin/code/01-main.kt:1", errors[0])
            self.assertIn("内容が一致しません: K01HelloKotlin/src/ex01/main.kt", errors[0])

    def test_mirror_without_copy_is_rejected(self):
        """複製コードを置き忘れた状態を検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt", self.KOTLIN_SOURCE)
            errors = self._mirror_errors(root, mirrors=self.MIRROR)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("teacher/hello-kotlin/code/01-main.kt:1", errors[0])
            self.assertIn("複製コードがありません", errors[0])

    def test_mirror_without_source_is_rejected(self):
        """元ファイルのパスを書き間違えた状態を検出する。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "teacher/hello-kotlin/code/01-main.kt", self.KOTLIN_SOURCE)
            errors = self._mirror_errors(root, mirrors=self.MIRROR)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("K01HelloKotlin/src/ex01/main.kt:1", errors[0])
            self.assertIn("複製コードの元ファイルがありません", errors[0])

    def test_project_without_mirrors_is_accepted(self):
        """mirrors を書かない単元では、何も照合しない（後方互換）。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "K01HelloKotlin/src/ex01/main.kt", self.KOTLIN_SOURCE)
            # 複製の置き場所には、わざと中身の違うファイルを置いてある。
            self._write(root, "teacher/hello-kotlin/code/01-main.kt", "fun main() {}\n")
            self.assertEqual(self._mirror_errors(root), [])

    # ------------------------------------------------------------------
    # 設定の必須キー（check_config）
    #
    # キーを書き忘れたときに、Pythonのトレースバックではなく日本語のエラーを出す。
    # トレースバックのままだと、設定のどこを直せばよいか分からない。
    # ------------------------------------------------------------------

    def _full_config(self) -> dict:
        """必須キーがそろった設定。ここから1つずつ落として試す。"""
        return {
            "scan_roots": [],
            "terms": [],
            "registration": {"targets": [{"path": "README.md", "requires": []}]},
            "projects": [self._project()],
        }

    def test_missing_top_level_key_is_reported_in_japanese(self):
        """scan_roots・terms・projects の書き忘れを、日本語のエラーにする。"""
        for key in ("scan_roots", "terms", "projects"):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                config = self._full_config()
                del config[key]
                self._write_config(root, config)
                self.assertEqual(
                    CHECKER.validate(root),
                    [f"config/teaching-materials.json:1: 設定に{key}がありません"])

    def test_missing_project_key_is_reported_in_japanese(self):
        """単元の設定のキーの書き忘れを、日本語のエラーにする。"""
        for key in ("name", "root", "docs", "snippets", "archive"):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                config = self._full_config()
                del config["projects"][0][key]
                self._write_config(root, config)
                errors = CHECKER.validate(root)
                self.assertEqual(len(errors), 1, errors)
                self.assertIn("config/teaching-materials.json:1", errors[0])
                self.assertIn(f"に{key}がありません", errors[0])

    def test_missing_registration_target_key_is_reported_in_japanese(self):
        """registration.targets の項目のキーの書き忘れを、日本語のエラーにする。"""
        for key in ("path", "requires"):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                config = self._full_config()
                del config["registration"]["targets"][0][key]
                self._write_config(root, config)
                self.assertEqual(CHECKER.validate(root), [
                    "config/teaching-materials.json:1: "
                    f"registration.targets[0]に{key}がありません"])

    def test_missing_mirror_key_is_reported_in_japanese(self):
        """mirrors の項目のキーの書き忘れを、日本語のエラーにする。"""
        for key in ("source", "copy"):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                config = self._full_config()
                config["projects"][0]["mirrors"] = [
                    {name: value for name, value in self.MIRROR[0].items() if name != key}]
                self._write_config(root, config)
                errors = CHECKER.validate(root)
                self.assertEqual(len(errors), 1, errors)
                self.assertIn(f"のmirrors[0]に{key}がありません", errors[0])

    def test_missing_nested_setting_key_is_reported_in_japanese(self):
        """registration と project_layout の中のキーの書き忘れも、日本語のエラーにする。"""
        cases = [
            ("registration", "registrationにtargetsがありません"),
            ("project_layout", "project_layoutにgitignore_referenceがありません"),
        ]
        for key, message in cases:
            with self.subTest(key=key), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                config = self._full_config()
                config[key] = {"メモ": "キーを書き忘れた設定"}
                self._write_config(root, config)
                self.assertEqual(CHECKER.validate(root),
                                 [f"config/teaching-materials.json:1: {message}"])

    def test_project_without_teacher_document_is_reported_in_japanese(self):
        """docs は学生向けと教員用の2つ。1つしか書かなくてもトレースバックにしない。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = self._full_config()
            config["projects"][0]["docs"] = ["docs/hello-kotlin/index.html"]
            self._write_config(root, config)
            errors = CHECKER.validate(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("config/teaching-materials.json:1", errors[0])
            self.assertIn("学生向けの教科書と教員用ガイドを2つ書いてください", errors[0])

    def test_complete_config_reaches_the_other_checks(self):
        """必須キーがそろっていれば、入口で引き返さずに本体の検査へ進む。"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(root, self._full_config())
            errors = CHECKER.validate(root)
            # 教材の実体が1つも無いので、本体の検査が言う。入口の検査は何も言わない。
            self.assertTrue(
                any("完成プロジェクトZIPがありません" in error for error in errors), errors)
            self.assertEqual([error for error in errors if "設定に" in error], [])


class ProgressKeyTest(unittest.TestCase):
    """チェック欄のあるページが、自分用の記録キーを持っているかの検査。

    docs/assets/textbook.js は、そのページで見つかった data-check だけを
    localStorage へ書き戻す。2つのページが同じキーを使うと、あとから開いた側が
    もう一方の記録を消す。
    """

    def _write(self, root: Path, name: str, text: str) -> Path:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def _page(self, key: str | None, checks: int) -> str:
        body = "<body>" if key is None else f'<body data-progress-key="{key}">'
        boxes = "".join(f'<input type="checkbox" data-check="step-{i}">' for i in range(checks))
        return f'<!doctype html><html lang="ja">{body}<main>{boxes}</main></body></html>'

    def _check(self, root: Path) -> list[str]:
        errors: list[str] = []
        CHECKER.check_progress_keys(root, errors)
        return errors

    def test_page_with_checks_needs_a_key(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            self._write(root, "docs/hello-kotlin/index.html", self._page(None, 2))
            errors = self._check(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("data-progress-key", errors[0])

    def test_page_without_checks_needs_no_key(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            self._write(root, "docs/common/apk.html", self._page(None, 0))
            self.assertEqual(self._check(root), [])

    def test_two_pages_must_not_share_a_key(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            self._write(root, "docs/hello-kotlin/index.html", self._page("jec-kotlin-hellokotlin-v1", 2))
            self._write(root, "docs/common/setup.html", self._page("jec-kotlin-hellokotlin-v1", 1))
            errors = self._check(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("docs/hello-kotlin/index.html", errors[0])

    def test_distinct_keys_pass(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            self._write(root, "docs/hello-kotlin/index.html", self._page("jec-kotlin-hellokotlin-v1", 2))
            self._write(root, "docs/common/setup.html", self._page("jec-kotlin-setup-v1", 1))
            self.assertEqual(self._check(root), [])


class SampleGuidanceCheckTest(unittest.TestCase):
    """教科書（docs/ のHTML）から完成プロジェクトへ案内していないかの検査（#264）。"""

    CONFIG = {"projects": [{"name": "A01HelloAndroid", "archive": "docs/hello-android/downloads/A01HelloAndroid.zip"}]}

    def _check(self, pages: dict[str, str]) -> list[str]:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for page, text in pages.items():
                path = root / page
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            errors: list[str] = []
            CHECKER.check_no_sample_guidance(root, self.CONFIG, errors)
            return errors

    def test_textbook_without_sample_guidance_is_accepted(self):
        """画像の置き場所（downloads/）へのリンクや、属性の中の語は案内にあたらない。"""
        errors = self._check({
            "docs/hello-android/index.html": (
                '<p><a href="downloads/character.png">画像</a></p>\n'
                '<img src="images/samples.png"\n alt="完成プロジェクトの画面">\n'
                "<p>完成版を起動したときの画面</p>"
            ),
        })
        self.assertEqual(errors, [])

    def test_sample_guidance_words_are_rejected(self):
        """本文に「完成プロジェクト」「samples」が出たら、共通資料でも行番号つきで検出する。"""
        errors = self._check({
            "docs/hello-android/index.html": "<p>見比べるときは</p>\n<p>完成プロジェクトを開きます。</p>",
            "docs/common/help.html": "<p><code>samples</code> フォルダを開きます。</p>",
        })
        self.assertEqual(len(errors), 2, errors)
        self.assertIn("docs/common/help.html:1", errors[0])
        self.assertIn("samples", errors[0])
        self.assertIn("docs/hello-android/index.html:2", errors[1])
        self.assertIn("完成プロジェクト", errors[1])

    def test_line_numbers_follow_tags_spanning_lines(self):
        """複数行にまたがるタグのあとでも、本文の行番号は元のファイルと合う。"""
        errors = self._check({
            "docs/hello-android/index.html": '<img src="a.png"\n alt="x">\n<p>samples を開く</p>',
        })
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("docs/hello-android/index.html:3", errors[0])

    def test_link_to_project_archive_is_rejected(self):
        """完成プロジェクトZIPへのリンクは、文言や引用符にかかわらず検出する。別ページからの相対パスや絶対URLも解決する。"""
        errors = self._check({
            "docs/hello-android/index.html": "<p>ダウンロード</p>\n<a href='downloads/A01HelloAndroid.zip' download>答え</a>",
            "docs/common/help.html": '<a href="../hello-android/downloads/A01HelloAndroid.zip?from=x">見本</a>',
            "docs/common/setup.html": '<a href="https://example.com/downloads/A01HelloAndroid.zip">見本</a>',
        })
        self.assertEqual(len(errors), 3, errors)
        self.assertIn("docs/common/help.html:1", errors[0])
        self.assertIn("docs/common/setup.html:1", errors[1])
        self.assertIn("docs/hello-android/index.html:2", errors[2])
        self.assertTrue(all("完成プロジェクトZIPへリンク" in error for error in errors), errors)

    def test_validate_runs_the_check(self):
        """validate() の流れからも呼ばれる。"""
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "config").mkdir()
            (root / "config/teaching-materials.json").write_text(
                json.dumps({"scan_roots": [], "terms": [], "projects": []}), encoding="utf-8")
            (root / "docs/common").mkdir(parents=True)
            (root / "docs/common/help.html").write_text("<p>完成プロジェクトの開き方</p>", encoding="utf-8")
            errors = CHECKER.validate(root)
            self.assertTrue(any("docs/common/help.html:1" in error and "基本方針」13" in error
                                for error in errors), errors)


class DiffBlockTest(unittest.TestCase):
    """差分ブロックの検査（README「授業用教科書の基本方針」14、#269）。

    すでにあるファイルを直すSTEPは、全文ではなく、足す行（<ins>）・消す行（<del>）・
    すでにある行（印なし）だけを載せる。その枠を直す前のファイルに当てると、直したあとの
    ファイルと1文字も違わないことを確かめる。全文のスニペットのバイト照合と同じ役目。
    """

    HTML = "docs/x/index.html"
    BEFORE = (
        "plugins {\n"
        "    alias(libs.plugins.android.application)\n"
        "}\n"
        "\n"
        "dependencies {\n"
        "    implementation(libs.material)\n"
        "    testImplementation(libs.junit)\n"
        "}"  # ウィザードが作るファイルと同じく、末尾に改行がない
    )
    AFTER = (
        "plugins {\n"
        "    alias(libs.plugins.android.application)\n"
        "    alias(libs.plugins.kotlinxSerialization)\n"
        "}\n"
        "\n"
        "dependencies {\n"
        "    implementation(libs.material)\n"
        "    implementation(libs.ktor.client.core)\n"
        "    testImplementation(libs.junit)\n"
        "}\n"
    )
    GAP = '<span class="diff-gap">⋮\n</span>'
    PLUGINS = (
        "plugins {\n"
        "    alias(libs.plugins.android.application)\n"
        "<ins>    alias(libs.plugins.kotlinxSerialization)\n</ins>"
        "}\n"
    )
    DEPENDENCIES = (
        "dependencies {\n"
        "    implementation(libs.material)\n"
        "<ins>    implementation(libs.ktor.client.core)\n</ins>"
        "    testImplementation(libs.junit)\n"
        "}\n"
    )

    # ------------------------------------------------------------------
    # 仮のリポジトリを組み立てる道具
    # ------------------------------------------------------------------

    def _write(self, root: Path, name: str, text: str) -> None:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _block(self, block_id: str, inner: str, classes: str = ' class="diff"') -> str:
        return f'<pre id="{block_id}"{classes} tabindex="0"><code>{inner}</code></pre>'

    def _project(self, **overrides) -> dict:
        project = {
            "name": "A03GithubSearch", "kind": "android", "root": "A03GithubSearch",
            "package": "jp.ac.jec.a03githubsearch",
            "docs": [self.HTML, "teacher/x/index.html"], "snippets": [], "archive": "x.zip",
            "diffs": [{"html": self.HTML, "ids": ["diff-gradle"], "before": "before.kts", "after": "after.kts"}],
        }
        project.update(overrides)
        return project

    def _errors(self, page: str, *, before: str | None = None, after: str | None = None,
                project: dict | None = None, extra: dict | None = None, config: dict | None = None) -> list[str]:
        """教科書に page を書いたときに、check_diffs が言うこと。"""
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            self._write(root, self.HTML, "<main>\n<p>直す場所だけを載せます。</p>\n" + page + "\n</main>")
            self._write(root, "before.kts", self.BEFORE if before is None else before)
            self._write(root, "after.kts", self.AFTER if after is None else after)
            for path, text in (extra or {}).items():
                self._write(root, path, text)
            project = project or self._project()
            errors: list[str] = []
            CHECKER.check_diffs(root, config or {"projects": [project]}, project, errors)
            return errors

    # ------------------------------------------------------------------
    # 当てた結果が、直したあとのファイルになるか
    # ------------------------------------------------------------------

    def test_block_that_gives_the_after_file_is_accepted(self):
        """足す行をすべて載せた枠は通る。あいだの変えない行は ⋮ で省ける。"""
        self.assertEqual(self._errors(self._block("diff-gradle", self.PLUGINS + self.GAP + self.DEPENDENCIES)), [])

    def test_block_missing_an_added_line_is_rejected(self):
        """足す行が1行でも足りないと、当てた結果が完成コードにならない。行番号と中身を出す。"""
        dependencies = self.DEPENDENCIES.replace("<ins>    implementation(libs.ktor.client.core)\n</ins>", "")
        errors = self._errors(self._block("diff-gradle", self.PLUGINS + self.GAP + dependencies))
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("docs/x/index.html:3", errors[0])
        self.assertIn("diff-gradleをbefore.ktsに当てても、after.ktsと一致しません", errors[0])
        self.assertIn("8行目", errors[0])
        self.assertIn("implementation(libs.ktor.client.core)", errors[0])

    def test_changed_line_needs_both_marks(self):
        """書き換える行は、消す行（<del>）と足す行（<ins>）の組で載せる。"""
        after = self.AFTER.replace("implementation(libs.material)", "implementation(libs.material3)")
        changed = (
            "dependencies {\n"
            "<del>    implementation(libs.material)\n</del>"
            "<ins>    implementation(libs.material3)\n"
            "    implementation(libs.ktor.client.core)\n</ins>"
            "    testImplementation(libs.junit)\n"
        )
        self.assertEqual(self._errors(self._block("diff-gradle", self.PLUGINS + self.GAP + changed), after=after), [])
        # 消す行を載せ忘れると、古い行が残って完成コードにならない。
        forgotten = changed.replace("<del>    implementation(libs.material)\n</del>", "    implementation(libs.material)\n")
        errors = self._errors(self._block("diff-gradle", self.PLUGINS + self.GAP + forgotten), after=after)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("一致しません", errors[0])

    def test_end_of_file_newlines_are_ignored(self):
        """末尾の改行や空行の違いは見ない（ウィザードのファイルは、末尾に改行がない）。"""
        page = self._block("diff-gradle", self.PLUGINS + self.GAP + self.DEPENDENCIES)
        self.assertEqual(self._errors(page, before=self.BEFORE + "\n\n", after=self.AFTER.rstrip()), [])

    def test_block_without_marks_is_an_excerpt(self):
        """印のない枠は「見比べるだけ」の抜粋。直す前と直したあとが同じなら通る。"""
        page = self._block("diff-gradle", "dependencies {\n    implementation(libs.material)\n", classes="")
        self.assertEqual(self._errors(page, after=self.BEFORE), [])
        # 抜粋の数字が、ファイルと1文字でも違えば検出する。
        page = self._block("diff-gradle", "dependencies {\n    implementation(libs.material3)\n", classes="")
        errors = self._errors(page, after=self.BEFORE)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("当てる場所がありません", errors[0])

    def test_several_blocks_are_applied_in_order(self):
        """1つのファイルの差分を、説明をはさんで複数の枠に分けて載せられる。"""
        page = (self._block("diff-plugins", self.PLUGINS) + "<p>次に、依存を足します。</p>"
                + self._block("diff-dependencies", self.DEPENDENCIES))
        project = self._project(diffs=[{"html": self.HTML, "ids": ["diff-plugins", "diff-dependencies"],
                                        "before": "before.kts", "after": "after.kts"}])
        self.assertEqual(self._errors(page, project=project), [])
        # 片方の枠だけでは、完成コードにならない。
        project = self._project(diffs=[{"html": self.HTML, "ids": ["diff-plugins"],
                                        "before": "before.kts", "after": "after.kts"}])
        errors = self._errors(page, project=project)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("一致しません", errors[0])

    # ------------------------------------------------------------------
    # 当てる場所が決まるか
    # ------------------------------------------------------------------

    def test_existing_line_that_differs_from_the_file_is_rejected(self):
        """すでにある行が、直す前のファイルと字下げ1つでも違えば、学生は場所を探せない。"""
        plugins = self.PLUGINS.replace("    alias(libs.plugins.android.application)\n",
                                       "  alias(libs.plugins.android.application)\n")
        errors = self._errors(self._block("diff-gradle", plugins + self.GAP + self.DEPENDENCIES))
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("diff-gradle: 1つ目のまとまりを当てる場所がありません", errors[0])
        self.assertIn("1行目までは直す前のファイルの1行目からと一致し、次の行が違います", errors[0])
        self.assertIn("直す前のファイル: before.kts", errors[0])

    def test_ambiguous_place_is_rejected(self):
        """すでにある行の並びが2か所にあると、どちらを直すのか決まらない。"""
        errors = self._errors(self._block("diff-gradle", "<ins>    // 足す行\n</ins>}\n"))
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("場所が1つに決まりません（同じ並びが3行目・8行目にあります）", errors[0])
        self.assertIn("前後のすでにある行を足してください", errors[0])

    def test_block_without_existing_line_is_rejected(self):
        """足す行しかない枠は、どこへ足すのかが分からない。"""
        errors = self._errors(self._block("diff-gradle", "<ins>    alias(libs.plugins.kotlinxSerialization)\n</ins>"))
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("すでにある行（印のない行か消す行）がありません", errors[0])

    def test_hunks_must_follow_the_file_order(self):
        """まとまりは、ファイルの上から下の順に並べる。"""
        errors = self._errors(self._block("diff-gradle", self.DEPENDENCIES + self.GAP + self.PLUGINS))
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("2つ目のまとまりが、前のまとまりと重なっているか、それより上の行を指しています", errors[0])

    # ------------------------------------------------------------------
    # 枠の書き方
    # ------------------------------------------------------------------

    def test_marks_must_cover_whole_lines(self):
        """印は行の単位で付ける。行の途中から始まる印は、どの行のことか決まらない。"""
        inline = self.PLUGINS.replace("<ins>    alias(libs.plugins.kotlinxSerialization)\n</ins>",
                                      "    <ins>alias(libs.plugins.kotlinxSerialization)\n</ins>")
        unclosed = self.PLUGINS.replace("kotlinxSerialization)\n</ins>", "kotlinxSerialization)</ins>\n")
        for inner in (inline, unclosed):
            with self.subTest(inner=inner):
                errors = self._errors(self._block("diff-gradle", inner + self.GAP + self.DEPENDENCIES))
                self.assertEqual(len(errors), 1, errors)
                self.assertIn("印は行の単位で付けてください", errors[0])

    def test_other_tags_are_rejected(self):
        """強調などのタグを混ぜると、学生が入力する文字と枠の中身が食い違う。"""
        inner = self.PLUGINS.replace("    alias(libs.plugins.kotlinxSerialization)\n",
                                     "    <b>alias</b>(libs.plugins.kotlinxSerialization)\n")
        errors = self._errors(self._block("diff-gradle", inner + self.GAP + self.DEPENDENCIES))
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("以外のタグは使えません", errors[0])

    def test_gap_must_sit_between_lines(self):
        """省略の目印は、まとまりとまとまりのあいだにだけ置く。"""
        cases = [
            (self.GAP + self.PLUGINS, "省略の目印（⋮）の前に、行がありません"),
            (self.PLUGINS + self.GAP + self.GAP + self.DEPENDENCIES, "省略の目印（⋮）の前に、行がありません"),
            (self.PLUGINS + self.GAP, "省略の目印（⋮）のあとに、行がありません"),
            ("", "差分ブロックが空です"),
        ]
        for inner, message in cases:
            with self.subTest(message=message, inner=inner):
                errors = self._errors(self._block("diff-gradle", inner))
                self.assertEqual(len(errors), 1, errors)
                self.assertIn(message, errors[0])

    def test_escaped_characters_are_compared_as_written_in_the_file(self):
        """枠の中の &lt; や &quot; は、ファイルの < や " と同じ文字として比べる。"""
        before = '<manifest>\n    <application android:label="x">\n</manifest>'
        after = '<manifest>\n    <uses-permission android:name="android.permission.INTERNET" />\n    <application android:label="x">\n</manifest>'
        inner = ("&lt;manifest&gt;\n"
                 "<ins>    &lt;uses-permission android:name=&quot;android.permission.INTERNET&quot; /&gt;\n</ins>"
                 '    &lt;application android:label="x"&gt;\n')
        self.assertEqual(self._errors(self._block("diff-gradle", inner), before=before, after=after), [])

    # ------------------------------------------------------------------
    # 直す前のファイル：ウィザードが作った直後の形（before_template）
    # ------------------------------------------------------------------

    TEMPLATE = {"root": "Panda2KotlinEmptyViewsActivity", "name": "Panda2KotlinEmptyViewsActivity",
                "package": "jp.ac.jec.panda2kotlinemptyviewsactivity"}
    GENERATED = ('android {\n    namespace = "jp.ac.jec.panda2kotlinemptyviewsactivity"\n}\n'
                 '// Theme.Panda2KotlinEmptyViewsActivity')
    NAMED = ('android {\n    namespace = "jp.ac.jec.a03githubsearch"\n'
             "    buildFeatures { viewBinding = false }\n}\n// Theme.A03GithubSearch\n")

    def _template_errors(self, inner: str) -> list[str]:
        project = self._project(diffs=[{"html": self.HTML, "ids": ["diff-gradle"],
                                        "before_template": "app/build.gradle.kts", "after": "after.kts"}])
        return self._errors(
            self._block("diff-gradle", inner), after=self.NAMED, project=project,
            extra={"Panda2KotlinEmptyViewsActivity/app/build.gradle.kts": self.GENERATED},
            config={"wizard_template": self.TEMPLATE, "projects": [project]})

    def test_template_is_read_with_the_names_of_the_unit(self):
        """ひな形のパッケージ名とプロジェクト名を、その単元の名前に置き換えてから当てる。

        学生が New Project で作った直後のファイルと同じ形になる。
        """
        inner = ('android {\n    namespace = "jp.ac.jec.a03githubsearch"\n'
                 "<ins>    buildFeatures { viewBinding = false }\n</ins>}\n")
        self.assertEqual(self._template_errors(inner), [])

    def test_block_written_with_the_template_names_is_rejected(self):
        """ひな形の名前のまま写した枠は、学生のファイルと合わない。"""
        inner = ('android {\n    namespace = "jp.ac.jec.panda2kotlinemptyviewsactivity"\n'
                 "<ins>    buildFeatures { viewBinding = false }\n</ins>}\n")
        errors = self._template_errors(inner)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("当てる場所がありません", errors[0])
        self.assertIn("Panda2KotlinEmptyViewsActivity/app/build.gradle.kts（名前をA03GithubSearchに置き換えた形）", errors[0])

    # ------------------------------------------------------------------
    # ファイルや枠が無いとき
    # ------------------------------------------------------------------

    def test_missing_block_and_files_are_reported(self):
        """枠のidの書き間違いと、直す前後のファイルの置き忘れを、それぞれ報告する。"""
        page = self._block("diff-gradle", self.PLUGINS + self.GAP + self.DEPENDENCIES)
        cases = [
            ({"ids": ["diff-typo"]}, "docs/x/index.html:1: 差分ブロックがありません: diff-typo"),
            ({"before": "missing.kts"}, "missing.kts:1: 差分ブロックの、直す前のファイルがありません"),
            ({"after": "missing.kts"}, "missing.kts:1: 差分ブロックの、直したあとのファイルがありません"),
            ({"html": "docs/x/missing.html"}, "docs/x/missing.html:1: 差分ブロックを載せる教材ファイルがありません"),
        ]
        for change, message in cases:
            with self.subTest(change=change):
                diff = {"html": self.HTML, "ids": ["diff-gradle"], "before": "before.kts", "after": "after.kts"}
                diff.update(change)
                self.assertEqual(self._errors(page, project=self._project(diffs=[diff])), [message])

    # ------------------------------------------------------------------
    # 登録もれ（check_diff_registration）
    # ------------------------------------------------------------------

    def _registration_errors(self, page: str, diffs: list) -> list[str]:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            self._write(root, self.HTML, page)
            errors: list[str] = []
            CHECKER.check_diff_registration(root, {"projects": [self._project(diffs=diffs)]}, errors)
            return errors

    def test_unregistered_diff_block_is_rejected(self):
        """登録のない差分ブロックは、当てた結果を誰も確かめていない。"""
        page = "<p>直す場所</p>\n" + self._block("diff-gradle", self.PLUGINS) + "\n" + self._block("diff-other", self.DEPENDENCIES)
        diffs = [{"html": self.HTML, "ids": ["diff-gradle"], "before": "before.kts", "after": "after.kts"}]
        errors = self._registration_errors(page, diffs)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("docs/x/index.html:7", errors[0])
        self.assertIn("差分ブロックがconfig/teaching-materials.jsonのdiffsにありません: diff-other", errors[0])

    def test_diff_block_without_id_is_rejected(self):
        """idのない差分ブロックは、登録のしようがない。"""
        errors = self._registration_errors('<pre class="diff"><code>x\n</code></pre>', [])
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("にidがありません", errors[0])

    def test_plain_code_blocks_need_no_registration(self):
        """全文のコード枠や比較欄（class="diff" でない <pre>）は、登録を求めない。"""
        page = '<pre id="code-main" tabindex="0"><code>x\n</code></pre><pre><code>y\n</code></pre>'
        self.assertEqual(self._registration_errors(page, []), [])

    # ------------------------------------------------------------------
    # 設定の書き方（check_config）
    # ------------------------------------------------------------------

    def _config_errors(self, diff: dict, *, template: dict | None = None, **project) -> list[str]:
        config = {"scan_roots": [], "terms": [], "projects": [self._project(diffs=[diff], **project)]}
        if template is not None:
            config["wizard_template"] = template
        return CHECKER.check_config(config)

    def test_incomplete_diff_setting_is_reported_in_japanese(self):
        """diffs の書き忘れや書き間違いを、トレースバックではなく日本語のエラーにする。"""
        complete = {"html": self.HTML, "ids": ["diff-gradle"], "before": "before.kts", "after": "after.kts"}
        self.assertEqual(self._config_errors(complete), [])
        for key in ("html", "ids", "after"):
            with self.subTest(key=key):
                errors = self._config_errors({name: value for name, value in complete.items() if name != key})
                self.assertEqual(len(errors), 1, errors)
                self.assertIn(f"のdiffs[0]に{key}がありません", errors[0])
        for ids in ("diff-gradle", [], [""]):
            with self.subTest(ids=ids):
                errors = self._config_errors({**complete, "ids": ids})
                self.assertEqual(len(errors), 1, errors)
                self.assertIn("idsは、<pre>のidを1つ以上並べた配列で書いてください", errors[0])

    def test_diff_needs_exactly_one_before(self):
        """直す前のファイルは、before か before_template のどちらか1つ。"""
        base = {"html": self.HTML, "ids": ["diff-gradle"], "after": "after.kts"}
        for extra in ({}, {"before": "before.kts", "before_template": "app/build.gradle.kts"}):
            with self.subTest(extra=extra):
                errors = self._config_errors({**base, **extra}, template=self.TEMPLATE)
                self.assertEqual(len(errors), 1, errors)
                self.assertIn("beforeかbefore_templateのどちらか1つを書いてください", errors[0])

    def test_before_template_needs_the_wizard_template(self):
        """before_template は、ひな形の場所（wizard_template）と、単元の package が要る。"""
        diff = {"html": self.HTML, "ids": ["diff-gradle"], "before_template": "app/build.gradle.kts", "after": "after.kts"}
        self.assertEqual(self._config_errors(diff, template=self.TEMPLATE), [])
        errors = self._config_errors(diff)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("設定にwizard_templateを書いてください", errors[0])
        errors = self._config_errors(diff, template={"root": "Panda2KotlinEmptyViewsActivity"})
        self.assertEqual(len(errors), 2, errors)
        self.assertIn("wizard_templateにnameがありません", errors[0])
        self.assertIn("wizard_templateにpackageがありません", errors[1])
        # 純Kotlin系の単元には package（文字列）がないので、ひな形の名前を置き換えられない。
        kotlin = self._project(diffs=[diff])
        del kotlin["package"]
        errors = CHECKER.check_config({"scan_roots": [], "terms": [], "wizard_template": self.TEMPLATE,
                                       "projects": [kotlin]})
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("before_templateは、packageを持つ単元（android）でだけ使えます", errors[0])

    # ------------------------------------------------------------------
    # 差分ブロックを作る（--print-diff）
    # ------------------------------------------------------------------

    def test_generated_block_passes_the_check(self):
        """--print-diff が作った枠は、そのまま検査を通る。"""
        before, after = CHECKER.code_lines(self.BEFORE), CHECKER.code_lines(self.AFTER)
        hunks = CHECKER.diff_hunks_between(before, after, 1)
        block = CHECKER.render_diff_block(hunks, "diff-gradle")
        self.assertIn('<pre id="diff-gradle" class="diff" tabindex="0"><code>', block)
        self.assertIn("<ins>    alias(libs.plugins.kotlinxSerialization)\n</ins>", block)
        self.assertEqual(self._errors(block), [])

    def test_generated_block_gets_enough_lines_to_fix_the_place(self):
        """前後1行だけでは場所が決まらないまとまりには、決まるまで行を足す。"""
        before = ["fun a() {", "    run()", "}", "", "fun b() {", "    run()", "}"]
        after = ["fun a() {", "    run()", "}", "", "fun b() {", "    run()", "    stop()", "}"]
        hunks = CHECKER.diff_hunks_between(before, after, 1)
        # 「    run()」と「}」だけでは a と b のどちらか決まらないので、「fun b() {」まで含める。
        self.assertEqual(hunks, [[(" ", "fun b() {"), (" ", "    run()"), ("+", "    stop()"), (" ", "}")]])
        self.assertEqual(CHECKER.apply_diff_hunks(before, hunks), after)

    def test_generated_hunks_close_to_each_other_are_joined(self):
        """あいだが数行しかないまとまりは、⋮ で省かずに1つにつなげる。"""
        before = [f"line {number}" for number in range(1, 21)]
        near = before[:3] + ["added A"] + before[3:8] + ["added B"] + before[8:]
        self.assertEqual(len(CHECKER.diff_hunks_between(before, near, 1)), 1)
        far = before[:3] + ["added A"] + before[3:15] + ["added B"] + before[15:]
        hunks = CHECKER.diff_hunks_between(before, far, 1)
        self.assertEqual(len(hunks), 2)
        self.assertEqual(CHECKER.render_diff_block(hunks, "x").count(self.GAP), 1)

    def test_head_lists_only_the_kinds_in_the_block(self):
        """見出しの凡例には、その枠に出てくる行の種類だけを並べる。"""
        added = [[(" ", "a"), ("+", "b")]]
        head = CHECKER.render_diff_head("app/build.gradle.kts", added)
        self.assertIn("<span>app/build.gradle.kts</span>", head)
        self.assertIn('<span class="diff-add">足す行</span><span class="diff-keep">すでにある行</span>', head)
        self.assertNotIn("消す行", head)
        self.assertIn('<span class="diff-del">消す行</span>',
                      CHECKER.render_diff_head("x", [[(" ", "a"), ("-", "b"), ("+", "c")]]))

    def test_print_diff_uses_the_registered_files(self):
        """登録した1件の、直す前後のファイルから枠を作って表示する。登録がなければ知らせる。"""
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            self._write(root, "before.kts", self.BEFORE)
            self._write(root, "after.kts", self.AFTER)
            self._write(root, "config/teaching-materials.json", json.dumps(
                {"scan_roots": [], "terms": [], "projects": [self._project()]}, ensure_ascii=False))
            output, problems = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(problems):
                self.assertEqual(CHECKER.print_diff(root, self.HTML, "diff-gradle", 3), 0)
                self.assertEqual(CHECKER.print_diff(root, self.HTML, "diff-typo", 3), 1)
            self.assertIn('<div class="code-head diff-head"><span>after.kts</span>', output.getvalue())
            self.assertIn('<pre id="diff-gradle" class="diff" tabindex="0"><code>plugins {\n', output.getvalue())
            self.assertIn("diffsに登録がありません: docs/x/index.html の diff-typo", problems.getvalue())

    def test_validate_runs_the_checks(self):
        """validate() の流れから、当てた結果の検査と登録もれの検査の両方が呼ばれる。"""
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            self._write(root, "before.kts", self.BEFORE)
            self._write(root, "after.kts", self.AFTER)
            self._write(root, self.HTML, self._block("diff-gradle", self.PLUGINS) + self._block("diff-other", self.DEPENDENCIES))
            self._write(root, "config/teaching-materials.json", json.dumps(
                {"scan_roots": [], "terms": [], "projects": [self._project()]}, ensure_ascii=False))
            errors = CHECKER.validate(root)
            self.assertTrue(any("diff-gradleをbefore.ktsに当てても、after.ktsと一致しません" in error
                                for error in errors), errors)
            self.assertTrue(any("diffsにありません: diff-other" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
