---
name: add-teaching-unit
description: Add a new Android teaching unit (A01-) to this Kotlin course repository - the completed project, the student textbook under docs/, the teacher guide under teacher/, the config registration, the README entries, and the sidebar links in every existing textbook. Also covers the short path for adding a Kotlin session (src/exNN/) to the single K01HelloKotlin unit, which does not add a unit. Use when asked to add, create, or register a new unit, a new textbook page, a new teacher guide, or a new exNN exercise.
---

# Add teaching unit

## はじめに：Kotlinの回を足すだけなら、この手順は要らない

**純Kotlin系の単元は `K01` の1つだけで、プロジェクトも `K01HelloKotlin` の1つだけ。** Kotlinの文法は全6コマをかけて、この1つのプロジェクトに `src/exNN/` のパッケージを足しながら進める。教科書も `docs/hello-kotlin/index.html` の1冊だけで、同じ教科書にSTEPを足していく。**`K02` 以降の単元は作らない。**

`K01HelloKotlin/src/exNN/` を1つ増やす作業は、**単元の追加ではない**。直すのは次の5か所だけで、この下の「1.」以降は読まなくてよい。

1. `K01HelloKotlin/src/exNN/main.kt` を足す（ファイルの先頭に `package exNN`。番号は前年度資料の節に対応させる）。
2. `config/teaching-materials.json` のK01の `packages`（配列）と `sources` に、その `exNN` を足す。
3. `docs/hello-kotlin/index.html` にSTEPを足し、サイドバーの `.progress` の `max` と `data-progress-label` の総数を直す。教科書に貼るコードは `snippets` に登録する。
4. `teacher/hello-kotlin/index.html` の進め方にその回を足し、`teacher/hello-kotlin/code/` に完成コードの複製を置いて `mirrors` に登録する。
5. 配布ZIPを作り直す。

   ```sh
   python3 scripts/package-project.py --project K01HelloKotlin --output docs/hello-kotlin/downloads/K01HelloKotlin.zip
   ```

**`config/teaching-materials.json` の `projects` に新しい単元を足さない。** 単元が増えないので、サイドバー・topbar・READMEの15コマ計画・GitHubのラベルは変わらない。`docs/` に新しいスラッグのフォルダも作らない。同じ手順は `AGENTS.md` の§9「Kotlinの回を足すときは、単元を増やさない」にもある。

## この先：Android系（`A01`〜）の単元を新しく足す手順

**新しく足す単元はAndroid系（`kind` は `"android"`、完成プロジェクトは `A0NXxx/`、IDEは Android Studio）だけ。** 単元名の例は `A02CalcGame`。`docs/<スラッグ>/` を作るだけでは足りない。ここに挙げたすべてに登録する。1つでも抜けると `python3 scripts/check-teaching-materials.py` が落ちる。

**この作業は1つのPRで完結させる。** 既存の教科書のサイドバーは、issueの「触る範囲」に挙がっていなくても、登録に必要な変更なので同じPRで直す。

## 1. 完成プロジェクト

**Android単元（`android`）**

- `A0NXxx/` をAndroid Studioで新規作成する。パッケージは `jp.ac.jec.` で始める。
- `app/build.gradle.kts` の `namespace` と `applicationId` を、configに書く `package` と一致させる。
- ビルドを通し、エミュレータ `jec_25cm_kotlin_Pixel 9a` で動かす。

  ```sh
  cd A0NXxx && ANDROID_HOME="$HOME/Library/Android/sdk" ./gradlew assembleDebug
  ```

- 完成プロジェクトの `README.md` は `A03GithubSearch/README.md` の形にそろえる（画面の構成の表 → 使用しているAPI → ソースコードの構成の表 → 処理の流れ → 実装のポイント → 主なライブラリ → ビルドと実行）。

**完成コードで守ること**

- Viewの取得は `findViewById`。ViewBindingもComposeも使わない。
- `@SuppressLint` で警告を隠さない。原因そのものを消す。
- ユーザーに伝えることは `Snackbar`（または `Toast`）で画面に出す。`Log.d` で済ませない。
- **1単元で導入する新概念は1つまで。** 画面で効果が見える形にする。
- **Unit Testは書かない。** テストしやすくするためのリファクタリングもしない。
- コメントは、学生が読んで意味が分かる日本語で書く。
- ライブラリは必要なときだけ足す。バージョンは `gradle/libs.versions.toml` で管理する。

## 2. 学生用の教科書 `docs/<スラッグ>/`

