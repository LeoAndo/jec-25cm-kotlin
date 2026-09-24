package jp.ac.jec.a03githubsearch

import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.engine.okhttp.OkHttp
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.request.get
import io.ktor.client.request.parameter
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

/** GitHubのリポジトリ検索APIを呼び出す。 */
object GithubApi {
    private const val SEARCH_REPOSITORIES_URL = "https://api.github.com/search/repositories"

    private val client = HttpClient(OkHttp) {
        install(ContentNegotiation) {
            // レスポンスにはここで定義していないフィールドが大量に含まれるため、未知のキーは無視する
            json(Json { ignoreUnknownKeys = true })
        }
    }

    /**
     * リポジトリを検索する。
     *
     * @param query 検索ワード
     * @param sort 並び替えの基準。空文字の場合はベストマッチ順
     */
    suspend fun searchRepositories(query: String, sort: String): List<GithubRepository> {
        val response: GithubSearchResponse = client.get(SEARCH_REPOSITORIES_URL) {
            parameter("q", query)
            if (sort.isNotEmpty()) parameter("sort", sort)
            parameter("per_page", PER_PAGE)
        }.body()
        return response.items
    }

    private const val PER_PAGE = 30
}
