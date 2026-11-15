# Figmaと共有CSSの対応付け

反映時には最新のFigmaとCSSを取得する。この文書は対応を調べる出発点で、色の現在値を複製して正本にするものではない。

## 参照先と範囲

- [K01 HelloKotlin 教科書｜PC版](https://www.figma.com/design/H7wKSKRPfDzvorCN16Gluu?node-id=2-2)
- fileKey: `H7wKSKRPfDzvorCN16Gluu`
- ページ: `K01 教科書・PC`（`0:1`）。基準フレーム: `K01 HelloKotlin｜PC 1440px`（`2:2`）。
- 用途色: `教科書｜色`（`VariableCollectionId:11:3`）、基本色: `教科書｜パレット`（`VariableCollectionId:11:2`）、書体・太さ: `教科書｜書体`（`VariableCollectionId:11:4`）。モードはライト。
- K01を共有デザインの代表とし、Android系も同じCSSを使う。2026-11-15の初回整備では用途色45、基本色38、書体・太さ7、Text Styles61、編集可能なTEXT2247。固定の件数を今後の合格条件にはしない。
- 名前だけで対応を決めず、変数ID・モード・解決値・ノードへの関連付けを確認する。取り込み時の改行やレイヤー分割で教材本文を変更しない。

## CSSのスコープ

`docs/assets/textbook.css` の前半は共通資料・教員用ガイドも使う基本規則、後半の `.textbook` は単元教科書用の規則。`:root` と `.textbook` にある同名の色変数は異なる値を持つため、対象ページの有効値を調べる。書体は `:root` の `--font-body` と `--font-code` に集約し、言語別フォールバックを保つ。`.textbook` の `--palette-*` は基本色で、用途変数がそこを参照する。Figmaも同じalias関係を持つ。

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
| コード操作ボタンの境界・hover背景 | `--code-button-border`、`--code-button-hover-bg` |
| ファイル・練習・ボタン | `--file-icon-border`、`--task-border`、`--action-bg` |
| 参照コード | `--reference-heading-bg`、`--reference-code-bg` |
| フォーカス・キーボード | `--focus-ring`、`--kbd-border` |

- 同じ初期値でも、確認欄の緑・構文の文字列・追加行の緑は別用途。参照するパレットと適用先を見て反映範囲を決める。
- `.diff` の `<ins>`・`<del>`・`.diff-gap` は学習上の意味を持つ。太字、取り消し線、行頭線を残す。構文強調で中身を平らなテキストに戻さない。
- `pre.diff` の `--diff-padding` と追加／削除行の負のmarginは連動する。コードpaddingを変える場合は横スクロール時の帯を確認する。
- Kotlin/Java/Swift比較は `.compare` と `.compare-item pre`。通常のコード枠と違い、長い行を折り返して見比べる。文字サイズ変更のときもページ全体の横はみ出しを許容しない。
- チェックボックスはHTMLではネイティブinput。Figmaの取り込み図形を根拠に、操作を独自の図形へ作り替えない。
- 影変数は色と不透明度を示す。位置やぼかしまで同時に変更されたとは判断しない。

## ブラウザ標準チェックボックスの例外

用途色45のうち42は実CSS変数に対応する。残る `--browser-checkbox-border`・`--browser-checkbox-background`・`--browser-checkbox-mark` は取り込み時のブラウザ標準の参考値で、CSSには未定義。基本色38のうち37はCSSにあり、`--browser-palette-767676` だけが標準枠線の参考値。これらのコード構文は対応を調べる名前で、実装済みトークンではない。

HTMLはネイティブinputと `accent-color` を維持する。Figmaの参考値を変えただけで独自チェックボックスへ作り替えず、変更する表示と操作状態を確定してからCSS側の対応を決める。

## 書体と寸法

本文は `--font-body`（Noto Sans JP）、コードは `--font-code`（Roboto Mono、日本語はNoto Sans JP）。`pre/code/kbd` だけでなくSTEP番号、ファイル名、アイコン、パスにも使うため `font-family` と `font` shorthandを両方検索する。

太さは `--font-weight-400/600/700/750/800` とFigmaのFLOAT変数を対応させ、fontFamilyとfontWeightの両方をText Styleへ結び付ける。共通資料の既存650はCSSの `--font-weight-650` に残す。これらは既存の明示値を変数化したもので、本文400や見出し700などブラウザ既定・継承に由来する太さは、変数の変更だけではすべて変わらない。太さを反映するときはブラウザ既定、`bolder`、継承を含む実効値を照合し、変更対象の用途へ必要な `font-weight` 規則を追加する。初回は全テキスト区間のstyle関連付けと実ウェイトが変わらないことを確認した。文字サイズ・行高・字間は用途ごとのCSS規則にある。FigmaのText Style名から推測せず、実ノードの解決値を比較する。初期値は単元本文18px、コード16px。比較コードも16pxで、印刷規則は別に持つ。

中国語各種・韓国語・アラビア語・ミャンマー語・モンゴル語の既存書体と、翻訳内の日本語指定を保つ。RTL本文とLTRコードの分離、論理方向のpadding／borderも維持する。

## 取り込み時の文章とコード

初回はHTMLの文章と照合した565個の混在インラインコンテナを、書体・サイズ・太さ・色・装飾・リンクを保持したリッチテキストへ整理した。段落内のcode/kbdの背景枠はA01と同じく編集・折り返しを優先して省略したが、HTMLには残す。通常のコードは改行を保持して横にはみ出す行を枠で切り、比較コードは折り返す。コード枠の高さは内容に追従し、差分の追加・削除・既存行を区別する。Figmaの全ページ高や文章の改行をHTMLへ固定値で写さない。
