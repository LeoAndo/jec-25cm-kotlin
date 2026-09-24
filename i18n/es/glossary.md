# 用語集：Español（es）

Kotlin演習の対訳表。訳すときは、この表の訳語を使う。新しく訳語を決めた用語は、行を足す。全言語に共通の翻訳ルールは `skills/translate-teaching-materials/SKILL.md` にある。メモに「要確認」とある行は、訳語に自信がないもの。翻訳PRで確かめたら「要確認」を消す。

**中南米のスペイン語にそろえる（2026-09-24 オーナー決定）。** 言語コードは `es` のままにし、言葉選びで中南米に合わせる。スペインの言い方（ordenador、fichero、vosotros など）は使わない（下の「書き方の決まり」）。

## 製品名（訳さない）

| 日本語 | 訳 | メモ |
| --- | --- | --- |
| Kotlin | Kotlin | |
| IntelliJ IDEA | IntelliJ IDEA | |
| Android Studio | Android Studio | |

## 両科目に共通の用語（jec-25cm-hybrid-app とそろえる）

同じ学生が、同じ学期にハイブリッドアプリ開発技法（jec-25cm-hybrid-app）も受けている。この表の訳語と、下の「書き方の決まり」は、あちらの `i18n/es/glossary.md` と同じにしてある（2026-09-25、あちらの main `e82ddfa` と照合）。変えるときは、あちらも同じように直す。メモは、この授業での使い方に合わせて書き直してある。

| 日本語 | 訳 | メモ |
| --- | --- | --- |
| プロジェクト | proyecto | `K01HelloKotlin`・`A01HelloAndroid` などのプロジェクト名は訳さない |
| パッケージ | paquete | `ex01`・`jp.ac.jec.…` などのパッケージ名は訳さない |
| 関数 | función | `fun main()` の表記は原文のまま |
| 変数 | variable | `val` / `var` の表記は原文のまま |
| 実行 | ejecutar | 名詞は ejecución。原文が英語で書いているボタン名 **Run** は英語のまま。K01の日本語表示のメニュー名は、下の「IntelliJ IDEAの画面に出る日本語」 |
| コンソール | consola | 実行結果が出る場所 |
| エミュレータ | emulador | Androidエミュレータ（emulador de Android）。Android系の単元で使う |
| アプリ | aplicación | app とも言うが、訳文では aplicación にそろえる |
| ビルド | compilación | 動詞は compilar。build と英字のまま書く資料もある。要確認 |
| デバッグ | depuración | 動詞は depurar |
| 実機 | dispositivo físico | |
| デバイス | dispositivo | Android Studio のデバイス選択の画面名は英語のまま |
| テンプレート | plantilla | Android Studio のテンプレート名（**Empty Views Activity**）は英語のまま |
| プレビュー | vista previa | A04 の CameraX の `Preview` は `<code>` のまま |
| コマ | clase | 1コマ＝90分の授業1回。「2コマ目」は clase 2。Kotlinの「クラス」（`class`）も clase になるので、同じ文に両方が出て紛らわしいときは、コマを clase 2 のように番号つきで書き、クラスは la clase `Person` のようにクラス名を添える。この書き分けは要確認（訳語の clase は、あちらと同じにしておく） |

## Kotlin演習の用語

並びは、ほかの言語の用語集（`i18n/en/glossary.md` など）に合わせてある。

