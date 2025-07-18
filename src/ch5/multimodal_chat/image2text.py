"""画像説明モジュール"""
import base64
from io import BytesIO
from PIL import Image
from config import *
from chat_template import *
from text2text import *

# 画像を説明する関数 --- (*1)
def image2text(image_path, prompt=None):
    """Ollama APIを使って画像を説明する関数"""
    # デフォルトのプロンプトを設定 --- (*2)
    if prompt is None:
        prompt = TEMPLATE_IMAGE_PROMPT
    # Ollama APIに画像付きでリクエストを送信 --- (*3)
    return text2text([{
        "role": "user",
        "content": prompt,
        "images": [get_image_b64data(image_path)]
    }], model=OLLAMA_IMAGE_MODEL)

# 画像をBase64エンコードして返す関数 --- (*4)
def get_image_b64data(image_path, size=(300, 300)):
    """画像が指定されている場合はBase64エンコードして追加"""
    img = Image.open(image_path)
    img.thumbnail(size) # 画像のサイズを調整
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    bin_data = buffer.getvalue()
    return base64.b64encode(bin_data).decode('utf-8')

if __name__ == "__main__":
    # テスト用のコード --- (*5)
    result = image2text("test_image.png")
    print(f"画像の説明: {result}")
