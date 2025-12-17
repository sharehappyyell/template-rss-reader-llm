import asyncio
import json
from ollama import AsyncClient
from config import OLLAMA_MODEL_NAME, OLLAMA_TIMEOUT_SECONDS


async def generate_answer(text: str):
    print("🤖 Ollamaで要約を生成しています...")
    try:
        client = AsyncClient()

        # asyncio.wait_for でタイムアウトを管理
        response = await asyncio.wait_for(
            client.chat(
                model=OLLAMA_MODEL_NAME,
                messages=[{'role': 'user', 'content': text}],
                think="high"
            ),
            timeout=OLLAMA_TIMEOUT_SECONDS
        )

        return json.loads(response['message']['content'])

    except asyncio.TimeoutError:
        print("⏰ タイムアウトしました")
        return None
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None
