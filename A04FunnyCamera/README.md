# A04FunnyCamera

カメラのプレビューにキャラクターを重ねて、その画面を写真として保存するAndroidアプリです。

起動するとカメラの権限を求められ、許可するとカメラ映像が画面いっぱいに表示されます。映像の上にはキャラクター（金魚）が表示されていて、指でドラッグして好きな位置に動かせます。「Take Picture」ボタンを押すと、カメラ映像とキャラクターを合成した画像を端末に保存します。

## 画面の構成

`app/src/main/res/layout/activity_main.xml`

| View | id | 役割 |
| --- | --- | --- |
| FrameLayout | `main` | 画面全体（子Viewを重ねて表示する） |
| PreviewView | `preview_view` | カメラのプレビュー |
| ImageView | `iv_character` | 指で動かせるキャラクター |
| Button | `btn_take_picture` | 画面の保存 |

FrameLayoutは子Viewを順番に重ねて表示するので、後に書いたViewほど手前に表示されます。そのため、カメラのプレビュー → キャラクター → ボタンの順に重なります。

## 使用している画像

| ファイル | 大きさ | 用途 |
| --- | --- | --- |
| `app/src/main/res/drawable/character.png` | 500×416 | プレビューに重ねるキャラクター（背景は透過） |

`drawable/` に置いた画像は、画面の密度が高い端末では読み込むときに自動で拡大されます（mdpi基準のため、例えば640dpiの端末では4倍）。元の画像は2000×1667と大きく、そのままだとメモリを使いすぎてアプリが落ちることがあるため、表示サイズ（200dp）に合わせて縮小しています。

## ソースコードの構成

`app/src/main/java/jp/ac/jec/a04funnycamera/`

| ファイル | 役割 |
| --- | --- |
| `MainActivity.kt` | 権限リクエスト、カメラの起動、キャラクターのドラッグ、画面の合成と保存 |

### 主な関数

| 関数 | 役割 |
| --- | --- |
| `onCreate()` | 画面の組み立て、カメラ権限のリクエスト、ボタンの設定 |
| `setupDragCharacter()` | キャラクターを指で動かせるようにする |
| `startCamera()` | CameraXでプレビューを開始する |
| `takeScreenshot()` | カメラ映像とキャラクターを1枚の画像に合成する |
| `saveBitmap()` | 合成した画像を共有ストレージに保存する |

### 処理の流れ

1. `onCreate()` でカメラの権限（`android.permission.CAMERA`）をリクエストする
2. 権限が許可されたら `startCamera()` でプレビューを開始する（許可されなかった場合はSnackbarでメッセージを表示する）
3. キャラクターをドラッグすると、`setupDragCharacter()` で登録したタッチ処理によって指の位置に合わせてキャラクターが移動する
4. 「Take Picture」ボタンが押されたら `takeScreenshot()` が呼ばれる
   1. `previewView.bitmap` でプレビューに表示中のカメラ映像をBitmapとして取り出す
   2. Canvasを使って、そのBitmapの上にキャラクターを同じ位置で描き込む
5. `saveBitmap()` で合成した画像をJPEGとして `Pictures/FunnyCamera` に保存し、結果をSnackbarで表示する

### 実装のポイント

- Viewの取得には `findViewById` を使っています（ViewBindingは使っていません）。
- **キャラクターのドラッグ**：`setOnTouchListener` でタッチイベントを受け取ります。指を置いた瞬間（`ACTION_DOWN`）に「指の位置とキャラクター左上のずれ」を記録しておき、指を動かしている間（`ACTION_MOVE`）は `指の位置 + ずれ` をキャラクターの `x` / `y` に設定します。ずれを記録しておかないと、キャラクターの左上が指の位置に飛んでしまいます。
- **画面の合成**：カメラ映像は `ImageCapture` で撮影するのではなく、`PreviewView.getBitmap()`（Kotlinでは `previewView.bitmap`）で画面に表示されている映像を取り出しています。そのため、保存される画像は画面に見えている範囲・大きさと同じになります。キャラクターは `canvas.translate()` で位置を合わせてから `characterView.draw(canvas)` で描き込みます。ボタンは描き込まないので、保存した画像には写りません。
- **画像の保存**：Android 10以降は、`MediaStore` を使えば権限なしで共有ストレージに画像を保存できます。書き込み中は `IS_PENDING` を `1` にして他のアプリから見えないようにし、書き込みが終わったら `0` に戻します。
- 画像の圧縮と書き込みは時間がかかることがあるため、`Executors.newSingleThreadExecutor()` で作ったスレッドで実行し、画面の更新（Snackbarの表示）は `runOnUiThread { }` でメインスレッドに戻してから行います。

### 保存先

端末の `Pictures/FunnyCamera/` に `yyyy-MM-dd-HH-mm-ss-SSS.jpg` という名前で保存されます。フォトアプリなどのギャラリーアプリから確認できます。

## 主なライブラリ

| ライブラリ | 用途 |
| --- | --- |
| CameraX（camera-core / camera-camera2 / camera-lifecycle / camera-view） | カメラのプレビュー表示 |
| Material Components | Snackbar |

`camera-camera2` は直接コードから使っていませんが、CameraXが内部で使うため、追加しないと実行時にエラーになります。

バージョンは `gradle/libs.versions.toml` で管理しています。

## ビルドと実行

Android Studioでこのディレクトリを開き、`app` の構成で実行してください。ターミナルからビルドする場合は次のコマンドを使います。

```
./gradlew :app:assembleDebug
```

- minSdk: 31（Android 12）
- targetSdk / compileSdk: 37
- カメラを使うため、実機またはカメラが有効なエミュレーターで実行してください。
