# Kotlin演習 — 授業用教材

JEC（25CM）の「Kotlin演習」で使う教材です。**1コマ90分**、**全15コマ**の授業を想定しています。

**受講生は Java と Swift を学習済みで、Kotlinを初めて書きます。** プログラミングの入門ではなく、**知っている言語との差分でKotlinを覚える授業**です。変数・条件分岐・繰り返し・クラスといった概念そのものは説明しません。説明するのは、Kotlinでの書き方と、Java／Swiftとの違い、そして違う理由です。そのため各単元の各STEPには、JavaかSwift（または両方）との比較を必ず置きます。予習なしで、授業内の操作・確認・ミニ練習まで進められる構成は変えません。

単元は2系統あります。前半は IntelliJ IDEA でコンソールアプリを書く**純Kotlin系（`K01` の1単元だけ）**、後半は Android Studio でアプリを作る**Android系（`A01`〜）**です。使うIDEが単元によって変わるので、教科書とサイドバーでは、いまどちらのIDEを開くのかを必ず先に書きます。

## 教科書一覧

- [K01：HelloKotlin — Kotlinを動かしてみよう](docs/hello-kotlin/index.html)
- [完成プロジェクト（初回から参照可能）](docs/hello-kotlin/downloads/K01HelloKotlin.zip)
- [共通資料：授業を始めるまでの準備（教材の受け取りから最初の実行まで）](docs/common/setup.html)
- [共通資料：提出課題とAPKの作り方（自分で作ったアプリを1つ選んで提出する）](docs/common/apk.html)
- [共通資料：ちがうAndroid Studioのバージョンで進めるとき](docs/common/other-versions.html)
- [教員用：K01HelloKotlinの授業の進め方・確認項目](teacher/hello-kotlin/index.html)
- [A01：HelloAndroid — Kotlinで画面を動かそう](docs/hello-android/index.html)
- [A01の完成プロジェクト](docs/hello-android/downloads/A01HelloAndroid.zip)
- [教員用：A01HelloAndroidの授業の進め方・確認項目](teacher/hello-android/index.html)
- [A02：CalcGame — 計算ゲームを作ろう](docs/calc-game/index.html)
- [A02の完成プロジェクト](docs/calc-game/downloads/A02CalcGame.zip)
- [教員用：A02CalcGameの授業の進め方・確認項目](teacher/calc-game/index.html)
- [A03：GithubSearch — GitHubのリポジトリを検索しよう](docs/github-search/index.html)
- [A03の完成プロジェクト](docs/github-search/downloads/A03GithubSearch.zip)
- [教員用：A03GithubSearchの授業の進め方・確認項目](teacher/github-search/index.html)
- [A04：FunnyCamera — カメラにキャラクターを重ねよう](docs/funny-camera/index.html)
- [A04の完成プロジェクト](docs/funny-camera/downloads/A04FunnyCamera.zip)
- [教員用：A04FunnyCameraの授業の進め方・確認項目](teacher/funny-camera/index.html)

**K01は、全6コマぶん（`ex01`〜`ex11`）の教科書と教員用ガイドがそろっています。** 教科書は `docs/hello-kotlin/index.html` の1冊です。Android系はA01（STEP 00〜13）とA02（STEP 00〜14）の各2コマぶんの教科書・教員用ガイド・配布登録がそろっています。A03（STEP 00〜18）の3コマぶんも登録済みです。A04（STEP 00〜14）の2コマぶんもそろい、全15コマを登録済みです。

### 開き方

教員はこのリポジトリをダウンロードした後、Finderで `docs/hello-kotlin/index.html` をダブルクリックし、ブラウザで開きます。GitHub上のHTMLファイルはソース表示になるため、ローカルで開いてください。教材の本文・操作機能は外部ライブラリを使わず、オフラインで利用できます。IntelliJ IDEAとAndroid Studioの初回準備・ビルドと、公式資料の閲覧にはインターネット接続が必要です。

ブラウザの印刷（macOS：`⌘ P`）で、教材を紙やPDFに出力できます。チェック欄は自分の進み具合を確認するためのものです。教員への提出・送信は行いません。

### 学生への配布