| 日本語 | 訳 | メモ |
| --- | --- | --- |
| 教材 | materiales | los materiales |
| 教科書 | libro de texto | |
| 単元 | unidad | |
| 版 | versión | |
| 完成プロジェクト | proyecto terminado | |
| 完成版 | versión terminada | |
| 見本 | ejemplo | 完成見本 → ejemplo terminado。配布物の `samples` フォルダの名前は訳さない |
| 実行結果 | salida | |
| 実行結果のウィンドウ | ventana de salida | |
| 画面 | pantalla | |
| ウィンドウ | ventana | |
| ツールウィンドウ | ventana de herramientas | |
| エディタ | editor | |
| コード補完 | autocompletado de código | |
| 実行の入口 | punto de entrada | |
| 実行設定 | configuración de ejecución | |
| ビルドツール | herramienta de compilación | ビルドの訳語にそろえる。要確認 |
| ライブラリ | biblioteca | librería とは書かない |
| 成功の目印 | Lo que deberías ver | |
| ここで止まって確認 | Detente aquí y verifica | |
| 公式資料 | documentación oficial | |
| もとのページ | página original | 共通資料の戻りリンク。página anterior にしない（直接開くと、直前のページではなく既定の単元へ戻るため） |
| 指定AVD | AVD designado | 男性名詞（el AVD）。AVD名 `jec_25cm_kotlin_Pixel 9a` は訳さない |
| 完成チェック | verificación final | |
| 困ったとき | Si tienes problemas | サイドバーのリンク |
| 完成プロジェクトを開く | Abrir el proyecto terminado | サイドバーのリンク |
| 共通資料 | material común | |
| 授業サポート | apoyo para la clase | |
| 共通：はじめの準備 | Común: Preparación inicial | サイドバーのリンク。`docs/common/setup.html` の見出しの訳とそろえる。要確認 |
| アレンジ | personalizar / personalización | |
| 赤い波線 | línea ondulada roja | |
| 確認日 | Última verificación | |
| 実行先 | dispositivo de destino | Android Studio の実行先の選択 |
| 部品（画面の） | elemento de la interfaz | |
| IDE | IDE | 男性名詞（el IDE） |
| URL | URL | 女性名詞（la URL） |
| UI | UI | 女性名詞（la UI） |
| 半角スペース | espacio de ancho medio | 日本語の入力に特有の言い方。要確認 |
| 進捗 / 目次（aria-label） | Progreso / Índice | |
| クラス | clase | `class` の表記は原文のまま。コマと同じ語になる（上の「コマ」のメモ） |
| 型 | tipo | |
| Null安全 | seguridad frente a null | 導入する文では null safety (Null安全) のように英語と日本語を添える。要確認 |
| 安全呼び出し | llamada segura | |
| 戻り値 / 戻り値の型 | valor de retorno / tipo de retorno | |
| 引数 | parámetro / argumento | 宣言の側は parámetro、呼び出しの側は argumento |
| 型注釈 / 型推論 | anotación de tipo / inferencia de tipos | |
| トップレベル関数 | función de nivel superior | 用語の表では トップレベル関数 — función de nivel superior |
| 再代入 | reasignar | |
| ガター | margen (gutter) | 行番号のとなりの ▷ が出る場所。要確認 |
| 途中コード / 途中画面 | código en progreso / pantalla en progreso | |
| 通信中の印 | indicador de carga | |
| 保存先 | ubicación de guardado | |
| 権限 / 許可・拒否 | permiso / permitir・denegar | エミュレータのダイアログの表示名は英語（**While using the app** など） |
| プライマリコンストラクタ | constructor primario | 定義する文では日本語を添える |
| バッキングフィールド | campo de respaldo | 同上 |
| スマートキャスト | conversión inteligente | 同上。smart cast と英字のまま書く資料も多い。要確認 |
| 拡張関数 / レシーバ型 | función de extensión / tipo receptor | 同上 |
| 名前付き引数 / 既定引数 | argumento con nombre / argumento predeterminado | 同上。Swift の引数ラベルは etiqueta de argumento |
| ラムダ式 / 委譲プロパティ | expresión lambda / propiedad delegada | 同上 |
| Google Classroom の表示 | 授業 (Trabajo de clase)、追加または作成 (Agregar o crear)、提出 (Entregar)、提出済み (Entregado)、提出を取り消す (Anular entrega) | 学生の画面の言語が分からないので、日本語を残してスペイン語の表示名を添える。要確認 |

## IntelliJ IDEAの画面に出る日本語（K01。日本語のまま残し、訳をかっこで添える）

K01の教科書は、日本語表示の IntelliJ IDEA のメニュー名を書いている。画面の言葉は訳さずに残し、うしろにこの表の訳をかっこで添える（例：**新規 → パッケージ** (Nuevo → Paquete)）。翻訳skillは、かっこにはその言語で表示したIDEの名前を添えるとしているが、IntelliJ IDEA が同梱している言語パックは日本語・韓国語・中国語で（翻訳skillの「前提」）、スペイン語の表示はない。そのため、この表の訳は実際の表示ではなく、意味を伝えるための訳である。スペイン語の表示が使えるようになったら、その表示で確かめて直す。原文が英語で書いている名前（**File → New → Project…** など）は英語のまま残す。

