---
name: add-teaching-unit
description: Add a new teaching unit to this Kotlin course repository - the completed project, the student textbook under docs/, the teacher guide under teacher/, the config registration, the README entries, and the sidebar links in every existing textbook. Use when asked to add, create, or register a new unit (K01-, A01-), a new textbook page, or a new teacher guide.
---

# Add teaching unit

新しい単元を足すときのチェックリスト。`docs/<スラッグ>/` を作るだけでは足りない。ここに挙げたすべてに登録する。1つでも抜けると `python3 scripts/check-teaching-materials.py` が落ちる。

**この作業は1つのPRで完結させる。** 既存の教科書のサイドバーは、issueの「触る範囲」に挙がっていなくても、登録に必要な変更なので同じPRで直す。

単元には2系統ある。どちらかを先に決める。

| 系統 | `kind` | 完成プロジェクト | IDE | 単元名の例 |
| --- | --- | --- | --- | --- |
| 純Kotlin | `kotlin-console` | `HelloKotlin/src/exNN/` | IntelliJ IDEA | `K02NullSafety` |
| Android | `android` | `A0NXxx/` | Android Studio | `A02CalcGame` |

## 1. 完成プロジェクト

**純Kotlin単元（`kotlin-console`）**

- `HelloKotlin/src/exNN/` にファイルを置く。ファイルの先頭に `package exNN` を書く（Kotlinなのでセミコロンなし）。
- `fun main()` を持たせ、IntelliJ IDEA の実行ボタンで動かせる形にする。Gradleは使わない。
- IntelliJ IDEA で実行し、Runツールウィンドウのコンソール出力を確かめる。教科書に書く出力と、1文字ずつ照合する。

**Android単元（`android`）**

- `A0NXxx/` をAndroid Studioで新規作成する。パッケージは `jp.ac.jec.` で始める。
- `app/build.gradle.kts` の `namespace` と `applicationId` を、configに書く `package` と一致させる。
- ビルドを通し、エミュレータ `jec_25cm_kotlin_Pixel 9a` で動かす。

  ```sh
  cd A0NXxx && ANDROID_HOME="$HOME/Library/Android/sdk" ./gradlew assembleDebug
  ```

- 完成プロジェクトの `README.md` は `A03GithubSearch/README.md` の形にそろえる（画面の構成の表 → 使用しているAPI → ソースコードの構成の表 → 処理の流れ → 実装のポイント → 主なライブラリ → ビルドと実行）。

**どちらの系統でも守ること**

- Viewの取得は `findViewById`。ViewBindingもComposeも使わない。
- `@SuppressLint` で警告を隠さない。原因そのものを消す。
- ユーザーに伝えることは `Snackbar`（または `Toast`）で画面に出す。`Log.d` で済ませない。
- **1単元で導入する新概念は1つまで。** 画面（またはコンソールの出力）で効果が見える形にする。
- **Unit Testは書かない。** テストしやすくするためのリファクタリングもしない。
- コメントは、学生が読んで意味が分かる日本語で書く。
- ライブラリは必要なときだけ足す。バージョンは `gradle/libs.versions.toml` で管理する。

## 2. 学生用の教科書 `docs/<スラッグ>/`

- `docs/<スラッグ>/index.html`。既存の教科書と同じHTMLの型を使う（`.skip` → `.topbar` → `.shell` → `.sidebar` → `main#main`、STEPは `<section id="step-N">`）。
- サイドバーの `.progress` の `max` と `data-progress-label` の総数を、STEP数に合わせる。
- **本文に単元名（`K02NullSafety` のような `projects[].name`）の表記を必ず入れる。** `check_project` がこれを探す。
- **Android単元は、単元名に加えて `package` の値（`jp.ac.jec.…`）も、教科書と教員用ガイドの本文に書く**（`check_project` が両方を探す）。純Kotlin系は単元名だけでよい（`packages` の `ex01` は短くて本文に偶然現れるため、検査の対象になっていない）。
- `docs/<スラッグ>/downloads/<Project>.zip` を作る。

  ```sh
  python3 scripts/package-project.py --project HelloKotlin --output docs/hello-kotlin/downloads/HelloKotlin.zip
  python3 scripts/package-project.py --project A02CalcGame --output docs/calc-game/downloads/A02CalcGame.zip
  ```

  **純Kotlin単元のプロジェクトは `HelloKotlin` の1つだけ**なので、K02以降の `archive` は K01 と同じ `docs/hello-kotlin/downloads/HelloKotlin.zip` を指す。ZIPを作り直すのは1回でよい。
