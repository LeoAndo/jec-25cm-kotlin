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
| 先生 / 教員 | tu docente | 冠詞の el を付けず、tu docente にそろえる（2026-09-25 オーナー決定、PR #94）。el docente だと冠詞が男性形になる。「先生が作った見本」は los ejemplos creados por tu docente |
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
| 困ったとき / うまくいかないとき | Si tienes problemas | サイドバーのリンクと、共通資料の「N. うまくいかないとき」の見出し |
| 完成プロジェクトを開く | Abrir el proyecto terminado | サイドバーのリンク |
| 共通資料 | material común | |
| 授業サポート | apoyo para la clase | |
| 共通：はじめの準備 | Común: Preparación inicial | サイドバーのリンクと、共通資料の本文のリンク。`docs/common/setup.html` の見出し（Preparación antes de empezar la clase）の短い言い方 |
| 共通：提出課題とAPK | Común: La tarea y el APK | 同上。`docs/common/apk.html` の題名は La tarea y cómo crear el APK |
| 共通：ちがうAndroid Studioの版 | Común: Otra versión de Android Studio | 同上。`docs/common/other-versions.html` の題名は Si usas otra versión de Android Studio |
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
| Google Classroom の表示 | 授業 (Trabajo en clase)、追加または作成 (Agregar o crear)、ファイル (Archivo)、提出 (Entregar)、提出済み (Entregada)、提出を取り消す (Anular la entrega)、未提出 (sin entregar) | 学生の画面の言語が分からないので、日本語を残してスペイン語の表示名を添える。表示名は Google Classroom ヘルプ「Cómo entregar una tarea」（`support.google.com/edu/classroom/answer/6020285?hl=es-419`）で確認した（2026-09-25）。「未提出」は先生の画面に出る語なので、表示名ではなく意味だけを小文字で添える |
| 提出課題 / 提出する / 提出 | tarea / entregar / entrega | Google Classroom の語にそろえる（tarea、Entregar）。「提出先」は dónde entregar |
| APK | APK | 男性名詞（el APK、el archivo APK）。「APKを作る」は crear el APK |
| デバッグ用 / リリース用（APK） | de depuración (debug) / de lanzamiento (release) | Android Studio のビルドの種類の名前を英語でかっこに添える |
| 署名 | firma (signing) | |
| コピーを取る | hacer una copia | Finder の **複製** は下の「macOSの画面に出る日本語」 |
| 元に戻す / 元に戻したいとき | volver al estado original / Si quieres volver al estado original | |
| ひな形 | proyecto plantilla | New Project ウィザードが生成したままのプロジェクト（`Panda2KotlinEmptyViewsActivity` など）。ウィザードのテンプレート（plantilla）と区別する |
| 読み替え / 読み替える | adaptación / sustituir por | 「A01の読み替え」は Adaptaciones para A01。「〜に読み替えてください」は Sustitúyelo por … |
| 照合 / 全文照合 | comparar / comparación completa | |
| 同期（Gradle） | sincronización | 「同期が赤い」は la sincronización aparece en rojo |
| 生成される設定 | configuración generada | |
| 基準 | estándar | 「授業の基準である Panda 2」は Panda 2, que es el estándar de la clase |
| 止まったとき | Si no puedes avanzar | 男女で形が変わる atascado/a を避ける |
| 確かめた範囲 | Lo que se verificó | |
| 内容（表の見出し） | Detalles | |
| 進め方 | Cómo proceder | |
| 起きたこと / やってみること | Lo que sucedió / Qué intentar | うまくいかないときの表の見出し |
| 完了の通知 | notificación de finalización | Build APK(s) のあとに右下に出るもの。**locate** は英語のまま |
| 更新日時 | fecha de modificación | Finder の表示 |
| 進み具合 / 進行表示 | progreso / indicador de progreso | |
| 表示の切り替え（Android / Project） | selector de vista | Android Studio 左上の切り替え。**Android**・**Project** は英語のまま |
| 赤い文字 | texto en rojo | |
| システムイメージ | imagen del sistema | |
| 検証用フォルダ / 検証コピー | carpeta de prueba / copia de prueba | |
| 段階別コード | código por etapas | |
| 余白処理 | código para los márgenes | A01 の生成コードが余白を調整する部分 |
| 手順N / N節 | paso N / sección N | 共通資料の「手順5」は paso 5 |
| 前半 / 後半 | primera mitad / segunda mitad | |
| 授業 / この授業 | la clase / esta materia | Google Classroom の「クラス」も clase なので、「この授業のクラス」は la clase de este curso |

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
| 複製 | Duplicar | Finder の右クリックのメニュー |
| （フォルダ名）のコピー | (A01HelloAndroid copia) | **複製** でできるフォルダの名前。`<code>A01HelloAndroidのコピー</code>` の中は日本語のまま残し、スペイン語表示の Mac でできる名前をかっこで添える |

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
- Google Classroom の表示名は、日本語のまま残して、上の表のスペイン語の表示名をかっこで添える（`<strong>提出</strong> (Entregar)`）。
- Finder の経路は、日本語の直後にかっこで訳を添えてから → を続ける（`<strong>書類 (Documentos) → Kotlin</strong>`）。英語版と同じ形。
- 範囲は en dash でつなぐ（STEP 00–13、STEP 02–03）。
- 同じページの見出しを本文で引用するときは “…” で囲み、その見出しの訳と1字も違えない（“Si quieres volver al estado original”、“Si no encuentras el menú”）。
- 手順の並びを示す → はそのまま残す（`<strong>probar que funciona → crear el APK de nuevo → cambiar el nombre</strong>`）。
