import os
from dataclasses import dataclass
from crawl4ai import CrawlerRunConfig, BrowserConfig, DefaultMarkdownGenerator, PruningContentFilter

# --- 設定 (環境変数がなければデフォルト値を使用) ---
RSS_URL = os.getenv("RSS_URL", "RSS_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "DISCORD_WEBHOOK_URL")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "extractor")
TIMESTAMP_FILE = os.getenv("TIMESTAMP_FILE", "last_item.json")
MAX_LOAD_ITEM = int(os.getenv("MAX_LOAD_ITEM", 3))
MAX_PROMPT_LENGTH = int(os.getenv("MAX_PROMPT_LENGTH", 4096))
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


# --- データ構造と関数 ---
@dataclass
class SummaryInfo:
    """要約情報を格納するデータクラス。"""
    name: str
    doc: str
    price: str
    url: str


def discord_payload(summary_info: SummaryInfo, url: str) -> dict:
    """Discord送信用ペイロードを作成します。"""
    return {
        "content": f"[情報元URL]({url})",
        "embeds": [
            {
                "title": summary_info.name,
                "description": summary_info.doc,
                "url": summary_info.url,
                "fields": [
                    {"name": "価格", "value": summary_info.price, "inline": False},
                    {"name": "関連するURL", "value": summary_info.url, "inline": False}
                ]
            }
        ]
    }
