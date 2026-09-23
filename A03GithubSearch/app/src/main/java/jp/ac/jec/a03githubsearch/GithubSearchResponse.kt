package jp.ac.jec.a03githubsearch

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * GitHubのリポジトリ検索APIのレスポンス。
 * https://docs.github.com/en/rest/search/search#search-repositories
 */
@Serializable
data class GithubSearchResponse(
    @SerialName("total_count") val totalCount: Int,
    val items: List<GithubRepository>,
)

@Serializable
data class GithubRepository(
    val id: Long,
    val name: String,
    val owner: Owner,
    @SerialName("stargazers_count") val stargazersCount: Int,
    @SerialName("forks_count") val forksCount: Int,
)

@Serializable
data class Owner(
    val login: String,
)
