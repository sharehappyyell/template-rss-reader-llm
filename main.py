import asyncio

# 作成した各モジュールと設定をインポート
from config import RSS_URL, MAX_PROMPT_LENGTH, DISCORD_WEBHOOK_URL, discord_payload, OLLAMA_TIMEOUT_SECONDS
from util.rss_handler import fetch_new_links
from util.web_crawler import get_content_from_url
from util.ollama_client import extract_summary_info
from util.discord_notifier import send_to_discord


async def process_link(url: str):
    """
    単一のリンクを処理する非同期関数。
    クロール -> 情報抽出 -> 結果表示 の一連の流れを実行する。
    """
    print(f"\n🔗 処理中のURL: {url}")
    # URLからコンテンツを取得
    content = await get_content_from_url(url)

    if not content:
        return

    # Ollamaに渡すプロンプトを作成（長すぎる場合は切り詰める）
    prompt = content.markdown.fit_markdown[:MAX_PROMPT_LENGTH]

    # Ollamaで情報を抽出
    summary_info = extract_summary_info(prompt, OLLAMA_TIMEOUT_SECONDS)

    if not summary_info:
        return

    # Discordに結果を送信
    print("🔗 Discordに結果を送信中...")
    send_to_discord(discord_payload(
        summary_info,
        content.redirected_url
    ), DISCORD_WEBHOOK_URL)


async def main():
    """
    アプリケーションのメイン処理。
    """
    print("🔍 RSSフィードで新しい記事をチェックしています...")
    links = fetch_new_links(RSS_URL)

    if not links:
        print("✅ 新しい記事は見つかりませんでした。")
        return

    print(f"🆕 {len(links)}件の新しい記事が見つかりました。処理を開始します。")

    for link in links:
        try:
            await process_link(link)
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"実行中に致命的なエラーが発生しました: {e}")
