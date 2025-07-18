"""画像を読んでそれが何かを説明するプログラム"""
import base64
from io import BytesIO

import requests
from PIL import Image

# Ollama APIエンドポイントとモデルを指定 --- (*1)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"

def image_to_text(image_path, prompt=None): # --- (*2)
    """画像を読んでそれが何かを説明する関数"""
    # 画像をファイルから読んで縮小 --- (*3)
    image = Image.open(image_path)
    image.thumbnail((512, 512))
    # 画像をBase64エンコード--- (*4)
    buf = BytesIO()
    image.save(buf, format="PNG")
    image_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    # デフォルトのプロンプトを設定 --- (*5)
    if prompt is None:
        prompt = "次の画像の内容を見て何かを説明してください。"
    # Ollama APIにリクエストを送信 --- (*6)
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "images": [image_b64],
        "stream": False,
        "temperature": 0.5,
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    result = response.json()
    return result["response"].strip()

if __name__ == "__main__":
    # コマンドライン引数を取得 --- (*7)
    import sys
    file = sys.argv[1] if len(sys.argv) > 1 else "images/001.png"
    # 画像の説明を取得して結果を表示 --- (*8)
    print(image_to_text(file))