- `docs/<スラッグ>/images/` は、**スクリーンショットを撮れるAndroid単元でだけ**使う。純Kotlin単元は、文章と表と手順で説明し、画像を使わない。「ここに画像を入れる」のようなプレースホルダも置かない。スクリーンショットは指定AVD `jec_25cm_kotlin_Pixel 9a` で撮る。
- コードのスニペットは、`<pre id="code-…"><code>` に置き、**ソースからHTMLエスケープして差し込む**。configの `snippets` がバイト単位で照合するので、手で写して直さない。
- 教科書の中から**ほかの単元へ本文で送らない**（共通資料へのリンクはサイドバーと明示の導線だけ）。
- **多言語展開の制約を守る**（`python3 scripts/localize-student-materials.py check` が行番号つきで落とす）。
  - 開始タグと終了タグを必ず対応させる。`<span/>` のような自己終了タグを書かない。
  - 属性値は必ず引用符で囲む（`<html lang="ja">`）。
  - 文の途中にHTMLコメントを書かない。段落の外に書く。
  - `/` で始まるルート相対リンクを使わない（`href="../assets/textbook.css"` と書く）。
  - 文の途中の要素に `translate="no"` を付けない。訳してほしくない文字は `<code>` で囲む。
- 1,000行を超える教科書HTMLは、章ごとに分けて書いてから結合する（1回で書こうとするとツール呼び出しが長くなりすぎて止まる）。

## 3. 教員用ガイド `teacher/<スラッグ>/`

- `teacher/<スラッグ>/index.html`。既存の教員用ガイドと同じ型にする。
- **「この単元の教材方針」の節を必ず置く。** 何を意図的に外したかを、理由つきで書く。
- `teacher/<スラッグ>/code/` に、STEPごとの照合コードを `NN-ファイル名.拡張子` の形式で置く（`01-main.kt`、`03-MainActivity.kt` など）。
- 本文に単元名の表記を入れる（`check_project` は `docs` に挙げた両方のHTMLを見る）。**Android単元は、教科書と同じく `package` の値（`jp.ac.jec.…`）も本文に書く。**

## 4. `config/teaching-materials.json`

```json
{
  "name": "K02NullSafety",
  "kind": "kotlin-console",
  "root": "HelloKotlin",
  "packages": ["ex02"],
  "sessions": 1,
  "docs": ["docs/null-safety/index.html", "teacher/null-safety/index.html"],
  "sources": ["HelloKotlin/src/ex02/main.kt"],
  "snippets": [
    { "html": "docs/null-safety/index.html", "id": "code-final-kotlin",
      "source": "HelloKotlin/src/ex02/main.kt" }
  ],
  "archive": "docs/hello-kotlin/downloads/HelloKotlin.zip"
}
```

`archive` が K01 と同じパスなのは、**純Kotlin系のプロジェクトが `HelloKotlin` の1つだけで、中身も1つしかない**ためである。`package-student-materials.py` は `(root, archive)` の重複を除いた組ごとにZIPを作るので、同じパスを指していれば `package-project.py` の呼び出しも1回で済む。単元ごとに別の `archive` を書くと、中身が同じZIPが単元の数だけ増える。

**純Kotlin系は `packages`（配列）、Android系は `package`（文字列）。** 書き分けを取り違えると設定エラーになる。1コマで複数の演習を扱う単元は、`"packages": ["ex03", "ex05", "ex06"]` のように並べ、`sources` にもそれぞれの `main.kt` を挙げる。`packages` に書いたのに `sources` が無いと落ちる。

Android単元は `kind: "android"` にし、`root` をプロジェクトのディレクトリ、`package` を `jp.ac.jec.…`、`layout` にレイアウトXMLのパスを書く。

直すのは次の4か所。

1. `scan_roots`：新しいディレクトリが既存の `scan_roots`（`README.md` / `docs` / `teacher` / `HelloKotlin`）の下に入らない場合だけ足す。Android単元を足したときは、そのプロジェクトのディレクトリを足す。
2. `terms[].required_in`：その単元の教科書・教員用ガイドで正式表記を使うなら足す（指定AVD名など）。用語に `applies_to` が書いてあると、その系統の単元にだけ表記が求められる。指定AVD名は `applies_to: ["android"]` なので、**Android単元を足したときは、その教科書と教員用ガイドを `required_in` に足す**。純Kotlin単元はエミュレータを使わないので足さない。
3. `projects`：**単元番号順の位置に足す。** 並び順は「最初に現れた接頭辞の順（K → A）」で、同じ接頭辞の中は番号の昇順。**一度Aに変わったあとでKに戻すとエラー**になる。サイドバーの検査がこの並びを基準にする。
4. `sessions`：正の整数。**`projects` の `sessions` の合計が `course.total_sessions`（15）を超えるとエラー**になる。15コマ計画表の割り当てと合わせる。

## 5. `README.md`

次のすべてに足す。`check_registration` は、READMEに `docs[0]`・`docs[1]`・`archive` の3つのパスが出てくることを確かめる。

