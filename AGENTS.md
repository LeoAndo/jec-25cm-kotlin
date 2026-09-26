# AGENTS.md — このリポジトリで作業するAIエージェントへの指示

このファイルは、全エージェント（Claude Code・Codex・Cursor・Antigravity・Devin など）に共通の、ただ1つの指示書です。`CLAUDE.md` はこのファイルを読み込むだけにしてあります。

- **ルールはここに書く。** オーナー（LeoAndo）から新しいルールや方針を受け取ったら、エージェント固有の記憶（Claude Codeのmemory、Cursorのrules、DevinのKnowledgeなど）ではなく、このファイルか `README.md` を直すPRにする。固有の記憶は、ほかのエージェントから読めない。
- **教材の方針は `README.md` にある。** 「基本方針」「授業用教科書の基本方針」「単元の範囲の決め方」「完成コードの書き方」は、教材を触る前に読む。ここには重複して書かない。例外は§11で、READMEの「完成コードの書き方」を、このリポジトリの実物のコードを引いて具体化してある。
- **受講生像だけは、ここにも書く。** 下の「受講生像と、教材の書き方」は教材の全判断の前提になるので、READMEを開く前にここで読めるようにしてある。
- **単元ごとの判断は教員用ガイドにある。** `teacher/<スラッグ>/index.html` の「この単元の教材方針」に、何を意図的に外したか、なぜその書き方にしたかが理由つきで書いてある。その単元を触る前に読む。
- issue・PR・コミットメッセージは日本語で書く。

この授業は **Kotlin演習（JEC / 25CM）、1コマ90分 × 全15コマ**。単元は2系統ある。

| 系統 | 単元番号 | IDE | プロジェクト | 実行のしかた |
| --- | --- | --- | --- | --- |
| 純Kotlin | `K01` の1つだけ | IntelliJ IDEA | `K01HelloKotlin` の1つだけ（回ごとに `K01HelloKotlin/src/exNN/*.kt` を足す。Gradleを使わない） | `fun main()` を実行してコンソール出力を見る |
| Android | `A01`〜`A04` | Android Studio | `A01HelloAndroid` `A02CalcGame` `A03GithubSearch` `A04FunnyCamera`（単元ごとに別プロジェクト。Gradle） | エミュレータ `jec_25cm_kotlin_Pixel 9a` で動かす |

**純Kotlin系の単元は `K01` の1つだけで、`K02` 以降は作らない。** Kotlinの文法は全6コマを `K01HelloKotlin` という1つのプロジェクトで扱い、回を重ねるごとに `K01HelloKotlin/src/exNN/` のパッケージと、教科書 `docs/hello-kotlin/index.html` のSTEPを足していく（前年度の配布資料PDFと同じ、1つのプロジェクトにファイルを足していく進め方）。教科書も `docs/hello-kotlin/index.html` の1冊だけで、回ごとに新しいスラッグのフォルダを作らない。**「Kotlinの回（`exNN`）を足す」と「単元を足す」は別の作業で、手順も違う**（§9）。単元そのものが増えるのは、Android系（`A01`〜）だけである。

**Android系の基準バージョンは Android Studio Panda 2。** 教科書の手順・画面・生成される設定は、すべて Panda 2 を前提に書く。ひな形は `Panda2KotlinEmptyViewsActivity`（AGP 9.1.1／Gradle 9.3.1／compileSdk 36／targetSdk 36）にある。教員の開発マシンには Quail 4 が入っているので、**自分の手元の Android Studio で作ったプロジェクトを、そのまま完成プロジェクトにしない。** 新しい完成プロジェクトは、ひな形と同じ構成になっているかを `app/build.gradle.kts`・`gradle/libs.versions.toml`・`gradle/wrapper/gradle-wrapper.properties` の3つで確かめる。

`A01HelloAndroid`〜`A04FunnyCamera` は、ひな形と同じ構成にそろえてある（2026-09-23 に 4つとも `./gradlew assembleDebug` が通り、エミュレータでの起動とA03の通信まで確認した）。**そろえる対象はバージョン番号だけではない。** `buildTypes` のDSL（`optimization { enable = false }` は AGP 9.4 の書き方で、9.1.1 では通らない）、R8のkeepルールの置き場（`keepRules/rules.keep` か `proguard-rules.pro` か）、`gradle-daemon-jvm.properties` の toolchain、`gradle.properties` の `configuration-cache` も版によって変わる。**8か所の一覧はREADMEの「教員が確認に使うプロジェクト」にある。**

2系統あることが、この運用のほとんどの分岐の理由になっている。**どちらの系統の作業かを先に決めてから読み進める。**

## 受講生像と、教材の書き方

**受講生は Java と Swift を学習済みで、Kotlinを初めて書く。** 「Kotlin初学者」とは「Kotlinという言語を初めて書く経験者」という意味で、プログラミングの入門者ではない。教材を1文でも書く前に、この前提を思い出すこと。

- **概念そのものの説明はしない。** 変数・条件分岐・繰り返し・クラスが何かは書かない。書くのは、**Kotlinでの書き方と、Java／Swiftとの違いと、違う理由**。
- **教科書の各STEPには、JavaかSwift（または両方）との比較を必ず置く。** 比較がないSTEPは未完成とみなす。比較する相手がないKotlin独自の機能（`by lazy` など）は比較を省かず、「Java／Swiftでは同じことをどう書くか、あるいは書けないか」を示す。
- **確認欄と「最後の3分」に、振り返りの言い方を書かない。** 「気づいたことを1つメモします」や「〜を言えた」「〜を説明できた」のように、学生に自分の理解を言葉で確かめさせる書き方はしない（オーナーの方針）。受講生はJavaとSwiftを書けるので、この足場は要らない。**確認欄には、画面で確かめられることだけを書く。** コンソールに出た行、赤い波線が出た行、マウスを重ねて出た型、`src` に並んだパッケージ。教員用ガイドの「終了時の確認」「到達度の確認」も同じ形にする。教員が問いを出して答えを確かめる「理解確認に使う短い問い」は、教員の技法なので残してよいが、答えの欄に「〜と言えれば十分」「〜まで言えたら到達」とは書かず、期待する答えそのものを書く。
- **用語に読みがなは振らない。** 代わりに、Kotlin固有の用語（プライマリコンストラクタ、スマートキャスト、拡張関数、委譲プロパティ）には**Java／Swiftでの対応物**を添える。
- **「1単元で導入する新概念は1つまで」の「新概念」は、JavaにもSwiftにもないものを指す。** `if` や `for` のように書き方だけが違うものは数えない（READMEの「単元の範囲の決め方」）。
- **予習も復習もしない前提で、前から順に読めば進める**という構成の原則と、**本文からほかの単元へ送らない**という原則は、いままでどおり守る（READMEの「授業用教科書の基本方針」）。
- **Android系の単元の教科書は、「アレンジできる場所」が分かる形で終わらせる。** 最後のSTEPまで進めた学生が、**どこを変えると、画面や動きの何が変わるか**を、その単元のコードの中で見つけられるようにする。挙げるのは、その単元で扱った範囲で変えられるもの（文字・色・数値・問題数など）だけで、新しい概念やAPIをここで足さない（新概念は1単元1つまで。READMEの「単元の範囲の決め方」）。提出課題が「自分で作ったAndroidアプリを1つ選んでアレンジし、APKで出す」形なので、単元の終わりが、そのときの手がかりになる（READMEの「提出課題」「授業用教科書の基本方針」の11）。例は挙げるが、正解は決めない。純Kotlin系（`K01`〜）はコンソールアプリで提出の対象外なので、この形は求めない。
- この比較方式は、前年度（2025年度）の配布資料PDFの書き方を引き継いだもの。資料の各節と `K01HelloKotlin/src/exNN/` の対応表はREADMEの「前年度の教材との関係」にある。**PDF自体はリポジトリにcommitしない**（置き場は `~/Documents/jec-25cm-kotlin-verification-deliverables/`。§2のPoC置き場と同じ）。

## 1. 作業の単位

**1 issue = 1 ブランチ = 1 worktree = 1 セッション = 1 PR。**

- 1つのセッションで、2つ目のissueや別の単元の作業を始めない。頼まれたら、別のセッション（別のworktree）で行うことを提案する。
- 例外：同じ種類の `size:XS` のissueは、1つのPRでまとめて閉じてよい（`Closes #<番号1>, closes #<番号2>`）。
- 新しい単元（Android系）は「完成プロジェクト」と「教材一式（教科書＋教員用ガイド＋登録）」の2つのissueに分ける。1つにまとめると `size:XL` になり、1セッションに収まらない（§6）。Kotlinの回（`exNN`）を足すissueは単元を増やさないので、この分割は要らない（§9）。

## 2. 作業場所

- ローカルのcloneは1つだけにする。cloneした場所そのもの（mainチェックアウト）は、オーナーとIntelliJ IDEA／Android Studioが使う。常に `main` のままにして、そこではブランチを切り替えず、コミットもしない。
- エージェントは必ずworktreeで作業する。ツールが自動で作るworktree（Claude Codeの `.claude/worktrees/` など）はそのまま使ってよい。手動で作るときは、mainチェックアウトの外に作る（次のコマンドはmainチェックアウトで実行する）。

  ```sh
  git fetch origin --prune
  git worktree add ../jec-25cm-kotlin.worktrees/issue-<番号>-<slug> -b issue-<番号>-<slug> origin/main
  ```

- `git stash` は使わない。stashは全worktreeで共有されるので、ほかのセッションの変更を取り出してしまう。退避したいときはWIPコミットにする。
- **Android単元**：worktreeには `local.properties` がない（Git管理外のため）。ビルドは環境変数 `ANDROID_HOME` で通す。未設定なら、コマンドの前に付ける。`local.properties` は作ってもコミットしない。

  ```sh
  cd A01HelloAndroid && ANDROID_HOME="$HOME/Library/Android/sdk" ./gradlew assembleDebug
  ```

