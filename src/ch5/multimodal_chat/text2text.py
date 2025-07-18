"""テキストチャットを行うモジュール"""
import json
import requests
from config import *

# テキストを生成する関数 --- (*1)
def text2text(messages, model=OLLAMA_CHAT_MODEL, show_output=True):
    """Ollama APIを使ってテキストチャットを行う関数"""
    data = {
        "model": model,
        "messages": messages,
        "templerature": 0.8,
        "stream": True  # ストリーム出力を有効にする --- (*2)
    }
    result = ""  # 結果を格納する変数
    with requests.post(OLLAMA_CHAT_URL, json=data,
                    stream=True, timeout=60) as response:
        # 繰り返しOllama APIからのレスポンスを処理 --- (*3)
        for line in response.iter_lines():
            if not line:
                continue
            try:
                # JSON形式のレスポンスをパース --- (*4)
                chunk = json.loads(line.decode("utf-8"))
                if "message" in chunk and "content" in chunk["message"]:
                    content = chunk["message"]["content"]
                    if show_output:
                        print(content, end='', flush=True)
                    result += content
            except ValueError:
                continue
    if show_output:
        print()  # 最後に改行を追加
    # 最終的な結果を返す --- (*5)
    if "</think>" in result:
        # thinkタグが含まれている場合はそれ以後を取得
        result = result.split("</think>")[-1].strip()
    return result

if __name__ == "__main__":
    # テスト用のコード --- (*6)
    test_messages = [
        {"role": "user", "content": "犬に関する豆知識を1つ教えて。"},
    ]
    response = text2text(test_messages)
    print(f"応答: {response}")
