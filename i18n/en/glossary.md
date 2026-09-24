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
| Null安全 | null safety | 導入する文では null safety (Null安全) |
| 安全呼び出し | safe call | 定義する文・用語の表では日本語を添える |
| 戻り値 / 戻り値の型 | return value / return type | |
| 引数 | parameter / argument | 宣言の側は parameter、呼び出しの側は argument |
| 型注釈 / 型推論 | type annotation / type inference | |
| トップレベル関数 | top-level function | 用語の表では トップレベル関数 — top-level function |
| 再代入 | reassign | |
| ガター | gutter | 行番号のとなりの ▷ が出る場所 |
| 途中コード / 途中画面 | in-progress code / in-progress screen | |
| 通信中の印 | loading indicator | |
| 保存先 | save location | |
| 権限 / 許可・拒否 | permission / allow・deny | エミュレータのダイアログの表示名は英語（**While using the app** など） |
| Preview（A04） | Preview | CameraX の `Preview` を指すので大文字のまま。一般の「プレビュー」は preview |
| プライマリコンストラクタ | primary constructor | 定義する文では日本語を添える |
| バッキングフィールド | backing field | 同上 |
| スマートキャスト | smart cast | 同上 |
| 拡張関数 / レシーバ型 | extension function / receiver type | 同上 |
| 名前付き引数 / 既定引数 | named argument / default argument | Swift の引数ラベルは argument label |
| ラムダ式 / 委譲プロパティ | lambda expression / delegated property | 同上 |
| 使うもの（表の見出し） | Tool（setup）/ What you use（K01） | K01の完成プロジェクトの表だけ、カタログの `overrides` で訳し分ける |
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
- 担当：翻訳は Codex の翻訳用subagent（モデル名は記録されていない）。独立照合は gpt-6-sol / high（対訳を並べて照合、2026-09-24）。照合後の修正は Claude Code / Opus 5.5。修正した文の再照合は Claude Code のsubagent / Sonnet 5（原文を見ずに逆翻訳を固定してから、原文・旧訳と比較）。
- 照合の全文：#37 のコメント。
- #90（2026-09-25）で原文の3文が変わり、訳し直した。原文の版：`134ec7a`（`docs/common/setup.html` のSHA256 `8e94def17d654d9a8a737dcb8100e8a2559890ac4ce5a5bbc9e0e791f13a7ed0`）。訳し直しは Claude Code の翻訳用subagent（Opus 5.5）、照合は別のモデルの subagent（Sonnet 5、対訳を並べて照合）。照合の全文：PR #98 のコメント。使われなくなった旧訳の3文（`178884106356`・`ecd84e748028`・`ef494d8c2da8`）は、カタログから消えた。

| ID | 原文 | 指摘 | 対応 |
| --- | --- | --- | --- |
| `26889935868a` | 前半のKotlinのプロジェクトは… | 照合の前に、複数形から単数に直した訳の確認 | 対応不要（K01は1つで、単数が正しい） |
| `4ffc83df5a6a`・`aff83e6eeacc` | もとのページへ戻る | 引き継ぎ時の確認候補：previous page が行き先を表しているか | original page に直した（PR #42）。直接開くと、直前のページではなく既定のK01へ進むため。再照合：対応不要 |
| `7c5134e4ba6f` | …教科書を開いて始められます | 任意：命令形より、原文の可能の文に近づける | 採用（PR #42）。準備の前に読む枠なので、命令形だと今すぐ開く指示に読める。再照合：対応不要 |
| `c7b65f15818d` | この教材での扱い | ミャンマー語の照合で挙がった「使い方」への意味のずれが、英語の How it is used にもある | How these materials handle it に直した（#37）。原文にない「版」の語は足さない。再照合：対応不要（逆翻訳は「教材での扱い」） |
| `a8be9db61ff2`・`edaa4d1af5f4`・`0425e93c10a7` | 成功の目印の本文（合わせて5つ）／`index.html` があるとき／その注記の本文 | #90 で変わった3文の照合。任意2：注記の見出しを If `index.html` is present にする。注記の本文の2つ目の「そのまま読み進め」にも simply を付ける | 採らない（PR #98）。見出しは、直前の目印の「フォルダ」を受けた言い方で、誤りではない。simply の有無は、原文の「構いません」（許可）と「読み進めます」（指示）の違いに合わせた |

