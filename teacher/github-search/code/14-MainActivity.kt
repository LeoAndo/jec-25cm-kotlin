package jp.ac.jec.a03githubsearch

import android.os.Bundle
import android.view.View
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.Spinner
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.progressindicator.CircularProgressIndicator
import com.google.android.material.textfield.TextInputEditText
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    private lateinit var editQuery: TextInputEditText
    private lateinit var spSort: Spinner
    private lateinit var btnSearch: Button
    private lateinit var progress: CircularProgressIndicator

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
        progress = findViewById(R.id.progress)

        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = repositoryAdapter

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
        val sort = SORT_ITEMS[spSort.selectedItemPosition].second

        lifecycleScope.launch {
            setLoading(true)
            runCatching { GithubApi.searchRepositories(query, sort) }
                .onSuccess { repositories ->
                    repositoryAdapter.submitList(repositories)
                    if (repositories.isEmpty()) showMessage("検索結果が0件でした")
                }
                .onFailure { e ->
                    repositoryAdapter.submitList(emptyList())
                    showMessage("検索に失敗しました: ${e.message}")
                }
            setLoading(false)
        }
    }

    private fun setLoading(isLoading: Boolean) {
        progress.visibility = if (isLoading) View.VISIBLE else View.INVISIBLE
        btnSearch.isEnabled = !isLoading
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
