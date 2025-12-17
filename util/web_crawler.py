from crawl4ai import AsyncWebCrawler
from typing import Optional

# 設定ファイルからクローラー設定をインポート
from config import CRAWLER_CONFIG, BROWSER_CONFIG


async def get_content_from_url(url: str) -> str | None:
    """
    指定されたURLからコンテンツをクロールする。
    """
    try:
        async with AsyncWebCrawler(config=BROWSER_CONFIG) as crawler:
            content = await crawler.arun(url=url, config=CRAWLER_CONFIG)
            if content.markdown:
                return content.markdown.fit_markdown
            else:
                return None

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None