### 残りの全ページ（共通資料2ページ・A01〜A04・K01。#56 の配布準備）

- 原文の版：main `69c5d95`（2026-09-24）。原文の誤りを直した文は、直したあとの原文で訳し直した（#63：`e798c6c`、#65：`00ad03d`、#64：`f73323f`）。
- 照合範囲：共通資料2ページ（269文）、A01〜A04（920文）、K01（1,082文）の計2,271文と、訳し直した文。
- 担当：翻訳は Claude Code の翻訳用subagent（Opus 5.5）10体。照合は、翻訳した担当とは別のモデルの subagent（Sonnet 5）10体。照合の担当は、翻訳スキル・用語集・日本語のページを自分で読み、対訳を並べて照合した。照合のあとで訳を変えた文は、別の subagent（Sonnet 5）が照合し直した（PR #69 の決まり。#57・#58 の分も、オーナーの判断でさかのぼって照合し直した。カタログを直接直した準備ガイドの3文と other-versions の1文は、#56 で照合し直した）。
- 照合の全文：各PRのコメント（PR #66・#70・#73・#74・#76・#84・#86）。

| 範囲 | PR | 照合した文 | 指摘 | 対応 |
| --- | --- | --- | --- | --- |
| 共通資料（apk・other-versions） | #66 | 269 | 任意1 | 採らない（`<code>` に残る日本語に意味を添える決まりどおり） |
| A01 | #70 | 202 | 対応必要2、任意2 | 確認欄を has been checked に、"point to code" を "are about a style" に直した。「または」の添え書きは (または = or) の形で残した。単元の冒頭の「対象」は Project のまま |
| A02 | #70 | 247 | 任意1 | 採用（初回の実行 → The first time you run it） |
| A03 | #74 | 253 | 任意1 | #65 で原文が `<code>it</code>` になったので、訳し直しで対応 |
| A04 | #74 | 218 | 対応必要3、任意1 | 定義する文の日本語2件を採用。Preview の小文字化と lede の "You move" は、照合し直しの指摘で戻した |
| K01（1〜3コマ目） | #73 | 637 | 対応必要1、任意5 | 確認欄は状態を書く文に。smart cast の日本語は照合の前に直していた。2つ目の「書類」への添え書きは採らない |
| K01（4〜6コマ目と付録） | #76 | 445 | 対応必要2 | 確認欄を状態を書く文に（STEP 19 はまだ実行していないので、出力が一致するとは書かない） |
| 訳し直し（#63 の3文、#65 の2文） | #73・#74 | 5 | 任意1 | 採らない（隣のセルの「表示文字」の言い回しの違い。どちらも誤りではない） |
| 訳し直し（#64 の4文。提出先を Google Classroom に、表の向きを上から下に） | #62 | 4 | 対応必要1 | 採用（「手順は7」をページのほかの手順と同じ step 7 に）。直した文の照合し直し：対応不要 |
| 照合し直し（照合のあとで変えた文） | #73・#74・#76・#62 | 61 | 対応必要3 | 採用（「(トップレベル)」を外す、A04の Preview を大文字に、lede を命令形に）。#57・#58 の19文は対応不要 |
| `overrides`（K01の「使うもの」→ What you use） | #76 | 1 | 採用 | 準備ガイドの Tool はそのまま |
| 照合し直し（#66・#70 でカタログを直接直した4文：準備ガイドの Lesson の大文字2文と samples 1文、other-versions の target device 1文） | #86 | 4 | 任意1 | 採らない（同じ文の「Runの実行先」の Run target を Run target device にそろえる案。Run target で意味は通る） |
| 全角の ＋ を + に直した2文（A01・A03の Device Manager の手順） | #86 | 2 | なし | 対応不要（A02の訳とそろった） |

- 原文の誤りは訳では直さず、issue にして日本語を直した（#63・#64・#65）。直すまでのあいだは、英語も原文どおりに訳していた。
- 翻訳の担当が「照合の担当の案」と食い違ったときは、日本語のページとほかの言語の訳を読み直して決め、理由を各PRの本文に残した。
