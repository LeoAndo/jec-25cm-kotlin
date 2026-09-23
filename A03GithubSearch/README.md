# A03GithubSearch

GitHubのリポジトリを検索して一覧表示する、ミニマムなAndroidアプリです。

検索ワードとソート順を指定して検索ボタンを押すと、GitHubの検索APIを呼び出し、結果をRecyclerViewで表示します。リストはタップできません（表示のみ）。

## 画面の構成

`app/src/main/res/layout/activity_main.xml`

| View | id | 役割 |
| --- | --- | --- |
| TextInputEditText | `edit_query` | 検索ワードの入力 |
| Spinner | `sp_sort` | ソート順の選択 |
| Button | `btn_search` | 検索の実行 |
| RecyclerView | `recycler_view` | 検索結果の一覧 |
| CircularProgressIndicator | `progress` | 通信中のぐるぐる |

`app/src/main/res/layout/list_item.xml`（リストの1行）では、所有者・リポジトリ名・スター数・フォーク数の4つをTextViewで表示します。

ソート順のSpinnerの選択肢と、APIに渡す`sort`パラメータの対応は次のとおりです。

| 表示ラベル | sortパラメータ |
| --- | --- |
| ベストマッチ | （指定なし） |
| スター数 | `stars` |
| フォーク数 | `forks` |
| 更新日時 | `updated` |

## 使用しているWeb API

GitHubのリポジトリ検索API（認証なしで使えます）。

```
GET https://api.github.com/search/repositories?q={検索ワード}&sort={ソート順}&per_page=30
```

- 公式ドキュメント: https://docs.github.com/en/rest/search/search#search-repositories
- レスポンスの実例を `docs/search_repositories_sample.json` に保存してあります。どのようなJSONが返ってくるか確認したいときに参照してください。
- 認証なしの場合、リクエスト数はIPアドレスごとに1分間に10回までに制限されています。短時間に何度も検索するとエラーになることがあります。

## ソースコードの構成

`app/src/main/java/jp/ac/jec/a03githubsearch/`

| ファイル | 役割 |
| --- | --- |
| `MainActivity.kt` | 画面の組み立て、検索の実行、結果の反映 |
| `GithubApi.kt` | Ktorを使ってGitHubの検索APIを呼び出す |
| `GithubSearchResponse.kt` | JSONを受け取るためのデータクラス |
| `RepositoryAdapter.kt` | RecyclerViewに検索結果を表示するAdapter |

### 処理の流れ

1. `MainActivity` の検索ボタンが押される
2. `lifecycleScope.launch { }` でコルーチンを起動し、通信中は`progress`を表示してボタンを無効化する
3. `GithubApi.searchRepositories()` がAPIを呼び出し、JSONを `GithubSearchResponse` に変換して `List<GithubRepository>` を返す
4. `RepositoryAdapter.submitList()` に渡して一覧を更新する
5. 失敗した場合や結果が0件の場合はToastでメッセージを表示する

### 実装のポイント

- Viewの取得には `findViewById` を使っています（ViewBindingは使っていません）。
- `RepositoryAdapter` は `ListAdapter` を継承しているため、`submitList()` を呼ぶだけで `DiffUtil` が差分を計算し、リストを更新してくれます。
- APIのレスポンスには大量のフィールドが含まれるので、`GithubApi.kt` でJSONの設定に `ignoreUnknownKeys = true` を指定し、データクラスに定義していないフィールドは無視するようにしています。
- ネットワーク通信には `AndroidManifest.xml` の `android.permission.INTERNET` パーミッションが必要です。

## 主なライブラリ

| ライブラリ | 用途 |
| --- | --- |
| Ktor Client (OkHttpエンジン) | HTTP通信 |
| kotlinx.serialization | JSONとデータクラスの相互変換 |
| RecyclerView / CardView | 一覧表示 |
| Material Components | TextInputLayout、CircularProgressIndicatorなど |

バージョンは `gradle/libs.versions.toml` で管理しています。

## ビルドと実行

Android Studioでこのディレクトリを開き、`app` の構成で実行してください。ターミナルからビルドする場合は次のコマンドを使います。

```
./gradlew :app:assembleDebug
```

- minSdk: 31（Android 12）
- targetSdk / compileSdk: 37