学生には [最新の教材リリース](https://github.com/LeoAndo/jec-25cm-kotlin/releases/latest) の Assets にあるZIPを案内します（初回公開後から利用可能）。ファイル名には `kotlin-student-materials-2026-09-23-a81c6585fd87.zip` のように版の日付とコミットIDの先頭12文字が入り、展開してできるフォルダも同じ名前になります。同じ日の別コミットから作った版でも名前が分かれ、同じ場所に展開しても混ざりません。

**授業で指定するときは、日付と末尾の12文字をセットで示します。** Google Classroomの投稿にもその日のZIP名を載せ、学生は開く前にフォルダ名と照合します。同じコミットから作り直したZIPは同じ名前になります。過去の公開版の検出は版タグで行い、日付だけの旧ZIP名もリリーススクリプトの入力として引き続き受け付けます。

展開後、はじめて授業を受ける学生は [共通資料：授業を始めるまでの準備](docs/common/setup.html) をブラウザで開き、上から順に準備します（同梱の `はじめに.txt` でも、単元一覧より前に案内しています）。準備が済んだら、その日の単元の教科書（第1回なら `docs/hello-kotlin/index.html`）をブラウザで開きます。完成プロジェクトは、展開済みの見本として配布物の `samples` フォルダに入っています。IntelliJ IDEA か Android Studio の Open で `samples/K01HelloKotlin` のように選ぶだけで開け、初回から参考資料として使えます（各教科書からZIPでも受け取れます）。

学生用ZIPには `docs` 一式と、展開済みの完成プロジェクト（`samples`）、開き方・版情報を収録します。**いまは日本語だけの構成で配布します。** 展開してできたフォルダの中身は `docs` / `samples` / `はじめに.txt` / `VERSION.json` の4つで、言語を選ぶ入口はありません。`config/i18n.json` の5言語がすべて `distribute: false` のためです（「多言語展開」）。翻訳を終えた言語を `distribute: true` にすると、言語を選ぶ入口の `index.html` がZIPに入り、`はじめに.txt` にも各言語の案内が付きます。`teacher` フォルダと、教員が確認に使うひな形（`Panda2KotlinEmptyViewsActivity` / `Quail4KotlinEmptyViewsActivity`）は収録しません。GitHubが自動で表示する **Source code (zip)** はリポジトリ全体のため、学生用ZIPには使いません。なお、このリポジトリ自体はPublicなので、教員用ファイルもGitHub上では閲覧できます。

授業中は教員が指定した版を使います。授業ごとの案内には、内容が固定された個別リリースのURLを使ってください。更新版は別フォルダに展開し、学生自身のプロジェクトは上書きしません。

各単元で、学生自身が毎回IDEからプロジェクトを新規作成します（純Kotlin系は IntelliJ IDEA、Android系は Android Studio）。完成版は動作確認とコード比較の参考資料として使います。作成先は `/Users/ユーザ名/Documents/Kotlin/<プロジェクト名>` です。

### 15コマ計画

**この割り当ては仮です。実際のコマ数は授業の進み具合に合わせて見直します。** 1コマ90分、合計で全15コマです。

受講生はJavaとSwiftを書けるので、文法そのものの説明は短く済みます。そのぶんの時間を「**Java／Swiftではこう書く → Kotlinではこう書く → 何が変わったか**」に使う前提で割り当てています。

| コマ | 単元 | 内容 | プロジェクト |
| --- | --- | --- | --- |
| 1–6 | K01 HelloKotlin | Kotlinの文法（前年度資料の §4〜§16 ＝ `ex01`〜`ex11`） | `K01HelloKotlin` |
| 7–8 | A01 HelloAndroid | KotlinでAndroidアプリを作る | `A01HelloAndroid` |
| 9–10 | A02 CalcGame | 停止・再開するタイマーと10問の計算ゲーム | `A02CalcGame` |
| 11–13 | A03 GithubSearch | 入力画面・固定データの一覧・Web API検索 | `A03GithubSearch` |
| 14–15 | A04 FunnyCamera | カメラのプレビュー・ドラッグ・合成画像の保存 | `A04FunnyCamera` |

K01の授業順は次のとおりです（2026-09-23、オーナー決定）。`exNN` は前年度資料との対応番号なので、授業順に合わせて付け替えません。

| コマ | 演習を進める順 |
| --- | --- |
| 1 | `ex01` 変数・数の型 |
| 2 | `ex02` Null安全 |
| 3 | `ex03` 関数 |
| 4 | `ex05` 条件式 → `ex06` 繰り返し → `ex04` クラス |
| 5 | `ex08` アクセサ → `ex09` data class → `ex07` 拡張関数 |
| 6 | `ex10` map → `ex11` lazy |

リストを作って読む操作を `map` より先に、クラスとプロパティをアクセサ・data classより先に置きます。前年度資料の節との対応は、下の「前年度の教材との関係」にあります。

**K01の全6コマ・11演習を、同じ教科書に掲載しています。** `docs/hello-kotlin/index.html` のSTEP 00〜35と教員用ガイドが対応し、`config/teaching-materials.json` の `packages`・`sources` には `ex01`〜`ex11` を登録しています。授業のコマ数を表す `sessions` は6のままです。

**純Kotlin系の単元は K01 の1つだけです。** K02以降は作りません。プロジェクトも `K01HelloKotlin` という1つのIntelliJ IDEAプロジェクトだけで、回を重ねるごとに `src/exNN/` のパッケージを足していきます。**単元ごとに別プロジェクトにしないのは、次の理由からです。**

- 1コマで書くコードは十数行です。毎回プロジェクトを作ると、90分のうち15〜20分がNew Projectウィザードの操作に消えます。
- 前の回に書いたコードが同じプロジェクトに並ぶので、学生がいつでも見返せます。
- 前年度の資料も、1つのプロジェクトにファイルを足していく形でした（「前年度の教材との関係」）。

**Android系（`A01`〜）は、いままでどおり単元ごとに別のAndroid Studioプロジェクトを作ります。** ウィザードでどの選択肢を選ぶかが教える対象そのものであること、そして `applicationId` が単元ごとに違い、1つのプロジェクトには同居できないためです。

**K01は6コマあり、1コマで複数の文法項目を扱う回があります。** 「1単元で導入する新概念は1つまで」（「基本方針」1、「単元の範囲の決め方」1）との関係は、下の「単元の範囲の決め方（全単元共通）」の「純Kotlin単元（K01）での新概念の数え方」にまとめています。

`config/teaching-materials.json` の `projects` には、教科書がそろったK01（6コマ）・A01（2コマ）・A02（2コマ）・A03（3コマ）・A04（2コマ）の計15コマを登録しています。登録と教科書・教員用ガイド・完成プロジェクト・配布ZIPをそろえ、`scripts/check-teaching-materials.py` で照合します。純Kotlin系（`kind` が `"kotlin-console"`）の単元は、扱う演習を **`packages`（配列）** に書きます（1つだけでも `["ex01"]` のように配列にします）。Android系（`kind` が `"android"`）の単元は、いままでどおり **`package`（文字列）** にKotlinパッケージ名を書きます。

### 提出課題

**学生は、自分で作ったAndroidアプリを1つ選び、アレンジを加えて、APKというファイルにして提出します。** 手順の詳細（コピーの取り方、アレンジの進め方、APKの作り方と見つけ方）は [共通資料：提出課題とAPKの作り方](docs/common/apk.html) にあります。ここには、この授業としての決めごとだけを書きます。

| 項目 | 決めごと |
| --- | --- |
| 選ぶ本数 | 1つ |
| 選べるもの | Android系の単元（`A01`〜）で、**学生自身が作ったプロジェクト** |
| 提出するもの | アレンジを加えたアプリのAPK（デバッグビルド） |
| 提出先 | この授業の Google Classroom（手順は [共通資料：提出課題とAPKの作り方](docs/common/apk.html) の7） |
| 締め切り | 授業で教員が案内します |

- **純Kotlin系（`K01HelloKotlin`）は対象外です。** IntelliJ IDEA で `fun main()` を実行するコンソールアプリで、Androidアプリではないため、APKにできません。選べるのはAndroid系の単元で作ったアプリだけです。
- **配布している完成プロジェクト（見本）をそのまま出しても、提出にはなりません。** 提出するのは、学生自身が授業で作ったプロジェクトに、学生自身がアレンジを加えたものです。完成プロジェクトは動作確認とコード比較のための参考資料という位置づけを変えません（「学生への配布」）。
- **提出先は Google Classroom と決めて、教材にも書きます**（オーナーの判断、2026-09-25。#64）。教材の配布にも同じクラスを使っているので、学生は迷いません。**締め切りは年度や運用で変わるため教材には書かず**、授業で教員が案内します。
- 提出するのはデバッグビルドのAPKです。署名鍵の作成・リリースビルド・ストアへの公開は、この授業では扱いません。

**参照元の「Androidプログラミング1」は3つ提出ですが、この授業は1つです。** あちらはAndroidだけを扱う授業なので、学生が作るアプリの本数が多くなります。こちらはKotlinの文法から入るため、全15コマのうちAndroid系に使えるのは9コマ（`A01`〜`A04`）で、学生が授業中に作るAndroidアプリは4本です。母数が4本では、3つ選んでも「選ぶ」余地がほとんど残らず、1本あたりのアレンジも薄くなります。本数ではなくアレンジの中身を見る方針にして、1つに絞ります。

Android系はA01〜A04の4冊の教科書がそろっています。提出時期は授業で案内し、その時点までに学生自身が作ったアプリから1つ選びます。

### 前年度の教材との関係

2025年度の「Kotlin演習」では、`2025-01_Kotlin演習_Kotlinプログラミングの基本.pdf` という配布資料を使いました。この資料は冒頭で「Kotlinを最短で習得できるように他言語（Java, Swift）と比較しながら解説したい」と宣言し、最後まで **「プログラミング」→「プログラム実行結果」→「他言語との比較」→「POINT」** という同じ型で書かれています。**今年のHTML教科書は、この型と比較方式を引き継ぎます。**

前年度の資料も、1つの `HelloKotlin` プロジェクトに節ごとのファイルを足していく形でした。今年の `K01HelloKotlin` も同じ形で、ファイルの代わりに `src/exNN/` のパッケージを足していきます。

資料の各節と `K01HelloKotlin/src/exNN/` の演習は、次のように対応しています。演習番号はこの対応表のまま保ち、授業では上の「15コマ計画」に記した順に進めます。

| 前年度資料の節 | 内容 | 対応する演習 |
| --- | --- | --- |
| 1 はじめに | Kotlinの成り立ち。Javaと比較して学ぶと宣言 | — |
| 2 Kotlinの概要 | 実行環境（JVM言語）、特徴（可読性・Javaとの相互運用・Null安全・Javaの資産） | — |
| 3 開発環境：Playground編 | まずブラウザで動かす。IDEはそのあと | — |
| 4 変数宣言、代入処理 | `val` / `var`、型推論、セミコロン不要 | `ex01` |
| 5 Null許容の変数宣言と安全な呼び出し | `?`、`?.` | `ex02` |
| 6 メソッド作成 | `fun`、`引数名: 型`、戻り値の `: 型` | `ex03` |
| 7 クラス作成 | プライマリコンストラクタ、`new` 不要、`val` / `var` とアクセサ | `ex04` |
| 7.4 バイトコードの確認方法 | Show Kotlin Bytecode → Decompile | — |
| 8 条件式（if文） | `==` で文字列を比較できる | `ex05` |
| 9 繰り返し（for文） | `for (x in list)` | `ex06` |
| 10 拡張メソッド | Swiftのextensionと同じ発想 | `ex07` |
| 11 アクセサメソッドをカスタマイズ | `get()` / `set()`、`field` | `ex08` |
| 12 data class | `equals` / `hashCode` / `toString` の自動生成 | `ex09` |
| 13 スマートキャスト | `is` のあとキャスト不要 | — |
| 14 Kotlin Standard Library | — | — |
| 15 コレクション変換操作：map関数 | `map { }` | `ex10` |
| 16 Lazyプロパティ | `by lazy` | `ex11` |
| 17 まとめ / 18 ドキュメント | — | — |

**この資料PDFはリポジトリにcommitしません。** 置き場は `~/Documents/jec-25cm-kotlin-verification-deliverables/` で、リポジトリの外です。教材を書くときの参照元としてだけ使い、学生への配布物（`docs/` と学生用ZIP）には含めません。今年の教材として学生が読むのは、HTMLの教科書だけです。

### 教員が確認に使うプロジェクト

| フォルダ | 役割 |
| --- | --- |
| `Panda2KotlinEmptyViewsActivity` | **授業の基準バージョン Android Studio Panda 2** の Kotlin / Empty Views Activity のひな形（学生には配布しません）。学生が New Project で作る出発点は、これと同じ形になります。AGP 9.1.1／Gradle 9.3.1／compileSdk 36／targetSdk 36 |
| `Quail4KotlinEmptyViewsActivity` | 上と同じ設定を、基準より新しい **Android Studio Quail 4** で作ったひな形（学生には配布しません）。基準との差分を確認するための比較用。AGP 9.4.1／Gradle 9.6.0／compileSdk 37／targetSdk 37 |
| `K01HelloKotlin` | **純Kotlin単元（K01、1〜6コマ目）の完成プロジェクト。** 純Kotlin系はこの1つだけです。Gradleを使わないIntelliJ IDEAプロジェクトで、演習ごとに `src/exNN/` のパッケージを持つ（`exNN` は前年度資料の節に対応）。**学生への配布対象**で、配布用ZIPを教科書に同梱し、初回から学生も参照可能 |
| `A01HelloAndroid` | 完成プロジェクト。TextViewとButton、Snackbar・Toast・Logcatでの結果の出し分けを扱う。**教科書・教員用ガイド・学生への配布登録済み** |
| `A02CalcGame` | 完成プロジェクト。Chronometerで時間を計りながら計算問題に答えるゲーム。**教科書・教員用ガイド・学生への配布登録済み** |
| `A03GithubSearch` | 完成プロジェクト。GitHubの検索APIをKtorで呼び、結果をRecyclerViewで一覧表示する。中身の説明は [`A03GithubSearch/README.md`](A03GithubSearch/README.md) にある。**教科書・教員用ガイド・学生への配布登録済み** |
| `A04FunnyCamera` | 完成プロジェクト。CameraXのプレビューにキャラクターを重ね、合成した画像を保存する。中身の説明は [`A04FunnyCamera/README.md`](A04FunnyCamera/README.md) にある。**教科書・教員用ガイド・学生への配布登録済み** |

2つのひな形は、Android Studioの版が変わったときに、New Projectウィザードが生成するコードや設定がどう変わるかを見るために置いています。教材のスクリーンショットや手順が古くなっていないかは、この2つを見比べて確かめます。単元ではないので `config/teaching-materials.json` には登録せず、学生用ZIPにも入りません。

**A01の教材と同じ時期に、[ちがうAndroid Studioの版で進める共通資料](docs/common/other-versions.html)を整備しました（issue #5、オーナー決定）。Panda 3は実測せず、互換性を確認済みとしては案内しません。**

**授業の基準バージョンは Android Studio Panda 2 です。** Android系の単元の教科書は、Panda 2 の New Project ウィザードの画面と、Panda 2 が生成する設定を前提に書きます。スクリーンショットも Panda 2 で撮ります。教員の開発マシンには Quail 4 が入っていますが（下の「開発環境：教員」）、教材の基準は Panda 2 です。

**完成プロジェクト `A01HelloAndroid`〜`A04FunnyCamera` は、Panda 2 のひな形と同じ構成にそろえてあります。**そろえたのはバージョン番号だけではありません。Quail 4 のウィザードだけが作る形が3つあり、それも Panda 2 の形に戻しています。

| そろえた場所 | Quail 4 が作る形 | Panda 2 の形（現在） |
| --- | --- | --- |
| `gradle/libs.versions.toml` | agp 9.4.1／coreKtx 1.19.0／`activity-ktx` | agp 9.1.1／coreKtx 1.17.0／`activity` |
| `app/build.gradle.kts` の compileSdk | `release(37)` | `release(36) { minorApiLevel = 1 }` |
| `app/build.gradle.kts` の targetSdk | 37 | 36 |
| `app/build.gradle.kts` の `buildTypes` | `optimization { enable = false }` | `isMinifyEnabled` ＋ `proguardFiles(...)` |
| R8のkeepルール | `app/src/main/keepRules/rules.keep` | `app/proguard-rules.pro` |
| `gradle/wrapper/gradle-wrapper.properties` | Gradle 9.6.0 | Gradle 9.3.1 |
| `gradle/gradle-daemon-jvm.properties` | toolchain 25 | toolchain 21 |
| `gradle.properties` | `org.gradle.configuration-cache=true` あり | なし |

下の3つは、バージョン表を見ているだけでは気付けません。とくに `optimization { enable = false }` は AGP 9.4 で入った書き方なので、バージョンだけ下げると AGP 9.1.1 で構成エラーになります。`keepRules/rules.keep` も Quail 4 のウィザードだけが作るファイルです。

**Android系の完成プロジェクトを新しく作るときは、`Panda2KotlinEmptyViewsActivity` と上の8か所を突き合わせてください。** 教員の開発マシンには Quail 4 が入っているので、手元で New Project したものをそのまま完成プロジェクトにすると、また Quail 4 の形が混ざります。

教員用ガイドとSTEPごとの照合用コードは `teacher/<スラッグ>/` にまとめます（K01は `teacher/hello-kotlin`、A01は `teacher/hello-android`、A02は `teacher/calc-game`、A03は `teacher/github-search`、A04は `teacher/funny-camera`）。完成版の見本は、配布物の `samples` フォルダに展開済みで入っています。学生が自分で置き場所を作ったり、ZIPを展開したりする必要はありません。

### 完成プロジェクトのZIPを更新する（教員用）

ZIPの再生成には、Gitと **Python 3.11以上**、および **`git clone` で取得したリポジトリ** が必要です。3.11以上が要るのは、`scripts/test_*.py` が `unittest.TestCase.enterContext`（3.11で入ったもの）を使っているためです。版は `python3 -V` で確かめられます。GitHubの「Download ZIP」で取得したフォルダにはGit管理情報がないため、再生成には使えません。教材の閲覧と、同梱済みの完成プロジェクトZIPの利用は「Download ZIP」でも可能です。

```sh
git clone https://github.com/LeoAndo/jec-25cm-kotlin.git
cd jec-25cm-kotlin
```

完成コードを変更したときは、このリポジトリ直下で次を実行し、配布用ZIPも更新します。

```sh
python3 scripts/package-project.py --project K01HelloKotlin --output docs/hello-kotlin/downloads/K01HelloKotlin.zip
python3 scripts/package-project.py --project A01HelloAndroid --output docs/hello-android/downloads/A01HelloAndroid.zip
python3 scripts/package-project.py --project A02CalcGame --output docs/calc-game/downloads/A02CalcGame.zip
python3 scripts/package-project.py --project A03GithubSearch --output docs/github-search/downloads/A03GithubSearch.zip
python3 scripts/package-project.py --project A04FunnyCamera --output docs/funny-camera/downloads/A04FunnyCamera.zip
```

学生用ZIPを作成するときは、完成プロジェクトのZIPをまとめて再生成し、HTMLのリンク確認も行います。

```sh
python3 scripts/package-student-materials.py
```

ZIPにはGitで管理しているプロジェクトのファイルを収録し、IDE設定（`.idea`）・ビルド出力（`build` / `out`）・ローカルSDK設定（`local.properties`）を除外します。既存ファイルの編集内容も反映します。ファイルを新しく追加した場合は、配布対象であることを確認して、そのファイルを `git add` してから再生成してください。

### GitHub Actionsでパッケージ化・リリースする（教員用）

**main更新時に自動準備し、学生向けの公開は手動で行います。** 学生からのフィードバックは随時mainへ反映し、授業前や修正がまとまったタイミングで公開します。

| 操作 | 自動で行う処理 | 学生向け公開 |
| --- | --- | --- |
| mainへのpush・PRマージ | テスト、完成版ZIPの再生成、教材ZIP生成、HTMLの相対リンク確認、リリースノート生成。未翻訳はSummaryに表示 | しない |
| main向けのPR | テスト、教材ZIP生成、相対リンク確認。未翻訳はSummaryに表示 | しない |
| 配布準備の翻訳PR | 配布対象の言語の差分翻訳、別AIによる照合、教材ZIPの確認 | しない |
| Run workflow（publishオフ） | mainの教材とリリースノートを再生成 | しない |
| Run workflow（publishオン） | mainの教材とリリースノートを再生成。配布対象の未翻訳が0文ならGitHub Releasesへ添付 | する |
| Run workflow（publishオン・allow_untranslatedオン） | 緊急公開として未翻訳だけを許可。日本語で表示される件数をリリースノートに記録 | する |

#### 初回の導入

1. `.github/workflows/student-materials.yml` を含む変更をmainへマージします。
2. GitHubの **Actions → Student materials** で実行結果を確認します。
3. `student-materials-ready-…` の成果物をダウンロードし、教材ZIPと `release-notes.md` を確認します。成果物の保存期間は30日です。GitHub Releasesの下書きはこの時点では作りません。
4. 公開したいタイミングで、以下の手動公開を実行します。

追加のSecretは不要です。リポジトリのGitHub Actionsが有効で、ワークフローの `contents: write` を許可するポリシーになっている必要があります。教材のパッケージ化にAndroid SDKは不要です。このワークフローではAndroidアプリのビルド・実機動作までは検証しません。純Kotlin系の `K01HelloKotlin` も、コンパイルはせずファイルを収録するだけです。

#### 手動公開

1. 配布準備のissueを起票し、`config/i18n.json` で `distribute: true` の言語の未翻訳を確認します。エージェントが [翻訳用skill](skills/translate-teaching-materials/SKILL.md) に従って差分だけを訳し、翻訳PRを作ります。翻訳はエージェントのセッションで行い、Actionsから翻訳APIは呼びません。
2. **翻訳PRを開いてから公開するまでは、`docs/` を触るPRをマージしません。** 訳したのとは別のAIが訳文を原文と照合し（教員が読めない言語では、日本語へ訳し戻してから比べます）、検査と配布ZIPの確認を済ませて翻訳PRをマージします。日本語の変更が先に入った場合は、最新のmainで差分を訳し直します。
3. **Actions → Student materials → Run workflow** を開きます。ブランチに **main** を選び、**publish** にチェックを入れます。**allow_untranslated** はオフのままにします。
4. **student_notes** に学生向けの案内を日本語で入力します。例：`K01HelloKotlin STEP 4の説明を修正。すでに完成している人はやり直し不要。`
5. **Run workflow** を押します。配布対象の言語に未翻訳があると公開前に失敗し、Summaryに言語・ページ別の件数が出ます。差分翻訳を反映してから新しく実行してください。成功すると、Releasesに教材ZIP・チェックサム・リリースノートが掲載されます。
6. 公開された個別リリースURLを授業で案内します。ここで `docs/` を触るPRのマージを再開します。

授業を進められない不具合などの緊急修正に限り、**publish** と **allow_untranslated** の両方にチェックを入れて公開できます。未翻訳の文は日本語で表示され、公開ゲートを解除したことと未翻訳の合計・言語別・ページ別の件数がリリースノートに残ります。HTMLや対訳カタログの不正、ZIPの破損、mainの更新は解除できません。`student_notes` には学生への影響と、日本語表示が残ることを補足してください。公開後は残った差分を翻訳PRで反映し、次の通常公開に備えます。

手動実行の開始時点のmainをパッケージ化します。以前の自動実行の成果物をそのまま昇格する方式ではないため、自動準備後にmainが変わっている場合は新しい内容になります。公開直前にもmainを確認し、実行中に更新されていた場合は公開を中止します。その場合は最新のmainで新しく実行してください。main以外を選ぶと、パッケージの検証のみ行い、ノート生成・公開は行いません。

版名は `materials-日付-コミットID` です。日付はコミット日時の日本時間で、同じコミットは同じ版になります。公開済みの版は再実行しても上書きしません。添付中に失敗した場合は下書きに留まり、mainが変わっていなければ同じ実行の **Re-run failed jobs** で再開できます。mainが更新された場合は新しく実行し、不要になった下書きはGitHubから削除してください。

#### リリースノートとフィードバックの扱い

- GitHubの自動生成ノートに、前回公開した教材からのPR一覧を載せます。初回は過去の変更を含みます。直接mainへコミットした変更も、折りたたみのコミット一覧で確認できます。
- PRタイトルは学生が読んで分かる日本語にします。例：`K01HelloKotlin：STEP 4の変数の説明を修正`。
- PRに `enhancement` を付けると「教材の追加」、`bug` は「誤記・不具合の修正」、それ以外は「その他の更新」に分類されます。`skip-release-notes` はPR一覧から除外しますが、コミット一覧には残ります。
- 自動生成はPRタイトルなどをまとめる機能です。修正内容をAIが解釈して学生への影響ややり直しの要否を書く機能ではないため、その案内は公開時の `student_notes` に記入します。
- フィードバックは「教材の版・単元/STEP・起きたこと」で集めます。授業を進められない不具合は修正後すぐに手動公開し、誤字や説明の補足はまとめて公開する運用がおすすめです。

#### ローカルで配布ZIPを確認する

```sh
python3 scripts/check-teaching-materials.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/localize-student-materials.py check
python3 scripts/package-student-materials.py
```

`dist/kotlin-student-materials-2026-09-23-a81c6585fd87.zip` のように、版の日付（HEADのコミット日時をJSTにした日付）とコミットIDの先頭12文字が入った名前で生成されます。日付・コミットIDは版タグと同じ値です。対象はGit管理された `docs` のファイルで、完成版ZIPはソースから再生成します。再生成したZIPの中身は、展開済みの見本として `samples/` にも収録します（`samples/` はリポジトリにはなく、配布ZIPの中だけにできます。`gradlew` の実行権限も引き継ぎます）。新しい教材は `git add` 後に実行してください。ローカルの編集内容も含むため、正式な配布版はGitHub Actionsから公開します。

**単元を追加するときに、配布スクリプトを直す必要はありません。** `scripts/package-student-materials.py` と `scripts/release-student-materials.py` は、完成プロジェクトのZIP生成・`はじめに.txt` の単元一覧・リリースノートの単元一覧を、すべて `config/teaching-materials.json` の `projects` から組み立てます。単元を足すときに直すのは、`config/teaching-materials.json`（`scan_roots`、指定AVD名の `required_in`、`projects`）とこのREADMEのリンク・表、そして既存の全教科書のサイドバーです（`scripts/check-teaching-materials.py` が `projects` の並びとサイドバーを照合するので、直し忘れるとCIが落ちます）。手順は [AGENTS.md](AGENTS.md) と [単元追加用skill](skills/add-teaching-unit/SKILL.md) にあります。

参考：[GitHubのリリースノート自動生成](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)、[ワークフローの手動実行](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)。

### 多言語展開

この教材を使う学生の母国語は、日本語・英語・中国語・韓国語・ミャンマー語・広東語の6つです。日本語で書いた教科書（`docs/`）を、配布前にほかの5言語へ展開します。

**いまは5言語とも `config/i18n.json` の `distribute` が `false` です。** 翻訳がまだ1文もないため、配布対象にすると公開ゲートで止まります。初回翻訳と、別のAIによる独立した照合まで終わった言語から、その言語だけ `distribute` を `true` に上げてください。配布対象にした言語は、ZIPを作るときに `docs/<言語>/` へ生成されます。対象が0言語のあいだは、言語の入口や翻訳HTMLは追加せず、日本語だけの構成で配布します。

| 言語 | コード | `distribute` | 書き方 |
| --- | --- | --- | --- |
| 英語 | `en` | `false` | |
| 中国語 | `zh-Hans` | `false` | 簡体字 |
| 韓国語 | `ko` | `false` | |
| ミャンマー語 | `my` | `false` | Unicode |
| 広東語 | `zh-Hant-HK` | `false` | 繁体字の書き言葉に、香港の語彙を使う |

- **日常のPRでは翻訳しません。** 教材は今までどおり日本語だけを直します。翻訳は、学生への配布前にまとめて翻訳PRで行います。
- **コミットするのは、翻訳済みのHTMLではなく対訳カタログです。** `i18n/<言語>/<ページ>.json` に、原文と訳文の対を文単位で置きます。各言語のHTMLは、カタログから作ります（リポジトリにはコミットしません）。コード・リンク・STEPの番号は日本語版からそのまま引き継ぐので、どの言語でも同じ位置に同じものが出ます。
- **日本語の文を直すと、その文は自動で未翻訳に戻ります。** 未翻訳の文は日本語のまま表示されます。古い訳が学生に届くことはありません。
- `<pre>` のコード、`<code>` の中身、IntelliJ IDEAやAndroid Studioの画面に出る言葉、学生が打ち込む日本語は訳しません。授業は日本語で進むので、翻訳は読んで理解するための補助という位置づけです。

配布対象の言語があるZIPには、入口の `index.html` と `はじめに.txt` に各言語の案内を入れます。教科書の冒頭にある言語リンクで同じページ・STEPへ移動できます。翻訳ページには「AIによる翻訳／日本語版が正／疑問は先生へ」の注記と日本語版へのリンクが付きます。コード・CSS・JS・完成版ZIPは日本語版と共有します。未翻訳の文は日本語のまま、`lang="ja"` を付けて表示します。

言語の一覧は `config/i18n.json`、翻訳の手順とルールは [skills/translate-teaching-materials/SKILL.md](skills/translate-teaching-materials/SKILL.md)、言語ごとの用語集は `i18n/<言語>/glossary.md` にあります。翻訳そのものはエージェントが行い、スクリプトは入口と出口をそろえます。

```sh
python3 scripts/localize-student-materials.py sync --lang en     # 未翻訳の文を dist/i18n-work/ に書き出す
python3 scripts/localize-student-materials.py merge --lang en    # 訳した結果を検査して、対訳カタログへ入れる
python3 scripts/localize-student-materials.py check              # 対訳カタログを検査する（CIでも実行）
python3 scripts/localize-student-materials.py status             # 言語×ページごとに、訳した数を出す
python3 scripts/localize-student-materials.py build --lang en    # dist/i18n-preview/docs/en/ に確認用のページを作る
```

CIは、対訳カタログが壊れていないことを確かめ、未翻訳の文の数を Summary に出します。通常のPRとmainへのpushは未翻訳があっても失敗にはしません。`publish` のときだけ、配布対象の言語に未翻訳があれば公開を止めます（緊急公開の手順は上の「手動公開」を参照）。教科書のHTMLは、開始タグと終了タグを必ず対応させてください（`<p>` や `<li>` の閉じ忘れがあると、文を取り出せず、`check` が失敗します）。

---

# 開発環境：教員
```
IntelliJ IDEA 2026.3 EAP
Build #IU-263.5153.40, built on September 18, 2026
Source revision: 6b844c266e728
ライセンス対象: IntelliJ IDEA EAP user: 玲生 安藤
有効期限: October 18, 2026
Runtime version: 25.0.4.1+1-b583.48 aarch64
VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
Toolkit: sun.lwawt.macosx.LWCToolkit
macOS 26.6.2
例外報告ツール ID: 2025-05-08_efc3ed8e-f1a7-49f4-9e79-a0d3d3315e3a
JetBrains Daemon version: 0.9.8679
JCEF バージョン: 150.0.14-263-b11
StudioFlags with current overrides:
  LazyStudioFlagSettings(StudioFlagSettings(data.size=0)):
  PropertyOverrides(cache.size=488):
  MendelOverrides(MendelFlagsProvider count=0):
  ServerFlagOverrides(No server flags are enabled.):
  AgpReleaseBranchProvider(releasedWithAgp=false):
    gradle.ide.use.alongside.agp=false
  AgpTestSuitesProvider(journeysWithGeminiEnabled=false):
GC: G1 Young Generation, G1 Concurrent GC, G1 Old Generation
Memory: 2048MiB
Cores: 14
Metal Rendering is ON
User VM options:
  -Dide.managed.by.toolbox=/Applications/JetBrains Toolbox.app/Contents/MacOS/jetbrains-toolbox
  -Dtoolbox.notification.token=bd06b49a-6ebc-401b-a45f-582682604c26
  -Dtoolbox.notification.portFile=/Users/ando/Library/Caches/JetBrains/Toolbox/ports/4d739ac2-1256-4161-a735-26014c4f35cd.port
Registry:
  ide.experimental.ui=true
  trace.state.event.service.url=https://api.jetbrains.cloud/trace-status
  chat.run.target.promo.enabled=true
Non-Bundled Plugins:
  com.intellij.nativeDebug (263.5153.37-mac-arm64)
  Subversion (263.5153.48)
  idea.plugin.protoeditor (263.5153.33)
  com.anthropic.code.plugin (0.1.14-beta)
  com.intellij.tasks (263.5153.33)
  com.codeium.intellij (2.12.27)
  intellij.jupyter (263.5153.33)
  com.intellij.jsp (263.5153.33)
  Dart (509.0.0)
  PerforceDirectPlugin (263.5153.37)
  com.intellij.ml.llm (263.5153.40)
  com.jetbrains.kmm (263.5153.40-IJ)
  com.intellij.velocity (263.5153.33)
  com.intellij.tasks.timeTracking (263.5153.33)
  org.jetbrains.android (263.5153.40-mac-arm64)
  com.android.tools.design (263.5153.40)
  org.jetbrains.kotlin-toolchain (263.5153.40)
  com.intellij.notebooks.core (263.5153.33)
  com.github.copilot (1.18.0-261-macos-arm64)
  androidx.compose.plugins.idea (263.5153.40)
  io.flutter (96.0.0)
Kotlin: 263.5153.40-IJ
```
```
Android Studio Quail 4 | 2026.1.4 Patch 1
Build #AI-261.26222.65.2614.16379836, built on September 18, 2026
Runtime version: 25.0.3+-15898627-b508.16 aarch64null
VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
Toolkit: sun.lwawt.macosx.LWCToolkit
macOS 26.6.2
Exception reporter ID: 270125222c3b097-4f29-4703-b739-482326ad65e1
StudioFlags with current overrides:
  LazyStudioFlagSettings(StudioFlagSettings(data.size=3)):
  PropertyOverrides(cache.size=477):
    flags.configuration.level=COMPLETE
  MendelOverrides(MendelFlagsProvider count=0):
  ServerFlagOverrides(No server flags are enabled.):
  AgpReleaseBranchProvider(releasedWithAgp=true):
    gradle.ide.use.alongside.agp=true
  AgpTestSuitesProvider(journeysWithGeminiEnabled=false):
Disabled bundled plugins: com.google.tools.ij.aiplugin
GC: G1 Young Generation, G1 Concurrent GC, G1 Old Generation
Memory: 2048M
Cores: 14
Metal Rendering is ON
Registry:
  ide.experimental.ui=true
Non-Bundled Plugins:
  org.jetbrains.completion.full.line (261.26222.129)
  com.intellij.marketplace (261.26222.65)
  Dart (509.0.0)
  com.codeium.intellij (2.12.27)
  com.anthropic.code.plugin (0.1.14-beta)
  org.jetbrains.junie (261.2144.120)
  com.github.copilot (1.18.0-261-macos-arm64)
  com.jetbrains.kmm (261.26222.147-AS)
  com.intellij.ml.llm (261.26222.129)
  Docker (261.26222.24)
  amazon.q (4.8.261)
  codiumai.codiumai (2.2.8)
  io.flutter (96.0.0)
```

# 開発環境：学生

- 学生の端末は **macOS** を前提にします。Windowsは対象外です。
- 前半の純Kotlin系（K01）は **IntelliJ IDEA**、後半のAndroid系（A01〜）は **Android Studio** を使います。**学校から貸し出しているMacには、どちらもインストール済みです。** 学生が自分で入れる作業はありません。準備の手順は [共通資料：授業を始めるまでの準備](docs/common/setup.html) にあります。
- Android系の単元では、エミュレータ `jec_25cm_kotlin_Pixel 9a` を使います。教科書に載せるスクリーンショットも、このエミュレータで撮ります。

## アンケート：普段授業で使っているパソコン

「普段授業で利用しているパソコンの Android Studio・Xcode・MacBook のバージョン」を聞き、**4件の回答**を得ました。**回答したのは一部の学生で、母数は分かりません。**下の表は回答のままで、教員による読み取りは次の節に分けて書きます。

| 回答日 | Android Studio | Xcode | macOS |
| --- | --- | --- | --- |
| 2026-09-16 | `2026.1` | 27 | macOS 27 Golden Gate バージョン27.0 |
| 2026-09-17 | `panda2` | 26.4 | tahoe ver.26.4.1 |
| 2026-09-18 | `Android Studio Panda 3 \| 2025.3.3` | Xcode Version 26.4 | macOS Tahoe 26.5.2 |
| 2026-09-21 | `Android Studio Panda 2 \| 2025.3` | Xcode Version 26.5 | macOS Tahoe バージョン 26.5.1 |

Xcode と macOS の欄も聞いていますが、この授業では使いません（Kotlinの前半は IntelliJ IDEA、後半は Android Studio とエミュレータ）。ほかの科目と共通のアンケートです。

### 回答の読み取り

- **2026-09-16 の `2026.1` は、Android Studio Quail 4 です。** 製品名が書かれていなかったため本人に聞き直し、**2026-09-23 に確定**しました。推測ではありません。
- **2026-09-21 の `2025.3` は、Panda 2 のバージョン番号**です。教員環境の Panda 2 と同じ版と読めます。
- 2026-09-17 の `panda2` も Panda 2 です。

### 教員環境・教材の基準とのバージョン差

**回答した4人のうち2人が、教材の基準（Android Studio Panda 2）より新しい版を使っています。**

| 回答日 | Android Studio | 基準との差 |
| --- | --- | --- |
| 2026-09-16 | Quail 4 | **2世代先** |
| 2026-09-17 | Panda 2 | 一致 |
| 2026-09-18 | Panda 3（2025.3.3） | 1パッチ先 |
| 2026-09-21 | Panda 2（2025.3） | 一致 |

**割合は結論にできません。** 母数が分からないので、「半分が新しい版」とは言えません。ただし1人でも基準より新しい版を使っている以上、読み替えの案内は要ります。

- **Quail 4 で進めると、教科書と食い違うところが実測で分かっています。** リポジトリにある2つのひな形（`Panda2KotlinEmptyViewsActivity` / `Quail4KotlinEmptyViewsActivity`）を突き合わせた結果、`buildTypes` の書き方（`isMinifyEnabled` ＋ `proguardFiles` ↔ `optimization { enable = false }`）と、R8のkeepルールの置き場（`app/proguard-rules.pro` ↔ `app/src/main/keepRules/rules.keep`）が違います。どちらも New Project ウィザードが生成する形そのものなので、学生が自分で作ったプロジェクトと教科書のコードを並べて見比べられなくなります。詳細は「教員が確認に使うプロジェクト」の表にあります。
- **Panda 3（2025.3.3）の差分は実測していません。** Panda 2 とはパッチ1つぶんの差なので、上の食い違いは出ない見込みですが、確かめてはいません。ひな形も置いていません。
- A01の教科書とあわせて、[共通資料：ちがうAndroid Studioのバージョンで進めるとき](docs/common/other-versions.html)を用意しました。Quail 4ではA01 STEP 01のPanda 2用カタログへ置き換えず、生成設定を保って進めます。設定の実測表、相談する条件、Panda 3が未実測であることをまとめています。

# 基本方針

学生から見たときに、この授業が何をどう扱うかの方針です。コードの書き方そのものは、下の「完成コードの書き方（全単元共通）」にまとめています。

1. **1コマで新しく覚えることは1つだけにする。** 1単元で導入する新概念は1つまでです。覚えることが増えるほど、コードを追えなくなる学生が出ます。ここでいう「新概念」は、**JavaにもSwiftにもないもの**を指します（下の「単元の範囲の決め方」）。書き方だけが違うものは、比較で見せれば足ります。
2. **やったことの結果が、必ず目に見える形にする。** 純Kotlin系ならコンソールの出力、Android系なら画面の変化として確かめられるところまでを1単元にします。
3. **Viewの取得は `findViewById` にそろえる。** ViewBindingもComposeも使いません。どの単元のコードも同じ形で読めるようにするためです。命名は `txtXxx` / `edtXxx` / `btnXxx` / `imgXxx` / `recyclerView` です。
4. **警告は隠さず、原因そのものを消す。** `@SuppressLint` は使いません。学生が同じ警告に出会ったとき、消し方ではなく直し方を覚えてほしいからです。
5. **伝えたいことは画面に出す。** 結果やエラーは `Snackbar`（または `Toast`）で見せます。`Log.d` だけで済ませません。Logcatは、学生が中身を確かめるための補助として扱う単元でだけ使います。
6. **完成プロジェクトにUnit Testは書きません。** テストしやすくするためのリファクタリングもしません。授業で扱わないコードが増えると、読む量だけが増えるためです（教材を検査する `scripts/test_*.py` はCIで動くので、通る状態を保ちます）。
7. **ライブラリは必要なときだけ足します。** バージョンは `gradle/libs.versions.toml` で管理します。
8. **コメントは日本語で書きます。** 学生が読んで意味が分かることを優先し、英語のコメントにはしません。
9. **次は扱いません。** タブレット・フォルダブル端末への対応、ダークテーマ対応、画面回転時のデータ保持と横画面レイアウト。考え方が必要になった単元で、その都度ふれます。
10. 完成プロジェクトの `README.md` は、[`A03GithubSearch/README.md`](A03GithubSearch/README.md) の形にそろえます（画面の構成の表 → 使用しているAPI → ソースコードの構成の表 → 処理の流れ → 実装のポイント → 主なライブラリ → ビルドと実行）。

# 授業用教科書の基本方針

1. 各単元で、学生自身が毎回IDEからプロジェクトを新規作成し、修正箇所を確認しながらハンズオン形式で進めます。純Kotlin系は `K01HelloKotlin` プロジェクトの中に演習ごとのパッケージ（`src/exNN/`）を作り、Android系は単元ごとにAndroid Studioプロジェクトを作ります。公開する完成版は動作確認・コード比較の参考資料とします。
2. **各STEPに、JavaかSwift（または両方）との比較を必ず置きます。** 受講生はJavaとSwiftを書けるので、いちばん短い説明は「あなたが知っているあの書き方が、Kotlinではこうなる」です。比較は、Kotlinを先頭にした横並びの比較ブロック（`<div class="compare">`）で見せます。比較する相手がないKotlin独自の機能（`by lazy` など）は、比較を省かずに「Java／Swiftでは同じことをどう書くか、あるいは書けないか」を示します。
3. **概念そのものの説明はしません。** 変数とは何か、繰り返しとは何かは書きません。書くのは、Kotlinでの書き方と、Java／Swiftとの違い、そして**なぜ違うのか**です。理由まで書くのは、書き方の暗記ではなく、次に似た場面で自分で判断できるようにするためです。
4. **用語に読みがなは振りません。** 受講生は用語を知っています。代わりに、Kotlin固有の用語（プライマリコンストラクタ、スマートキャスト、拡張関数、委譲プロパティなど）には、**Java／Swiftでの対応物**を添えます（例：拡張関数はSwiftのextensionと同じ発想、`by lazy` はSwiftの `lazy var` に近い）。
5. 教科書はGoogle Codelabなどを参考にした、STEPを前から順にたどる構成にします。各STEPは、前年度資料と同じ **「書いてみる」→「実行結果」→「Java／Swiftではどう書くか」→「POINT」** の順で組み立てます。
6. 教科書はHTML形式とします。1単元＝1ファイル（`docs/<スラッグ>/index.html`）です。
7. 複数の単元で共有する説明が出てきたら、そのつど共通資料として別のHTMLファイルに切り出します。具体例：授業を始めるまでの準備、エミュレータの設定手順。
8. 教科書に載せるスクリーンショットは、教員の開発マシンにあるエミュレータ `jec_25cm_kotlin_Pixel 9a` で撮ります。
9. **大半の学生は予習も復習もしないという前提で書きます。** 学生が教科書を読むのは授業中が最初で、そのとき読むのはその単元を前から順にだけです。過去の単元を読み返していないのと同じように、先の単元もまだ読んでいません。判断基準は「予習も復習もしない学生が、その単元を前から順に読んで躓かないか」です。「家で読んでおいてください」のように、予習してきたことを当てにした導入は採りません。
10. **手順やコードをその単元に書かずに、ほかの単元へ送ってはいけません。** 過去の単元へ送る場合も、先の単元へ送る場合も同じ扱いです。先の単元はまだ読んでいないので、学生にとって手がかりになりません。ほかの単元を挙げてよいのは「これは初めてではない」と伝えるときだけで、そう書いたら直後に手順とコードをすべて書きます。学生に指示すること（チェックを入れない、ここには書かない、など）の理由も、その単元の中に書きます。同じ単元の中で別のSTEPを指す参照は対象外です。サイドバーの単元一覧と共通資料へのリンクは本文ではなく導線なので、これも対象外です。
11. **Android系の単元の教科書は、学生が「アレンジできる場所」が分かる形で終わります。** 最後まで進めた学生が、**どこを変えると、画面や動きの何が変わるか**を、その単元のコードの中で見つけられるようにします（文字・色・数値・問題数のように、その単元で扱った範囲で変えられるもの）。提出課題は、学生自身が作ったアプリを1つ選んでアレンジし、APKにして出す形なので（「提出課題」）、単元の終わりが、そのときの手がかりになります。例は挙げますが、正解は決めません。ここで新しい概念やAPIを足すことはしません（「単元の範囲の決め方」）。

# 単元の範囲の決め方（全単元共通）

演習と教科書を作るとき、範囲が広がりすぎていないかを次の3点で判断します。

1. **1単元で導入する新概念は1つまで。** 「新概念」は、それまでの単元に1度も出ていない考え方やAPIのうち、**JavaにもSwiftにもない**ものを指します。実在するかは `git grep` で確認します。2つ以上必要に見えるときは、単元を分けるか、片方を後の単元へ回します。
   - 受講生はJavaとSwiftを学習済みなので、`if` や `for` のように**書き方だけが違うもの**は新概念に数えません。K01が1コマで関数・条件式・繰り返しを、別の1コマで `data class`・スマートキャスト・拡張関数をまとめて扱えるのは、このためです。新概念に数えるのは、委譲プロパティ（`by lazy` の `by`）のように、**JavaにもSwiftにも対応物がなく、知っている言語の知識では説明が付かないもの**です。数え方は下の「純Kotlin単元（K01）での新概念の数え方」にまとめています。
2. **その概念の効果を、学生が目で確かめられる形にする。** 純Kotlin系ならコンソールの出力、Android系なら画面上の変化です。どちらにも出てこない概念は、その単元では導入しません。「実務ではこう書く」は理由にしません。
3. **網羅を目的にしない。** 型のバリエーション、APIの全メソッド、同じ操作の複数パターンを並べても、理解は増えず読む量だけが増えます。代表的な1つに絞り、残りは発展課題か後の単元へ回します。

ただし**公式ドキュメントが「こう書け」と指定している形は削りません**。削ってよいのは、公式が推奨する形のうち「その単元では効果が見えない部分」だけで、それは後の単元へ回します。バグになる指定は、単元に関係なく最初から入れます。

判断に迷ったときは、その概念が**後続の単元で必要になるか**で決めます。次の単元で使うなら残します。使わないなら、発展課題か「解説」の読み物にします。

## 純Kotlin単元（K01）での新概念の数え方

**「新概念」は、JavaにもSwiftにもない考え方を指します。書き方だけが違うものは数えません。** 受講生はJavaとSwiftを書けるので、どちらかに対応物がある項目は「あの書き方が、Kotlinではこうなる」と見せれば伝わります。1コマに入るのは、覚えることの数ではなく、比較で片付かないものの数です。**純Kotlin単元のK01が6コマで `ex01`〜`ex11` の文法項目をまとめて扱えるのは、このためです**（「15コマ計画」）。

各項目のJava／Swiftでの対応物は次のとおりです。`演習` は前年度資料の節に対応します（対応表は上の「前年度の教材との関係」）。教科書では、この対応物を比較ブロックで見せます（「授業用教科書の基本方針」2・4）。

| 演習 | Kotlinで扱う項目 | Javaでの対応物 | Swiftでの対応物 |
| --- | --- | --- | --- |
| `ex01` | `val` / `var`、型推論 | `final` 付きの変数／通常の変数、`var`（Java 10以降） | `let` / `var`、型推論 |
| `ex01` | セミコロン不要 | 文末に `;` が必要 | 同じく不要 |
| `ex02` | Null許容型 `?`、安全呼び出し `?.` | **対応物なし**（`Optional` は型システムの外側の約束） | オプショナル `String?`、オプショナルチェイン `?.` |
| `ex03` `ex05` `ex06` | 関数 `fun`、条件式 `if`、繰り返し `for (x in list)` | メソッド、`if`、拡張for文 | `func`、`if`、`for x in list` |
| `ex04` | クラス、プライマリコンストラクタ | コンストラクタ（クラス本体の中に書く） | イニシャライザ、structのメンバーワイズイニシャライザ |
| `ex08` | プロパティとアクセサ（`get()` / `set()` / `field`） | getter / setterを自分で書く | computed property、`willSet` / `didSet` |
| `ex09` | `data class` | `record`（Java 16以降） | `struct`（`Equatable` などの自動合成） |
| （演習なし） | スマートキャスト | `instanceof` のパターンマッチ（Java 16以降） | `if let`、`as?` |
| `ex07` | 拡張関数 | **対応物なし** | `extension` |
| `ex10` | `map` などのコレクション操作 | Stream APIの `map` | `map` |
| `ex11` | `by lazy`（委譲プロパティ） | **対応物なし** | **対応物なし**（`lazy var` は結果が似るだけで、委譲の仕組みはない） |

- **両方が「対応物なし」なのは `by lazy`（委譲プロパティ）だけです。** K01の6コマ全体でこの数え方に引っかかる新概念は、`ex11` のこの1つです。だから `data class`・スマートキャスト・拡張関数の3つを1コマで扱っても「1単元1新概念」に反しません。3つとも、受講生が知っている書き方の言い換えとして説明できます。
- **片方だけ「対応物なし」の項目は、正直にそう書きます。** Null許容型（`ex02`）と拡張関数（`ex07`）はJavaにありません。Javaだけを知っている人には新概念ですが、この授業の受講生はSwiftで同じ考え方を使っています。教科書では、Javaとの比較で「Javaではこうは書けない」を見せ、Swiftとの比較で「知っているあれと同じ」を見せます。
- **「対応物なし」の項目は、比較を省きません。** 相手がないときは、Java／Swiftでは同じことをどう書くか、あるいは書けないかを示します（「授業用教科書の基本方針」2）。ここが本当の新概念なので、時間はここに使います。
- **Android系（A01〜）には、従来どおり「1単元1新概念」をそのまま適用します。** この数え方が効くのは、KotlinとJava／Swiftが同じことを別の書き方でするからです。Androidの仕組み（Activityのライフサイクル、レイアウトのXML、実行時の権限、CameraXなど）は、Kotlinの文法ではなくプラットフォームの決まりごとで、言語の差分では説明できません。数え方を緩める理由がないので、緩めません。

# 完成コードの書き方（全単元共通）

完成プロジェクトのコードは、単元をまたいで同じ書き方にそろえます。教科書に掲載するコードと `teacher/<スラッグ>/code` の照合コードも同じ形にします。

1. **Viewの取得は `findViewById` を使う。ViewBindingもComposeも使わない。** `val txtXxx = findViewById<TextView>(R.id.txt_xxx)` の形で、`onCreate` の冒頭（インセットのリスナ設定の直後）にまとめます。命名は `txtXxx` / `edtXxx` / `btnXxx` / `imgXxx` / `recyclerView` です。`onCreate` 以外からも使うViewはフィールドにし、同じidに対して `findViewById` を2回呼びません。
2. **`@SuppressLint` で警告を隠さない。** 警告の原因そのものを消します。`A04FunnyCamera` では `setOnTouchListener` をやめ、`AppCompatImageView` を継承して `onTouchEvent()` と `performClick()` をオーバーライドしています。
3. **ユーザーに伝えることは `Snackbar`（または `Toast`）で画面に出す。`Log.d` で済ませない。** Logcatは、学生が中身を確かめるための補助として扱う単元でだけ使います。
4. **1単元で導入する新概念は1つまで。** 画面（またはコンソールの出力）で効果が見える形にします。
5. **完成プロジェクトにUnit Testは書かない。** テストしやすくするためのリファクタリングもしません。教材を検査する `scripts/test_*.py` はCIで動くので、通る状態を保ちます。
6. 完成プロジェクトの `README.md` は、[`A03GithubSearch/README.md`](A03GithubSearch/README.md) の形にそろえます（画面の構成の表 → 使用しているAPI → ソースコードの構成の表 → 処理の流れ → 実装のポイント → 主なライブラリ → ビルドと実行）。
7. **ライブラリは必要なときだけ足す。** バージョンは `gradle/libs.versions.toml` で管理します。
8. 純Kotlin系の完成コードは `K01HelloKotlin/src/exNN/` に置き、ファイルの先頭に `package exNN` を書きます。`fun main()` を持たせて、IntelliJ IDEAの実行ボタンで動かせる形にします。**`exNN` の番号は、前年度資料の節に対応させます**（対応表は上の「前年度の教材との関係」）。新しい番号を勝手に振らず、その節の演習として置きます。1つの単元が複数の `exNN` を扱うこともあります。
9. コメントは、学生が読んで意味が分かる日本語で書きます。英語のコメントにはしません。
10. **ここに書いた書き方を保ちます。** レビューで「初学者向けにかみ砕くべき」と指摘されても、既定の対応は「教科書で説明する」です。採用するのは、動作を変えない小さな明確化だけにします。受講生はJavaとSwiftを書けるので、コードを薄めるより、Java／Swiftとの比較を1つ足すほうが早く伝わります。
