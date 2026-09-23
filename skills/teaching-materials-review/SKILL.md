---
name: teaching-materials-review
description: Review teaching materials against Kotlin console and Android project sources, canonical terminology, code snippets, and student distribution archives; when explicitly requested, summarize the result in a PR comment. Use for PRs that change docs, completed projects, packaging, or release workflows in this repository.
---

# Teaching materials review

このリポジトリ（Kotlin演習・1コマ90分 × 全15コマ）の教材変更をレビューするときは、文章だけでなく、教材・完成プロジェクト・配布ZIPの整合性を確認する。

単元には**2系統**ある。どちらの系統かで、確かめることが変わる。

| 系統 | `config/teaching-materials.json` の `kind` | 完成プロジェクト | 動かし方 |
| --- | --- | --- | --- |
| 純Kotlin（`K01`〜） | `kotlin-console` | `K01HelloKotlin/src/exNN/` | IntelliJ IDEA で `fun main()` を実行 |
| Android（`A01`〜） | `android` | `A01HelloAndroid` など | Android Studio、エミュレータ `jec_25cm_kotlin_Pixel 9a` |

## 必須確認

1. 次の4つを実行する。

   ```sh
   python3 scripts/check-teaching-materials.py
   python3 -m unittest discover -s scripts -p 'test_*.py'
   python3 scripts/localize-student-materials.py check
   python3 scripts/package-student-materials.py
   ```

2. 検査が失敗した場合は、PRを承認可能と判断しない。
3. `config/teaching-materials.json` の `terms` の正式表記を基準にし、禁止表記を個別に修正する。
4. 教材の完成コードとプロジェクトの実ファイルが一致することを確認する。`snippets` はバイト単位で照合されるので、教科書のコードを手で写して直していないかを見る。
5. ZIPの内容が現行ソースと一致し、IDE設定・SDK設定・ビルド生成物（`.idea` `.gradle` `.kotlin` `build` `out` `local.properties`）を含まないことを確認する。
6. PRレビュー指摘には、妥当性・再現性・デグレの可能性・修正コスト・既存仕様への影響を確認したうえで、対応が必要、任意対応、対応不要のいずれかを明記する。

### 系統ごとに確かめること

**純Kotlin単元（`kind: "kotlin-console"`）**

- `sources` の各 `.kt` が `K01HelloKotlin/src/<package>/` の下にあり、先頭に `package <package>`（セミコロンなし）が書いてあること。
- `fun main()` があり、IntelliJ IDEA の実行ボタンで動かせる形であること。Gradleは使わない。
- IntelliJ IDEA で実行し、**Runツールウィンドウのコンソール出力**が教科書に書いてある出力と一致すること。出力の行数・順番・型の見え方（`2.0` と `3.0` など）まで見る。
- レビュワーがIntelliJ IDEAを開けない場合は、出力の照合を「未確認項目」として総括コメントに残す。推測で「一致した」と書かない。

**Android単元（`kind: "android"`）**

- ビルドが通ること。

  ```sh
  cd A01HelloAndroid && ANDROID_HOME="$HOME/Library/Android/sdk" ./gradlew assembleDebug
  ```

- `app/build.gradle.kts` の `namespace` と `applicationId` が `package`（`jp.ac.jec.` で始まる）と一致すること。
- `layout` に挙げたXMLが存在し、教科書の説明と `id` が食い違っていないこと。
- 画面の確認は、エミュレータ `jec_25cm_kotlin_Pixel 9a` で行う。別のAVDで撮った画面やスクリーンショットは、指摘として挙げる。
- 依存ライブラリを足す変更は、`gradle/libs.versions.toml` でバージョンを管理しているかを見る。

## 完成コードの判断基準

完成プロジェクトのコードは、次の書き方を基準に読む。ここから外れていれば指摘し、ここに沿っていれば「読みやすく書き直すべき」という指摘は採用しない。

