"""設定ファイル"""
import os
import base64
from io import BytesIO
from PIL import Image

# 各種パスを指定 --- (*1)
DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_IMAGES = os.path.join(DIR_ROOT, "images")
# Ollama APIの設定 --- (*2)
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_CHAT_MODEL = "gemma3:4b"  # チャット用モデル名
OLLAMA_IMAGE_MODEL = "gemma3:4b"  # 画像の説明に使うモデル名
# 画像生成モデルを指定 --- (*3)
IMAGE_GEN_MODEL = "Linaqruf/anything-v3-1"
# パスの作成
if not os.path.exists(DIR_IMAGES):
    os.makedirs(DIR_IMAGES)

# 強調表示のための関数 --- (*4)
def print_title(title):
    """タイトルを強調表示する関数"""
    esc_b = "\033[41;37m"
    esc_e = "\033[0m"
    print("=" * 80)
    print(f"{esc_b}{title}{esc_e}")

# 画像を表示する関数 --- (*5)
def show_image_cli(image_path):
    """iTerm2やKittyターミナルで画像を表示する関数"""
    img = Image.open(image_path)
    img.thumbnail((400, 400))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    bin_data = buffer.getvalue()
    b64 = base64.b64encode(bin_data).decode('utf-8')
    size = len(bin_data)
    if is_iterm2():
        print(f"\033]1337;File=inline=1;width=auto;height=auto;preserveAspectRatio=1:{b64}\a")
    elif is_kitty():
        print(f"\033_Gf=100,a=T,t=d,s={size};{b64}\033\\")
    else:
        print("画像パス:", image_path)
# ターミナルに画像が表示できるか判定
def is_iterm2():
    """"iTerm2ターミナルかどうかを判定"""
    return os.environ.get("TERM_PROGRAM") == "iTerm.app"
def is_kitty():
    """Kittyターミナルかどうかを判定"""
    return "KITTY_WINDOW_ID" in os.environ