| 画面の言葉 | かっこに添える訳 | 場所 |
| --- | --- | --- |
| 新規… | Nuevo… | ホーム画面のメニュー |
| 新規プロジェクト… / 新規プロジェクト | Nuevo proyecto… / Nuevo proyecto | ホーム画面のメニュー／新規プロジェクトの画面の見出し |
| 開く… | Abrir… | ホーム画面のメニュー |
| ジェネレーター | Generadores | 新規プロジェクトの画面 |
| 場所 | Ubicación | 新規プロジェクトの画面 |
| プロジェクト | Proyecto | ツールウィンドウ |
| 新規 → パッケージ | Nuevo → Paquete | 右クリックのメニュー |
| 新規 → Kotlin ファイル/クラス | Nuevo → Clase/archivo de Kotlin | 右クリックのメニュー |
| ファイル / クラス | Archivo / Clase | 新しい Kotlin ファイルの種類の一覧 |
| 'MainKt' の実行 | Ejecutar 'MainKt' | ガターの ▷ のメニュー |
| 実行 | Ejecutar | ツールウィンドウ |
| 表示 → ツールウィンドウ → 実行 | Ver → Ventanas de herramientas → Ejecutar | メニュー |
| 新しいウィンドウ | Ventana nueva | プロジェクトを開くときのダイアログ |

## macOSの画面に出る日本語（日本語のまま残し、訳をかっこで添える）

| 画面の言葉 | かっこに添える訳 | 場所 |
| --- | --- | --- |
| 書類 | Documentos | Finder |
| ダウンロード | Descargas | Finder |
| アプリケーション | Aplicaciones | Finder |
| 移動 → ホーム | Ir → Inicio | Finder のメニュー。要確認 |

## 書き方の決まり

- **学生への呼びかけは tú にする。** 手順は tú の命令形で書く（Haz clic en **Run**.、Abre el archivo.）。usted・vos・vosotros は使わない。複数の人に向けるときは ustedes。
- **中南米の言い方にする。** スペインの言い方と分かれる語は、次の表の「中南米」の列の訳を使う。

  | 日本語 | 中南米（この用語集） | 使わない言い方 |
  | --- | --- | --- |
  | パソコン | computadora | ordenador |
  | ノートパソコン | laptop | portátil |
  | ファイル | archivo | fichero |
  | マウス | mouse | ratón |
  | キー・ボタンを押す | presionar | pulsar |
  | 画面をタップする | tocar | pulsar |
  | スマートフォン | celular | móvil |

- **疑問符と感嘆符は、文頭の ¿ ¡ と文末の ? ! を対で書く。**
- **見出しは文頭だけ大文字にする**（Tres objetivos）。英語のように各語の頭を大文字にしない。
- **引用符は “…”、引用の中の引用は ‘…’。** 画面やアプリに出る日本語を囲むときは「」のまま残してよい（翻訳skillのルール）。
- 学生と先生を指すときは、男女で形が変わらない語を選ぶ（estudiante、docente）。`config/i18n.json` の翻訳の注記（pregúntale a tu docente）も、この書き方にそろえてある。
- 英字の用語に冠詞を付けるときは、上の表のメモの性に従う（el IDE、la URL、la UI、el AVD）。

ここから下は、この授業だけの決まり。

- 確認欄（ここで止まって確認）は、画面で確かめられる状態を現在形で書く（Aparece…、Se muestra…）。「〜できた」「〜と言えた」のような振り返りの言い方にしない。
- Kotlin固有の用語を定義する文では、訳語のうしろに日本語をかっこで添える（constructor primario (プライマリコンストラクタ)）。
- 全角の記号はASCIIにする（`＋` → `+`、`〜` の範囲 → en dash `–`）。サイドバーの「番号＋全角スペース＋題名」の全角スペースだけは残す。

## 照合の記録

### 共通：はじめの準備（`docs/common/setup.html`）

