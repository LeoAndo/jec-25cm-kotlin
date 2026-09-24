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

## 書き方の決まり

- 操作は命令形、説明と画面で確認する文は現在形で書く。
- 見出しはsentence caseにする。通常の引用は "…"、実際の日本語UIを囲む「」は保持して意味を添える。

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
