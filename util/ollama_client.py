import json
from typing import Optional
import xml.etree.ElementTree as ET
import ollama

# 設定ファイルからモデル名をインポート
from config import OLLAMA_MODEL_NAME


def generate_answer(text: str) -> dict[str, object] | None:
    """
    Ollamaモデルを呼び出してテキストから要約情報を抽出する。
    指定した時間以上かかった場合はタイムアウトとして処理し、それまでの生成結果を返す。
    """
    print("🤖 Ollamaで要約を生成しています...")

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL_NAME,
            messages=[
                {
                    'role': 'user',
                    'content': text,
                },
            ],
            think="high"
        )

        result = json.loads(response['message']['content'])
        return result

    except Exception as e:
        print(f"❌ Ollamaでの要約中にエラーが発生しました: {e}")
        print(
            f"Ollamaがローカルで起動しているか、またモデル '{OLLAMA_MODEL_NAME}' が利用可能か確認してください。")
        return None


def is_none_element(element: Optional[ET.Element]) -> bool:
    """要素がNoneまたはテキスト内容が「なし」か判定するヘルパー関数。"""
    return element is None or element.text is None or element.text.strip() == 'なし'
