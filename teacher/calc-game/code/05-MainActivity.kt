package jp.ac.jec.a02calcgame

import android.os.Bundle
import android.os.SystemClock
import android.widget.Button
import android.widget.Chronometer
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {
    private var elapsedTimeMillis: Long = 0 // タイマーの経過時間(ms)
    private lateinit var txtMessage: TextView // メッセージの表示欄。onCreate以外のメソッドからも使うためフィールドにする

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        this.enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // Viewのインスタンスを取得する
        val chronometer: Chronometer = findViewById(R.id.chronometer)
        txtMessage = findViewById(R.id.txt_message)
        val btnStart: Button = findViewById(R.id.btn_start)
        val btnStop: Button = findViewById(R.id.btn_stop)
        val btnReset: Button = findViewById(R.id.btn_reset)

        // Startボタンを押下した時の処理
        btnStart.setOnClickListener { _ ->
            chronometer.setBase(SystemClock.elapsedRealtime() - elapsedTimeMillis)
            chronometer.start()
            btnStop.setEnabled(true)
            btnStart.setEnabled(false)
            btnReset.setEnabled(false)
        }

        // Stopボタンを押下した時の処理
        btnStop.setOnClickListener { _ ->
            chronometer.stop()
            elapsedTimeMillis = SystemClock.elapsedRealtime() - chronometer.getBase()
            btnStop.setEnabled(false)
            btnStart.setEnabled(true)
            btnReset.setEnabled(true)
        }

        // Resetボタンを押下した時の処理
        btnReset.setOnClickListener { _ ->
            chronometer.stop()
            chronometer.setBase(SystemClock.elapsedRealtime())
            btnStop.setEnabled(false)
            btnStart.setEnabled(true)
            btnReset.setEnabled(false)
            txtMessage.text = ""
            elapsedTimeMillis = 0
        }

    }
}
