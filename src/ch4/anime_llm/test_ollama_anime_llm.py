"""Ollama API経由でanime_llmをテスト"""
import requests

OLLAMA_API = "http://localhost:11434/api/generate"

def generate(prompt):
    """指示文を与えて応答を生成する関数"""
    # プロンプトをAPIに送信
    sys_prompt = f"<s>### 指示:\n{prompt}\n\n### 応答:\n"
    response = requests.post(OLLAMA_API, json={
        "model": "anime_llm",
        "prompt": sys_prompt,
        "stream": False,
    }, timeout=60)
    response.raise_for_status()  # エラーチェック
    result = response.json().get("response", "").strip()
    return result

if __name__ == "__main__":
    # テスト用の指示文を与えて応答を得る
    prompt = f"アニメ「ドカベン」の主人公を教えてください。"
    print(">>>", prompt) 
    print(generate(prompt))