- **スラッグは、単元名から番号を取った部分をハイフン区切りの小文字にした形**（`K01HelloKotlin` → `hello-kotlin`、`A01HelloAndroid` → `hello-android`、`A02CalcGame` → `calc-game`）。この節から下の例は、まだ作っていない `A01`・`A02` を足すときの形で書いてある。
- `docs/<スラッグ>/index.html`。既存の教科書と同じHTMLの型を使う（`.skip` → `.topbar` → `.shell` → `.sidebar` → `main#main`、STEPは `<section id="step-N">`）。
- サイドバーの `.progress` の `max` と `data-progress-label` の総数を、STEP数に合わせる。
- **本文に単元名（`A02CalcGame` のような `projects[].name`）の表記を必ず入れる。** `check_project` がこれを探す。
- **Android単元は、単元名に加えて `package` の値（`jp.ac.jec.…`）も、教科書と教員用ガイドの本文に書く**（`check_project` が両方を探す）。純Kotlin系の `K01HelloKotlin` は単元名だけでよい（`packages` の `ex01` は短くて本文に偶然現れるため、検査の対象になっていない）。
- `docs/<スラッグ>/downloads/<Project>.zip` を作る。Android単元は単元ごとに別プロジェクトなので、ZIPも単元ごとに1つ。

  ```sh
  python3 scripts/package-project.py --project A0NXxx --output docs/<スラッグ>/downloads/A0NXxx.zip
  ```

  **純Kotlin系のZIPは `docs/hello-kotlin/downloads/K01HelloKotlin.zip` の1つだけ**で、`K01HelloKotlin` のプロジェクトが1つしかないため増えない（作り直すのは、上の「Kotlinの回を足すだけなら」の5）。
- `docs/<スラッグ>/images/` は、**その教科書で実際に使うスクリーンショットがあるときだけ**作る。Android単元の画面は、指定AVD `jec_25cm_kotlin_Pixel 9a` で撮る。「ここに画像を入れる」のようなプレースホルダは置かない。
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

`projects` に足す項目は、Android単元なら次の形になる（`A02CalcGame` を足す場合）。

```json
{
  "name": "A02CalcGame",
  "kind": "android",
  "root": "A02CalcGame",
  "package": "jp.ac.jec.a02calcgame",
  "layout": "A02CalcGame/app/src/main/res/layout/activity_main.xml",
  "sessions": 2,
  "docs": ["docs/calc-game/index.html", "teacher/calc-game/index.html"],
  "sources": ["A02CalcGame/app/src/main/java/jp/ac/jec/a02calcgame/MainActivity.kt"],
  "snippets": [
    { "html": "docs/calc-game/index.html", "id": "code-main-activity",
      "source": "A02CalcGame/app/src/main/java/jp/ac/jec/a02calcgame/MainActivity.kt" }
  ],
  "archive": "docs/calc-game/downloads/A02CalcGame.zip"
}
```

`package` の値は、`app/build.gradle.kts` の `namespace` と `applicationId` の両方と一致している必要がある。`root` はプロジェクトのディレクトリ、`layout` はレイアウトXMLのパス。Android単元は単元ごとに別プロジェクトなので、`root` も `archive` も単元ごとに別になる。

**純Kotlin系は `packages`（配列）、Android系は `package`（文字列）。** 書き分けを取り違えると設定エラーになる。`kotlin-console` の単元は `K01HelloKotlin` の1つだけで、回を足すたびに `packages` が伸びる（`["ex01"]` → `["ex01", "ex02"]` → …）。`sources` にもそれぞれの `main.kt` を挙げる。**`packages` に書いたのに `sources` が無いと落ちる。** K01の `archive` は `docs/hello-kotlin/downloads/K01HelloKotlin.zip` の1つだけで、回を足しても増えない（`package-student-materials.py` は `(root, archive)` の重複を除いた組ごとにZIPを作る）。

直すのは次の4か所。

1. `scan_roots`：新しいディレクトリが既存の `scan_roots`（`README.md` / `docs` / `teacher` / `K01HelloKotlin`）の下に入らない場合だけ足す。Android単元を足したときは、そのプロジェクトのディレクトリを足す。
2. `terms[].required_in`：その単元の教科書・教員用ガイドで正式表記を使うなら足す（指定AVD名など）。用語に `applies_to` が書いてあると、その系統の単元にだけ表記が求められる。指定AVD名は `applies_to: ["android"]` なので、**Android単元を足したときは、その教科書と教員用ガイドを `required_in` に足す**。純Kotlin系の `K01HelloKotlin` はエミュレータを使わないので足さない。
3. `projects`：**単元番号順の位置に足す。** 並び順は「最初に現れた接頭辞の順（K → A）」で、同じ接頭辞の中は番号の昇順。**一度Aに変わったあとでKに戻すとエラー**になる。先頭は `K01HelloKotlin` で固定なので、Android単元はそのうしろへ番号順に足す。サイドバーの検査がこの並びを基準にする。
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

