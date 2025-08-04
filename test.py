import asyncio

# 作成した各モジュールと設定をインポート
from config import MAX_PROMPT_LENGTH
from web_crawler import get_content_from_url
from ollama_client import extract_summary_info


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
    summary_info = extract_summary_info(prompt)

    print(summary_info)


async def main():
    """
    アプリケーションのメイン処理。
    """
    try:
        await process_link(input("URLを入力してください: ").strip())
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"実行中に致命的なエラーが発生しました: {e}")