- 教科書一覧のリンク（`docs/<スラッグ>/index.html`）
- 完成プロジェクトのリンク（`archive` のパス）
- 教員用ガイドのリンク（`teacher/<スラッグ>/index.html`）
- 15コマ計画表の行（コマ数・単元・内容・プロジェクト）
- フォルダ表（プロジェクトを新しく作ったとき）
- 完成プロジェクトのZIPを更新するコマンド（`package-project.py` の行）

## 6. サイドバーの直し方（**既存の全教科書を直す**）

サイドバーの `<div class="resources">` に並ぶ単元は、**configの `projects` の順・リンク先・表示名まで**照合される。1冊でも直し忘れると検査が落ちる。

- 表示名は `<番号>：<ラベル>`。`K02NullSafety` なら `K02：NullSafety`。
- ほかの単元は `<a href="../<スラッグ>/index.html">`、**自単元は `<span aria-current="page">`**。
- 単元の項目は、**文字だけの `<a>` か `<span>`**。中に `<strong>` などの別タグを入れない。
- 「困ったとき」「完成プロジェクトを開く」と共通資料へのリンクは、単元として数えない。共通資料へのリンクには `?from=<自分のスラッグ>` を付ける。

**既存の K01 の教科書（`docs/hello-kotlin/index.html`）に K02 を足す**

```html
<div class="resources"><a href="#help">困ったとき</a><a href="#sample-project">完成プロジェクトを開く</a><span aria-current="page">K01：HelloKotlin</span><a href="../null-safety/index.html">K02：NullSafety</a><a href="../common/setup.html?from=hello-kotlin">共通：はじめの準備</a></div>
```

**新しい K02 の教科書（`docs/null-safety/index.html`）には、全単元を並べる**

```html
<div class="resources"><a href="#help">困ったとき</a><a href="#sample-project">完成プロジェクトを開く</a><a href="../hello-kotlin/index.html">K01：HelloKotlin</a><span aria-current="page">K02：NullSafety</span><a href="../common/setup.html?from=null-safety">共通：はじめの準備</a></div>
```

**Android単元（A01）を足したときは、K系のうしろに並べる**

```html
<div class="resources"><a href="#help">困ったとき</a><a href="#sample-project">完成プロジェクトを開く</a><a href="../hello-kotlin/index.html">K01：HelloKotlin</a><a href="../null-safety/index.html">K02：NullSafety</a><span aria-current="page">A01：HelloAndroid</span><a href="../common/setup.html?from=hello-android">共通：はじめの準備</a></div>
```

**topbar は、直前の単元へのリンク1つ。** ブランドは `JEC / Kotlin演習` にそろえる。

```html
<header class="topbar"><span class="brand">JEC / Kotlin演習</span><a href="../hello-kotlin/index.html">← K01：HelloKotlin</a></header>
```

単元を途中に挿入したときは、**次の単元のtopbar**も新しい単元へ付け替える。topbarは検査されないので、目で確かめる。

## 7. GitHubのラベル

`area:K<NN>` または `area:A<NN>`（`area:K02`、`area:A01`）をラベルに追加し、issueとPRに付ける。

## 8. 翻訳

**日常のPRでは翻訳しない。** 新単元のPRでは日本語だけを足し、文を取り出せることを確かめる。

```sh
python3 scripts/localize-student-materials.py check
```

翻訳は、配布準備の翻訳PRでまとめて行う（`skills/translate-teaching-materials/SKILL.md`）。各言語のHTMLはコミットしない。

## 配布スクリプトへの追記は不要

**`scripts/package-student-materials.py` と `scripts/release-student-materials.py` は直さない。**
どちらも `config/teaching-materials.json` の `projects` から単元一覧を読むので、上の「4」でconfigに足した時点で、次のすべてが自動で追従する。

- 完成プロジェクトZIPの再生成（`(root, archive)` の重複を除いた組ごと）
- 「完成プロジェクトが見つかりません」の検査
- `はじめに.txt` の単元一覧
- リリースノートの単元一覧

**ここがこのリポジトリと参照元との一番大きな違い。** 配布スクリプトに単元名を直書きしない。もし直書きを足したくなったら、それはconfigの読み込み漏れなので、スクリプト側の不具合として扱う。

## 検証

最後に、次の4つをすべて通す。

```sh
python3 scripts/check-teaching-materials.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/localize-student-materials.py check
python3 scripts/package-student-materials.py
```

Android単元を触ったときは、そのプロジェクトをビルドする。

```sh
cd A01HelloAndroid && ANDROID_HOME="$HOME/Library/Android/sdk" ./gradlew assembleDebug
```

純Kotlin単元は IntelliJ IDEA で `fun main()` を実行して、コンソール出力を確かめる。

`package-student-materials.py` が作った配布ZIPを展開し、入口から新しい単元の教科書・完成プロジェクト・共通資料へのリンクがたどれることも確かめる。