- **純Kotlin系（`K01`）**：`K01HelloKotlin` はGradleプロジェクトではないので、コマンドラインのビルドがない。**IntelliJ IDEA で `K01HelloKotlin` を開き、対象の `exNN/main.kt` の `fun main()` を実行して、Runツールウィンドウの出力を目で確かめる。** プロジェクトは1つだけなので、どの回の作業でも開くのは `K01HelloKotlin` である。`.idea/` はGit管理外（リポジトリ直下の `.gitignore`）なので、worktreeで初めて開いたときはJDKとKotlinの設定を聞かれる。これは正常で、設定ファイルはコミットしない。
- **commitしないPoC成果物は、リポジトリの外に置く。** 置き場は `~/Documents/jec-25cm-kotlin-verification-deliverables`。なければ作る。

  ```sh
  mkdir -p ~/Documents/jec-25cm-kotlin-verification-deliverables
  ```

  ここに置くのは、検証のために撮った大量のスクリーンショット、検証結果をまとめただけのHTML、配布予定のないPoCプロジェクト、コンソール出力を貼っただけのログなど、commitするとリポジトリが重くなるもの。リポジトリの外なので `.gitignore` は要らない。worktreeの中に作ると、`git clean` やworktreeの削除で消える。
- この置き場のバックアップは取らない。消えて困るものは置かない。教材として配布するスクリーンショットは、ここではなく `docs/<スラッグ>/images/` にcommitする。

## 3. 着手から後片付けまで

1. `git fetch origin --prune` してから、issueを読む（`gh issue view <番号>`）。
2. 重複着手がないことを確認する。`gh pr list --state open` と `git branch -r` に `issue-<番号>-` があれば、誰かが作業中。マージ済みのブランチはGitHubが自動で消すので（リポジトリ設定の **Automatically delete head branches**。APIでは `delete_branch_on_merge`）、リモートにブランチがあること自体が作業中の目印になる。issue本文に「#NN とは同時に進めない」と相手の番号が挙がっていたら、その番号についても同じ確認をする。
   - **リモートだけでは足りない。ローカルのブランチとworktreeも見る。** 手順4のとおりすぐpushしても、ブランチを作ってからpushするまでの数十秒は、リモートに何も出ない。まとめて起動された並行セッションは、全員が同時にこの窓に入る。

     ```sh
     git branch -vv | grep "issue-<番号>-"
     git worktree list
     ```

     ローカルのcloneは1つだけなので（§2）、worktreeとローカルブランチは全セッションで共有される。まだpushされていない別セッションのブランチも、この2つには出る。
   - **見つけたら、先に着手した側を優先し、あとから来た側が降りる。** どちらが先かは `git reflog show --date=iso <ブランチ名>` で分かる。reflogは新しい順に出るので、作成時刻は末尾の `Created from` の行を見る（手順4でブランチ名を直していると、その上に `renamed` の行が載る）。降りるときは、自分が出してしまった目印を全部片付ける。worktreeを消し（`git worktree remove <パス>`）、その外からローカルブランチを消し（コミット済みなら `git branch -D`）、pushしていればリモートも消す（`git push -d origin issue-<番号>-<slug>`）。手順9がworktreeとローカルブランチの削除を書いているのは「マージ後」なので、降りるときは自分で3つとも消す。ローカルに残すと、この確認が、やめた作業を作業中と誤判定する。
3. 共有ファイル（§4）を触るissueなら、共有ファイルを触るPRがほかに開いていないことを確認する（`gh pr list --state open --label area:shared`）。
4. `origin/main` からブランチ `issue-<番号>-<slug>` を作り、**コミットがなくてもすぐ `git push -u origin issue-<番号>-<slug>` する。** 調査の長いissueでは最初のコミットまで時間がかかることがあり、その間、手順2で見える「作業中」の目印が何も出ない。エージェント名（`claude/`、`codex/`）は付けない。ツールが別の名前でブランチを作っていたら、pushする前に `git branch -m issue-<番号>-<slug>` で直す。
5. 最初のコミットをpushしたら、すぐDraft PRを開く（本文に `Closes #<番号>`）。このときの本文はひな形でよく、完成版に仕上げるのはDraftのうちにする（§8）。Draft PRは「作業中」の目印で、利用制限などで別のエージェントに交代するときの引き継ぎ先にもなる。進み具合はセッションの中ではなく、pushしたコミットとPR本文のチェックリストに残す。
6. **編集を始める直前と、pushの直前に、もう一度 `git fetch origin --prune` する。** 調査やsubagentの待ち時間が長いと、その間に `origin/main` が進み、同じファイルを触るPRが先にマージされていることがある。あわせて手順2・3の確認もやり直す。手順2のローカルのブランチとworktreeも、そのたびに見る。着手したときは未pushだった別セッションが、ここで初めて見えることがある。このとき、手順4で出した自分のブランチ・worktree・PRは数えない（`issue-<自分の番号>-` と自分のPR番号を除いて見る）。
   - まだコミットがなければ、`git merge --ff-only origin/main` で追従してから編集する。
   - コミット済みで、`origin/main` が自分と同じファイルを変えていたら、試しにマージして（作業ツリーは変わらない）、衝突の有無とマージ後のファイルの形を確かめる。

     ```sh
     if T=$(git merge-tree --write-tree HEAD origin/main); then
       git show "${T}:teacher/hello-kotlin/index.html"   # 衝突なし。マージ後の形を確認する
     else
       echo "$T"                                        # 衝突あり。競合したファイルが出る
     fi
     ```

     衝突があると終了コードが1になり、`$T` はtree IDだけでなく競合情報も含む複数行になる。そのまま `git show "${T}:..."` に渡すと `invalid object name` で失敗するので、終了コードで分ける。

     zshでは `git show $T:teacher/...` と書くと `:t` が修飾子と解釈されて失敗するので、`"${T}:..."` と波かっこで囲む。
   - push前ならrebaseしてよい。push済みなら履歴は書き換えず（§5）、必要なら `git merge origin/main` する。
7. issueの「触る範囲」の外は触らない。範囲外で気付いたことは§6の手順でissueにする。
8. コミットは§5、検証は§7の手順で行う。検証が済んだらDraftを外す。レビュー対応は§8。
9. マージ後はworktreeを消す（`git worktree remove <パス>`）。ローカルブランチは `git branch -d` で消す。マージせずに作業をやめたときは、手順4で出した目印のブランチも消す（`git push -d origin issue-<番号>-<slug>`）。GitHubが自動で消すのはマージ済みのブランチだけなので、残すとほかのセッションが作業中と誤解する。
   - **マージしたのにリモートのブランチが残っていたら、設定を確かめる。** 2026-09-24まではこの設定が無効で、マージしたブランチが残っていた（#47）。`false` なら、オーナーに報告してから自分のブランチを `git push -d` で消す。

     ```sh
     gh api repos/LeoAndo/jec-25cm-kotlin --jq .delete_branch_on_merge   # true のはず
     ```

   - **`git branch -d` が `not fully merged` で止まることがある。** リモートのブランチが消えると、`-d` はリモートではなく、いまいるworktreeのHEADと比べる。HEADが古いmainのままだと、マージ済みでも止まる。mainに入っていることを確かめてから `-D` で消す。

     ```sh
     git fetch origin --prune
     git merge-base --is-ancestor issue-<番号>-<slug> origin/main && git branch -D issue-<番号>-<slug>
     ```

## 4. 並行してよい範囲

| 触る場所 | 並行 |
| --- | --- |
| Android単元ごとの場所だけ（`A0NXxx/` と、その単元の `docs/<スラッグ>/`・`teacher/<スラッグ>/`） | 別の単元のissueとは並行してよい。同じ単元のissue同士は直列 |
| 純Kotlin（`K01`）の回ごとの場所だけ（`K01HelloKotlin/src/exNN/` の中だけ） | 別の `exNN` のissueとは並行してよい。ただし下の注意を読む |
| 共有ファイル：リポジトリ直下のファイル（`README.md`、`AGENTS.md`、`CLAUDE.md`、`.gitignore`）、`config/`、`scripts/`、`docs/common/`、`docs/assets/`、`.github/`、`skills/` | 同時に開くPRは1本まで（ラベル `area:shared`） |
| 対訳カタログ：`i18n/<言語>/`（§12） | 別の言語のissueとは並行してよい。単元や共有ファイルのissueとも並行してよい。同じ言語のissue同士は直列（ラベル `area:i18n`） |

- **純Kotlin系は、回が別でもプロジェクトが1つ（`K01HelloKotlin`）であることに注意する。** `K01HelloKotlin/src/exNN/` の中だけなら、別の `exNN` のissueと並行してよい。ただし、次の3つは回をまたいで共有される。
  - `K01HelloKotlin/.gitignore` とプロジェクト直下。ここを触るissueは共有ファイル扱いにする。
  - 配布ZIP `docs/hello-kotlin/downloads/K01HelloKotlin.zip`。K01の `archive` はこの1つで、どの `exNN` を足してもこのZIPの中身が変わる。**並行する2本のPRが両方このZIPを作り直すと、バイナリなのでマージで必ず衝突する。** 片方がマージされたあと、§3の手順6でもう一度 `python3 scripts/package-project.py --project K01HelloKotlin --output docs/hello-kotlin/downloads/K01HelloKotlin.zip` を実行し直して、自分のPRのZIPを作り直す。ZIPは決め打ちタイムスタンプで作るので、中身が同じなら同じバイト列になる。
  - 教科書 `docs/hello-kotlin/index.html`、教員用ガイド `teacher/hello-kotlin/index.html`、`config/teaching-materials.json` のK01の項目。**回を足すと、この3つは必ず同じ場所（STEPの列、進め方、`packages`／`sources`）が伸びる。** `config/` は共有ファイルなので、教科書やconfigまで触る回のissueは、同時に開くPRを1本までにする（ラベル `area:shared`）。並行してよいのは、`K01HelloKotlin/src/exNN/` だけで完結するissueである。
