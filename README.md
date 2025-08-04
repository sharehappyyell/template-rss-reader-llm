# template-rss-reader-llm

template

- `.github\workflows-template\ollama.yml` の
    `ollama create template-extractor -f ./Modelfile` の
    template 部分

- `config.py` の

    ```py
    OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "template-extractor")
    ```

    の template 部分

- Modelfile をカスタマイズ

- Repository secrets
  - `DISCORD_WEBHOOK_URL` を設定
  - `RSS_URL` を設定

- `.github/workflows-template` を `.github/workflows` にして、GitHub Actions を有効化
