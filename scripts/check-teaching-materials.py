"""教材・完成プロジェクト・配布物の整合性を検査する。"""

from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
import re
import subprocess
import sys
from zipfile import BadZipFile, ZipFile


CONFIG = Path("config/teaching-materials.json")
TEXT_SUFFIXES = {
    ".bat", ".css", ".gradle", ".html", ".java", ".js", ".json", ".kt", ".kts",
    ".md", ".properties", ".py", ".sh", ".toml", ".txt", ".xml", ".yml",
    ".yaml",
}
# out はIntelliJ IDEAのビルド出力。build はGradleのビルド出力。
IGNORED_PARTS = {".git", ".gradle", ".idea", ".kotlin", "__pycache__", "build", "dist", "out"}
IGNORED_ARCHIVE_PARTS = {".gradle", ".idea", ".kotlin", "build", "out"}
# 単元の種類。純Kotlin系はIntelliJ IDEAのコンソールアプリ、Android系はAndroid Studioのアプリ。
KINDS = ("android", "kotlin-console")
# 設定に無いまま検査へ進むと、日本語のエラーではなくPythonのトレースバックになるキー。
REQUIRED_CONFIG_KEYS = ("scan_roots", "terms", "projects")
REQUIRED_PROJECT_KEYS = ("name", "root", "docs", "snippets", "archive")
REQUIRED_MIRROR_KEYS = ("source", "copy")
REQUIRED_TARGET_KEYS = ("path", "requires")
# Kotlinのpackage宣言。Javaと違ってセミコロンが付かない。
PACKAGE_DECLARATION = re.compile(r"^package\s+([\w.]+)\s*$", re.MULTILINE)


