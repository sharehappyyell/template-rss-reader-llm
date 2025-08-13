import time
from typing import Optional
import xml.etree.ElementTree as ET
import ollama
import dataclasses
import re

# 設定ファイルからモデル名をインポート
from config import OLLAMA_MODEL_NAME, SummaryInfo


def extract_summary_info(text: str, timeout_seconds: int = 60) -> Optional[SummaryInfo]:
    """
    Ollamaモデルを呼び出してテキストから要約情報を抽出する。
    指定した時間以上かかった場合はタイムアウトとして処理し、それまでの生成結果を返す。
    """
    print("🤖 Ollamaで要約を生成しています...")
    start_time = time.time()
    generated_text = ""

    try:
        # ollama.chatをstream=Trueで実行
        stream = ollama.chat(
            model=OLLAMA_MODEL_NAME,
            messages=[
                {
                    'role': 'user',
                    'content': text,
                },
            ],
            stream=True
        )

        for chunk in stream:
            # 各チャンクの受信後に経過時間をチェック
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout_seconds:
                print(f"⌛ タイムアウト ({timeout_seconds}秒)になりました。それまでの生成結果を返します。")
                return parse_summary_xml(generated_text)

            # チャンクからコンテンツを結合
            content = chunk['message']['content']
            generated_text += content

        return parse_summary_xml(generated_text)

    except Exception as e:
        print(f"❌ Ollamaでの要約中にエラーが発生しました: {e}")
        print(
            f"Ollamaがローカルで起動しているか、またモデル '{OLLAMA_MODEL_NAME}' が利用可能か確認してください。")
        return None


def is_none_element(element: Optional[ET.Element]) -> bool:
    """要素がNoneまたはテキスト内容が「なし」か判定するヘルパー関数。"""
    return element is None or element.text is None or element.text.strip() == 'なし'


def parse_summary_xml(xml_string: str) -> Optional[SummaryInfo]:
    """
    XML文字列を動的に解析し、SummaryInfoを返します。
    パースエラーを防ぐため、不正な文字を事前にエスケープ処理します。
    """
    print("📄 XMLを解析しています...")
    try:
        cleaned_xml_string = re.sub(
            r'&(?!(?:[a-zA-Z]+|#[0-9]+);)', '&amp;', xml_string)

        root = ET.fromstring(cleaned_xml_string)

        extracted_data = {}
        # SummaryInfoのフィールドを動的にループ処理
        for field in dataclasses.fields(SummaryInfo):
            field_name = field.name
            element = root.find(field_name)

            if is_none_element(element):
                print(f"⚠️ 必須要素 '{field_name}' が見つからないか、内容が空です。")
                return None

            extracted_data[field_name] = element.text.strip()

        # 辞書を展開してSummaryInfoインスタンスを生成
        return SummaryInfo(**extracted_data)

    except ET.ParseError as e:
        print(f"❌ XMLの解析に失敗しました: {e}")
        # エラー発生時は、元の（クリーンアップ前）文字列を表示して問題の特定を容易にする
        print(f"受信したXML文字列: {xml_string}")
        return None
