package jp.ac.jec.a03githubsearch

import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.Spinner
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.textfield.TextInputEditText

class MainActivity : AppCompatActivity() {
    private lateinit var editQuery: TextInputEditText
    private lateinit var spSort: Spinner
    private lateinit var btnSearch: Button

    private val repositoryAdapter = RepositoryAdapter()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        editQuery = findViewById(R.id.edit_query)
        spSort = findViewById(R.id.sp_sort)
        btnSearch = findViewById(R.id.btn_search)

        val recyclerView: RecyclerView = findViewById(R.id.recycler_view)
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = repositoryAdapter
        repositoryAdapter.submitList(
            listOf(
                GithubRepository(1L, "HelloKotlin", Owner("student"), 12, 3),
                GithubRepository(2L, "CalcGame", Owner("classroom"), 5, 1),
            ),
        )

        spSort.adapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_item,
            SORT_ITEMS.map { it.first },
        ).apply {
            setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        }

        btnSearch.setOnClickListener { search() }
    }

    private fun search() {
        val query = editQuery.text?.toString()?.trim().orEmpty()
        if (query.isEmpty()) {
            showMessage("検索ワードを入力してください")
            return
        }
        showMessage("入力: $query")
    }

    private fun showMessage(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }

    companion object {
        /** Spinnerに表示するラベルと、APIのsortパラメータの組。空文字はベストマッチ順を表す */
        private val SORT_ITEMS = listOf(
            "ベストマッチ" to "",
            "スター数" to "stars",
            "フォーク数" to "forks",
            "更新日時" to "updated",
        )
    }
}
