# template-rss-reader-llm

このプロジェクトは、RSSフィードの情報をLLM（大規模言語モデル）を使って要約し、
Discordに通知するためのテンプレートです。

## 前提条件

リポジトリがパブリックであること。
※デフォルトの大規模モデルの gpt-oss:20b はRAMが16GB以上必要です。

プライベートリポジトリの場合は8GBに減ってしまうため GitHub Actions をセルフホストするか、大規模言語モデルを他のものに変更する必要があります。

## 使い方

このテンプレートをリポジトリで利用するには、以下の3つのステップを設定してください。

### 1. Modelfileをカスタマイズ

まず、LLMの動作を定義するModelfileを自分の好みに合わせてカスタマイズします。

- **`FROM`**: ベースとなるモデルを指定します。（例：`llama3`, `gemma`など）
- **`SYSTEM`**: モデルに与える指示（プロンプト）を記述します。どのような要約をしてほしいかなどを具体的に書きましょう。

-----

### 2. Repository secrets の設定

次に、リポジトリに2つの重要な情報を「Secret」として登録します。
リポジトリの Settings > Secrets and variables > Actions に移動し、以下の2つのRepository secretsを登録してください。
これにより、URLなどの機密情報を安全に管理できます。

- **`DISCORD_WEBHOOK_URL`**: 通知を送りたいDiscordチャンネルのWebhook URLを設定します。
  - サーバーリストから適当なサーバーを選択 > ＋ボタンからチャンネルを追加
  - サーバーを右クリック > サーバー設定 > 連携サービス > ウェブフック > 新しいウェブフック > お名前、チャンネル名を設定し、ウェブフックURLをコピー

- **`RSS_URL`**: 読み込みたいRSSフィードのURLを設定します。
  - WordPress系サイトの場合は、URLの最後に/feedをつけます。　例）<https://サイトURL/feed>

-----

これだけで設定は完了です。GitHub Actions で、2時間毎にRSSフィードをチェックして、要約がDiscordに自動で投稿されるようになります。
なお、チェックする周期の時間は　`.github/workflows/ollama.yml` から変更できます。

## 動作確認

Actions > Ollama Python Push Workflow > Run workflow > Run workflow を実行
