import requests


def send_to_discord(payload: dict, webhook_url: str):
    """
    指定されたペイロードをDiscordのWebhook URLに送信する関数。

    Args:
        payload (dict): Discordに送信するデータ（埋め込みメッセージなど）。
        webhook_url (str): 送信先のDiscord Webhook URL。
    """
    # Webhook URLが設定されているかを確認します。
    if not webhook_url:
        print("❌ エラー: 'DISCORD_WEBHOOK_URL' が設定されていません。")
        return

    # Webhook URLにPOSTリクエストを送信します。
    try:
        response = requests.post(webhook_url, json=payload)
        # レスポンスのステータスコードが2xx（成功）以外の場合、HTTPErrorを発生させます。
        response.raise_for_status()
        print("✅ Discordに正常に送信しました。")
    # requestsライブラリ関連のエラー（例: 接続エラー、タイムアウト）を捕捉します。
    except requests.exceptions.RequestException as e:
        print(f"❌ Discordへの送信中にエラーが発生しました: {e}")