def display(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def line_of(text: str, needle: str) -> int:
    position = text.find(needle)
    return text.count("\n", 0, position) + 1 if position >= 0 else 1


def positive_int(value) -> bool:
    """正の整数かどうか。JSONのtrue/falseはintの仲間なので、別に弾く。"""
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def text_files(root: Path, scan_roots: list[str]):
    seen = set()
    for item in scan_roots:
        path = root / item
        if not path.exists():
            continue
        candidates = [path] if path.is_file() else path.rglob("*")
        for candidate in candidates:
            if not candidate.is_file() or candidate.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if any(part in IGNORED_PARTS for part in candidate.relative_to(root).parts):
                continue
            key = candidate.resolve()
            if key not in seen:
                seen.add(key)
                yield candidate


def tracked_files(root: Path, project_root: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", project_root],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError("git ls-filesを実行できません。Git cloneしたリポジトリで実行してください。")
    return [name for name in result.stdout.decode().split("\0") if name]


def archive_sources(root: Path, project_root: str) -> set[str]:
    """完成プロジェクトZIPに入れるファイル。Git管理下で、IDE設定やビルド出力でないもの。"""
    return {
        name for name in tracked_files(root, project_root)
        if not any(part in IGNORED_ARCHIVE_PARTS for part in Path(name).parts)
        and Path(name).name != "local.properties"
    }


def add(errors: list[str], root: Path, path: Path | str, line: int, message: str) -> None:
    shown = path if isinstance(path, str) else display(root, path)
    errors.append(f"{shown}:{line}: {message}")


def check_config(config: dict) -> list[str]:
    """検査に必ず要る設定のキーがそろっているか確かめる。

    書き忘れたまま検査へ進むと、日本語のエラーではなくPythonのトレースバックが出て、
    設定のどこを直せばよいか分からなくなる。入口で日本語にして引き返すための検査。
    書かなくてよいキー（course・registration・project_layout・mirrors など）は求めない。
    """
    shown = CONFIG.as_posix()
    errors = [f"{shown}:1: 設定に{key}がありません"
              for key in REQUIRED_CONFIG_KEYS if key not in config]
    if errors:
        return errors  # 以降の検査は、この3つがそろっている前提で書いてある。
    registration = config.get("registration")
    if registration:
        if "targets" not in registration:
            errors.append(f"{shown}:1: registrationにtargetsがありません")
        else:
            for index, target in enumerate(registration["targets"]):
                for key in REQUIRED_TARGET_KEYS:
                    if key not in target:
                        errors.append(
                            f"{shown}:1: registration.targets[{index}]に{key}がありません")
    layout = config.get("project_layout")
    if layout and "gitignore_reference" not in layout:
        errors.append(f"{shown}:1: project_layoutにgitignore_referenceがありません")
    for index, project in enumerate(config["projects"]):
        label = f"projects[{index}]"
        if isinstance(project.get("name"), str) and project["name"]:
            label += f"（{project['name']}）"
        for key in REQUIRED_PROJECT_KEYS:
            if key not in project:
                errors.append(f"{shown}:1: {label}に{key}がありません")
        # docs は「学生向け・教員用」の順に2つ。あとで docs[1] まで読むので、ここで数も確かめる。
        docs = project.get("docs")
        if isinstance(docs, list) and len(docs) < 2:
            errors.append(f"{shown}:1: {label}のdocsには、"
                          f"学生向けの教科書と教員用ガイドを2つ書いてください: {docs!r}")
        for mirror_index, mirror in enumerate(project.get("mirrors", [])):
            for key in REQUIRED_MIRROR_KEYS:
                if key not in mirror:
                    errors.append(
                        f"{shown}:1: {label}のmirrors[{mirror_index}]に{key}がありません")
    return errors


def check_course(root: Path, config: dict, errors: list[str]) -> None:
    """授業のコマ数の整合を確かめる。

    単元を足していくうちに、決めた全コマ数を超えてしまう事故を捕まえる。
    合計が全コマ数に足りないのは、まだ単元にしていないだけなので許す。
    """
    course = config.get("course")
    if not course:
        return
    total = course.get("total_sessions")
    if not positive_int(total):
        add(errors, root, CONFIG.as_posix(), 1,
            f"course.total_sessionsは正の整数で書いてください: {total!r}")
        return
    used = 0
    for project in config["projects"]:
        sessions = project.get("sessions")
        if not positive_int(sessions):
            add(errors, root, CONFIG.as_posix(), 1,
                f"{project['name']}のsessionsは正の整数で書いてください: {sessions!r}")
            continue
        used += sessions
    if used > total:
        add(errors, root, CONFIG.as_posix(), 1,
            f"projectsのsessionsの合計が、course.total_sessionsの{total}コマを超えています: {used}コマ")
    # 授業の分量は、READMEを読んだ人に最初に伝わる。設定だけ直して書き換え忘れるのを捕まえる。
    readme_path = root / "README.md"
    if not readme_path.is_file():
        add(errors, root, "README.md", 1, "コマ数の表記を確かめるREADME.mdがありません")
        return
    readme = read(readme_path)
    needed = [f"全{total}コマ"]
    minutes = course.get("minutes_per_session")
    if not positive_int(minutes):
        add(errors, root, CONFIG.as_posix(), 1,
            f"course.minutes_per_sessionは正の整数で書いてください: {minutes!r}")
    else:
        needed.append(f"1コマ{minutes}分")
    for word in needed:
        if word not in readme:
            add(errors, root, "README.md", 1, f"READMEに授業の分量の表記がありません: {word}")


def check_terms(root: Path, config: dict, errors: list[str]) -> None:
    for item in config["scan_roots"]:
        if not (root / item).exists():
            add(errors, root, item, 1, "表記揺れ検査対象のパスがありません")
    files = list(text_files(root, config["scan_roots"]))
    contents = {path: read(path) for path in files}
    for term in config["terms"]:
        for path, content in contents.items():
            for line_number, line in enumerate(content.splitlines(), 1):
                for forbidden in term.get("forbidden", []):
                    if forbidden in line:
                        add(errors, root, path, line_number, f"{term['name']}は{term['canonical']}を使用してください（禁止表記: {forbidden}）")
        for required in term.get("required_in", []):
            path = root / required
            if not path.is_file():
                add(errors, root, required, 1, "正式表記を確認する対象ファイルがありません")
                continue
            content = read(path)
            if term["canonical"] not in content:
                add(errors, root, path, 1, f"{term['name']}の正式表記がありません: {term['canonical']}")


def value_from_gradle(text: str, key: str) -> str | None:
    match = re.search(rf'^\s*{re.escape(key)}\s*=\s*"([^"]+)"', text, re.MULTILINE)
    return match.group(1) if match else None


def package_declaration(path: Path) -> tuple[str | None, int]:
    """Kotlinソースのpackage宣言と、その行番号を返す。宣言がなければ (None, 1)。"""
    source = read(path)
    match = PACKAGE_DECLARATION.search(source)
    return (match.group(1) if match else None, line_of(source, "package"))


def android_package(root: Path, project: dict, errors: list[str]) -> str | None:
    """Android系のpackage（文字列）を読む。書き方が正しくなければ報告してNoneを返す。"""
    package = project.get("package")
    if package is None and "packages" in project:
        return None  # 書き分けの取り違えは check_project が報告済み。
    if not isinstance(package, str) or not package:
        add(errors, root, CONFIG.as_posix(), 1,
            f"{project['name']}のpackageは、パッケージ名を文字列で書いてください: {package!r}")
        return None
    return package


def kotlin_console_packages(root: Path, project: dict, errors: list[str]) -> list[str] | None:
    """純Kotlin系のpackages（配列）を読む。書き方が正しくなければ報告してNoneを返す。

    1コマで複数の演習（exNN）を扱う単元があるので、1件しかなくても配列で書く。
    """
    packages = project.get("packages")
    if packages is None and "package" in project:
        return None  # 書き分けの取り違えは check_project が報告済み。
    if not isinstance(packages, list) or not packages:
        add(errors, root, CONFIG.as_posix(), 1,
            f"{project['name']}のpackagesは、パッケージ名を1つ以上並べた配列で書いてください: {packages!r}")
        return None
    invalid = [item for item in packages if not isinstance(item, str) or not item]
    if invalid:
        add(errors, root, CONFIG.as_posix(), 1,
            f"{project['name']}のpackagesには、パッケージ名を文字列で書いてください: {invalid!r}")
        return None
    return packages


def check_android_sources(root: Path, project: dict, package: str, errors: list[str]) -> None:
    """Android系の完成コードのpackage宣言が、設定のpackageと同じか確かめる。"""
    for name in project["sources"]:
        path = root / name
        if not path.is_file():
            add(errors, root, path, 1, "完成コードのファイルがありません")
            continue
        actual, line = package_declaration(path)
        if actual != package:
            add(errors, root, path, line,
                f"Kotlinのpackage宣言が一致しません: {actual!r} != {package!r}")


def check_kotlin_console_sources(root: Path, project: dict, packages: list[str],
                                 errors: list[str]) -> None:
    """純Kotlin系の完成コードが、packagesのどれかに属し、その置き場所にあるか確かめる。

    Gradleを使わないIntelliJ IDEAのプロジェクトなので、package名とフォルダ名がそろって
    いないと、学生が実行ボタンを押したときに動かない。
    packagesに書いたのに完成コードを足し忘れる事故も、ここで捕まえる。
    """
    shown = "、".join(packages)
    declared: set[str] = set()
    for name in project["sources"]:
        path = root / name
        if not path.is_file():
            add(errors, root, path, 1, "完成コードのファイルがありません")
            continue
        actual, line = package_declaration(path)
        if actual is None:
            add(errors, root, path, line,
                f"Kotlinのpackage宣言がありません: "
                f"{project['name']}のpackages（{shown}）のどれかを宣言してください")
            continue
        if actual not in packages:
            add(errors, root, path, line,
                f"Kotlinのpackage宣言が、{project['name']}のpackagesにありません: "
                f"{actual!r}（packagesは{shown}）")
            continue
        declared.add(actual)
        expected = posixpath.join(project["root"], "src", actual.replace(".", "/"))
        if posixpath.dirname(name) != expected:
            add(errors, root, path, 1, f"完成コードの置き場所が{expected}/ではありません")
    for package in packages:
        if package not in declared:
            add(errors, root, CONFIG.as_posix(), 1,
                f"{project['name']}のpackagesに書いた{package}の完成コードが、sourcesにありません")


def check_sources(root: Path, project: dict, expected: str | list[str] | None,
                  errors: list[str]) -> None:
    """完成コードの検査の入口。sourcesが空でないことを確かめて、kindごとの検査へ渡す。

    expected は、Android系ならpackage（文字列）、純Kotlin系ならpackages（配列）。
    設定そのものが誤っているとき（None）は、報告済みなので中身までは見ない。
    """
    if not project.get("sources"):
        add(errors, root, CONFIG.as_posix(), 1,
            f"{project['name']}のsourcesに、完成コードのパスを1つ以上書いてください")
        return
    if expected is None:
        return
    if project["kind"] == "kotlin-console":
        check_kotlin_console_sources(root, project, expected, errors)
    else:
        check_android_sources(root, project, expected, errors)


def check_project(root: Path, project: dict, errors: list[str]) -> None:
    kind = project.get("kind")
    if kind not in KINDS:
        add(errors, root, CONFIG.as_posix(), 1,
            f"{project['name']}のkindが不正です: {kind!r}（{'か'.join(KINDS)}と書いてください）")
        return

    # パッケージの書き方は単元の種類で違う。純Kotlin系は1コマで複数の演習（exNN）を扱うので
    # packages（配列）、Android系はアプリのパッケージが1つだけなので package（文字列）。
    # 取り違えたまま素通りすると完成コードの検査が効かなくなるので、設定エラーとして報告する。
    if kind == "kotlin-console" and "package" in project:
        add(errors, root, CONFIG.as_posix(), 1,
            f"{project['name']}はkotlin-consoleなので、packageではなくpackagesに配列で書いてください")
    if kind == "android" and "packages" in project:
        add(errors, root, CONFIG.as_posix(), 1,
            f"{project['name']}はandroidなので、packagesではなくpackageに文字列で書いてください")

    if kind == "android":
        expected = android_package(root, project, errors)
        gradle_path = root / project["root"] / "app/build.gradle.kts"
        if not gradle_path.is_file():
            add(errors, root, gradle_path, 1, "app/build.gradle.ktsがありません")
            return
        gradle = read(gradle_path)
        if expected is not None:
            for key in ("namespace", "applicationId"):
                actual = value_from_gradle(gradle, key)
                if actual != expected:
                    add(errors, root, gradle_path, line_of(gradle, key),
                        f"{key}が一致しません: {actual!r} != {expected!r}")
        layout_name = project.get("layout")
        if layout_name and not (root / layout_name).is_file():
            add(errors, root, layout_name, 1, "レイアウトXMLがありません")
    else:
        expected = kotlin_console_packages(root, project, errors)
    check_sources(root, project, expected, errors)

    for doc_name in project["docs"]:
        path = root / doc_name
        if not path.is_file():
            add(errors, root, path, 1, "教材ファイルがありません")
            continue
        content = read(path)
        # 純Kotlin系のpackagesは ex01 のような短い語で、本文のどこかに偶然現れる。
        # 表記を確かめるのは単元名だけにする。
        required = [project["name"]]
        if kind == "android" and expected is not None:
            required.append(expected)
        for word in required:
            if word not in content:
                add(errors, root, path, 1, f"教材に必要な表記がありません: {word}")

    for snippet in project["snippets"]:
        html_path = root / snippet["html"]
        source_path = root / snippet["source"]
        if not html_path.is_file() or not source_path.is_file():
            continue
        document = read(html_path)
        match = re.search(rf'<pre\s+id="{re.escape(snippet["id"])}"[^>]*><code>(.*?)</code></pre>', document, re.DOTALL)
        if not match:
            add(errors, root, html_path, 1, f"コードスニペットがありません: {snippet['id']}")
            continue
        expected = read(source_path).rstrip()
        actual = html.unescape(match.group(1)).rstrip()
        if actual != expected:
            add(errors, root, html_path, line_of(document, f'id="{snippet["id"]}"'), f"{snippet['id']}と{snippet['source']}が一致しません")

    archive_path = root / project["archive"]
    if not archive_path.is_file():
        add(errors, root, archive_path, 1, "完成プロジェクトZIPがありません")
        return
    try:
        expected_names = archive_sources(root, project["root"])
        with ZipFile(archive_path) as archive:
            actual_names = set(archive.namelist())
            for name in sorted(expected_names - actual_names):
                add(errors, root, archive_path, 1, f"ZIPにソースがありません: {name}")
            for name in sorted(actual_names - expected_names):
                add(errors, root, archive_path, 1, f"ZIPに配布対象外ファイルがあります: {name}")
            for name in sorted(expected_names & actual_names):
                source = root / name
                if archive.read(name) != source.read_bytes():
                    add(errors, root, archive_path, 1, f"ZIPとソースの内容が一致しません: {name}")
                source_executable = bool(source.stat().st_mode & 0o100)
                archive_executable = bool((archive.getinfo(name).external_attr >> 16) & 0o100)
                if archive_executable != source_executable:
                    add(errors, root, archive_path, 1, f"ZIPとソースの実行権限が一致しません: {name}")
    except (BadZipFile, OSError) as error:
        add(errors, root, archive_path, 1, f"ZIPを読み込めません: {error}")



def check_mirrors(root: Path, project: dict, errors: list[str]) -> None:
    """教材に置いた複製コードが、完成プロジェクトのソースと1バイトも違わないか確かめる。

    教員用ガイドの teacher/<スラッグ>/code/ は、完成プロジェクトを開かなくても
    授業中にコードを見せられるように置いた複製である。
    完成コードだけを直すと、複製が古いまま静かに残るので、ここで捕まえる。
    照合するのは mirrors を書いた単元だけで、書かない単元では何もしない。
    """
    for mirror in project.get("mirrors", []):
        source_path = root / mirror["source"]
        copy_path = root / mirror["copy"]
        if not source_path.is_file():
            add(errors, root, mirror["source"], 1, "複製コードの元ファイルがありません")
            continue
        if not copy_path.is_file():
            add(errors, root, mirror["copy"], 1, "複製コードがありません")
            continue
        try:
            if copy_path.read_bytes() != source_path.read_bytes():
                add(errors, root, copy_path, 1,
                    f"複製コードと元ファイルの内容が一致しません: {mirror['source']}"
                    "（元ファイルからコピーし直してください）")
        except OSError as error:
            add(errors, root, copy_path, 1, f"複製コードを読み込めません: {error}")


class SectionTexts(HTMLParser):
    """<section> ごとに、中に書かれた文字を集める。入れ子の <section> は外側にまとめる。"""

    def __init__(self):
        super().__init__()
        self.texts: list[str] = []
        self._depth = 0
        self._parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "section":
            self._depth += 1

    def handle_data(self, data):
        if self._depth:
            self._parts.append(data)

    def handle_endtag(self, tag):
        if tag != "section" or not self._depth:
            return
        self._depth -= 1
        if not self._depth:
            # 改行や字下げの違いで照合が外れないよう、空白は1つにまとめる。
            self.texts.append(" ".join("".join(self._parts).split()))
            self._parts = []


def check_downloads(root: Path, project: dict, errors: list[str]) -> None:
    """教材のフォルダから学生が自分でコピーするファイルが、完成プロジェクトのソースと同じか確かめる。

    ZIPの検査が「ZIPの中身＝ソース」を保証するので、ここで「配布ファイル＝ソース」を確かめれば、
    学生がどこから取っても同じ中身になる。
    学生は、教材のフォルダをFinderで開いてコピーする。ダウンロードボタンにはしない。
    教科書をファイルとして開いていると（file://）ブラウザが download 属性を無視し、
    押しても保存されずに中身が表示されるだけだからである。
    教科書から置き場所やファイル名の案内が消えたら、ここで検出する。
    """
    downloads = project.get("downloads", [])
    if not downloads:
        return
    sources = archive_sources(root, project["root"])
    textbook_path = root / project["docs"][0]
    sections = SectionTexts()
    if textbook_path.is_file():
        sections.feed(read(textbook_path))
    unguided_folders: set[str] = set()
    for item in downloads:
        download_path = root / item["download"]
        source_path = root / item["source"]
        name = Path(item["download"]).name
        if name != Path(item["source"]).name:
            # 学生は手に入れたファイルをそのままプロジェクトに入れる。
            # 名前が違うと @drawable/… やクラス名が解決できない。
            add(errors, root, item["download"], 1, f"配布ファイルとソースのファイル名が一致しません: {item['source']}")
        if item["source"] not in sources:
            add(errors, root, item["source"], 1, "配布ファイルの元ファイルが、完成プロジェクトZIPに入るファイルではありません")
        elif not download_path.is_file():
            add(errors, root, item["download"], 1, "配布ファイルがありません")
        else:
            try:
                if download_path.read_bytes() != source_path.read_bytes():
                    add(errors, root, download_path, 1, f"配布ファイルとソースの内容が一致しません: {item['source']}（ソースからコピーし直してください）")
            except OSError as error:
                add(errors, root, download_path, 1, f"配布ファイルを読み込めません: {error}")
        if not textbook_path.is_file():
            continue
        # Finderで開かせるので、置き場所のフォルダとファイル名が、同じSTEP（<section>）に書いてあること。
        # 教科書のどこかにあればよい、とはしない。同じフォルダのファイルを別々のSTEPで使うときに、
        # 片方のSTEPから案内が消えても、もう片方の案内で通ってしまう。
        # 置き場所は配布物の中での場所なので、リポジトリのパスをそのまま矢印でつないだ形で照合する。
        folder = " → ".join(Path(item["download"]).parent.parts)
        guided = [text for text in sections.texts if folder in text]
        if not guided:
            # 同じフォルダのファイルが何枚あっても、直す場所は1つなので1回だけ出す。
            if folder not in unguided_folders:
                unguided_folders.add(folder)
                add(errors, root, textbook_path, 1, f"配布ファイルの置き場所の案内がありません: {folder}")
        elif not any(name in text for text in guided):
            add(errors, root, textbook_path, 1, f"配布ファイルのファイル名の案内がありません: {name}（置き場所 {folder} と同じSTEPに書いてください）")


def _split_unit(name: str) -> tuple[str, str]:
    """K01HelloKotlin を ("K01", "K01HelloKotlin") に分ける。

    単元は2系統ある。K は純Kotlin系（IntelliJ IDEA）、A は Android系。
    """
    match = re.match(r"^([KA]\d+)(.*)$", name)
    return (match.group(1), match.group(2)) if match else (name, name)


def check_registration(root: Path, config: dict, errors: list[str]) -> None:
    """単元が設定とREADMEの両方に登録されているか確かめる。

    配布スクリプトは単元一覧を config から読むので、ここでは確かめない。
    """
    setting = config.get("registration")
    if not setting:
        return
    scan_roots = set(config["scan_roots"])
    # 用語ごとに、どの系統の単元へ求めるかを持つ。applies_to を書かなければ全系統に求める。
    # 指定AVD名のようにAndroid系でしか使わない用語を、純Kotlin系の教科書にまで求めないため。
    term_requirements = [
        (term.get("applies_to"), {name for name in term.get("required_in", [])})
        for term in config["terms"]
    ]
    targets = []
    for target in setting["targets"]:
        path = root / target["path"]
        if not path.is_file():
            add(errors, root, target["path"], 1, "登録確認の対象ファイルがありません")
            continue
        targets.append((target["path"], read(path), target["requires"]))
    for project in config["projects"]:
        name = project["name"]
        if project["root"] not in scan_roots:
            add(errors, root, CONFIG.as_posix(), 1, f"{name}がscan_rootsにありません")
        for applies_to, required_in in term_requirements:
            if applies_to is not None and project.get("kind") not in applies_to:
                continue
            for doc in project["docs"]:
                if doc not in required_in:
                    add(errors, root, CONFIG.as_posix(), 1, f"{name}の{doc}がterms.required_inにありません")
        paths = {
            "student_doc": project["docs"][0],
            "teacher_doc": project["docs"][1],
            "archive": project["archive"],
        }
        for shown, content, requires in targets:
            for key in requires:
                needed = paths.get(key)
                if needed is None:
                    add(errors, root, CONFIG.as_posix(), 1,
                        f"registration.targetsのrequiresに、知らない項目があります: {key}")
                elif needed not in content:
                    add(errors, root, shown, 1, f"{name}の{needed}への参照がありません")


class SidebarUnits(HTMLParser):
    """教科書のサイドバー <div class="resources"> に並ぶ単元を、出てきた順に集める。

    ほかの単元は <a href="../<単元>/index.html">、いま開いている単元は
    <span aria-current="page"> で書く。「困ったとき」や共通資料へのリンクは集めない。
    resources の外（topbarの直前の単元へのリンクなど）も集めない。
    """

    UNIT_HREF = re.compile(r"\.\./[^/?#]+/index\.html")

    def __init__(self):
        super().__init__()
        self.found = False
        self.line = 1  # <div class="resources"> の行
        self.units: list[tuple[str | None, str]] = []  # (リンク先。現在地は None, 表示名)
        self.nested: list[str] = []  # 単元の項目の中に入っていたタグ
        self._depth = 0  # resources の中にいるあいだの <div> の深さ
        self._tag: str | None = None  # いま集めている単元を開いたタグ
        self._href: str | None = None
        self._text: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "div":
            if self._depth:
                self._depth += 1
            elif "resources" in (values.get("class") or "").split():
                if not self.found:
                    self.line = self.getpos()[0]
                self.found = True
                self._depth = 1
            return
        if not self._depth:
            return
        if self._text is not None:
            # 単元の項目は、文字だけの <a> か <span>。入れ子にすると、リンクと現在地を取り違える。
            self.nested.append(tag)
        elif tag == "a" and self.UNIT_HREF.fullmatch(values.get("href") or ""):
            self._tag, self._href, self._text = tag, values["href"], []
        elif tag == "span" and values.get("aria-current") == "page":
            self._tag, self._href, self._text = tag, None, []

    def handle_data(self, data):
        if self._text is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "div" and self._depth:
            self._depth -= 1
        elif tag == self._tag and self._text is not None:
            self.units.append((self._href, "".join(self._text).strip()))
            self._tag = self._text = None


def check_sidebar_units(root: Path, config: dict, errors: list[str]) -> None:
    """どの教科書のサイドバーにも、全単元が projects の順で並んでいるか確かめる。

    単元を足したのに、ほかの単元のサイドバーを直し忘れる事故を捕まえる。
    いま開いている単元はリンクにせず、現在地（aria-current="page"）として示す。
    見るのは単元の並び・リンク先・表示名で、共通資料へのリンクとの位置関係は見ない。
    topbar（直前の単元へのリンク）も見ない。
    """
    projects = config["projects"]
    # サイドバーは projects の順と照合するので、projects そのものが単元番号順でなければならない。
    # 単元は2系統あるので、「K系→A系」のように、系統が出てきた順に固まって並んでいることを確かめる。
    # 同じ系統の中は番号の昇順。いちどA系に移ったあとでK系に戻るのは、授業の進み方と合わない。
    numbered = []
    for project in projects:
        match = re.match(r"^([KA])(\d+)", project["name"])
        if match:
            numbered.append((match.group(1), int(match.group(2)), project["name"]))
    order: list[str] = []  # 系統の接頭辞が最初に出てきた順
    for prefix, _, _ in numbered:
        if prefix not in order:
            order.append(prefix)
    for (previous_prefix, previous_number, previous_name), (prefix, number, name) in zip(numbered, numbered[1:]):
        if prefix == previous_prefix:
            out_of_order = number <= previous_number
        else:
            out_of_order = order.index(prefix) < order.index(previous_prefix)
        if out_of_order:
            add(errors, root, CONFIG.as_posix(), 1, f"projectsが単元番号順に並んでいません: {previous_name}のあとに{name}があります")
    for current in projects:
        textbook_name = current["docs"][0]
        path = root / textbook_name
        if not path.is_file():
            continue  # 教科書がないことは check_project が報告する。
        text = read(path)
        sidebar = SidebarUnits()
        sidebar.feed(text)
        if not sidebar.found:
            add(errors, root, path, 1, 'サイドバー（<div class="resources">）がありません')
            continue
        line = sidebar.line
        for tag in sidebar.nested:
            add(errors, root, path, line, f"サイドバーの単元の中に、別のタグがあります: <{tag}>")
        expected: list[tuple[str | None, str]] = []
        for unit in projects:
            number, label = _split_unit(unit["name"])
            href = None if unit is current else posixpath.relpath(
                unit["docs"][0], posixpath.dirname(textbook_name))
            expected.append((href, f"{number}：{label}"))
        if sidebar.units == expected:
            continue
        before = len(errors)
        for href, shown in expected:
            if (href, shown) in sidebar.units:
                continue
            if href is None:
                add(errors, root, path, line, f'サイドバーに現在地がありません: <span aria-current="page">{shown}</span>')
            else:
                add(errors, root, path, line, f'サイドバーに単元へのリンクがありません: <a href="{href}">{shown}</a>')
        for href, shown in sidebar.units:
            if (href, shown) in expected:
                continue
            if href and posixpath.normpath(posixpath.join(posixpath.dirname(textbook_name), href)) == textbook_name:
                add(errors, root, path, line, f"サイドバーで、いま開いている単元がリンクになっています: {shown}")
            else:
                add(errors, root, path, line, f"サイドバーに、登録のない単元があります: {shown}（{href or '現在地'}）")
        if len(errors) == before:
            # 過不足はないのに一致しない。順番が違うか、同じ単元が2回出ている。
            actual = "、".join(shown for _, shown in sidebar.units)
            add(errors, root, path, line, f"サイドバーの単元が、{CONFIG.as_posix()}のprojectsの順に並んでいません: {actual}")


def check_project_layout(root: Path, config: dict, errors: list[str]) -> None:
    """単元プロジェクトの.gitignoreと、追跡してはいけないファイルを確かめる。

    .gitignoreの基準は kind ごとに違う（IntelliJ IDEAのプロジェクトとAndroidのプロジェクトで
    無視するものが違う）ので、kind → パス の辞書で書く。
    """
    setting = config.get("project_layout")
    if not setting:
        return
    reference_setting = setting["gitignore_reference"]
    if not isinstance(reference_setting, dict):
        # 文字列で書かれていたら、全kind共通の基準とみなす（参照リポジトリの書き方との後方互換）。
        reference_setting = {kind: reference_setting for kind in KINDS}
    references: dict[str, str] = {}  # kind → 基準ファイルの中身
    for kind, reference_name in sorted(reference_setting.items()):
        reference_path = root / reference_name
        if reference_path.is_file():
            references[kind] = read(reference_path)
        else:
            add(errors, root, reference_name, 1, ".gitignoreの基準ファイルがありません")
    parts = set(setting.get("untracked_parts", []))
    names = set(setting.get("untracked_names", []))
    checked: set[str] = set()
    for project in config["projects"]:
        kind = project.get("kind")
        if kind not in KINDS:
            continue  # kindの誤りは check_project が報告する。
        project_root = project["root"]
        if project_root in checked:
            continue  # 純Kotlin系は、複数の単元が1つのプロジェクトを共有する。
        checked.add(project_root)
        path = root / project_root / ".gitignore"
        reference_name = reference_setting.get(kind)
        if reference_name is None:
            add(errors, root, CONFIG.as_posix(), 1,
                f"project_layout.gitignore_referenceに{kind}の基準がありません")
        elif not path.is_file():
            add(errors, root, path, 1, ".gitignoreがありません")
        elif kind in references and read(path) != references[kind]:
            add(errors, root, path, 1, f"{reference_name}と内容が異なります")
        for name in tracked_files(root, project_root):
            tracked = Path(name)
            if parts.intersection(tracked.parts) or tracked.name in names:
                add(errors, root, name, 1, "Git管理してはいけないファイルです")


def validate(root: Path) -> list[str]:
    config_path = root / CONFIG
    if not config_path.is_file():
        return [f"{CONFIG}:1: 設定ファイルがありません"]
    try:
        config = json.loads(read(config_path))
    except (OSError, json.JSONDecodeError) as error:
        return [f"{CONFIG}:1: 設定ファイルを読み込めません: {error}"]
    # 必須のキーが無いまま先へ進むとトレースバックになる。日本語のエラーにして引き返す。
    missing = check_config(config)
    if missing:
        return missing
    errors: list[str] = []
    check_course(root, config, errors)
    check_terms(root, config, errors)
    check_registration(root, config, errors)
    check_sidebar_units(root, config, errors)
    check_project_layout(root, config, errors)
    for project in config["projects"]:
        check_project(root, project, errors)
        check_mirrors(root, project, errors)
        check_downloads(root, project, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        print("教材整合性チェック: NG", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("教材整合性チェック: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
