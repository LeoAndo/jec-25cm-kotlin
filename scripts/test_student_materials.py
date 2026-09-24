"""配布物の境界、リンク切れ、GitHub公開の失敗・再実行を検証する。"""

import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
from shutil import copy2
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile


SCRIPTS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("release", SCRIPTS / "release-student-materials.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)
spec = importlib.util.spec_from_file_location("packager", SCRIPTS / "package-student-materials.py")
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)

# JSTでは翌日になる時刻。配布物の名前が版タグと同じJSTの日付になることを確かめる。
FIXTURE_COMMITTED = "2026-09-19T15:30:00+00:00"
FIXTURE_STEM = "kotlin-student-materials-2026-09-20"

# 仮のリポジトリに置く「教材整合性チェック」。終了コードだけを決められるようにしている。
# 本物の scripts/check-teaching-materials.py の中身は scripts/test_check_teaching_materials.py が
# 受け持つ。ここで確かめたいのは「配布物を作る前に必ず検査を実行し、落ちたらZIPを作らない」ことだけで、
# 配布物のテストはリンク切れなど、整合性チェックも嫌がる壊れ方をわざと作るため、本物は使わない。
INTEGRITY_CHECK = '''"""テスト用：教材整合性チェックの代わり。"""

import sys

print("教材整合性チェック: テスト用", file=sys.stderr)
raise SystemExit({status})
'''

# 単元の一覧は config/teaching-materials.json から読む。K01とK02は同じ K01HelloKotlin を指すので、
# 完成プロジェクトZIPを作る組は「K01HelloKotlin」と「A01HelloAndroid」の2つになる。
FIXTURE_PROJECTS = [
    {
        "name": "K01HelloKotlin",
        "kind": "kotlin-console",
        "root": "K01HelloKotlin",
        "packages": ["ex01"],
        "sessions": 1,
        "docs": ["docs/hello-kotlin/index.html", "teacher/hello-kotlin/index.html"],
        "sources": ["K01HelloKotlin/src/ex01/main.kt"],
        "snippets": [],
        "archive": "docs/hello-kotlin/downloads/K01HelloKotlin.zip",
    },
    {
        "name": "K02NullSafety",
        "kind": "kotlin-console",
        "root": "K01HelloKotlin",
        "packages": ["ex02"],
        "sessions": 1,
        "docs": ["docs/null-safety/index.html", "teacher/null-safety/index.html"],
        "sources": ["K01HelloKotlin/src/ex02/main.kt"],
        "snippets": [],
        "archive": "docs/hello-kotlin/downloads/K01HelloKotlin.zip",
    },
    {
        "name": "A01HelloAndroid",
        "kind": "android",
        "root": "A01HelloAndroid",
        "package": "jp.ac.jec.a01helloandroid",
        "sessions": 2,
        "docs": ["docs/hello-android/index.html", "teacher/hello-android/index.html"],
        "sources": ["A01HelloAndroid/MainActivity.kt"],
        "snippets": [],
        "archive": "docs/hello-android/downloads/A01HelloAndroid.zip",
    },
]


def page(title, body):
    """仮の教科書。翻訳したHTMLは<body>の中に導線を差し込むので、断片ではなく1枚の文書にする。"""
    return ('<!doctype html><html lang="ja"><head><meta charset="utf-8">'
            f'<title>{title}</title></head><body><main>{body}</main></body></html>')


class PackageStudentMaterialsTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "scripts").mkdir()
        for script in ("package-project.py", "package-student-materials.py", "localize-student-materials.py"):
            copy2(SCRIPTS / script, self.root / "scripts" / script)
        self.set_integrity_check(0)
        (self.root / "config").mkdir()
        config = json.loads((SCRIPTS.parent / "config/i18n.json").read_text(encoding="utf-8"))
        for language in config["languages"]:
            language["distribute"] = False
        (self.root / "config/i18n.json").write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
        self.set_projects(FIXTURE_PROJECTS)
        for name, text in {
            "docs/common/setup.html": page("はじめの準備", '<a href="../hello-kotlin/index.html">第1単元へ</a>'),
            "docs/hello-kotlin/index.html": page("K01 HelloKotlin",
                                                 '<a href="downloads/K01HelloKotlin.zip">完成プロジェクト</a>'
                                                 '<a href="../common/setup.html">はじめの準備</a>'),
            "docs/hello-kotlin/downloads/K01HelloKotlin.zip": "stale ZIP",
            "docs/null-safety/index.html": page("K02 NullSafety",
                                                    '<a href="../hello-kotlin/downloads/K01HelloKotlin.zip">完成プロジェクト</a>'),
            "docs/hello-android/index.html": page("A01 HelloAndroid",
                                                  '<a href="downloads/A01HelloAndroid.zip">完成プロジェクト</a>'),
            "docs/hello-android/downloads/A01HelloAndroid.zip": "stale ZIP",
            "docs/.DS_Store": "finder settings",
            "teacher/hello-kotlin/index.html": "teacher only",
            "K01HelloKotlin/src/ex01/main.kt": "package ex01\n\nfun main() {\n}\n",
            "K01HelloKotlin/src/ex02/main.kt": "package ex02\n\nfun main() {\n}\n",
            "K01HelloKotlin/.idea/misc.xml": "IDE settings",
            "K01HelloKotlin/out/production/K01HelloKotlin/ex01/MainKt.class": "build output",
            "A01HelloAndroid/MainActivity.kt": "original source",
            "A01HelloAndroid/gradlew": "#!/bin/sh",
            "A01HelloAndroid/.idea/misc.xml": "IDE settings",
            "A01HelloAndroid/local.properties": "local SDK",
        }.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        (self.root / "A01HelloAndroid/gradlew").chmod(0o755)
        self.git("init")
        self.git("add", "-f", ".")
        self.git(
            "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "fixture",
            env={"GIT_AUTHOR_DATE": FIXTURE_COMMITTED, "GIT_COMMITTER_DATE": FIXTURE_COMMITTED},
        )
        self.revision = self.git("rev-parse", "HEAD").stdout.decode().strip()
        self.stem = f"{FIXTURE_STEM}-{self.revision[:12]}"
        self.archive = self.root / f"dist/{self.stem}.zip"

    def set_integrity_check(self, status):
        """教材整合性チェックの代わりを、指定の終了コードで置き直す。"""
        (self.root / "scripts/check-teaching-materials.py").write_text(
            INTEGRITY_CHECK.format(status=status), encoding="utf-8")

    def set_projects(self, projects):
        (self.root / "config/teaching-materials.json").write_text(
            json.dumps({"course": {"name": "Kotlin演習", "total_sessions": 15, "minutes_per_session": 90},
                        "scan_roots": [], "terms": [], "projects": projects}, ensure_ascii=False),
            encoding="utf-8",
        )

    def git(self, *args, env=None):
        return subprocess.run(
            ["git", *args], cwd=self.root, check=True, capture_output=True,
            env={**os.environ, **env} if env else None,
        )

    def package(self):
        return subprocess.run([sys.executable, "scripts/package-student-materials.py"], cwd=self.root, capture_output=True, text=True)

    def enable_translation(self):
        path = self.root / "config/i18n.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        config["languages"][0]["distribute"] = True
        path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
        (self.root / "docs/assets").mkdir()
        for name in ("textbook.js", "textbook.css"):
            copy2(SCRIPTS.parent / "docs/assets" / name, self.root / "docs/assets" / name)
        source = ('<!doctype html><html lang="ja"><head><title>はじめの準備</title>'
                  '<link rel="stylesheet" href="../assets/textbook.css">'
                  '<script src="../assets/textbook.js" defer></script></head>'
                  '<body data-progress-key="jec-test-v1"><main><section id="step1"><h1>日本語の見出し</h1>'
                  '<p>訳した文</p><p>未翻訳の文<strong>も残す</strong></p>'
                  '<a href="downloads/K01HelloKotlin.zip">完成プロジェクト</a>'
                  '<input type="checkbox" data-check="step1"><pre><code>日本語のコード</code></pre>'
                  '</section></main></body></html>')
        (self.root / "docs/hello-kotlin/index.html").write_text(source, encoding="utf-8")
        catalog = self.root / "i18n/en/hello-kotlin/index.json"
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps({"source": "docs/hello-kotlin/index.html", "language": "en",
                                      "entries": [{"source": "訳した文", "translation": "Translated sentence"}]}, ensure_ascii=False),
                           encoding="utf-8")
        self.git("add", "docs/assets", "docs/hello-kotlin/index.html", "i18n/en/hello-kotlin/index.json", "config/i18n.json")

    def test_asset_stem_is_kotlin_student_materials(self):
        """配布ZIPの名前は授業ごとに決まっている。リリース側の検査と組で守る。"""
        self.assertEqual(packager.ASSET_STEM, "kotlin-student-materials")
        self.assertEqual(self.package().returncode, 0)
        self.assertTrue(self.archive.exists(), self.archive)

    def test_shared_project_is_packaged_once(self):
        """同じ完成プロジェクトを指す単元が複数あっても、ZIPは1回だけ作る。

        純Kotlin系は K01・K02… が同じ K01HelloKotlin を指すので、重複を除かないと
        同じZIPを何度も作り直すことになる。
        """
        calls = []
        run = subprocess.run

        def record(command, *args, **kwargs):
            calls.append([str(part) for part in command])
            return run(command, *args, **kwargs)

        with patch.object(packager, "ROOT", self.root.resolve()), patch.object(packager.subprocess, "run", record):
            packager.build(self.root / "dist")
        packaged = [call for call in calls if any("package-project.py" in part for part in call)]
        self.assertEqual([call[call.index("--project") + 1] for call in packaged],
                         ["K01HelloKotlin", "A01HelloAndroid"])

    def test_instructions_list_every_registered_unit(self):
        """はじめに.txt の単元一覧は config/teaching-materials.json から作る。"""
        self.assertEqual(self.package().returncode, 0)
        with ZipFile(self.archive) as archive:
            instructions = archive.read(f"{self.stem}/はじめに.txt").decode()
        self.assertIn("Kotlin演習 学生用教材", instructions)
        self.assertIn("  K01 HelloKotlin：docs/hello-kotlin/index.html", instructions)
        self.assertIn("  K02 NullSafety：docs/null-safety/index.html", instructions)
        self.assertIn("  A01 HelloAndroid：docs/hello-android/index.html", instructions)
        self.assertIn("IntelliJ IDEA", instructions)
        self.assertIn("Android Studio", instructions)

    def test_added_unit_appears_without_touching_the_script(self):
        """単元を設定に足すだけで、配布物の案内にも見本にも反映される。"""
        added = dict(FIXTURE_PROJECTS[0], name="K03Functions",
                     docs=["docs/functions/index.html", "teacher/functions/index.html"])
        self.set_projects([*FIXTURE_PROJECTS, added])
        textbook = self.root / "docs/functions/index.html"
        textbook.parent.mkdir(parents=True)
        textbook.write_text(page("K03 Functions",
                                 '<a href="../hello-kotlin/downloads/K01HelloKotlin.zip">完成プロジェクト</a>'),
                            encoding="utf-8")
        self.git("add", "config/teaching-materials.json", "docs/functions/index.html")
        self.assertEqual(self.package().returncode, 0)
        with ZipFile(self.archive) as archive:
            instructions = archive.read(f"{self.stem}/はじめに.txt").decode()
        self.assertIn("  K03 Functions：docs/functions/index.html", instructions)

    def test_missing_project_archive_rejects_package(self):
        """教科書を配るのに完成プロジェクトZIPがない単元を見つける。"""
        self.git("rm", "--cached", "docs/hello-android/downloads/A01HelloAndroid.zip")
        result = self.package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("HelloAndroidの完成プロジェクトが見つかりません", result.stderr)
        self.assertFalse(self.archive.exists())

    def test_integrity_check_failure_stops_packaging(self):
        """教材整合性チェックが落ちたら、配布物を書き出さない。"""
        self.set_integrity_check(1)
        result = self.package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("教材のパッケージ化に失敗しました", result.stderr)
        self.assertFalse(self.archive.exists())

    def test_distributed_language_has_static_navigation_and_shared_assets(self):
        self.enable_translation()
        result = self.package()
        self.assertEqual(result.returncode, 0, result.stderr)
        prefix = f"{self.stem}/"
        with ZipFile(self.archive) as archive:
            names = archive.namelist()
            english = archive.read(prefix + "docs/en/hello-kotlin/index.html").decode()
            japanese = archive.read(prefix + "docs/hello-kotlin/index.html").decode()
            entrance = archive.read(prefix + "index.html").decode()
            instructions = archive.read(prefix + "はじめに.txt").decode()
            self.assertIn('href="../../hello-kotlin/index.html"', english)
            self.assertIn('href="../en/hello-kotlin/index.html"', japanese)
            self.assertIn('data-language-link', english)
            self.assertIn('hreflang="ja"', english)
            self.assertIn('translated by AI', english)
            self.assertIn('Japanese version is authoritative', english)
            self.assertIn('ask your teacher', english)
            self.assertIn('data-progress-key="jec-test-v1"', english)
            self.assertIn('"progress": "{count} / {total} steps checked"', english)
            self.assertIn('<p>Translated sentence</p>', english)
            self.assertIn('<span lang="ja">未翻訳の文<strong>も残す</strong></span>', english)
            self.assertIn('<title lang="ja">はじめの準備</title>', english)
            self.assertIn('<pre><code>日本語のコード</code></pre>', english)
            self.assertIn('href="../../hello-kotlin/downloads/K01HelloKotlin.zip"', english)
            self.assertIn('src="../../assets/textbook.js"', english)
            # 入口は共通資料。言語を選んだ先が「はじめの準備」になる。
            self.assertIn('href="docs/en/common/setup.html"', entrance)
            self.assertIn('Kotlin演習 / Kotlin Programming Exercises', entrance)
            self.assertIn('Open index.html in your browser, then choose English.', instructions)
            self.assertFalse(any('/docs/en/' in name and not name.endswith('.html') for name in names))
            self.assertFalse(any('/docs/ko/' in name for name in names))

    def test_all_supported_languages_have_their_own_ui_and_shared_pages(self):
        self.enable_translation()
        path = self.root / "config/i18n.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        for language in config["languages"]:
            language["distribute"] = True
        path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
        result = self.package()
        self.assertEqual(result.returncode, 0, result.stderr)
        prefix = f"{self.stem}/"
        with ZipFile(self.archive) as archive:
            for language in config["languages"]:
                page = archive.read(prefix + f"docs/{language['code']}/hello-kotlin/index.html").decode()
                # 右から左の言語だけ、ページ全体と、日本語のまま残す部分に向きを付ける。
                rtl = language.get("dir") == "rtl"
                page_dir, japanese_dir = (' dir="rtl"', ' dir="ltr"') if rtl else ("", "")
                self.assertIn(f'<html lang="{language["code"]}"{page_dir}>', page)
                # 注記、UIと全言語の導線はカタログの有無に左右されない。
                self.assertIn(language['translation_notice'], page)
                self.assertIn(language['ui']['copy'], page)
                self.assertEqual(page.count('hreflang='), len(config['languages']) + 1)
                self.assertIn(f'<span lang="ja"{japanese_dir}>未翻訳の文', page)
                # 言語の切り替えでは、どのページでも、言語名をその言語の向きで出す。
                nav = page.split('<nav class="language-nav"', 1)[1].split("</nav>", 1)[0]
                for choice in config["languages"]:
                    direction = choice.get("dir", "ltr")
                    self.assertIn(f'lang="{choice["code"]}" dir="{direction}"', nav)
                self.assertIn('lang="ja" dir="ltr"', nav)
            entrance = archive.read(prefix + "index.html").decode()
            self.assertIn('<li lang="ja" dir="ltr">', entrance)
            for language in config["languages"]:
                self.assertIn(f'<li lang="{language["code"]}" dir="{language.get("dir", "ltr")}">', entrance)
        # アラビア語は右から左の言語として設定してある（この検査で右から左の出力を必ず通すため）。
        self.assertIn("rtl", [language.get("dir") for language in config["languages"]])

    def test_translation_does_not_include_untracked_pages(self):
        self.enable_translation()
        (self.root / 'docs/draft.html').write_text('<p>書きかけ', encoding="utf-8")
        result = self.package()
        self.assertEqual(result.returncode, 0, result.stderr)
        with ZipFile(self.archive) as archive:
            self.assertFalse(any('draft.html' in name for name in archive.namelist()))

    def test_localized_links_are_checked(self):
        self.enable_translation()
        generate = packager.add_localized_materials

        def with_broken_link(files):
            languages = generate(files)
            files["docs/en/hello-kotlin/index.html"] += b'<a href="missing.html">broken</a>'
            return languages

        # 日本語にはない壊れたリンクが生成されたときも、ZIPを書き出してはいけない。
        with patch.object(packager, "ROOT", self.root.resolve()), patch.object(packager, "add_localized_materials", with_broken_link):
            with self.assertRaisesRegex(ValueError, 'docs/en/hello-kotlin/index.html → missing.html'):
                packager.build(self.root / "dist")
        self.assertFalse(self.archive.exists())

    def test_no_distributed_language_preserves_original_html_and_entrypoints(self):
        original = (self.root / "docs/hello-kotlin/index.html").read_bytes()
        result = self.package()
        self.assertEqual(result.returncode, 0, result.stderr)
        prefix = f"{self.stem}/"
        with ZipFile(self.archive) as archive:
            self.assertNotIn(prefix + 'index.html', archive.namelist())
            self.assertEqual(archive.read(prefix + 'docs/hello-kotlin/index.html'), original)
            self.assertNotIn(b'Language /', archive.read(prefix + 'はじめに.txt'))
            self.assertFalse(any('/docs/en/' in name for name in archive.namelist()))

    def test_student_contents_regeneration_and_repeatable_zip(self):
        (self.root / "docs/untracked.txt").write_text("not for distribution", encoding="utf-8")
        (self.root / "K01HelloKotlin/src/ex01/main.kt").write_text("package ex01\n\nfun main() {\n    println(1)\n}\n", encoding="utf-8")
        result = self.package()
        self.assertEqual(result.returncode, 0, result.stderr)
        prefix = f"{self.stem}/"
        with ZipFile(self.archive) as archive:
            names = archive.namelist()
            self.assertFalse(any("teacher" in name or ".DS_Store" in name or "untracked" in name for name in names))
            self.assertIn(prefix + "はじめに.txt", names)
            self.assertIn(prefix + "VERSION.json", names)
            data = archive.read(prefix + "docs/hello-kotlin/downloads/K01HelloKotlin.zip")
            with ZipFile(io.BytesIO(data)) as project:
                self.assertEqual(project.read("K01HelloKotlin/src/ex01/main.kt").decode(),
                                 "package ex01\n\nfun main() {\n    println(1)\n}\n")
                self.assertFalse(any(".idea" in name or "/out/" in name for name in project.namelist()))
            data = archive.read(prefix + "docs/hello-android/downloads/A01HelloAndroid.zip")
            with ZipFile(io.BytesIO(data)) as project:
                self.assertFalse(any(".idea" in name or "local.properties" in name for name in project.namelist()))
                self.assertEqual(project.getinfo("A01HelloAndroid/gradlew").external_attr >> 16, 0o100755)
        first = self.archive.read_bytes()
        self.assertEqual(self.package().returncode, 0)
        self.assertEqual(self.archive.read_bytes(), first)
        checksum = (self.root / "dist/SHA256SUMS.txt").read_text(encoding="utf-8")
        self.assertEqual(checksum.split()[0], hashlib.sha256(first).hexdigest())

    def test_extracted_samples_match_the_project_zip(self):
        self.assertEqual(self.package().returncode, 0)
        prefix = f"{self.stem}/"
        bundled_total = 0
        with ZipFile(self.archive) as archive:
            for archive_name in ("docs/hello-kotlin/downloads/K01HelloKotlin.zip",
                                 "docs/hello-android/downloads/A01HelloAndroid.zip"):
                data = archive.read(prefix + archive_name)
                with ZipFile(io.BytesIO(data)) as project:
                    # 展開済みの見本は、教科書からリンクしているZIPと同じ中身。
                    # 学生はIntelliJ IDEAかAndroid StudioのOpenで選ぶだけで開ける。
                    for item in project.infolist():
                        sample = archive.getinfo(prefix + "samples/" + item.filename)
                        self.assertEqual(archive.read(sample), project.read(item))
                        self.assertEqual(sample.external_attr >> 16, item.external_attr >> 16)
                    bundled_total += len(project.namelist())
            bundled = [name for name in archive.namelist() if name.startswith(prefix + "samples/")]
            self.assertEqual(len(bundled), bundled_total)
            # 配布物の書き出しは権限を644にそろえるが、gradlew の実行権限だけは引き継ぐ。
            self.assertEqual(archive.getinfo(prefix + "samples/A01HelloAndroid/gradlew").external_attr >> 16, 0o100755)
            self.assertEqual(archive.getinfo(prefix + "samples/K01HelloKotlin/src/ex01/main.kt").external_attr >> 16, 0o100644)

    def test_asset_name_and_folder_carry_the_release_date_and_revision(self):
        self.assertEqual(self.package().returncode, 0)
        with ZipFile(self.archive) as archive:
            names = archive.namelist()
        # 同日の別版も混ざらないよう、先頭フォルダにも日付とコミットIDを入れる。
        self.assertTrue(all(name.startswith(f"{self.stem}/") for name in names), names)
        checksum = (self.root / "dist/SHA256SUMS.txt").read_text(encoding="utf-8")
        self.assertEqual(checksum.split()[1], self.archive.name)
        metadata = json.loads((self.root / "dist/release-metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["asset"], self.archive.name)
        # 版タグの日付と、配布物の名前の日付がそろっている。
        self.assertEqual(metadata["version"], f"materials-2026.09.20-{self.revision[:12]}")
        self.assertEqual(metadata["revision"], self.revision)
        self.assertTrue(self.archive.name.endswith(f"-{self.revision[:12]}.zip"))

    def test_two_commits_on_the_same_day_have_separate_archives_and_folders(self):
        self.assertEqual(self.package().returncode, 0)
        first_bytes = self.archive.read_bytes()
        source = self.root / "K01HelloKotlin/src/ex01/main.kt"
        source.write_text("package ex01\n\nfun main() {\n    println(2)\n}\n", encoding="utf-8")
        self.git("add", "K01HelloKotlin/src/ex01/main.kt")
        self.git(
            "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "same-day revision",
            env={"GIT_AUTHOR_DATE": FIXTURE_COMMITTED, "GIT_COMMITTER_DATE": FIXTURE_COMMITTED},
        )
        second_revision = self.git("rev-parse", "HEAD").stdout.decode().strip()
        self.assertEqual(self.package().returncode, 0)
        metadata = json.loads((self.root / "dist/release-metadata.json").read_text(encoding="utf-8"))
        second_archive = self.root / "dist" / metadata["asset"]
        self.assertNotEqual(second_archive, self.archive)
        self.assertEqual(self.archive.read_bytes(), first_bytes)
        self.assertEqual(metadata["revision"], second_revision)
        self.assertEqual(second_archive.stem, f"{FIXTURE_STEM}-{second_revision[:12]}")
        with ZipFile(self.archive) as first, ZipFile(second_archive) as second:
            first_folders = {name.split("/", 1)[0] for name in first.namelist()}
            second_folders = {name.split("/", 1)[0] for name in second.namelist()}
            self.assertEqual(first_folders, {self.archive.stem})
            self.assertEqual(second_folders, {second_archive.stem})
            self.assertTrue(first_folders.isdisjoint(second_folders))
            copied = second.read(f"{second_archive.stem}/samples/K01HelloKotlin/src/ex01/main.kt")
            self.assertEqual(copied, source.read_bytes())

    def test_missing_link_rejects_package(self):
        (self.root / "docs/hello-kotlin/index.html").write_text('<a href="../missing.html">資料</a>', encoding="utf-8")
        result = self.package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("リンク先がありません", result.stderr)
        self.assertFalse(self.archive.exists())

    def test_link_to_teacher_rejects_package(self):
        (self.root / "docs/hello-kotlin/index.html").write_text('<a href="../../teacher/hello-kotlin/index.html">教員用</a>', encoding="utf-8")
        self.assertNotEqual(self.package().returncode, 0)

    def test_symlink_rejects_package(self):
        (self.root / "docs/private.txt").symlink_to(self.root / "teacher/hello-kotlin/index.html")
        self.git("add", "docs/private.txt")
        result = self.package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("シンボリックリンク", result.stderr)


class StudentReleaseTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.dist = Path(temporary.name)
        self.repo = "owner/repo"
        self.asset = "kotlin-student-materials-2026-09-15-123456789abc.zip"
        self.metadata = {"version": "materials-2026.09.15-123456789abc", "revision": "123456789abc" * 3 + "1234", "asset": self.asset}
        (self.dist / self.asset).write_bytes(b"student package")
        (self.dist / release.CHECKSUMS).write_text(f"{hashlib.sha256(b'student package').hexdigest()}  {self.asset}\n")
        (self.dist / "release-notes.md").write_text("学生向けノート", encoding="utf-8")
        # リリースノートの単元一覧も設定から作る。ほかの単元の作業と混ざらないよう、仮の設定を使う。
        self.source = self.dist / "source"
        (self.source / "config").mkdir(parents=True)
        (self.source / "config/teaching-materials.json").write_text(
            json.dumps({"projects": FIXTURE_PROJECTS}, ensure_ascii=False), encoding="utf-8")
        self.enterContext(patch.object(release, "ROOT", self.source))
        self.enterContext(patch.object(release, "DIST", self.dist))
        self.enterContext(patch.dict(os.environ, {"GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_REF": "refs/heads/main", "STUDENT_NOTES": "STEP 4の説明修正。やり直し不要。", "ALLOW_UNTRANSLATED": "false"}))
        self.summary = self.enterContext(patch.object(release, "summary"))
        self.translations = self.enterContext(patch.object(release, "translation_report", return_value=[]))
        self.gh = self.enterContext(patch.object(release, "gh", return_value=""))
        self.items = self.enterContext(patch.object(release, "releases", return_value=[]))
        self.api = self.enterContext(patch.object(release, "api", side_effect=self.api_response))

    def api_response(self, path, payload=None):
        if path.endswith("/commits/main"):
            return {"sha": self.metadata["revision"]}
        if "/git/matching-refs/" in path:
            return []
        if path.endswith("/generate-notes"):
            return {"body": "* K01HelloKotlinの説明を修正 #2"}
        raise AssertionError(f"Unexpected API: {path}")

    def incomplete_report(self):
        return [{"language": {"code": "en", "name": "English", "distribute": True}, "rows": [
            {"page": "docs/hello-kotlin/index.html", "total": 4, "translated": 1},
            {"page": "docs/common/setup.html", "total": 2, "translated": 1},
        ]}]

    def test_asset_pattern_matches_this_course_only(self):
        """配布ZIPの名前が、この授業のものであることを確かめる。"""
        self.assertTrue(release.ASSET_PATTERN.fullmatch(self.asset))
        self.assertTrue(release.ASSET_PATTERN.fullmatch("kotlin-student-materials-2026-09-15.zip"))
        for name in (
            "android1-student-materials-2026-09-15-123456789abc.zip",
            "kotlin-student-materials-2026-09-15-not-a-commit.zip",
            "kotlin-student-materials-2026-09-15-1234567.zip",
            "kotlin-student-materials-2026-09-15-123456789abcd.zip",
            "kotlin-student-materials-2026-09-15-123456789abc.zip.exe",
            "../kotlin-student-materials-2026-09-15-123456789abc.zip",
        ):
            with self.subTest(name=name):
                self.assertFalse(release.ASSET_PATTERN.fullmatch(name))

    def test_main_accepts_the_new_asset_name_before_preparing(self):
        (self.dist / "release-metadata.json").write_text(json.dumps(self.metadata), encoding="utf-8")
        with patch.object(release.sys, "argv", ["release-student-materials.py", "prepare"]), \
                patch.dict(os.environ, {"GH_REPO": self.repo}), \
                patch.object(release.subprocess, "check_output", return_value=self.metadata["revision"]), \
                patch.object(release, "prepare") as prepare:
            release.main()
        prepare.assert_called_once_with(self.repo, self.metadata)

    def test_release_notes_list_units_from_the_configuration(self):
        """リリースノートの単元一覧は config/teaching-materials.json から作る。"""
        with patch.object(release.subprocess, "check_output", return_value="- 修正 (abc123)"):
            release.prepare(self.repo, self.metadata)
        text = (self.dist / "release-notes.md").read_text(encoding="utf-8")
        self.assertIn(f"# Kotlin演習 教材 {self.metadata['version']}", text)
        self.assertIn("- `K01 HelloKotlin：docs/hello-kotlin/index.html`", text)
        self.assertIn("- `K02 NullSafety：docs/null-safety/index.html`", text)
        self.assertIn("- `A01 HelloAndroid：docs/hello-android/index.html`", text)
        self.assertIn("`samples/K01HelloKotlin`", text)
        self.assertIn("IntelliJ IDEA", text)

    def test_download_guidance_covers_every_configured_language(self):
        """翻訳を配る言語を増やしたときに、公開案内の書き忘れを見つける。"""
        config = json.loads((SCRIPTS.parent / "config/i18n.json").read_text(encoding="utf-8"))
        self.assertEqual(sorted(release.DOWNLOAD_GUIDANCE),
                         sorted(language["code"] for language in config["languages"]))

    def test_untranslated_publish_stops_before_release_mutation(self):
        self.translations.return_value = self.incomplete_report()
        with self.assertRaisesRegex(ValueError, "未翻訳が4文"):
            release.publish(self.repo, self.metadata)
        self.gh.assert_not_called()
        report = self.summary.call_args.args[0]
        self.assertIn("en（English） | `docs/hello-kotlin/index.html` | 3", report)
        self.assertIn("en（English） | `docs/common/setup.html` | 1", report)

    def test_emergency_publish_records_actual_counts_without_duplicates(self):
        self.translations.return_value = self.incomplete_report()
        with patch.dict(os.environ, {"ALLOW_UNTRANSLATED": "true"}):
            release.publish(self.repo, self.metadata)
            release.publish(self.repo, self.metadata)
        notes = (self.dist / "release-notes.md").read_text(encoding="utf-8")
        self.assertIn("公開ゲートを解除", notes)
        self.assertIn("**4文**", notes)
        self.assertIn("`docs/hello-kotlin/index.html` | 3", notes)
        self.assertEqual(notes.count(release.EXCEPTION_MARKER), 1)
        self.assertIn("--draft=false", self.gh.call_args_list[-1].args)

    def test_emergency_flag_does_not_bypass_invalid_catalog(self):
        self.translations.side_effect = ValueError("対訳カタログの検査に失敗しました")
        with patch.dict(os.environ, {"ALLOW_UNTRANSLATED": "true"}):
            with self.assertRaisesRegex(ValueError, "対訳カタログ"):
                release.publish(self.repo, self.metadata)
        self.gh.assert_not_called()

    def test_false_override_still_rejects_untranslated_content(self):
        self.translations.return_value = self.incomplete_report()
        with patch.dict(os.environ, {"ALLOW_UNTRANSLATED": "false"}):
            with self.assertRaisesRegex(ValueError, "未翻訳"):
                release.publish(self.repo, self.metadata)
        self.gh.assert_not_called()

    def test_prepare_with_untranslated_content_keeps_preparation_available(self):
        self.translations.return_value = self.incomplete_report()
        with patch.object(release.subprocess, "check_output", return_value="- 修正 (abc123)"):
            release.prepare(self.repo, self.metadata)
        notes = (self.dist / "release-notes.md").read_text(encoding="utf-8")
        self.assertIn("### English", notes)
        self.assertIn("Open `index.html`", notes)
        self.assertNotIn(release.EXCEPTION_MARKER, notes)
        self.gh.assert_not_called()

    def test_prepare_emergency_notes_record_counts(self):
        self.translations.return_value = self.incomplete_report()
        with patch.dict(os.environ, {"ALLOW_UNTRANSLATED": "true"}), patch.object(release.subprocess, "check_output", return_value=""):
            release.prepare(self.repo, self.metadata)
        self.assertIn("**4文**", (self.dist / "release-notes.md").read_text(encoding="utf-8"))

    def test_right_to_left_guidance_is_wrapped_with_its_direction(self):
        """GitHubのMarkdownは段落に向きを付けないので、右から左の言語の案内だけを dir で囲む。"""
        report = [{"language": {"code": "ar", "name": "العربية", "dir": "rtl"}, "rows": []},
                  {"language": {"code": "en", "name": "English"}, "rows": []}]
        notes = release.localized_download_guidance(report, self.asset)
        arabic, english = notes.split("### English")
        self.assertTrue(arabic.startswith('<div dir="rtl">\n\n### العربية\n'), arabic)
        self.assertIn(self.asset, arabic)
        self.assertIn("</div>", arabic)
        self.assertNotIn("dir=", english)

    def test_each_distribution_language_has_native_opening_instructions(self):
        report = [{"language": {"code": code, "name": code}, "rows": []} for code in release.DOWNLOAD_GUIDANCE]
        notes = release.localized_download_guidance(report, self.asset)
        self.assertEqual(notes.count("`index.html`"), len(release.DOWNLOAD_GUIDANCE))
        self.assertEqual(notes.count(self.asset), len(release.DOWNLOAD_GUIDANCE))

    def test_first_publish_uploads_before_publication(self):
        release.publish(self.repo, self.metadata)
        commands = [call.args[:2] for call in self.gh.call_args_list]
        self.assertEqual(commands, [("release", "create"), ("release", "upload"), ("release", "edit")])
        self.assertIn("--draft", self.gh.call_args_list[0].args)
        self.assertIn(self.metadata["revision"], self.gh.call_args_list[0].args)
        self.assertIn(f"Kotlin演習 教材 {self.metadata['version']}", self.gh.call_args_list[0].args)
        # 添付するのは版の日付が入ったZIP。名前はrelease-metadata.jsonから受け取る。
        self.assertIn(str(self.dist / self.asset), self.gh.call_args_list[1].args)
        self.assertIn("--draft=false", self.gh.call_args_list[-1].args)

    def test_upload_failure_does_not_publish(self):
        def execute(*args, **kwargs):
            if args[:2] == ("release", "upload"):
                raise subprocess.CalledProcessError(1, "upload")
            return ""
        self.gh.side_effect = execute
        with self.assertRaises(subprocess.CalledProcessError):
            release.publish(self.repo, self.metadata)
        self.assertFalse(any("--draft=false" in call.args for call in self.gh.call_args_list))

    def test_existing_draft_resumes_without_creating_another(self):
        self.items.return_value = [{"tag_name": self.metadata["version"], "draft": True, "target_commitish": self.metadata["revision"]}]
        release.publish(self.repo, self.metadata)
        self.assertEqual([call.args[:2] for call in self.gh.call_args_list], [("release", "edit"), ("release", "upload"), ("release", "edit")])

    def test_published_release_is_not_overwritten(self):
        self.items.return_value = [{"tag_name": self.metadata["version"], "draft": False, "html_url": "https://github.com/owner/repo/releases/tag/materials-test"}]
        release.publish(self.repo, self.metadata)
        self.gh.assert_not_called()

    def test_main_changed_stops_before_mutation(self):
        self.api.side_effect = lambda *args: {"sha": "different revision"}
        with self.assertRaisesRegex(ValueError, "mainが更新"):
            release.publish(self.repo, self.metadata)
        self.gh.assert_not_called()

    def test_main_changed_during_upload_keeps_release_as_draft(self):
        def execute(*args, **kwargs):
            if args[:2] == ("release", "upload"):
                self.api.side_effect = lambda *args: {"sha": "updated during upload"}
            return ""
        self.gh.side_effect = execute
        with self.assertRaisesRegex(ValueError, "下書きの公開を中止"):
            release.publish(self.repo, self.metadata)
        self.assertEqual([call.args[:2] for call in self.gh.call_args_list], [("release", "create"), ("release", "upload")])

    def test_automatic_event_cannot_publish(self):
        with patch.dict(os.environ, {"GITHUB_EVENT_NAME": "push"}):
            with self.assertRaisesRegex(ValueError, "Run workflow"):
                release.publish(self.repo, self.metadata)
        self.gh.assert_not_called()

    def test_corrupt_package_cannot_publish(self):
        (self.dist / self.asset).write_bytes(b"corrupt package")
        with self.assertRaisesRegex(ValueError, "チェックサム"):
            release.publish(self.repo, self.metadata)
        self.gh.assert_not_called()

    def test_prepare_first_release_has_student_notes_and_direct_commits(self):
        with patch.object(release.subprocess, "check_output", return_value="- 直接修正 (abc123)"):
            release.prepare(self.repo, self.metadata)
        text = (self.dist / "release-notes.md").read_text(encoding="utf-8")
        self.assertIn(f"**{self.asset}**", text)
        self.assertIn("STEP 4の説明修正。やり直し不要。", text)
        self.assertIn("K01HelloKotlinの説明を修正 #2", text)
        self.assertIn("直接修正", text)
        payload = self.api.call_args.args[1]
        self.assertEqual(payload["target_commitish"], self.metadata["revision"])
        self.assertNotIn("previous_tag_name", payload)
        self.gh.assert_not_called()

    def test_previous_release_ignores_drafts_prereleases_and_other_products(self):
        def item(tag, date, **kwargs):
            return {"tag_name": tag, "published_at": date, "draft": False, "prerelease": False, **kwargs}
        previous = item("materials-previous", "2026-09-14",
                        assets=[{"name": "kotlin-student-materials-2026-09-14.zip"}])
        items = [previous, item("other-product", "2026-09-15"), item("materials-draft", None, draft=True), item("materials-preview", "2026-09-15", prerelease=True), item(self.metadata["version"], "2026-09-15")]
        self.assertEqual(release.previous_release(items, self.metadata["version"]), previous)

    def test_notes_compare_against_last_published_materials(self):
        self.items.return_value = [{"tag_name": "materials-previous", "published_at": "2026-09-14", "draft": False, "prerelease": False}]
        base = "a" * 40
        self.api.side_effect = [{"sha": base}, {"body": "前回からのPR一覧"}]
        with patch.object(release.subprocess, "run") as ancestry, patch.object(release.subprocess, "check_output", return_value="- 追加修正 (def456)") as log:
            release.prepare(self.repo, self.metadata)
        payload = self.api.call_args.args[1]
        self.assertEqual(payload["previous_tag_name"], "materials-previous")
        self.assertEqual(log.call_args.args[0][-1], f"{base}..{self.metadata['revision']}")
        self.assertEqual(ancestry.call_args.args[0], ["git", "merge-base", "--is-ancestor", base, self.metadata["revision"]])

    def test_conflicting_tag_stops_before_mutation(self):
        self.api.side_effect = [
            {"sha": self.metadata["revision"]},
            [{"ref": f"refs/tags/{self.metadata['version']}"}],
            {"sha": "different revision"},
        ]
        with self.assertRaisesRegex(ValueError, "タグが別のコミット"):
            release.publish(self.repo, self.metadata)
        self.gh.assert_not_called()


class TranslationReleaseGateTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for directory in ("scripts", "config", "docs", "i18n/en"):
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        copy2(SCRIPTS / "localize-student-materials.py", self.root / "scripts/localize-student-materials.py")
        self.config = {"source_language": "ja", "source_root": "docs", "catalog_root": "i18n", "languages": [
            {"code": "en", "name": "English", "distribute": True},
            {"code": "ko", "name": "한국어", "distribute": False},
        ]}
        (self.root / "config/i18n.json").write_text(json.dumps(self.config, ensure_ascii=False), encoding="utf-8")
        (self.root / "docs/index.html").write_text('<html lang="ja"><p>準備します。</p></html>', encoding="utf-8")
        self.enterContext(patch.object(release, "ROOT", self.root))
        self.enterContext(patch.dict(os.environ, {"ALLOW_UNTRANSLATED": "false"}))

    def test_report_uses_only_languages_included_in_distribution(self):
        report = release.translation_report()
        self.assertEqual([item["language"]["code"] for item in report], ["en"])
        self.assertEqual(release.missing_translations(report), 1)

    def test_translated_distribution_ignores_untranslated_disabled_language(self):
        (self.root / "i18n/en/index.json").write_text(json.dumps({
            "source": "docs/index.html", "language": "en",
            "entries": [{"source": "準備します。", "translation": "Get ready."}],
        }, ensure_ascii=False), encoding="utf-8")
        with patch.object(release, "summary"):
            self.assertEqual(release.missing_translations(release.check_translation_gate()), 0)

    def test_changed_japanese_source_returns_to_untranslated(self):
        (self.root / "i18n/en/index.json").write_text(json.dumps({
            "source": "docs/index.html", "language": "en",
            "entries": [{"source": "準備します。", "translation": "Get ready."}],
        }, ensure_ascii=False), encoding="utf-8")
        (self.root / "docs/index.html").write_text('<html lang="ja"><p>アプリを起動します。</p></html>', encoding="utf-8")
        with patch.object(release, "summary"):
            with self.assertRaisesRegex(ValueError, "未翻訳が1文"):
                release.check_translation_gate()

    def test_missing_counts_are_written_to_github_summary_by_page(self):
        target = self.root / "summary.md"
        with patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": str(target)}):
            with self.assertRaisesRegex(ValueError, "未翻訳が1文"):
                release.check_translation_gate()
        self.assertIn("en（English） | `docs/index.html` | 1", target.read_text(encoding="utf-8"))

    def test_emergency_override_does_not_skip_html_structure_check(self):
        (self.root / "docs/index.html").write_text('<html lang="ja"><p>準備します。</html>', encoding="utf-8")
        with patch.dict(os.environ, {"ALLOW_UNTRANSLATED": "true"}):
            with self.assertRaisesRegex(ValueError, "検査に失敗"):
                release.check_translation_gate()

    def test_emergency_override_does_not_skip_malformed_catalog(self):
        (self.root / "i18n/en/index.json").write_text('{broken', encoding="utf-8")
        with patch.dict(os.environ, {"ALLOW_UNTRANSLATED": "true"}):
            with self.assertRaisesRegex(ValueError, "検査に失敗"):
                release.check_translation_gate()


if __name__ == "__main__":
    unittest.main()
