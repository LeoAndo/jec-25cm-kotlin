package jp.ac.jec.a04funnycamera

import android.Manifest
import android.content.ContentValues
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import android.widget.Button
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts.RequestMultiplePermissions
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageCapture.OnImageSavedCallback
import androidx.camera.core.ImageCapture.OutputFileOptions
import androidx.camera.core.ImageCapture.OutputFileResults
import androidx.camera.core.ImageCaptureException
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
                Snackbar.make(
                    window.decorView,
                    "全ての権限を許可しないとアプリが正常に動作しません",
                    Snackbar.LENGTH_LONG
                ).show()
            }
        }

    private var imageCapture: ImageCapture? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        this.enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // Camera機能を使うために権限リクエストを行う
        // OS version 10以降のAndroidデバイスでCameraと共有ストレージへの書き込みで必要な権限リクエスト
        requestPermissions.launch(arrayOf(Manifest.permission.CAMERA))

        findViewById<Button>(R.id.btn_take_picture).setOnClickListener { takePicture() }
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

                val viewFinder = findViewById<PreviewView>(R.id.preview_view)
                val preview = Preview.Builder().build()
                preview.surfaceProvider = viewFinder.surfaceProvider
                imageCapture = ImageCapture.Builder().build()

                // フロントカメラかバックカメラを指定する
                val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

                // 再バインドする前にユースケースのバインドを解除する
                cameraProvider.unbindAll()

                // ユースケース(今回の場合、画像キャプチャのみ)をカメラにバインドする
                cameraProvider.bindToLifecycle(this, cameraSelector, preview, imageCapture)
            } catch (e: ExecutionException) {
                Log.e(TAG, "error: ", e)
            } catch (e: InterruptedException) {
                Log.e(TAG, "error: ", e)
            }
        }, ContextCompat.getMainExecutor(this))
    }

    /**
     * 写真撮影と撮影データの保存を行う
     */
    private fun takePicture() {
        val imageCapture = imageCapture ?: return

        // 撮影データを共有ストレージに保存するための処理
        val dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd-HH-mm-ss-SSS")
        val fileName = LocalDateTime.now().format(dateTimeFormatter)
        val contentValues = ContentValues()
        contentValues.put(MediaStore.MediaColumns.DISPLAY_NAME, fileName)
        contentValues.put(MediaStore.MediaColumns.MIME_TYPE, "image/jpeg") // ファイル形式はjpeg
        // 共有ストレージのPicturesディレクトリ配下にFunnyCameraというディレクトリを作成する
        contentValues.put(MediaStore.Images.Media.RELATIVE_PATH, "Pictures/FunnyCamera")
        // 共有ストレージのPicturesディレクトリのパスを取得する
        val imageCollection =
            MediaStore.Images.Media.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY)
        val outputOptions =
            OutputFileOptions.Builder(
                contentResolver,
                imageCollection,
                contentValues
            ).build()

        // 写真撮影のイベント処理
        imageCapture.takePicture(
            outputOptions,
            ContextCompat.getMainExecutor(this),
            object : OnImageSavedCallback {
                override fun onImageSaved(output: OutputFileResults) {
                    val savedUri = output.savedUri // nullの場合がある
                    Log.d(TAG, "savedUri $savedUri")
                }

                override fun onError(exception: ImageCaptureException) {
                    Log.e(TAG, "error ", exception)
                }
            })
    }

    companion object {
        private val TAG: String = MainActivity::class.java.simpleName // ログ出力時のタグ
    }
}