- **`Panda2KotlinEmptyViewsActivity` と `Quail4KotlinEmptyViewsActivity` は単元ではない。** Android StudioのNew Projectウィザードが生成したひな形を、版ごとにそのまま置いてあるものである（Panda 2 と Quail 4）。教材の手順が古くなっていないかを、この2つを見比べて確かめるために置いている。`config/teaching-materials.json` には登録せず、学生用ZIPにも入れない。**中身に手を入れない。** 手を入れると「ウィザードが生成したそのままの形」という価値がなくなり、比較の基準として使えなくなる。版を上げるときは、新しい版のAndroid Studioで作り直したものを別のフォルダとして足す。
- 新しい単元の登録（§9。登録するのはAndroid系の単元だけ）は必ず共有ファイルに当たる。2つの単元を同時に登録しない。登録のPRは、既存の全単元の教科書のサイドバーも触る（§9の手順6）。`<div class="resources">` は全体で1行なので、ほかの単元のPRが同じ行を触っていると、先にマージされた側と衝突する。相手のPRが開いているあいだは、手順6では分からない（比べる相手が `origin/main` だけのため）。相手がマージされたあとの§3の手順6で確かめ、両方の変更を残す。
- 教科書 `docs/<スラッグ>/index.html` から他単元へのリンクは、topbarとサイドバーの2か所にある。どちらも本文ではなく導線で、手順やコードを他単元へ送るものではない（READMEの「授業用教科書の基本方針」が禁じているのは、本文から送ること）。サイドバーに先の単元へのリンクがあっても、方針違反ではない。
  - **サイドバー**（`<div class="resources">` の1行）には、どの単元でも全単元を単元番号順に並べる。位置は「完成プロジェクトを開く」のあと、「共通：…」の前。いま開いている単元だけはリンクにせず、現在地として書く（K01なら `<span aria-current="page">K01：HelloKotlin</span>`）。表示名は、`projects[].name` を番号と残りに分けて全角コロンでつないだ形にする。項目の中に別のタグは入れない。`scripts/check-teaching-materials.py` が、`config/teaching-materials.json` の `projects` の並びと、リンク先・表示名まで照合する。単元を足して1冊でも直し忘れると、CIが落ちる。位置は検査されない。
  - **2系統の並び順は「K→A」。** 検査は、`projects` に最初に現れた接頭辞の順で並んでいること、同じ接頭辞の中では番号が昇順であることを見る。**一度Aに変わったあとでKに戻るとエラーになる。** 純Kotlin系は `K01HelloKotlin` の1つだけなので、`projects` は `K01HelloKotlin` を先頭に、そのうしろへAndroid単元を番号順に並べる形で固定される。Kotlinの回を足しても、この並びは変わらない（単元が増えないため）。
  - **topbar** は、直前の単元へのリンク1つだけにする（K01はなし）。こちらは検査されない。単元を挿入したときや、並行して作った単元をマージしたあとは、次の単元のtopbarが直前の単元を指しているかを目で確かめる。指す先が実在するかぎりリンク切れにはならないので、CIでは検出できない。

## 5. コミットのしかた

- `git add -A` と `git add .` は使わない。パスを明示する。
- **コミットの直前に必ず `git diff --cached --name-only` を見て、意図したファイルだけがstageされていることを確認する。** IntelliJ IDEA と Android Studio が新規ファイルを自動でstageすることがあり、パスを明示して `git add` しても無関係なファイルが紛れ込む。このリポジトリで特に紛れやすいのは次の3つ。

  | 混入するもの | 出どころ |
  | --- | --- |
  | `.idea/`、`*.iml` | IntelliJ IDEA で `K01HelloKotlin` を開いたとき |
  | `out/`、`.kotlin` | `fun main()` を実行したとき（`K01HelloKotlin/.gitignore` が無視する） |
  | `local.properties`、`.gradle/`、`build/` | Android Studio でGradle同期したとき |

- 混入に気付いたら、push前なら `git rm --cached` して `--amend` する。push済みなら別コミットで `git rm --cached` する（履歴は書き換えない）。
- PRタイトルは、学生が読んで分かる日本語にする。学生向けリリースノートに載るため（READMEの「リリースノートとフィードバックの扱い」）。

## 6. 気付いた別課題はissueにする

- 今のissueの完了条件に含まれるもの、PRを正しくするために必要なものは、そのPRで直す。
- それ以外は、その場で直さずにissueにする。今のPRには混ぜない。
- 起票の前に既存のissueを検索する（closedも含める）。検索語は1つずつ指定する。`OR` でつなぐと、リポジトリの絞り込みが外れて他人のリポジトリのissueが返る。

  ```sh
  gh issue list --state all --search "<語>"
  ```

- ラベルは `size:*` を1つ、`area:*` を当てはまるだけ付ける。本文は次の書式にする。

  ```markdown
  ## 背景
  ## 目的
  ## 再現条件（不具合でなければ「対象」）
  ## 完了条件
  ## 見積（基準：Claude Code / Opus 5 / effort high、2026-09-23）
  - サイズ：S（同種の既存issueと比べて決めた）
  - 推奨構成：軽い構成で可（判断の要らない機械的な修正）
  - 人間の確認：XS（差分の目視のみ）
  - 触る範囲：K01HelloKotlin/src/ex02/、docs/hello-kotlin/、teacher/hello-kotlin/、config/teaching-materials.json（共有ファイルあり）
  ```

  サイズの根拠には、**実在する既存のissue・PRの番号だけ**を書く。思い当たる番号がなければ、番号を書かずに「同種の既存issueと比べて決めた」と書く。存在しない番号を書くと、あとから根拠をたどれない。
- issueを分割・統合してクローズしたら、そのissueを「同時に進めない」相手として挙げているほかのissueの本文も直す。参照先が古いままだと、§3の手順2どおりに相手の状況を調べても、実際に作業中のissueに気付けない。

### 見積の基準

サイズは時間ではなく、**基準の構成で1セッション（1コンテキスト）に収まるか**で決める。基準の構成は `Claude Code / Opus 5 / effort high、2026-09-23`。差分の行数では決めない（Androidプロジェクトのひな形でファイル数が膨らむため）。過去のissue・PRと比べて「あれと同じくらい」と決めると、モデルの世代が変わっても使える。

| サイズ | 定義と、このリポジトリでの例 |
| --- | --- |
| `size:XS` | 1ファイル、判断不要、ビルドも実行確認も要らない。例：教科書の誤記を1か所直す、READMEのリンクを1本直す、`teacher/` のコメントを足す |
| `size:S` | 1単元（Kotlinなら1回）に閉じた数ファイルの変更。検査スクリプトか、1回の実行・ビルドで確認できる。例：`K01HelloKotlin/src/exNN` を1つ足して教科書にSTEPを1つ書き足す（§9のKotlinの回の手順）、Android単元の文言を直して `assembleDebug` を通す |
| `size:M` | 複数の単元や共有ファイルにまたがり、全体の照合が要る。例：`scripts/` のロジックを変える、`config/teaching-materials.json` のスキーマを変える、`docs/common/` にページを足す、全教科書のサイドバーを機械的に直す |
| `size:L` | 単元の完成プロジェクト1つ、または教材一式（教科書＋教員用ガイド＋登録）1単元ぶん。1セッションの上限。例：`A0NXxx/` を新規に作る、Android単元の教科書を1冊書いて登録まで済ませる |
| `size:XL` | 1セッションに収まらない。見積値ではなく分割の合図。このまま着手しない。例：完成プロジェクトと教材一式を1つのPRにまとめる、2つの単元を同時に登録する |

- **推奨構成**は、その作業に足りる最小のモデルとエフォートを書く。判断の要らない機械的な修正（XS・S）は軽い構成でよい。教材の設計判断が要る作業は、最上位のモデルと高いエフォートにする。
- ClaudeとCodexのエフォート段階は同じ尺度ではないので、換算係数は作らない。基準は見出しの1構成に固定し、ほかのエージェントについては「この作業に使える／使えない」だけを書く。基準の構成を変えるときは、この節の書式例と日付を直す。
- **人間の確認**は、オーナーの確認にかかる手間を書く。XS＝差分の目視のみ、S＝IntelliJ IDEAでの実行かエミュレータでの動作確認、M＝複数の単元やファイルの確認、L＝教科書の通読。
- PR本文の最後に実績を1行で残す。見積と実績がずれたら、上の表の例を直す。

  ```markdown
  実績：Claude Code / Opus 5 / high、1セッション、レビュー往復2回
  ```

## 7. 検証

- 教材・設定・スクリプトを触ったら、次の4つを通す。**4つ目は配布物に入れるファイルを `git ls-files -- docs` で選ぶので、新しいファイルは先に `git add` しておく。** 未追跡のままだと、エラーにならずに配布物から抜け落ちる。**3つ目は `docs/` 配下のHTMLをファイルシステムから直接読むので、未追跡のHTMLも検査の対象になる**（`git add` の前でも、禁止事項を書いていれば行番号つきで落ちる）。

  ```sh
  python3 scripts/check-teaching-materials.py
  python3 -m unittest discover -s scripts -p 'test_*.py'
  python3 scripts/localize-student-materials.py check
  python3 scripts/package-student-materials.py
  ```

  **Python 3.11以上が要る。** `scripts/test_*.py` が `unittest.TestCase.enterContext`（3.11で入ったもの）を使っている。3.10以下だと2つ目のコマンドだけが大量に失敗するので、コードの不具合と取り違えないこと。`python3 -V` で確かめる。

  それぞれが見ているもの：1つ目は `config/teaching-materials.json` と教材の照合（コマ数の合計、サイドバーの並び、スニペットのバイト一致、ZIPの内容一致、指定AVD名の表記）、2つ目はスクリプト自身のテスト、3つ目は教科書HTMLから翻訳用の文を取り出せるか（§12の禁止事項を行番号つきで落とす）、4つ目は配布ZIPが最後まで組み立つか。
