import feedparser
import json
import time
import calendar  # time.struct_timeをUTCタイムスタンプに変換するために使用
from typing import List

# 設定ファイルからタイムスタンプファイルのパスをインポート
from config import TIMESTAMP_FILE, MAX_LOAD_ITEM


def _is_new_item(item, last_item_timestamp: time.struct_time) -> bool:
    """記事が最後に記録されたアイテムの時刻より新しいかを判定する"""
    # itemに 'published_parsed' が存在し、Noneでないことを確認
    if item.get('published_parsed'):
        return item['published_parsed'] > last_item_timestamp
    return False


def _read_last_item_timestamp(filepath: str) -> time.struct_time:
    """最後に取得したアイテムの時刻をファイルから読み込む"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            # time.gmtime()はfloatを引数にとる
            return time.gmtime(data.get("last_item_timestamp", 0))
    except (FileNotFoundError, json.JSONDecodeError):
        # ファイルが存在しない、または中身が不正な場合はUNIXエポックを返す
        return time.gmtime(0)


def _write_last_item_timestamp(timestamp_struct: time.struct_time, filepath: str):
    """指定されたアイテムの公開時刻（time.struct_time）をファイルに書き込む"""
    # time.struct_timeをUTC基準のfloat型タイムスタンプに変換
    timestamp_float = calendar.timegm(timestamp_struct)
    data_to_write = {"last_item_timestamp": timestamp_float}
    try:
        with open(filepath, 'w') as f:
            json.dump(data_to_write, f, indent=4)
    except IOError as e:
        print(f"⚠️ 警告: タイムスタンプファイル '{filepath}' の書き込みに失敗しました: {e}")


def fetch_new_links(rss_url: str) -> List[str]:
    """
    RSSフィードから新しい記事のリンクを取得する。
    新しい記事が見つかった場合、その中で最も新しい記事の公開時刻を記録する。
    """
    # 1. 最後に記録したアイテムの時刻をファイルから読み込む
    last_item_timestamp = _read_last_item_timestamp(TIMESTAMP_FILE)

    feed = feedparser.parse(rss_url)
    if feed.bozo:
        print(f"⚠️ 警告: RSSフィード '{rss_url}' の解析に問題がある可能性があります。")
        # print(f"詳細: {feed.bozo_exception}")

    # 2. 最後に記録した時刻よりも新しい全アイテムを取得
    new_entries = [
        entry for entry in feed.entries
        if entry.get('link') and _is_new_item(entry, last_item_timestamp)
    ]

    # 3. 新しい記事が見つかった場合のみ処理を実行
    if new_entries:
        print(f"✅ {len(new_entries)}件の新しい記事が見つかりました。")
        print("最大取得数制限: ", MAX_LOAD_ITEM)

        new_entries_trimmed = new_entries[-MAX_LOAD_ITEM:]  # 最大取得数を制限

        # 4. 最大取得数を制限した中で新しい記事の中で最も新しいものを取得
        latest_entry = max(
            new_entries_trimmed,
            key=lambda item: item['published_parsed']
        )

        # 5. 最大取得数を制限した中で最も新しい記事の公開時刻をファイルに書き込む
        _write_last_item_timestamp(
            latest_entry['published_parsed'],
            TIMESTAMP_FILE
        )

        # 新しい記事のリンクを返す（公開時刻の降順でソート）
        new_links = [
            e.link for e in sorted(new_entries_trimmed, key=lambda item: item['published_parsed'], reverse=True)
        ]
    else:
        print("ℹ️ 新しい記事はありませんでした。")
        new_links = []

    return new_links