- 表示名は `<番号>：<ラベル>`。単元名から先頭の番号を切り離してつなぐので、`A02CalcGame` なら `A02：CalcGame`、`K01HelloKotlin` なら **`K01：HelloKotlin`**（`K01：K01HelloKotlin` にしない）。
- ほかの単元は `<a href="../<スラッグ>/index.html">`、**自単元は `<span aria-current="page">`**。
- 単元の項目は、**文字だけの `<a>` か `<span>`**。中に `<strong>` などの別タグを入れない。
- 「困ったとき」「完成プロジェクトを開く」と共通資料へのリンクは、単元として数えない。共通資料へのリンクには `?from=<自分のスラッグ>` を付ける。
- **純Kotlin系は `K01：HelloKotlin` の1項目だけ**で、Kotlinの回（`exNN`）を足しても増えない。増えるのはAndroid単元だけなので、新しい項目はいつもK01のうしろに並ぶ。

**既存の K01 の教科書（`docs/hello-kotlin/index.html`）に A01 を足す**

```html
<div class="resources"><a href="#help">困ったとき</a><a href="#sample-project">完成プロジェクトを開く</a><span aria-current="page">K01：HelloKotlin</span><a href="../hello-android/index.html">A01：HelloAndroid</a><a href="../common/setup.html?from=hello-kotlin">共通：はじめの準備</a><a href="../common/apk.html?from=hello-kotlin">共通：提出課題とAPK</a></div>
```

**新しい A01 の教科書（`docs/hello-android/index.html`）には、全単元を並べる**

```html
<div class="resources"><a href="#help">困ったとき</a><a href="#sample-project">完成プロジェクトを開く</a><a href="../hello-kotlin/index.html">K01：HelloKotlin</a><span aria-current="page">A01：HelloAndroid</span><a href="../common/setup.html?from=hello-android">共通：はじめの準備</a><a href="../common/apk.html?from=hello-android">共通：提出課題とAPK</a></div>
```

**次の A02 を足したときは、A01 のうしろに並べる**（`docs/calc-game/index.html` のサイドバー）

```html
<div class="resources"><a href="#help">困ったとき</a><a href="#sample-project">完成プロジェクトを開く</a><a href="../hello-kotlin/index.html">K01：HelloKotlin</a><a href="../hello-android/index.html">A01：HelloAndroid</a><span aria-current="page">A02：CalcGame</span><a href="../common/setup.html?from=calc-game">共通：はじめの準備</a><a href="../common/apk.html?from=calc-game">共通：提出課題とAPK</a></div>
```

**topbar は、直前の単元へのリンク1つ。** ブランドは `JEC / Kotlin演習` にそろえる。A01の直前の単元はK01なので、次のようになる。

```html
<header class="topbar"><span class="brand">JEC / Kotlin演習</span><a href="../hello-kotlin/index.html">← K01：HelloKotlin</a></header>
```

単元を途中に挿入したときは、**次の単元のtopbar**も新しい単元へ付け替える。topbarは検査されないので、目で確かめる。

## 7. GitHubのラベル

`area:A<NN>`（`area:A01`、`area:A02`）をラベルに追加し、issueとPRに付ける。Kotlinの回のissueは単元が増えないので、`area:K01` をそのまま使う。

## 8. 翻訳

**日常のPRでは翻訳しない。** 新単元のPRでは日本語だけを足し、文を取り出せることを確かめる。

```sh
python3 scripts/localize-student-materials.py check
```

翻訳は、配布準備の翻訳PRでまとめて行う（`skills/translate-teaching-materials/SKILL.md`）。各言語のHTMLはコミットしない。

## 配布スクリプトへの追記は不要

**`scripts/package-student-materials.py` と `scripts/release-student-materials.py` は直さない。**
どちらも `config/teaching-materials.json` の `projects` から単元一覧を読むので、上の「4」でconfigに足した時点（Kotlinの回なら `packages`・`sources` を足した時点）で、次のすべてが自動で追従する。

- 完成プロジェクトZIPの再生成（`(root, archive)` の重複を除いた組ごと）
- 「完成プロジェクトが見つかりません」の検査
- `はじめに.txt` の単元一覧
- リリースノートの単元一覧

**ここがこのリポジトリと参照元との一番大きな違い。** 配布スクリプトに単元名を直書きしない。もし直書きを足したくなったら、それはconfigの読み込み漏れなので、スクリプト側の不具合として扱う。

## 検証

最後に、次の4つをすべて通す。**Kotlinの回を足しただけのときも、この4つは同じように通す。**

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

Kotlinの回を足したときは、IntelliJ IDEA で `K01HelloKotlin` を開き、その `exNN` の `fun main()` を実行して、コンソール出力が教科書に書いたとおりかを確かめる。

`package-student-materials.py` が作った配布ZIPを展開し、入口から教科書・完成プロジェクト・共通資料へのリンクがたどれることも確かめる。
