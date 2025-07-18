import os
from datetime import datetime
from text2text import text2text
from image2text import image2text
from text2image import text2image_easy
from chat_template import TEMPLATE_SELECT_TASK
from config import *

# チャット履歴を保持するリスト --- (*1)
chat_history = [
    {"role": "system",
     "content": "あなたは親切なAIアシスタントです。"},
]

# タスクを選択するための関数 --- (*2)
def check_task(user):
    """ユーザーの入力からタスクを選択する関数"""
    # タスク選択のためのプロンプトを生成 --- (*3)
    prompt = TEMPLATE_SELECT_TASK.format(input=user)
    r = text2text(
        [{"role": "user", "content": prompt}],
        model=OLLAMA_CHAT_MODEL, show_output=False)
    # タスクの選択肢を確認 --- (*4)
    if "Text-to-Image" in r:
        return "Text-to-Image"
    if "Text-to-Text" in r:
        return "Text-to-Text"
    return "Text-to-Text"

# チャットを行うメイン関数 --- (*5)
def main_chat():
    """チャットインターフェースを提供する関数"""
    while True:
        # タイトルを表示
        print_title("マルチモーダルチャット")
        print("<<< 終了するには `/bye` と入力してください。")
        print("<<< 画像を説明するには、`/image=(path)`と入力してください。")
        # ユーザーからの入力を取得 --- (*6)
        user = input(">>> ")
        if user.lower() == '/bye':
            print("チャットを終了します。")
            break
        if user == "":
            continue
        # 画像を説明する --- (*7)
        if user.startswith('/image='):
            # 画像ファイルのパスを取得
            image_file = user.split('=')[1].strip()
            print_title("<<< 画像ファイルを説明します:")
            if not os.path.exists(image_file):
                print("<<< エラー: 画像ファイルが存在しません")
                image_file = None
                continue
            user = "画像を説明してください。"
            desc = image2text(image_file)
            chat_history.append({"role": "user", "content": user})
            chat_history.append({"role": "assistant", "content": desc})
            continue
        # タスク選択のプロンプトを生成 ----(*8)
        task = check_task(user)
        print_title(f"<<< 選択されたタスク: {task}")
        if task == "Text-to-Image": # 画像生成タスクの場合
            ctime = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = os.path.join(DIR_IMAGES,  f"image{ctime}.png")
            text2image_easy(user, fname, history=chat_history)
            print_title("<<< 画像が生成されました")
            show_image_cli(fname)
            continue
        # テキスト生成タスク --- (*9)
        chat_history.append({"role": "user", "content": user})
        print_title("<<< AIが応答します...")
        r = text2text(chat_history)
        chat_history.append({"role": "assistant", "content": r})

if __name__ == "__main__":
    main_chat()
