# 用語集：English（en）

Kotlin演習の対訳表。訳すときは、この表の訳語を使う。新しく訳語を決めた用語は、行を足す。全言語に共通の翻訳ルールは `skills/translate-teaching-materials/SKILL.md` にある。

## 教材と操作の用語

| 日本語 | 訳 | メモ |
| --- | --- | --- |
| Kotlin | Kotlin | 製品名。訳さない |
| IntelliJ IDEA | IntelliJ IDEA | 製品名。訳さない |
| Android Studio | Android Studio | 製品名。訳さない |
| プロジェクト | project | |
| パッケージ | package | `ex01` などのパッケージ名は訳さない |
| 関数 | function | `fun main()` の表記は原文のまま |
| 変数 | variable | `val` / `var` の表記は原文のまま |
| 実行 | run | ボタンの名前を指すときは **Run** のまま |
| コンソール | console | 実行結果が出る場所。IntelliJ IDEAの画面名 **Run** は原文のまま |
| エミュレータ | emulator | Android系の単元で使う |
| 教材 | materials | |
| 教科書 | textbook | |
| 単元 | unit | |
| コマ | lesson | |
| 完成プロジェクト | completed project | |
| 実行結果 | output | |
| 実行結果のウィンドウ | output window | |
| コード補完 | code completion | |
| 実行の入口 | entry point | |
| 実行設定 | run configuration | |
| 成功の目印 | What you should see | |
| ここで止まって確認 | Stop here and check | |
| 公式資料 | Official documentation | |
| もとのページ | original page | 共通資料の戻りリンク。previous page にしない（直接開くと、直前のページではなく既定の単元へ戻るため） |
| 見本 | sample | 完成見本 → completed sample。教材の `samples` フォルダと、IntelliJ IDEA の **Add sample code** に合わせる |
| 指定AVD | designated AVD | AVD名 `jec_25cm_kotlin_Pixel 9a` は訳さない。（指定AVDで撮影）→ (taken on the designated AVD) |
| 完成チェック | completion check | |
| 困ったとき | If you get stuck | サイドバーのリンク |
| 完成プロジェクトを開く | Open the completed project | サイドバーのリンク |
| 共通：はじめの準備 | Shared: Getting ready for class | ほかの共通資料は Shared: The assignment and the APK、Shared: A different Android Studio version |
| アレンジ | customize / customization | |
| 赤い波線 | red squiggly line | |
| 確認日 | Last checked | |
| 対象（単元の冒頭の行） | Project | 共通資料の足もとの「対象」（環境）は For |
| 実行先 | target device | Android Studio の表示に合わせる。Xcode との比較では run destination |
| 部品（画面の） | UI element | |
| 完成版 | finished app | K01（コンソール）では completed version |
| 進捗 / 目次（aria-label） | Progress / Table of contents | |
| Google Classroom の表示 | 授業 (Classwork)、追加または作成 (Add or create)、提出 (Turn in)、提出済み (Turned in)、提出を取り消す (Unsubmit) | 学生の画面の言語が分からないので、日本語を残して英語の表示名を添える |

## 書き方の決まり

- 操作は命令形、説明と画面で確認する文は現在形で書く。
- 見出しはsentence caseにする。通常の引用は "…"、実際の日本語UIを囲む「」は保持して意味を添える。
- 「Nコマ目」は、本文でも見出しでも Lesson N と大文字で書く（Lessons 1–6 のように範囲も同じ）。
- 確認欄（ここで止まって確認）は、画面で確かめられる状態を現在形で書く。すでに済んだ操作は has been checked / has been shown の形にする。「〜できた」「〜と言えた」のような振り返りの言い方にしない。
- 教科書が日本語表示のIDEのメニュー名を書いているとき（K01のIntelliJ IDEA）は、`<strong>` の日本語を残し、英語の表示名をかっこで添える（**新規 → パッケージ** (New → Package)）。原文が英語で書いている名前は英語のまま。
- `<code>` の中に残る日本語（学生が読み替える語、画面に出る語）は、うしろに意味を添える（`(値 = value)`、`(または = or)`、`(Nth time)`）。
- Kotlin固有の用語を定義する文では、英語のうしろに日本語をかっこで添える（primary constructor (プライマリコンストラクタ)、smart cast (スマートキャスト)）。
- 全角の記号はASCIIにする（`＋` → `+`、`〜` の範囲 → en dash `–`）。サイドバーの「番号＋全角スペース＋題名」の全角スペースだけは残す。

## 繰り返し出る形

| 日本語 | English |
| --- | --- |
| STEP 07 · 2コマ目 · 目安 5分 | STEP 07 · Lesson 2 · About 5 min |
| 1コマ目 · STEP 00〜06 | Lesson 1 · STEP 00–06 |
| ミニ練習 / 完成（STEPの題） | Mini practice / Finished code |
| Nコマ目の完成 / Nコマ目を始める / Nコマ目のゴール（…） | Lesson N complete / Starting Lesson N / Lesson N goals (…) |
| 次へ：… → | Next: … → |
| src/ex01/main.kt · 完成コード / · 全体を置き換える / · ファイル全体 | · Completed code / · Replace the whole file / · Whole file |
| Runの結果 · このN行が出れば成功 | Run output · Success if these N lines appear |
| N / 36 ステップ確認済み | N / 36 steps checked（`config/i18n.json` の `ui.progress` と同じ） |
| 練習A/B/C / 演習 | Practice A/B/C / exercise |

## 照合の記録

### 共通：はじめの準備（`docs/common/setup.html`）

- 原文の版：`e2b5e5d`（`docs/common/setup.html` のSHA256 `5a0d0200d398842c8b85640ca843b08ff78fea97fcc81dcd3b8ca7278d1bab10`）
- 照合範囲：217文すべて。同じ原文を持つ8ページの261件に入る。
- 担当：翻訳は Codex の翻訳用subagent。独立照合は gpt-6-sol / high（対訳を並べて照合、2026-09-24）。照合後の修正は Claude Code / Opus 5.5。修正した文の再照合は Claude Code のsubagent / Sonnet 5（原文を見ずに逆翻訳を固定してから、原文・旧訳と比較）。
- 照合の全文：#37 のコメント。

| ID | 原文 | 指摘 | 対応 |
| --- | --- | --- | --- |
| `26889935868a` | 前半のKotlinのプロジェクトは… | 照合の前に、複数形から単数に直した訳の確認 | 対応不要（K01は1つで、単数が正しい） |
| `4ffc83df5a6a`・`aff83e6eeacc` | もとのページへ戻る | 引き継ぎ時の確認候補：previous page が行き先を表しているか | original page に直した（PR #42）。直接開くと、直前のページではなく既定のK01へ進むため。再照合：対応不要 |
| `7c5134e4ba6f` | …教科書を開いて始められます | 任意：命令形より、原文の可能の文に近づける | 採用（PR #42）。準備の前に読む枠なので、命令形だと今すぐ開く指示に読める。再照合：対応不要 |
| `c7b65f15818d` | この教材での扱い | ミャンマー語の照合で挙がった「使い方」への意味のずれが、英語の How it is used にもある | How these materials handle it に直した（#37）。原文にない「版」の語は足さない。再照合：対応不要（逆翻訳は「教材での扱い」） |
