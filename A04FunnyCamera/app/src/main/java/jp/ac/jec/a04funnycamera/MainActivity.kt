package jp.ac.jec.a04funnycamera

import android.Manifest
import android.annotation.SuppressLint
import android.content.ContentValues
import android.graphics.Bitmap
import android.graphics.Canvas
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import android.view.MotionEvent
import android.view.View
import android.widget.Button
import android.widget.ImageView
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts.RequestMultiplePermissions
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.google.android.material.snackbar.Snackbar
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.concurrent.ExecutionException
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

/**
 *Android 2 FunnyCameraアプリのKotlin化は一部の学生にとっては難易度が高いかもしれない。
 * なので、Android 2 カメラ演習アプリ相当の内容をKotlin化する方向で進める.
 */
class MainActivity : AppCompatActivity() {
    /**
     * 権限リクエストの結果を受け取るためのActivityResultLauncher
     */
    private val requestPermissions =
        registerForActivityResult(RequestMultiplePermissions()) { grantStates ->
            val isPermissionAllGranted = grantStates.entries.all { it.value }
            Log.d(TAG, "isPermissionAllGranted: $isPermissionAllGranted")
            if (isPermissionAllGranted) {
                startCamera()
            } else {
                Log.w(TAG, "全ての権限を許可しないとアプリが正常に動作しません")
                showMessage("全ての権限を許可しないとアプリが正常に動作しません")
            }
        }

    private lateinit var previewView: PreviewView
    private lateinit var characterView: ImageView

    // 画像の保存処理はメインスレッド以外で行う
    private val saveExecutor: ExecutorService = Executors.newSingleThreadExecutor()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        this.enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        previewView = findViewById(R.id.preview_view)
        characterView = findViewById(R.id.iv_character)

        // Camera機能を使うために権限リクエストを行う
        requestPermissions.launch(arrayOf(Manifest.permission.CAMERA))

        setupDragCharacter()
        findViewById<Button>(R.id.btn_take_picture).setOnClickListener { takeScreenshot() }
    }

    override fun onDestroy() {
        super.onDestroy()
        saveExecutor.shutdown()
    }

    /**
     * キャラクターを指でドラッグして移動できるようにする
     */
    @SuppressLint("ClickableViewAccessibility")
    private fun setupDragCharacter() {
        // タッチした位置とキャラクター左上の差分
        var offsetX = 0f
        var offsetY = 0f
        characterView.setOnTouchListener { view, event ->
            when (event.actionMasked) {
                MotionEvent.ACTION_DOWN -> {
                    offsetX = view.x - event.rawX
                    offsetY = view.y - event.rawY
                }

                MotionEvent.ACTION_MOVE -> {
                    view.x = event.rawX + offsetX
                    view.y = event.rawY + offsetY
                }
            }
            true
        }
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
                cameraProvider.bindToLifecycle(this, cameraSelector, preview)
            } catch (e: ExecutionException) {
                Log.e(TAG, "error: ", e)
            } catch (e: InterruptedException) {
                Log.e(TAG, "error: ", e)
            }
        }, ContextCompat.getMainExecutor(this))
    }

    /**
     * プレビュー画面とキャラクターを合成したスクリーンショットを作成して保存する
     */
    private fun takeScreenshot() {
        // プレビューに表示中のカメラ映像を取得する (カメラ起動前はnull)
        val previewBitmap = previewView.bitmap ?: run {
            showMessage("カメラの準備ができていません")
            return
        }

        // カメラ映像の上にキャラクターを描画する
        val screenshot = previewBitmap.copy(Bitmap.Config.ARGB_8888, true)
        val canvas = Canvas(screenshot)
        canvas.translate(characterView.x - previewView.x, characterView.y - previewView.y)
        characterView.draw(canvas)

        saveExecutor.execute {
            val isSaved = saveBitmap(screenshot)
            runOnUiThread {
                showMessage(if (isSaved) "保存しました" else "保存に失敗しました")
            }
        }
    }

    /**
     * Bitmapを共有ストレージ(Pictures/FunnyCamera)にJPEGで保存する
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

        // 共有ストレージのPicturesディレクトリのパスを取得する
        val imageCollection =
            MediaStore.Images.Media.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY)
        val uri = contentResolver.insert(imageCollection, contentValues) ?: return false

        return try {
            contentResolver.openOutputStream(uri)?.use { outputStream ->
                bitmap.compress(Bitmap.CompressFormat.JPEG, 95, outputStream)
            }
            // 書き込み完了
            contentValues.clear()
            contentValues.put(MediaStore.MediaColumns.IS_PENDING, 0)
            contentResolver.update(uri, contentValues, null, null)
            Log.d(TAG, "savedUri $uri")
            true
        } catch (e: Exception) {
            Log.e(TAG, "error ", e)
            contentResolver.delete(uri, null, null)
            false
        }
    }

    private fun showMessage(message: String) {
        Snackbar.make(findViewById<View>(R.id.main), message, Snackbar.LENGTH_SHORT).show()
    }

    companion object {
        private val TAG: String = MainActivity::class.java.simpleName // ログ出力時のタグ
    }
}
