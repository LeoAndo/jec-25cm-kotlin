package jp.ac.jec.a03githubsearch

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView

/** 検索結果のリポジトリ一覧を表示する。タップ操作は受け付けない。 */
class RepositoryAdapter : ListAdapter<GithubRepository, RepositoryAdapter.ViewHolder>(DIFF_CALLBACK) {

    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val txtOwnerName: TextView = itemView.findViewById(R.id.txt_owner_name)
        val txtRepositoryName: TextView = itemView.findViewById(R.id.txt_repository_name)
        val txtStargazersCount: TextView = itemView.findViewById(R.id.txt_stargazers_count)
        val txtForksCount: TextView = itemView.findViewById(R.id.txt_forks_count)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val itemView = LayoutInflater.from(parent.context)
            .inflate(R.layout.list_item, parent, false)
        return ViewHolder(itemView)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val repository = getItem(position)
        holder.txtOwnerName.text = "所有者: ${repository.owner.login}"
        holder.txtRepositoryName.text = "リポジトリ名: ${repository.name}"
        holder.txtStargazersCount.text = "スター数: ${repository.stargazersCount}"
        holder.txtForksCount.text = "フォーク数: ${repository.forksCount}"
    }

    companion object {
        private val DIFF_CALLBACK = object : DiffUtil.ItemCallback<GithubRepository>() {
            override fun areItemsTheSame(oldItem: GithubRepository, newItem: GithubRepository) =
                oldItem.id == newItem.id

            override fun areContentsTheSame(oldItem: GithubRepository, newItem: GithubRepository) =
                oldItem == newItem
        }
    }
}
