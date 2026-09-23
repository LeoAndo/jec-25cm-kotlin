package jp.ac.jec.a04funnycamera

import android.Manifest
import android.content.ContentValues
import android.graphics.Bitmap
import android.graphics.Canvas
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import android.widget.Button
import android.widget.ImageView
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts.RequestPermission
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.lifecycleScope
import com.google.android.material.snackbar.Snackbar
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.IOException
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

/**
 * カメラのプレビューにキャラクターを重ねて、その画面を画像として保存するActivity
 *
 * - キャラクターは指でドラッグして動かせる (DraggableImageView)
 * - 「Take Picture」ボタンを押すと、カメラ映像とキャラクターを合成した画像を保存する
 */
class MainActivity : AppCompatActivity() {
    /**
     * カメラ権限のリクエスト結果を受け取るためのActivityResultLauncher
     */
    private val requestCameraPermission =
        registerForActivityResult(RequestPermission()) { isGranted ->
            Log.d(TAG, "isGranted: $isGranted")
            if (isGranted) {
                startCamera()
            } else {
                Log.w(TAG, "カメラの権限を許可しないとアプリが正常に動作しません")
                Snackbar.make(
                    findViewById(R.id.main),
                    "カメラの権限を許可しないとアプリが正常に動作しません",
                    Snackbar.LENGTH_LONG
                ).show()
            }
        }

    private lateinit var previewView: PreviewView
    private lateinit var characterView: ImageView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        previewView = findViewById(R.id.preview_view)
        characterView = findViewById(R.id.iv_character)

        // Camera機能を使うために権限リクエストを行う
        requestCameraPermission.launch(Manifest.permission.CAMERA)

        findViewById<Button>(R.id.btn_take_picture).setOnClickListener { takeScreenshot() }
    }

    /**
     * Cameraのプレビュー表示を行う
     */
    private fun startCamera() {
        // 現在のプロセスに関連付けられているProcessCameraProviderを取得
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)

        // イベントリスナーの登録
        cameraProviderFuture.addListener(Runnable {
            try {
                val cameraProvider = cameraProviderFuture.get()

                val preview = Preview.Builder().build()
                preview.surfaceProvider = previewView.surfaceProvider

                // フロントカメラかバックカメラを指定する
                val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

                // 再バインドする前にユースケースのバインドを解除する
                cameraProvider.unbindAll()

                // ユースケース(今回の場合、プレビューのみ)をカメラにバインドする
                // 背面カメラがない端末では例外が発生する
                cameraProvider.bindToLifecycle(this, cameraSelector, preview)
            } catch (e: Exception) {
                Log.e(TAG, "error: ", e)
                Snackbar.make(
                    findViewById(R.id.main),
                    "カメラを起動できませんでした",
                    Snackbar.LENGTH_LONG
                ).show()
            }
        }, ContextCompat.getMainExecutor(this))
    }

    /**
     * プレビュー画面とキャラクターを合成したスクリーンショットを作成して保存する
     */
    private fun takeScreenshot() {
        // プレビューに表示中のカメラ映像を取得する (カメラ起動前はnull)
        val previewBitmap = previewView.bitmap
        if (previewBitmap == null) {
            Log.d(TAG, "カメラの準備ができていません")
            return
        }

        // カメラ映像の上にキャラクターを描画する
        val screenshot = previewBitmap.copy(Bitmap.Config.ARGB_8888, true)
        val canvas = Canvas(screenshot)
        canvas.translate(characterView.x - previewView.x, characterView.y - previewView.y)
        characterView.draw(canvas)

        // 画像の保存は時間がかかることがあるため、コルーチンを使ってメインスレッド以外で行う
        lifecycleScope.launch {
            val isSaved = withContext(Dispatchers.IO) {
                saveBitmap(screenshot)
            }
            // ここはメインスレッドに戻っているので画面を更新できる
            val message = if (isSaved) "保存しました" else "保存に失敗しました"
            Snackbar.make(findViewById(R.id.main), message, Snackbar.LENGTH_SHORT).show()
        }
    }

    /**
     * Bitmapを共有ストレージ(Pictures/FunnyCamera)にJPEGで保存する
     *
     * @return 保存に成功したらtrue
     */
    private fun saveBitmap(bitmap: Bitmap): Boolean {
        val dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd-HH-mm-ss-SSS")
        val fileName = LocalDateTime.now().format(dateTimeFormatter)
        val contentValues = ContentValues()
        contentValues.put(MediaStore.MediaColumns.DISPLAY_NAME, fileName)
        contentValues.put(MediaStore.MediaColumns.MIME_TYPE, "image/jpeg") // ファイル形式はjpeg
        // 共有ストレージのPicturesディレクトリ配下にFunnyCameraというディレクトリを作成する
        contentValues.put(MediaStore.Images.Media.RELATIVE_PATH, "Pictures/FunnyCamera")
        // 書き込みが終わるまで他のアプリから見えないようにする
        contentValues.put(MediaStore.MediaColumns.IS_PENDING, 1)

        // 共有ストレージに保存先のファイルを作成する
        val imageCollection =
            MediaStore.Images.Media.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY)
        val uri = contentResolver.insert(imageCollection, contentValues)
        if (uri == null) {
            Log.e(TAG, "保存先のファイルを作成できませんでした")
            return false
        }

        // 作成したファイルにJPEG形式で書き込む
        var isWritten = false
        try {
            val outputStream = contentResolver.openOutputStream(uri)
            if (outputStream != null) {
                outputStream.use {
                    isWritten = bitmap.compress(Bitmap.CompressFormat.JPEG, 95, it)
                }
            }
        } catch (e: IOException) {
            Log.e(TAG, "error ", e)
        }

        // 書き込みに失敗したら、作成したファイルを削除する
        if (!isWritten) {
            contentResolver.delete(uri, null, null)
            return false
        }

        // 書き込み完了。他のアプリから見えるようにする
        contentValues.clear()
        contentValues.put(MediaStore.MediaColumns.IS_PENDING, 0)
        contentResolver.update(uri, contentValues, null, null)
        Log.d(TAG, "savedUri $uri")
        return true
    }

    companion object {
        private const val TAG = "MainActivity" // ログ出力時のタグ
    }
}