- **Android単元**を触ったら、その単元をビルドする（§2）。画面に関わる変更は、エミュレータ `jec_25cm_kotlin_Pixel 9a` で確認する。教科書のスクリーンショットもこのエミュレータで撮る。
- **純Kotlin系（`K01`）**を触ったら、IntelliJ IDEA でその `exNN` の `fun main()` を実行し、コンソール出力が教科書に書いたとおりかを目で確かめる（§2）。教科書の `<pre id="...">` とソースのバイト一致は1つ目のコマンドが見るが、**出力が正しいかどうかは、上の4つのコマンドでは確かめられない。**
  - **エージェントは、IntelliJ IDEA に同梱の Kotlin コンパイラで、出力と警告をコマンドラインから確かめられる。** 教科書に載せる実行結果・「赤くなる／通る」と書いた挙動・完成コードに警告が出ないことは、**書く前に必ずこれで確かめる。** 一時ファイルはリポジトリの外（`/tmp` など）に置く。

    ```sh
    (
      set -e
      KC="$HOME/Applications/IntelliJ IDEA.app/Contents/plugins/Kotlin/kotlinc"
      "$KC/bin/kotlinc-jvm" -version  # 版を確かめる（2026-09-23 時点で 2.4.10）
      KOTLIN_CHECK_DIR=$(mktemp -d "${TMPDIR:-/tmp}/jec-kotlin-check.XXXXXX")
      trap 'rm -rf "$KOTLIN_CHECK_DIR"' EXIT
      "$KC/bin/kotlinc-jvm" -d "$KOTLIN_CHECK_DIR" K01HelloKotlin/src/ex03/main.kt
      java -cp "$KOTLIN_CHECK_DIR:$KC/lib/kotlin-stdlib.jar" ex03.MainKt
    )
    ```

    毎回新しい出力先を使い、コンパイルに失敗したら実行せずに終了する。最後に出力先を削除するので、以前のクラスの出力を今回の結果と取り違えない。警告もコンパイル時に表示される。

    **`-nowarn` を付けない。** 付けると警告が消え、確かめたことにならない。これで見つかった誤りが2つある。1コマ目で `Val cannot be reassigned` と書いたが、Kotlin 2.x（K2）が出すのは `'val' cannot be reassigned` だった。2コマ目の完成コードの最後の `name2?.count()` には `unnecessary safe call` の警告が出るのに、教科書に説明がなかった。**エラーや警告の文言は教科書に引用しない**（「おおよそこういう意味のメッセージが出ます。言い回しは版で変わります」と書く）。確かめるのは、止まるか通るか、どの行か、警告が出るかどうかである。
- **完成プロジェクトにUnit Testは書かない。** 動作はIntelliJ IDEAの実行と、エミュレータ・Logcatで確認する。`scripts/test_*.py` はCIで実行されるので、通る状態を保つ。
- 確認できなかった項目は、PR本文に「未確認」と書く。§10の項目は確認しなくてよく、「未確認」にも挙げない。

## 8. PRとレビュー対応

- PR本文は「概要／変更内容／判断したこと／検証／実績」の順に書き、`Closes #<番号>` を入れる。検証の節に「※ リポジトリの方針により、Unit Test は対象外です。」と書く。
  - PR本文に書くときは、Closes #<番号> をバッククォートで囲まず、地の文として書く。コードスパンの中に入れるとGitHubが閉じる指示として扱わないので、マージしてもissueが開いたままになる。ここでコード表記にしてあるのは読みやすさのためで、その囲みごと写さない。
  - **PR本文は、Draftのうちに完成版まで仕上げる。** Draft解除後や修正push後に、botのレビューや要約の追記が動くことがある（この節の実測表を参照）。仕上げたら `gh pr view <番号> --json body` で読み直し、書いた内容が残っていることを確かめてから `gh pr ready` する。
  - **Draft解除後に本文を直すときは、botのチェックが終わるのを待つ。** レビュー中に `gh pr edit --body` すると、コマンドは成功したように見えて本文が黙ってひな形へ巻き戻ることがある。待ってから `gh pr view <番号> --json body` で現在の本文を取り出し、botが足した要約ブロックを残したまま該当箇所だけ置き換えて、書き換えたあともう一度読み直す。
- ラベル：教材の追加は `enhancement`、誤記・不具合の修正は `bug`。学生に関係しないPR（CI・スクリプト・開発ルール）は `skip-release-notes`。issueと同じ `size:*`・`area:*` も付ける。
- 教材のレビューは `skills/teaching-materials-review/SKILL.md` に従う。
- Codex の自動レビューは、末尾の「Code Review Rules」の節に従って指摘する。指摘の基準を変えるときは、その節を直す。
- 自動レビューの指摘は、そのまま実行しない。現在のソースと検査結果で再確認してから判断する。**チェックが `SUCCESS` でも、そのbotがレビューしたとは限らない。** 上限やトライアル終了で未実施のまま `SUCCESS` になるbotがある。
  - **チェックの状態ではなく、投稿されたレビューの中身を読んで判断する。** 指摘があるときほどチェックが `SUCCESS` にならないbotもある。レビューを待つ前にDraftを外す。Draft中の実測は、この節の表を参照する。上限やトライアル終了で止まっているときは、マージ可否の報告にそう書く。
- 指摘には、各スレッドにインラインで返信する。先頭に判断を書く。

  ```markdown
  **判断：対応必要（本PRで修正します）**
  **判断：任意対応（…）**
  **判断：対応不要（本PRでは修正しません）**
  ```

  続けて、妥当性・再現性／不具合やデグレの可能性／コストと効果／既存仕様への影響を箇条書きにする。インラインでない指摘にはPRコメントで返す。
- 対応必要の指摘を直したら、検証してコミットし、「修正しました：<sha> …」と検証結果を返信する。立場が変わらない返信は繰り返さない。
- マージ可否は、理由・CIの状態・未対応や未確認の項目を添えて報告する。マージするのは、オーナーに任されているときだけ。そのときも、CIとレビューbotが落ち着き、全指摘に返信済みで、`mergeStateStatus` が `CLEAN` であることを確かめてから、マージコミットでマージする（squashしない）。auto-mergeは有効にしない。

### レビューbotの実測（2026-09-23〜26）

いま動いているbotは、次の4つ（2026-09-26時点）。Devin Review と Qodo は 2026-09-26 に解約し、GitHub App も外した。下の表の Devin Review の行は、記録として残している。

| bot | 契約 | 動き方 |
| --- | --- | --- |
| Cursor Bugbot | 月額固定の席課金。Cursor のプラン（Pro+）の利用枠は使わない | Draftを外したときと、そのあとのpushのたびにレビューする |
| CodeRabbit | Essentials。枠を超えた分は従量課金（1ファイル $0.25）で続ける設定（Continue automatically） | 自動でレビューする。直近7日のレビュー件数が多いと、1時間あたりの枠が減り、超えた分は従量課金でレビューする（下の「2026-09-26の集計」） |
| Codex | ChatGPT Pro に含まれる。2026-09-26 に自動レビューを有効にした | PRを開いたとき・Draftを外したとき・`@codex review` とコメントしたときにレビューする。pushでは見直さないので、修正のあとに見直させたいときは `@codex review` とコメントする。GitHub では P0・P1 だけを指摘し、見出しがちょうど「Code Review Rules」の節に従う。指摘がないときは、PR本文への 👍 か「Didn't find any major issues」のコメントだけを残す（下の「2026-09-26の集計」） |
| Copilot | 教員の無償の Copilot Pro | 月の枠を使い切ると、未実施の通知だけをレビューとして投稿する。枠は毎月1日 09:00（日本時間）に戻る |

