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
import java.util.concurrent.ThreadLocalRandom

class MainActivity : AppCompatActivity() {
    private var nowNo = 1 // 今の問題が何問目かのカウント数
    private var correctNo = 0 // 正解数
    private var answer = 0 // 計算結果の答え
    private var elapsedTimeMillis: Long = 0 // タイマーの経過時間(ms)
    private var isPlaying = false // ゲーム中かどうかのフラグ (Chronometer#mStartedフラグを取得できないため用意)
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
            // 初回開始時だけ問題を作る。STOP後のSTARTでは現在の問題をそのまま再開する
            if (answer == 0) {
                startQuestion()
            }
            isPlaying = true
        }

        // Stopボタンを押下した時の処理
        btnStop.setOnClickListener { _ ->
            chronometer.stop()
            elapsedTimeMillis = SystemClock.elapsedRealtime() - chronometer.getBase()
            btnStop.setEnabled(false)
            btnStart.setEnabled(true)
            btnReset.setEnabled(true)
            isPlaying = false
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
            nowNo = 1
            correctNo = 0
            answer = 0
            isPlaying = false
        }

    }

    /**
     * 問題を開始する
     */
    private fun startQuestion() {
        val randomNumber = ThreadLocalRandom.current().nextInt(1, 10)
        // var randomNumber = RandomGenerator.getDefault().nextInt(1, 10); // API Level 35から利用可能. OSバージョンの分岐は使わない
        answer = 10 - randomNumber
        val message = nowNo.toString() + "問目: 10 - " + randomNumber + " ="
        txtMessage.text = message
    }
}
