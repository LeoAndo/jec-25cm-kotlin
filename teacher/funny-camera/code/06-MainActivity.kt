package jp.ac.jec.a04funnycamera

import android.Manifest
import android.os.Bundle
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
import com.google.android.material.snackbar.Snackbar

/**
 * カメラのプレビューにキャラクターを重ねて、その画面を画像として保存するActivity
 *
 * - キャラクターは指でドラッグして動かせる (DraggableImageView)
 * - 14コマ目はプレビューと移動を確認する。画像の保存は15コマ目で追加する
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

        findViewById<Button>(R.id.btn_take_picture).setOnClickListener {
            Snackbar.make(findViewById(R.id.main), "プレビューを確認中です", Snackbar.LENGTH_SHORT).show()
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

    companion object {
        private const val TAG = "MainActivity" // ログ出力時のタグ
    }
}
