import os
from crawl4ai import CrawlerRunConfig, BrowserConfig, DefaultMarkdownGenerator, PruningContentFilter

# --- 設定 (環境変数がなければデフォルト値を使用) ---
RSS_URL = os.getenv("RSS_URL", "RSS_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "DISCORD_WEBHOOK_URL")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "extractor")
TIMESTAMP_FILE = os.getenv("TIMESTAMP_FILE", "last_item.json")
MAX_LOAD_ITEM = int(os.getenv("MAX_LOAD_ITEM", 2))
MAX_PROMPT_LENGTH = int(os.getenv("MAX_PROMPT_LENGTH", 8192))
OLLAMA_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", 2700))

# --- クローラー設定 ---
PRUNE_FILTER = PruningContentFilter(
    threshold_type="fixed",
    threshold=0.5
)
MD_GENERATOR = DefaultMarkdownGenerator(content_filter=PRUNE_FILTER)
CRAWLER_CONFIG = CrawlerRunConfig(
    exclude_external_images=True,  # 外部画像を除外
    markdown_generator=MD_GENERATOR
)

# --- ブラウザ設定 ---
BROWSER_CONFIG = BrowserConfig(
)


def discord_payload(answer: dict[str, object], url: str) -> dict[str, object]:
    """Discord送信用ペイロードを作成します。"""
    return {
        "content": f"[情報元URL]({url})",
        "embeds": [
            {
                "title": answer["name"],
                "description": answer["doc"],
                "url": answer["url"],
                "fields": [
                    {"name": "価格", "value": answer["price"], "inline": False},
                    {"name": "商品の販売URL", "value": answer["url"], "inline": False}
                ]
            }
        ]
    }