1. **Viewの取得は `findViewById`。** ViewBindingもComposeも使わない。`val txtXxx = findViewById<TextView>(R.id.txt_xxx)` の形で `onCreate` の冒頭にまとめる。命名は `txtXxx` / `edtXxx` / `btnXxx` / `imgXxx` / `recyclerView`。
2. **`@SuppressLint` で警告を隠さない。** 警告が出たら、原因そのものを消す（`setOnTouchListener` をやめて `AppCompatImageView` を継承し、`onTouchEvent()` と `performClick()` をオーバーライドする、など）。`@SuppressLint` が足されていたら「対応が必要」とする。
3. **ユーザーに伝えることは `Snackbar`（または `Toast`）で画面に出す。** `Log.d` で済ませない。Logcatは、学生が中身を確かめるための補助として扱う単元でだけ使う。
4. **1単元で導入する新概念は1つまで。** 画面（またはコンソールの出力）で効果が見える形になっているかを見る。2つ目の新概念が混ざっていたら、別issueへ分ける指摘にする。
5. **完成プロジェクトにUnit Testは書かない。** テストしやすくするためのリファクタリングもしない。テストの追加や、そのための構造変更を求める指摘は「対応不要」とする。`scripts/test_*.py` はCIで動くので、通る状態を保つ。
6. **完成プロジェクトの `README.md` は `A03GithubSearch/README.md` の形**（画面の構成の表 → 使用しているAPI → ソースコードの構成の表 → 処理の流れ → 実装のポイント → 主なライブラリ → ビルドと実行）にそろえる。
7. **ライブラリは必要なときだけ足す。** バージョンは `gradle/libs.versions.toml` で管理する。
8. 純Kotlin系の完成コードは `K01HelloKotlin/src/exNN/` に置き、ファイル先頭に `package exNN` を書く。
9. コメントは、学生が読んで意味が分かる**日本語**で書く。英語のコメントは指摘する。
10. **オーナーの書き方を保つ。** 「初学者向けに書き直すべき」という指摘の既定の対応は「教科書で説明する」。採用するのは、動作を変えない小さな明確化だけにする。

## PRコメントの扱い

- PR番号またはURLがレビュー対象として明示され、ユーザーがPRへの投稿を依頼した場合に限り、レビュー結果をGitHubへ投稿する。単に「レビューして」と依頼された場合は、結果をこの会話で報告し、外部へ投稿しない。
- 投稿する場合は、個別コメントを大量に作らず、原則として1件の総括コメントにまとめる。行固有の修正が必要な指摘だけは、総括コメントから該当ファイル・行へリンクする。
- 総括コメントには、対象PR、レビュー対象コミット、必須検査と関連テストの結果、指摘一覧、マージ可否を含める。各指摘には「対応が必要」「任意対応」「対応不要」のいずれかを付ける。
- 対応が必要な指摘がある場合は「マージ不可」、任意対応だけまたは指摘がない場合は「マージ可」、検査を完了できない場合は「判断保留」と明記する。検査不能の理由と未確認項目も記載する。
- 同じPRへ再レビュー結果を投稿する場合は、`<!-- teaching-materials-review-summary -->` マーカー付きの既存総括コメントを更新し、重複投稿しない。既存コメントがなければこのマーカーを付けて新規投稿する。
- 総括コメントの投稿は、承認・変更要求・マージ・ラベル変更を意味しない。これらは別途明示的に依頼された場合のみ行う。
- コメントは日本語で書く。実在しないissue番号・PR番号・URLを書かない。

## 判断基準

- 正式表記や配布物の不一致は、学生配布前に直す必要がある指摘として扱う。
- 初学者向けのコード構成を変えるだけの改善は、教材の学習目標と変更範囲を比較して判断する（上の「完成コードの判断基準」10）。
- 自動レビューの指摘はそのまま実行せず、必ず現在のソースと検査結果で再確認する。
- マージ可否は、次の優先順位で判定する。①必須検査を実行して失敗した場合は「マージ不可」とし、必須検査の失敗を「マージ可」と判定しない。②必須検査を実行できない、または完了できない場合は「判断保留」とする。③必須検査が成功していても対応が必要なレビュー指摘があれば「マージ不可」とする。④必須検査が成功し、対応が必要な指摘がなく、任意対応のみまたは指摘がない場合に限り「マージ可」とする。関連テストの結果も総括コメントに記載する。
- 「承認可能」と「マージ可」は別の概念として扱う。必須確認2により、必須検査に失敗したPRを承認可能と判断してはならず、レビュー上も「マージ可」としてはならない。マージ操作自体はユーザーの依頼がない限り実行しない。

## 対象外（指摘しない）

次の項目は指摘しない。botに指摘されたら「対応不要」と返信する。検証もしない。

- 完成プロジェクトのUnit Test。テストしやすくするためのリファクタリングも含む。
- Windows。教員も学生もmacOSで、CIはubuntu。
- ダークテーマ。確認は既定のライトテーマだけで行う。
- タブレット・フォルダブル対応、画面回転と横画面。
