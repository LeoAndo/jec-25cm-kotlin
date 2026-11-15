# Figmaと共有CSSの対応付け

反映時には最新のFigmaとCSSを取得する。この文書は対応を調べる出発点で、色の現在値を複製して正本にするものではない。

## 参照先と範囲

- [K01 HelloKotlin 教科書｜PC版](https://www.figma.com/design/H7wKSKRPfDzvorCN16Gluu)
- fileKey: `H7wKSKRPfDzvorCN16Gluu`
- K01を共有デザインの代表とし、Android系も同じCSSを使う。具体的なノードIDは今回の取得結果とPRに記録する。
- 名前だけで対応を決めず、変数ID・モード・解決値・ノードへの関連付けを確認する。取り込み時の改行やレイヤー分割で教材本文を変更しない。

## CSSのスコープ

`docs/assets/textbook.css` の前半は共通資料・教員用ガイドも使う基本規則、後半の `.textbook` は単元教科書用の規則。`:root` と `.textbook` にある同名の色変数は異なる値を持つため、対象ページの有効値を調べる。書体は `:root` の `--font-body` と `--font-code` に集約し、言語別フォールバックを保つ。

## 用途とCSS

| 用途 | CSS変数・対象 |
| --- | --- |
| 本文・補助・ページ・境界線・強調・確認背景 | `--ink`、`--muted`、`--paper`、`--line`、`--blue`、`--mint` |
| 目標・注意 | `--surface-goal`、`--surface-note`、`--note-border`、`--note-title` |
| コードの背景・見出し・境界・インライン | `--surface-code`、`--surface-code-heading`、`--border-code`、`--code-inline-bg` |
| 構文のキーワード・文字列・型・コメント | `--syntax-keyword`、`--syntax-string`、`--syntax-type`、`--syntax-comment` |
| 目次の境界・選択・背景・影 | `--nav-border`、`--nav-selected-bg`、`--nav-selected-text`、`--nav-menu-bg`、`--menu-shadow` |
| 確認欄の強調・枠 | `--check-accent`、`--check-border`。ネイティブcheckboxは `accent-color` |
| 追加行の背景・文字・境界 | `--diff-add-bg`、`--diff-add-text`、`--diff-add-border` |
| 削除行の背景・文字・境界 | `--diff-del-bg`、`--diff-del-text`、`--diff-del-border` |
| 既存行・省略記号 | `--diff-keep-text`、`--diff-keep-border`、`--surface-code` |
| ファイル・練習・ボタン | `--file-icon-border`、`--task-border`、`--action-bg` |
| 参照コード | `--reference-heading-bg`、`--reference-code-bg` |
| フォーカス・キーボード | `--focus-ring`、`--kbd-border` |

- 同じ初期値でも、確認欄の緑・構文の文字列・追加行の緑は別用途。参照するパレットと適用先を見て反映範囲を決める。
- `.diff` の `<ins>`・`<del>`・`.diff-gap` は学習上の意味を持つ。太字、取り消し線、行頭線を残す。構文強調で中身を平らなテキストに戻さない。
- `pre.diff` の `--diff-padding` と追加／削除行の負のmarginは連動する。コードpaddingを変える場合は横スクロール時の帯を確認する。
- Kotlin/Java/Swift比較は `.compare` と `.compare-item pre`。通常のコード枠と違い、長い行を折り返して見比べる。文字サイズ変更のときもページ全体の横はみ出しを許容しない。
- チェックボックスはHTMLではネイティブinput。Figmaの取り込み図形を根拠に、操作を独自の図形へ作り替えない。
- 影変数は色と不透明度を示す。位置やぼかしまで同時に変更されたとは判断しない。

## 書体と寸法

本文は `--font-body`（Noto Sans JP）、コードは `--font-code`（Roboto Mono、日本語はNoto Sans JP）。`pre/code/kbd` だけでなくSTEP番号、ファイル名、アイコン、パスにも使うため `font-family` と `font` shorthandを両方検索する。

文字サイズ・太さ・行高・字間は用途ごとのCSS規則にある。FigmaのText Style名から推測せず、実ノードの解決値を比較する。初期値は単元本文18px、コード16px。比較コードも16pxで、印刷規則は別に持つ。

中国語各種・韓国語・アラビア語・ミャンマー語・モンゴル語の既存書体と、翻訳内の日本語指定を保つ。RTL本文とLTRコードの分離、論理方向のpadding／borderも維持する。
