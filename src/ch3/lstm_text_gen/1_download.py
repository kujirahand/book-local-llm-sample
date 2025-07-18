"""青空文庫の全テキストをダウンロードして解凍するスクリプト"""
import os
import requests
import zipfile
from config import *

# 青空文庫の全テキストをダウンロードするURL --- (*1)
url = "https://github.com/aozorahack/aozorabunko_text/archive/refs/heads/master.zip"

# corpus/modelディレクトリがなければ作成
if not os.path.exists(DIR_CORPUS):
    os.makedirs(DIR_CORPUS)
if not os.path.exists(DIR_MODEL):
    os.makedirs(DIR_MODEL)
# 青空文庫の全テキストを全部ダウンロード --- (*2)
if not os.path.exists(FILE_AOZORA_ZIP):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()  # 問題があれば例外を発生
        print("Downloading...", url)
        with open(FILE_AOZORA_ZIP, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024 * 8):
                f.write(chunk)
                print(".", end="", flush=True) # 1MBごとに進捗表示
            print("\nダウンロード完了!")
# ダウンロードしたzipファイルを解凍 --- (*3)
with zipfile.ZipFile(FILE_AOZORA_ZIP, "r") as zip_ref:
    zip_ref.extractall(DIR_CORPUS)
    print("解凍完了!")