対象は [PR #1](https://github.com/LeoAndo/jec-25cm-kotlin/pull/1)・[PR #4](https://github.com/LeoAndo/jec-25cm-kotlin/pull/4)・[PR #7](https://github.com/LeoAndo/jec-25cm-kotlin/pull/7)。PR #7は `c36853e` 時点。所要時間と上限は、その時点の契約・残り枠による実測であり、今後の動作を保証するものではない。

| bot | Draft中 | Draft解除後・修正push後 | 実際の指摘 | PR本文への追記 |
| --- | --- | --- | --- | --- |
| Cursor Bugbot | PR #4・#7ではレビュー投稿なし | 解除から約2〜3分で完了。指摘なしは `SUCCESS`。PR #1で指摘があった回は `NEUTRAL`（`gh pr checks` では `skipping`）。修正push後も再レビューする | PR #1で2件。修正後にbot自身がスレッドを解決済みにした。PR #7の最新コミットも指摘なし | 3本とも `<!-- CURSOR_SUMMARY -->` の要約を追記 |
| CodeRabbit | `SUCCESS / Review skipped: draft pull request` | PR #4は解除から約13分、PR #7は約17分でレビューを投稿。修正push後は両PRで `SUCCESS / Review rate limited`。PR #1はマージ時まで `PENDING` でレビュー投稿なし、その後 `SUCCESS / Review skipped` へ変化 | PR #4で1件、PR #7で7件。上限中でも個別スレッドへの返信は行われ、PR #7の7件はbot自身が解決済みにした。ただし最新コミット全体の再レビュー完了とは別 | 3本とも「Summary by CodeRabbit」を追記 |
| Devin Review | 未確認 | PR #1の初回はレビューを投稿。その後のPR #1・#4では `SUCCESS / Full review skipped: trial expired and no credits remaining` | 初回の3件は進捗の消去・同日公開のZIP名衝突・Python版の前提。以降の `SUCCESS` はレビュー未実施 | なし |
| Copilot | 未確認 | PR #1・#4・#7でレビューを投稿したが、本文はクォータ上限による未実施通知 | コードへの指摘なし | なし |

- **チェックの `SUCCESS` やレビュー投稿の存在だけで、レビュー済みと判断しない。** チェックの説明・レビュー本文・対象コミットを読む。Devin Reviewの未実施通知やCodeRabbitの上限通知を、指摘なしのレビューと取り違えない。
- **CodeRabbitが `PENDING` のまま止まると、`mergeStateStatus` が `CLEAN` にならない場合がある。** [PR #1のマージ時点の記録](https://github.com/LeoAndo/jec-25cm-kotlin/pull/1#issuecomment-5793899227)がこの例である。レビュー投稿なしで止まっていることをマージ可否の報告に書き、オーナーに判断を仰ぐ。
- **BugbotとCodeRabbitはPR本文に要約を追記する**（CodeRabbitは、上限で止まっている回は追記しない）。本文を変更するときは、チェックが終わってから現在の本文を取り直し、両botの要約ブロックを残して該当箇所だけ変更する。
- 契約・上限・動作が変わったら、この表を更新するissueを立てる（§6）。実測せずに、ほかのリポジトリの表を写さない。

#### 2026-09-24の実測（CodeRabbitが上限で止まった回）

対象は [PR #42](https://github.com/LeoAndo/jec-25cm-kotlin/pull/42)（`9ff8668`）・[PR #49](https://github.com/LeoAndo/jec-25cm-kotlin/pull/49)（`268f02b`）。どちらもDraftのうちに本文を仕上げてから解除した。

| bot | Draft中 | Draft解除後 | 実際の指摘 | PR本文への追記 |
| --- | --- | --- | --- | --- |
| Cursor Bugbot | PR #42ではチェックなし | PR #42は解除から約3分、PR #49は約2分で `SUCCESS` | 両PRとも指摘なし | 両PRとも `<!-- CURSOR_SUMMARY -->` の要約を追記 |
| CodeRabbit | `SUCCESS / Review skipped: draft pull request`。PRコメント「Draft PR not reviewed」に「Trigger a manual review」のチェックボックスが付く | 解除とほぼ同時に `SUCCESS / Review rate limited`。同じPRコメントが「Review paused — included plan limit reached」に書き換わり、チェックボックスが2つ付く（下の注意）。次の枠までの待ち時間は、PR #42で26分、PR #49で8分と表示 | 両PRともレビュー投稿なし | なし |
| Devin Review | PR #42ではチェックなし | 両PRとも `SUCCESS / Full review skipped: trial expired and no credits remaining` | レビュー未実施 | なし |
| Copilot | PR #42ではレビュー投稿なし | 両PRとも、クォータ上限による未実施通知をレビューとして投稿 | レビュー未実施 | なし |

- **CodeRabbitのコメントにあるチェックボックスは押さない。** 「Run this review for free」はオンデマンドレビューで、2026-09-24の表示では16日間は無料、そのあとは1ファイル0.25ドルかかる。「Ask an admin to make reviews automatic」は管理者への依頼である。どちらも課金や契約に関わるので、使うかどうかはオーナーが決める。Draft中の「Trigger a manual review」も押さない（レビューの枠を使ううえ、Draftを外してからレビューを受けるこの節の進め方と合わない）。
- 表示された待ち時間が過ぎたあと、自動でレビューが始まるかは未確認。PR #42はオーナーの指示で、PR #49は同じ日の続きの作業として、CodeRabbitを待たずにマージした。この指示はその日の作業に限ったもので、恒久の規則ではない。上限で止まっているときは、これまでどおりマージ可否の報告にそう書き、待つかどうかをオーナーに聞く。

#### 2026-09-26の集計（PR 72本）

対象は、2026-09-23〜25 に開いた全PR 72本（#1〜#199）。各PRのチェック・status・レビュー・コメントを読み、botごとに数えた。「対応必要」は、指摘への返信の判断（この節の書式）で数えた。

| bot | 記録のあったPR | レビューしたPR | 止まった理由（最後のコミットの状態） | 指摘 | うち対応必要 |
| --- | --- | --- | --- | --- | --- |
| CodeRabbit（Essentials） | 72 | 17 | 上限 56、`Review in progress` のまま 2（#1・#106）、Draft 2 | 21 | 13 |
| Cursor Bugbot | 71（#97 だけ記録なし） | 71 | なし | 2（#1） | 2 |
| Devin Review | 63 | 1（#1、トライアル中） | trial expired 62 | 3 | 2（ほかの1件は一部対応で、#2 → #11 になった） |
| Copilot | 27（9/23・24 のみ） | 0 | 枠切れ 27 | 0 | 0 |
| Qodo | 0 | 0 | — | 0 | 0 |

- **CodeRabbit は、PRが多いと大半をレビューしない。** Essentials の枠は、直近7日のレビュー件数で決まる。この3日間は、PRコメントの表示（`Plan: Essentials`、`Included review availability`）で「1時間に1件」まで下がり、72本のうち55本は一度もレビューされなかった。K01 の5・6コマ目（#16・#17）と A03 の教科書（#24）も、その中に入る。
- **ただし、本物の指摘の大半は CodeRabbit が出した。** 対応必要13件は、どれも Bugbot が指摘なしとしたPR（#4・#7・#15・#26・#115・#196）で出た。中身は、教科書の説明の誤り、教員用ガイドの食い違い、スクリプトの不具合などである。対応不要5件のうち4件は、差分ではなく「Docstring Coverage」「Linked Issues」の自動チェックだった。
- **Bugbot は全PRで動いたが、指摘は PR #1 の2件だけ**（進捗の保存キーの衝突、実行されないテスト）。スクリプトを直したPR（#111〜#113・#196）を含め、ほかの70本では指摘が出なかった。
- **Bugbot の課金は、いまは月額固定の席課金である。** Cursor の画面では、使用量課金に切り替えると1回約 $1.20 と見積もられている（2026-09-26）。切り替えるかどうかはオーナーが決める。
- **Copilot は、最初のPR（#1、9/23 11:00 UTC）の時点で、月の枠を使い切っていた。** 10月に枠が戻って動いたら、実測を足す。
- **Codex の最初の実測は #202。** Draft のあいだ（約3分）は、レビューもコメントも投稿しなかった。Draft を外してから9分以内に、PR本文に 👍 のリアクションが1つ付き、レビューとコメントの投稿はなかった。修正を push しても見直さず、👍 も付いたままだった（push の4分後）。`@codex review` とコメントすると、2分後に `chatgpt-codex-connector[bot]` が「Codex Review: Didn't find any major issues.」とコメントした。このコメントには、レビューが始まるのは「PRを開いたとき・Draftを外したとき・`@codex review` とコメントしたとき」、指摘がなければ 👍 を付ける、と書かれている。上限に達したときの表示は、まだ出ていないので未観測。
- **Codex を手動で呼ぶときは、PRの会話のコメントに `@codex review` とだけ書く。** インラインのスレッドの返信に `@codex` と書くと、コードとして囲んでいても Codex が反応し、「To use Codex here, create a Codex account and connect to github」と返した（#202）。Codex を呼ぶとき以外は、コメントに `@codex` と書かない。
- **#202 では、Bugbot は Draft を外してから約4分半で完了し（指摘なし）、PR本文に要約（`<!-- CURSOR_SUMMARY -->`）を足さなかった。** 72本では、記録のあった71本すべてで足していた。本文を直すときは、要約があるかどうかを決めつけずに読む。
- **#202 では、CodeRabbit は Draft を外してから約10分でレビューを投稿した（指摘2件）。** レビュー本文には「この回で枠を使い切った。いまの枠は1時間に1件」と出た。修正の push のあとの2回目のレビューは、枠を超えた分として従量課金で行われ、コメントに「Usage-based review receipt」（Mode: Continue automatically、1ファイル $0.25 のところ免除されて $0.00）が付いた。このため、上限に達しても「Review paused」で止まらずにレビューが続く。無料の期間が終わると課金されるので、この設定を変えるかどうかはオーナーが決める。

## 9. 新しい単元を追加するとき

**先に、どちらの作業かを決める。**

- **Kotlinの回（`exNN`）を足すだけなら、単元は増やさない。** 次の「Kotlinの回を足すときは、単元を増やさない」の5つだけをやる。
- **単元そのものを足すのは、Android系（`A01`〜）だけ。** そのときは、下の「単元そのものを足す手順（Android系）」の1〜9をすべて行う。

### Kotlinの回を足すときは、単元を増やさない

**純Kotlin系の単元は `K01` の1つだけで、プロジェクトも `K01HelloKotlin` の1つだけ。** 前年度資料の節を1つ進めて `exNN` を足すのは「回」を足す作業で、「単元」を足す作業ではない。教科書も `docs/hello-kotlin/index.html` の1冊のままで、同じ教科書にSTEPを足していく。やることは次の5つだけで、下の1〜9の手順は要らない。

1. `K01HelloKotlin/src/exNN/main.kt` を足す。**ファイルの先頭に `package exNN` を書く**（§11の8。`exNN` の番号は前年度資料の節に対応させる。対応表はREADMEの「前年度の教材との関係」）。
2. `config/teaching-materials.json` のK01の `packages`（配列）と `sources` に、その `exNN` を足す。**`packages` に書いたのに `sources` が無いと検査が落ちる。** `sessions`（K01に割くコマ数）は、回を足しても増やさない。
3. `docs/hello-kotlin/index.html` にSTEPを足す。**サイドバーの `.progress` の `max` と `data-progress-label` の総数を、増えたSTEP数に直す。** 教科書に貼ったコードは、configの `snippets` に `<pre id="…">` とソースの組を足して照合させる（手で写さず、ソースから差し込む）。
4. `teacher/hello-kotlin/index.html` の進め方にその回を足し、`teacher/hello-kotlin/code/NN-main.kt` に完成コードの複製を置く。configの `mirrors` にも `source` と `copy` の組を足す（1バイトでも違うと検査が落ちるので、元ファイルからコピーする）。
5. 配布ZIPを作り直す。

   ```sh
   python3 scripts/package-project.py --project K01HelloKotlin --output docs/hello-kotlin/downloads/K01HelloKotlin.zip
   ```

   並行するPRとの衝突のしかたは§4にある。

**`projects` に新しい単元を足さない。** 単元が増えないので、READMEの15コマ計画の行も増えず、サイドバー（§4）もtopbarも変わらない。`docs/` に新しいスラッグのフォルダも作らない。GitHubのラベルは `area:K01` をそのまま使う。

### 単元そのものを足す手順（Android系）

**この手順を使うのは、Android系（`A01`〜）の単元を新しく作るときだけ。** `docs/<スラッグ>/` を作るだけでは足りない。次のすべてに登録する。手順は `skills/add-teaching-unit/SKILL.md` にもある。

1. 完成プロジェクト `A0NXxx/`（Android Studioで新規作成し、ひな形 `Panda2KotlinEmptyViewsActivity` と同じ構成にそろえる）。
2. `docs/<スラッグ>/index.html`、`images/`（画像を使う単元だけ）、`downloads/<Project>.zip`。ZIPは次で作る。

   ```sh
   python3 scripts/package-project.py --project A0NXxx --output docs/<スラッグ>/downloads/A0NXxx.zip
   ```

   `--project` と `--output` はどちらも必須で、既定値はない。純Kotlin系のZIPは `docs/hello-kotlin/downloads/K01HelloKotlin.zip` の1つだけで、回を足したときに作り直す（上の「Kotlinの回を足すときは、単元を増やさない」の5）。
   - **`images/` を作るのは、その教科書で実際に使うスクリーンショットがあるときだけ**（`skills/add-teaching-unit/SKILL.md` と同じ条件）。Android系は画面をエミュレータ `jec_25cm_kotlin_Pixel 9a` で撮る。純Kotlin系（`K01`）に画面はないので、撮るのは IntelliJ IDEA の操作（メニュー・ダイアログ・Runツールウィンドウ）だけで、文法の説明は文章と表と手順で書く（`docs/hello-kotlin/images/`）。**「ここに画像を入れる」のようなプレースホルダは置かない。**
3. `teacher/<スラッグ>/index.html` と `teacher/<スラッグ>/code/`（STEPごとの照合コード。`NN-ファイル名.拡張子` の形式）。「この単元の教材方針」の節を必ず置き、何を意図的に外したかを理由つきで書く。
   - **教科書（手順2）と教員用ガイドの本文には、単元名（`projects[].name`）の表記を必ず入れる。** `scripts/check-teaching-materials.py` の `check_project` が、`docs` に挙げたHTMLを1つずつ開いて探す。**Android系（`kind` が `"android"`）の単元は、単元名に加えて `package` の値（`jp.ac.jec.…`）も本文に書く。両方を探すので、どちらか一方でも欠けている教科書・教員用ガイドがあると落ちる。** 純Kotlin系（`kind` が `"kotlin-console"`）は単元名だけでよい（`packages` の `ex01` のような短い語は本文に偶然現れるため、検査の対象にしていない）。
4. `config/teaching-materials.json`：`scan_roots`、指定AVD名の `required_in`（Android単元だけ。教科書と教員用ガイドの両方）、`projects`。
   - `projects` は単元番号順の位置に足す（サイドバーの検査がこの並びを基準にする。§4）。**K→Aの順を崩さない。** 先頭は `K01HelloKotlin` で固定なので、Android単元はそのうしろへ番号順に足す。
   - `kind` は `"kotlin-console"` か `"android"` のどちらか。ほかの値はエラーになる。**新しく足すのは `"android"` だけ**（`"kotlin-console"` の単元は `K01HelloKotlin` の1つだけ）。
   - **`kind` によって、扱うパッケージの書き方が違う。**
     - `"kotlin-console"`：**`packages`（配列）** に、その単元で扱う演習を並べる。1つだけでも `["ex01"]` と配列で書く。`package`（単数）は書かない。**K01は回を重ねるごとにここが伸びていく**（`["ex01"]` → `["ex01", "ex02"]` → …）。
     - `"android"`：いままでどおり **`package`（文字列）** にKotlinパッケージ名（`jp.ac.jec.…`）を書く。`packages` は書かない。
     - 書き間違えると `scripts/check-teaching-materials.py` が設定エラーとして落とす。`packages` に書いた演習の完成コードが `sources` に1つもないときも落ちる（書いたのに足し忘れる事故を捕まえるため）。
   - `sessions` は、その単元に割くコマ数。**`projects` の `sessions` の合計が `course.total_sessions`（15）を超えるとエラー。** 未満は、まだ単元化していないだけなので通る。K01の `sessions` はKotlinの回を足しても変えない（単元が増えないため）。
   - `snippets` は `<pre id="…">` とソースをバイト単位で照合するので、コードは手で写さずソースから生成する。
5. `README.md`：教科書リンク、完成プロジェクトのリンク、教員用リンク、15コマ計画表、フォルダ表。
6. 単元どうしのリンク（§4）。サイドバーは、**既存の全単元の教科書**に新しい単元へのリンクを単元番号順の位置へ足し、新しい単元の教科書には全単元を並べる（自単元は `<span aria-current="page">`）。1冊でも直し忘れると、`scripts/check-teaching-materials.py` が落ちる。topbarは、新しい単元に直前の単元へのリンクを置く。単元を途中に挿入したときは、次の単元のtopbarも新しい単元へ付け替える。topbarは検査されないので、目で確かめる。既存の教科書のサイドバーは、issueの「触る範囲」に挙がっていなくても、登録に必要な変更なので同じPRで直す（§6）。
7. GitHubのラベル `area:A<NN>`（Kotlinの回のissueは、単元が増えないので `area:K01` をそのまま使う）。
8. 翻訳の対象は `docs/` のHTMLから自動で見つかる。新単元のPRでは日本語だけを追加し、`python3 scripts/localize-student-materials.py check` で文を取り出せることを確かめる（§7）。翻訳そのものは日常のPRでは行わない（§12）。
9. **Android系の単元を足したときは、`docs/common/apk.html` の「アプリを1つ選ぶ」の説明が古くなっていないかを確かめる。** 提出課題は、学生自身が作ったAndroidアプリを1つ選んでアレンジし、APKにして出す形（READMEの「提出課題」）。Android単元が増えると、学生が選べるアプリの本数と顔ぶれが変わるので、単元名を挙げている箇所と、本数に触れている箇所が古くなる。古くなっていたら、この登録のPRで一緒に直す（`docs/common/` は共有ファイル。§4）。Kotlinの回（`exNN`）を足したときは、`K01` がコンソールアプリで提出の対象外なので、直す必要はない。READMEの「提出課題」の本数の根拠（Android系に使えるコマ数とアプリの本数）も、同じときに読み直す。

### 配布スクリプトへの追記は不要

**`scripts/package-student-materials.py` と `scripts/release-student-materials.py` には、単元を足しても何も書かない。** どちらも単元の一覧を `config/teaching-materials.json` の `projects` から読む。完成プロジェクトZIPの再生成も、`はじめに.txt` の単元一覧も、リリースノートの単元一覧も、Android系なら上の手順4、Kotlinの回なら `packages`・`sources` を足すだけで自動的に付いてくる。

参照にした Androidプログラミング1 のリポジトリでは、この3か所が配布スクリプトに直書きしてあり、単元を足すたびに `config` と2つのスクリプトの計3か所を同じ順序で直す必要があった。**単元一覧が3か所に散っていること自体が、直し忘れの原因になっていた。** このリポジトリでは、単元の一覧が正しいかどうかを `config/teaching-materials.json` の1か所だけで判断できるようにしてある。**スクリプトに単元名や単元番号を直書きしない**（配布ZIPの名前や見出しのような、単元に依存しない固定値は直書きでよい）。

## 10. 対象外

次の項目は、レビューで指摘しない。botに指摘されたら「対応不要」と返信する。検証もしない。

- 完成プロジェクトのUnit Test（§7、§11の5）。テストしやすくするためのリファクタリングもしない。
- Windows。教員も学生もmacOSで、CIはubuntu（READMEの「開発環境：教員」「開発環境：学生」）。
- ダークテーマ。確認は既定のライトテーマだけで行う。直書きの色もそのままにする。
- タブレット・フォルダブル対応、画面回転と横画面。
- **提出課題のAPKの署名（リリースビルド）。** 学生が提出するのは**デバッグビルドのAPK**で、署名鍵の作成・リリースビルド・ストアへの公開は授業の範囲外とする（READMEの「提出課題」、学生向けの手順は `docs/common/apk.html`）。「このAPKはストアに出せない」「署名されていない」「鍵の作り方も書くべき」という指摘は、仕様どおりなので「対応不要」と返信する。教材にも、署名の手順は書かない。

## 11. 完成コードの書き方（Kotlin）

READMEの「完成コードの書き方（全単元共通）」を、このリポジトリの実物のコードで具体化したもの。教材のコードを書くとき・レビューするときは、ここを基準にする。

1. **Viewの取得は `findViewById` を使う。ViewBindingもComposeも使わない。** `onCreate` の冒頭にまとめる。型は `findViewById<T>()` の型引数か、変数の宣言側で見せる。

   ```kotlin
   // A03GithubSearch/app/src/main/java/jp/ac/jec/a03githubsearch/MainActivity.kt
   editQuery = findViewById(R.id.edit_query)   // 宣言は private lateinit var editQuery: TextInputEditText
   val recyclerView: RecyclerView = findViewById(R.id.recycler_view)
   ```

   ```kotlin
   // A04FunnyCamera/app/src/main/java/jp/ac/jec/a04funnycamera/MainActivity.kt
   findViewById<Button>(R.id.btn_take_picture).setOnClickListener { takeScreenshot() }
   ```

   命名は `txtXxx` / `edtXxx` / `btnXxx` / `imgXxx` / `recyclerView` など、部品の種類が名前から分かる形にする。**リスナを付けるためだけに使うViewは、変数に入れずその場でつないでよい**（2つ目の例）。ViewBindingを使わない理由は、Androidが初めての受講生が「XMLに書いたidとKotlinの変数がどうつながっているか」を1行で追えるようにするため。自動生成のクラスが間に入ると、その対応が見えなくなる。受講生はJavaとSwiftを書けるが、Androidの画面のしくみは初めてなので、ここだけは遠回りをしない。

2. **`@SuppressLint` で警告を隠さない。警告の原因そのものを消す。** このリポジトリに `@SuppressLint` は1つもない。

   `A04FunnyCamera` は、画像を指でドラッグさせるために `setOnTouchListener` を使うと `ClickableViewAccessibility` の警告が出る。これを抑制する代わりに、`AppCompatImageView` を継承したViewを作り、`onTouchEvent()` と `performClick()` をオーバーライドしてある。

   ```kotlin
   // A04FunnyCamera/app/src/main/java/jp/ac/jec/a04funnycamera/DraggableImageView.kt
   class DraggableImageView(context: Context, attrs: AttributeSet?) :
       AppCompatImageView(context, attrs) {

       override fun onTouchEvent(event: MotionEvent): Boolean {
           when (event.actionMasked) {
               // …（省略）…
               MotionEvent.ACTION_UP -> performClick() // （アクセシビリティ対応）
           }
           return true
       }

       /**
        * onTouchEventをオーバーライドしたViewは、performClickもオーバーライドする必要がある
        * (オーバーライドしないとLintがアクセシビリティの警告 ClickableViewAccessibility を出す)
        */
       override fun performClick(): Boolean {
           return super.performClick()
       }
   }
   ```

   レイアウトからは `<jp.ac.jec.a04funnycamera.DraggableImageView android:id="@+id/iv_character" …>` として使う。`@SuppressLint` を1つ許すと、学生は「警告は消せばよい」と覚える。**警告は、まだ書けていないコードの在りかを示している**ので、そこを書くのが教材になる。

3. **ユーザーに伝えることは `Snackbar`（または `Toast`）で画面に出す。`Log.d` で済ませない。**

   ```kotlin
   // A04FunnyCamera：保存の結果を画面に出す
   val message = if (isSaved) "保存しました" else "保存に失敗しました"
   Snackbar.make(findViewById(R.id.main), message, Snackbar.LENGTH_SHORT).show()
   ```

   ```kotlin
   // A03GithubSearch：同じ役目を Toast でまとめてある
   private fun showMessage(message: String) {
       Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
   }
   ```

   学生は、アプリを動かしているときLogcatを見ていない。`Log.d` だけだと「押しても何も起きない」アプリになり、自分の書いたコードが動いたかどうかを確かめられない。Logcatは、`A04FunnyCamera` のカメラ権限の可否や保存先URIのように、**学生が中身を確かめるための補助として扱う単元でだけ**使う。

4. **1単元で導入する新概念は1つまで。** 画面（Android系）またはコンソールの出力（純Kotlin系）で、効果が目に見える形にする。見えない変更は、学生には「何も起きなかった」と同じ。

5. **完成プロジェクトにUnit Testは書かない。** テストしやすくするためのリファクタリングもしない（§10）。`scripts/test_*.py` はCIで動くので、通る状態を保つ（§7）。

6. **完成プロジェクトの `README.md` は `A03GithubSearch/README.md` の形にそろえる。** 節の順は、画面の構成の表 → 使用しているAPI（または画像・素材）→ ソースコードの構成の表 → 処理の流れ → 実装のポイント → 主なライブラリ → ビルドと実行。`A04FunnyCamera/README.md` も同じ形になっている。

7. **ライブラリは必要なときだけ足す。** バージョンは各プロジェクトの `gradle/libs.versions.toml` で管理し、`build.gradle.kts` にバージョンを直書きしない。単元で使わないライブラリは足さない。

8. **純Kotlin系の完成コードは `K01HelloKotlin/src/exNN/` に置き、ファイル先頭に `package exNN` を書く。** `fun main()` を持たせて、IntelliJ IDEA の実行ボタンで動かせる形にする。回を重ねるごとに `exNN` が増えていき、**プロジェクトは `K01HelloKotlin` の1つのまま**である（新しいプロジェクトを作らない）。

   ```kotlin
   // K01HelloKotlin/src/ex01/main.kt
   package ex01

   fun main() {
       val number1 = 1
       val number2 = 2.0 // Double
       // …
   }
   ```

   **`exNN` の番号は、前年度（2025年度）の配布資料PDFの節に対応させる。** 対応表はREADMEの「前年度の教材との関係」にある（`ex01` は「4 変数宣言、代入処理」、`ex07` は「10 拡張メソッド」…）。新しい番号を勝手に振らない。教科書のどのSTEPがどの節の焼き直しかが分からなくなり、比較の書き方も引き継げなくなる。

   `check-teaching-materials.py` は、`sources` の各 `.kt` に `package <値>` 宣言があることと、そのファイルが `root/src/<値>/` の下にあることを見る。`<値>` は、`kotlin-console` の単元なら `packages`（配列）のいずれか、`android` の単元なら `package`（文字列）。ディレクトリ名とパッケージ名は必ずそろえる。

9. **コメントは、学生が読んで意味が分かる日本語で書く。英語のコメントにしない。** 「何をしているか」ではなく「なぜそう書いたか」を書く。上の `DraggableImageView` の `performClick` のKDocが、この形になっている。

10. **オーナーの書き方を保つ。** レビューで「初学者向けにかみ砕くべき」「もっとやさしく書き直すべき」と指摘されても、**既定の対応は「教科書で説明する」**。採用するのは、動作を変えない小さな明確化だけにする。コードを平易にするより、教科書のSTEPを1つ増やすほうを選ぶ。受講生はJavaとSwiftを書けるので、コードを薄めるより、Java／Swiftとの比較を1つ足すほうが早く伝わる。

## 12. 多言語展開（対訳カタログ）

日本語の教科書（`docs/`）を、配布前にほかの言語へ展開する。しくみの説明は `README.md` の「多言語展開」、翻訳の手順とルールは `skills/translate-teaching-materials/SKILL.md` にある。対象は日本語（原文）＋英語・中国語（簡体）・韓国語・ミャンマー語・広東語（繁体・香港）・台湾華語（繁体・台湾）・スペイン語・アラビア語・モンゴル語（キリル文字）の9言語。

- **2026-09の学生アンケート（母国語の確認）で対象を広げた（2026-09-24 オーナー決定）。** 台湾華語・スペイン語・アラビア語・モンゴル語を加えた（アラビア語は、右から左の表示に対応した #78 で、モンゴル語は、読む文字を学生本人に確かめてから #92 で加えた）。スペイン語は中南米の言い方にそろえ、言語コードは `es` にする。回答のなかった言語も、未回答の学生がいるので外さない。**アンケートの回答ファイルは学生のメールアドレスを含むので、リポジトリにもissue・PRにも写さない。** 書いてよいのは、挙がった言語の一覧までにする。
- **モンゴル語は、モンゴル国のキリル文字（`mn`、横書き）で加えた（2026-09-25 オーナー確認）。** 学生本人に読む文字を確かめた結果である（ハイブリッドアプリ開発技法の [jec-25cm-hybrid-app #40](https://github.com/LeoAndo/jec-25cm-hybrid-app/issues/40) と同じ判断）。伝統的モンゴル文字（縦書き、`mn-Mong`）には対応しない。
- **台湾華語とスペイン語の「両科目に共通の用語」は、ハイブリッドアプリ開発技法（jec-25cm-hybrid-app）の用語集と同じ訳語にしてある。** 同じ学生が同じ学期に両方を受けるためである。`i18n/zh-Hant-TW/glossary.md`・`i18n/es/glossary.md` のその節を変えるときは、あちらの同じ節も同じように直す。アラビア語（`i18n/ar/glossary.md`）とモンゴル語（`i18n/mn/glossary.md`）も同じ扱いにする。
- **アラビア語（`ar`）は右から左に書く（#78）。** `config/i18n.json` の `"dir": "rtl"` で、翻訳ページの `<html>` に `dir="rtl"`、未翻訳の日本語に `dir="ltr"` が付く。左から右の言語のページの本文のHTMLは変わらない（言語の切り替えと入口のリンクには、どの言語にも `dir` が付く）。右から左の文の中での数字・引用符・矢印の書き方は `i18n/ar/glossary.md` の「書き方の決まり」にある。
- **教科書のCSS（`docs/assets/textbook.css`）に、左右を決め打ちした指定を書かない。** `margin-left`・`padding-right`・`border-left`・`text-align: left`・`left:` の代わりに、論理プロパティ（`margin-inline-start`・`padding-inline-end`・`border-inline-start`・`text-align: start`・`inset-inline-start`）を使う。決め打ちすると、右から左のページで囲みの線やリストの字下げが逆の側に出る。右から左のページだけに当てる指定は `[dir="rtl"]` の下に書き、日本語のページの見た目を変えない。特に `unicode-bidi: isolate` は、日本語の文の中の `<code>` の折り返しを変えるので、日本語のページに当てない（#78 で、13ページ×3つの幅の全要素の位置を前後で比べて見つけた）。
- **初版は、日本語・英語・中国語（簡体）の3言語で配布する（2026-09-25 オーナー決定）。** 2026-09-28の授業開始に間に合わせるためである。ほかの7言語（広東語・台湾華語・韓国語・ミャンマー語・スペイン語・アラビア語・モンゴル語）は、後期の授業が始まってから、1言語ずつ段階的に訳し、照合して配布対象に加える（#116 の子issue）。全言語がそろうまで、初版の公開を待たない。
- **いまは `config/i18n.json` で `distribute: true` なのは英語と中国語（簡体）**（英語は2026-09-25、#56。中国語（簡体）は2026-09-25、#126。どちらも全ページの翻訳と、別のモデルによる照合が済んだ）。ほかの7言語は `false`。翻訳が途中の言語を `true` にすると、公開ゲート（`localize-student-materials.py status --require-complete`）で止まる。**英語と中国語（簡体）が配布対象なので、日本語を直した文は、次の公開の前に両方とも訳し直す**（直した文は未翻訳に戻り、公開ゲートが止める）。訳し直すのは、下の「配布準備のissueと翻訳PR」の手順で行い、日常のPRでは訳さない。
- **`true` に上げてよいのは、次の2つが両方終わった言語だけ。**
  1. その言語の未翻訳が0件になっている（`python3 scripts/localize-student-materials.py status`）。
  2. 翻訳したのとは別のAIが、その言語の全文を原文と1回照合し終えている（前に照合したページも含める）。**照合は、翻訳と同じセッション・同じPRの中のsubagentが行ってもよい**（オーナーの判断、2026-09-24）。照合の担当は、訳した担当とは別のモデルにする。自分で訳して自分で照合しない。
- **`true` に上げるのは、1PRにつき1言語。** `distribute` を上げるPRは共有ファイル（`config/`）を触るので `area:shared` になる（§4）。
- **照合は、学生の手に渡る前に1回だけ行う（2026-09-25 オーナー決定、#100）。** 訳すたびには照合しない。基準は、きれいな訳文ではなく、学生が操作を間違えないことに置く（翻訳ページには日本語版が正という注記と、日本語版へのリンクがある。コード・キー・正式表記は `check` が検査する）。
  - `distribute: false` の言語の翻訳PRでは、照合しない。`check` と確認用ページの目視までにする。
  - `distribute` を `true` に上げるときに、その言語の全文を1回照合する（上の2）。
  - `distribute: true` の言語の差分翻訳は、訳した文が50文以上のときだけ照合する（下の手順4）。
  - 照合し直すのは、照合のあとで意味が変わる修正をした文だけ。記号・大文字と小文字・言い回しのそろえでは照合し直さない。
  - 原文を見ずに日本語へ訳し戻して比べるのは、ミャンマー語だけ。ほかの言語は対訳を並べて読む。
  - 照合の記録は、PR本文と、指摘の全件を残すPRのコメントだけにする。用語集には「照合の記録」を書き足さない（2026-09-25より前の記録は、過去の判断の理由として残す）。
- **日常のPRでは翻訳しない。** `docs/` の日本語を直しても、`i18n/` は触らない。直した文は自動で未翻訳に戻り、CIは未翻訳の数を表示するだけで落ちない。翻訳は、配布前の翻訳PRでまとめて行う。配布していない言語（`distribute: false`）の文は、配布前の翻訳PRでも訳さず、日本語で表示されるままにする。その言語の翻訳PRか、その言語を配布対象に上げるときに訳す。
- **教科書のHTMLには、次の形を書かない。** どれも `python3 scripts/localize-student-materials.py check` が行番号つきで落とす（§7の `unittest` にも含まれる）。黙って壊れるより、書いた人がその場で気付けるようにしてある。
  - 開始タグと終了タグの不一致（`<p>`・`<li>`・`<td>` の閉じ忘れ）と、`<span/>` のような自己終了タグ。文を取り出せない。
  - 引用符で囲んでいない属性（`<html lang=ja>`、`href=images/x.png`）。値の終わりが決まらず、書き換えた結果が壊れる。
  - 文の途中のHTMLコメント（`<p>あいう<!-- メモ -->えお</p>`）。訳文で置き換えるとコメントが消え、前後の文字が連結される。段落の外に書く。
  - `/` で始まるルート相対のリンク（`href="/docs/assets/textbook.css"`）。GitHub Pagesがリポジトリ名の下にあるので日本語版でも使えない。
  - 文の途中の要素に付けた `translate="no"`（`<span translate="no">`）。その文が断片に割れて訳せなくなる。
- **訳してほしくない文字は、`<code>` で囲む。** `<code>`・`<kbd>`・`<pre>` の中身は、どの言語でも日本語版のまま出る。Java／Swiftとの比較ブロックのコードも `<pre>` の中なので、どの言語版でもそのまま出る。言語名のラベルだけは文になるので、`<p class="compare-lang" translate="no">Java</p>` のように**ブロック要素に** `translate="no"` を付けて外す（文の途中の要素には付けない。下の禁止事項）。Kotlinのキーワード（`val` `var` `fun main`）、IDEのメニュー名、指定AVD名、パッケージ名はここに入れる。段落や表のセルを丸ごと訳の対象から外したいときは、その要素（`<p>`・`<td>`・`<div>` など、文の区切りになる要素）に `translate="no"` を付ける。
- **各言語のHTMLはコミットしない。** コミットするのは `i18n/<言語>/` の対訳カタログと `glossary.md`（用語集）だけ。確認用のページは `dist/i18n-preview/` に作る（`dist/` はGit管理の対象外）。
- **カタログの `source` は手で書き換えない。** 訳を直すときは `translation` だけを直す。並べ替えと、使わなくなった訳の削除は、`sync` と `merge` が行う。
- 翻訳のPRには `area:i18n` を付ける。学生用ZIPに入るまでは `skip-release-notes` も付ける。

### 配布準備のissueと翻訳PR

1. 配布準備のissueを起票し、対象の版・言語・未翻訳の件数を書く。§6の書式とサイズ見積を使い、`area:i18n` と `size:*` を付ける。翻訳PRにも同じラベルと `enhancement` を付ける。まだ配布対象でない言語だけのPRには `skip-release-notes` も付ける。
2. 最新のmainで `python3 scripts/localize-student-materials.py status` を実行する。翻訳用skillに従い、未翻訳の文だけを訳す。Actionsで翻訳APIを呼ぶ処理やSecretは追加しない。
3. **配布準備の翻訳PR（`distribute: true` の言語の差分翻訳）を開いてから学生向けの公開が終わるまでは、`docs/` を触るPRをマージしない。** 翻訳PRの本文に、この期間と対象の版を書く。日本語の変更が入った場合は最新のmainを取り込み、差分だけを訳し直す。止める理由は、公開ゲート（`status --require-complete`）が配布対象の言語の未翻訳0件を求めるので、訳しているあいだに日本語が変わると、公開の直前に未翻訳が出るためである。
   - **配布していない言語（`distribute: false`）の翻訳PRでは、`docs/` を触るPRのマージを止めない**（#104）。学生向けの公開がないので、止める理由がない。日本語が先に変わったら、翻訳PRの側が最新のmainを取り込む。変わった文は、そのPRで訳しても、日本語のまま残してもよい（#100 の決まり）。
4. **訳した文が50文以上なら**、翻訳したのとは別のAIが、新しく訳した文を原文と照合する。50文未満なら照合せず、翻訳の担当が訳を見直して、その旨と文の数をPR本文に書く。照合では、ミャンマー語だけ原文を見ずに訳文を日本語へ訳し戻してから比べ、ほかの言語は対訳を並べて読む（翻訳用skillの「別のモデルによる照合」）。意味の違い・訳し落とし・足しすぎ・操作順・用語集との不一致を確かめる。**照合の担当には資料を自分で読ませ、指摘は全件を要約せずにPRのコメントに残し（ミャンマー語の綴りは写さない）、照合のあとで意味が変わる修正をした文だけ照合し直す**（くわしくは翻訳用skillの同じ節）。PR本文には担当と照合範囲、指摘への対応を残す。全体を訳し直す必要はない。
5. §7の4つの検証に加え、`python3 scripts/localize-student-materials.py status --require-complete` を通す。ZIPの入口 `index.html` から配布対象の言語を開き、リンク・コードのコピー・共通資料からの戻り先を確認する。

## Code Review Rules

Codex の自動レビューは、この節で指摘するかどうかを決める。Codex は見出しがちょうど「Code Review Rules」の節を読むので、見出しの文字列を変えない（[OpenAI の説明](https://developers.openai.com/blog/custom-code-review-rules-for-codex)）。コメントは日本語で書く。前提は「受講生像と、教材の書き方」・§10・§11 にある。

次のものは P1 として指摘する（学生の手に渡る前に直すもの）。

- 教科書・教員用ガイドの説明が、完成コードや、コンパイル・実行の結果と食い違っている
- STEP番号・ファイル名・メニュー名・`id`・パッケージ名が、教科書・教員用ガイド・完成コードのあいだで食い違っている
- 手順どおりに進めると学生が止まる、または別の結果になる（手順の抜け、順番の入れ替わり、まだ扱っていない内容を前提にした説明）
- 教科書のSTEPに Java／Swift との比較がない。確認欄や「最後の3分」に振り返りの言い方がある。エラーや警告の文言を引用している
- `scripts/` の不具合で、配布ZIPや翻訳ページが壊れる、または検査が素通りする
- 翻訳カタログで、操作を誤らせる訳（用語集 `i18n/<言語>/glossary.md` と違う訳語を含む）。言い回しの好みは指摘しない

次のものは指摘しない。

- §10 の対象外（完成プロジェクトのUnit Test、Windows、ダークテーマ、タブレット・横画面、提出APKの署名）
- §11 の書き方（`findViewById` を使い、ViewBinding や Compose を使わない など）を変える提案と、「初学者向けにかみ砕くべき」という提案
