import json
import os
import re

from markov import *

def train_dir(model, dir_path): # ---(*1)
    """指定されたディレクトリ内のテキストファイルを学習する"""
    # ディレクトリ内のファイルを再帰的に取得 --- (*2)
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if not file.endswith(".md"):
                continue
            # テキストファイルを読み込む --- (*3)
            print("read:", file)
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                # 不要な記号を削除する --- (*4)
                text = re.sub(r"(</+?>|&[a-z]+;|\{.+?\})", "", text) # タグを削除
                text = re.sub(r"[\(\) |（）「」\u3000]", "", text)
                text = text.replace("&mdash;", "")
                # テキストを学習する --- (*5)
                train(model, text)

if __name__ == "__main__": # --- (*6)
    MODEL_FILE = "markov_model_kinoko.json"
    if os.path.exists(MODEL_FILE):
        # モデルが存在する場合は読み込む
        with open(MODEL_FILE, "r", encoding="utf-8") as f:
            model = json.load(f)
    else:
        # モデルが存在しない場合は学習する
        model = {}
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        SRC_DIR = os.path.join(ROOT_DIR, "kinokobooks", "src")
        train_dir(model, SRC_DIR)
        # モデルを保存する
        with open(MODEL_FILE, "w", encoding="utf-8") as f:
            json.dump(model, f, ensure_ascii=False, indent=4)
    # テキストを生成する
    for _ in range(3):
        print("-", generate(model))
