# template-rss-reader-llm

このプロジェクトは、RSSフィードの情報をLLM（大規模言語モデル）を使って要約し、
Discordに通知するためのテンプレートです。

## 使い方

このテンプレートをリポジトリで利用するには、以下の3つのステップを設定してください。

### 1. Modelfileをカスタマイズ

まず、LLMの動作を定義する`Modelfile`を自分の好みに合わせてカスタマイズします。

- **`FROM`**: ベースとなるモデルを指定します。（例：`llama3`, `gemma`など）
- **`SYSTEM`**: モデルに与える指示（プロンプト）を記述します。どのような要約をしてほしいかなどを具体的に書きましょう。

-----

### 2. Repository secrets の設定

次に、リポジトリに2つの重要な情報を「Secret」として登録します。これにより、URLなどの機密情報を安全に管理できます。

リポジトリの **Settings** \> **Secrets and variables** \> **Actions** に移動し、以下の2つの`Repository secrets`を登録してください。

- **`DISCORD_WEBHOOK_URL`**: 通知を送りたいDiscordチャンネルのWebhook URLを設定します。
- **`RSS_URL`**: 読み込みたいRSSフィードのURLを設定します。

-----

### 3. GitHub Actions の有効化

最後に、このプロジェクトの自動化の仕組みであるGitHub Actionsを有効にします。

1. リポジトリ内にある `.github/workflows-template` という名前のフォルダを `.github/workflows` に変更します。

これだけで設定は完了です。GitHub Actionsが有効になり、定期的にRSSフィードをチェックして、要約がDiscordに自動で投稿されるようになります。