- 原文の版：`7785786`（`docs/common/setup.html` のSHA256 `5a0d0200d398842c8b85640ca843b08ff78fea97fcc81dcd3b8ca7278d1bab10`。ほかの言語の `e2b5e5d` と同じ内容）
- 照合範囲：217文すべて。同じ原文でほかの7ページのカタログに入った44文は、そのページでの役割（表の見出しなど）だけを見た。
- 担当：翻訳は Antigravity / Gemini 3.8 Flash (High)（#80）。逆翻訳による照合は Claude Code / Opus 5.5（訳し戻しは、原文を見ない Claude Code の subagent / Opus 5.5、2026-09-25）。照合後の修正は Claude Code / Opus 5.5。修正した文と #90 で変わった3文の照合し直しは Claude Code の subagent / Sonnet 5（原文を見ずに逆翻訳を固定してから、別の subagent が原文と比較、2026-09-25）。照合し直しの17件は、すべて指摘なし。
- 照合の全文：PR #94 のコメント（照合、指摘への対応、照合し直し）。
- #90（2026-09-25）で原文の3文が変わった。原文の版：`134ec7a`（`docs/common/setup.html` のSHA256 `8e94def17d654d9a8a737dcb8100e8a2559890ac4ce5a5bbc9e0e791f13a7ed0`）。旧訳の3文（`178884106356`・`ecd84e748028`・`ef494d8c2da8`）はカタログから消えた。新しい3文（`a8be9db61ff2`・`edaa4d1af5f4`・`0425e93c10a7`）は Claude Code / Opus 5.5 が訳し、上の照合し直しで照合した。

| ID | 原文 | 指摘 | 対応 |
| --- | --- | --- | --- |
| `57788987ffb1` | 移動した先のフォルダを… | 要修正：carpeta de destino は「書類」そのものと読める | la carpeta que acabas de mover にした（PR #94）。照合し直し：対応不要 |
| `9eb121868fa3` | アプリケーションフォルダに… | 要修正：確認欄の文だけ、Finderの表示名の日本語が落ちている | アプリケーション (Aplicaciones) にした（PR #94。071と同じ形）。照合し直し：対応不要 |
| `828d4cec1f3c`（K01の `td`） | 場所 | 要修正：K01では日本語表示の IntelliJ IDEA の画面の項目名 | `i18n/es/hello-kotlin/index.json` の `overrides` で 場所 (Ubicación) にした（PR #94）。準備ガイドとA02〜A04の表の見出しは Ubicación のまま。照合し直し：対応不要 |
| `51d7d6a9e0ee`（K01の `th`） | 使うもの | 要修正：K01では列の中身がプロジェクトで、Herramienta は合わない | `i18n/es/hello-kotlin/index.json` の `overrides` で Lo que usarás にした（PR #94）。準備ガイドは Herramienta のまま。照合し直し：対応不要 |
| `72487ce81901`・`5c85b7d753dd`・`517fd4b8ada6`・`655af778cbe1`・`dee7449392f0` | 自分が作ったプロジェクトは…／準備なしで…／…それが入口になります／…時間がかかります／…ビルドツールを挟まない… | 任意：不自然な言い回し、表の列の人称、指す語の曖昧さ、1人称複数 | 採用（PR #94）。Los proyectos que creaste、Ejecutas… verificas…、esa función、tarda en、usarás／que no usa una herramienta de compilación aparte。照合し直し：対応不要 |
| `d207d4a66067`・`685b29533b7b` | …同じプログラムを動かせます／実行したいファイル… | 任意：correr と ejecutar が混ざる | ejecutar にそろえた（PR #94）。照合し直し：対応不要 |
| `f2fa84e375bf`・`0453f6c464a9`・`8e35209c2b3d` | …覚えておいてください／…つまずいたところは…／候補が1つも出ない… | 任意：memoriza は強い、te trabaste は口語、candidato は不自然 | 採用（PR #94）。ten presente、tuviste dificultades、ninguna opción。照合し直し：対応不要 |
| `ef494d8c2da8` | …足りないときだけ、先に進まずに先生に見せてください。 | 任意：avisa（知らせる）を、ほかの「見せる」と同じ muéstraselo に | #90 で原文が変わり、旧訳は消えた。新しい文 `0425e93c10a7` で muéstraselo にした。照合し直し：対応不要 |
| `0126fdc18f43` | …<code>Pixel</code> と <code>9a</code> の間は半角スペース… | 任意：espacio de ancho medio は全角・半角を知らない人に通じにくい | 採らない。この表の訳語どおりで、訳し戻しの担当は原文を見ずに「半角のスペース」と読めた。「半角スペース」の行の「要確認」は残す |
| `a8be9db61ff2`・`edaa4d1af5f4`・`0425e93c10a7` | 成功の目印の本文（合わせて5つ）／`index.html` があるとき／その注記の本文 | #90 で変わった3文の照合し直し。指摘なし | 対応不要（PR #94） |
