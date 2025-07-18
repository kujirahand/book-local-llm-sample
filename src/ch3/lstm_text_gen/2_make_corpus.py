"""青空文庫のテキストを全て結合して1つのテキストファイルにする"""
import os
import re
from config import *

# 特定の作家の作品のみを抽出する --- (*1)
authors = ["夏目漱石", "太宰治", "芥川竜之介", "宮沢賢治"]

def enum_files(path): # --- (*2)
    """指定したディレクトリ内の全てのテキストファイルを列挙する"""
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                yield os.path.join(root, file)

def make_corpus(): # --- (*3)
    """青空文庫のテキストを全て結合して1つのテキストファイルにする"""
    with open(FILE_CORPUS_TXT, "w", encoding="utf-8") as outfile:
        for file in enum_files(DIR_CORPUS):
            try:
                # 青空文庫のテキストはShift_JIS(CP932) --- (*4)
                with open(file, "r", encoding="cp932") as infile:
                    text = format_txt(infile.read())
                    if len(text) < 300:
                        continue
                    # 特定の作家の作品のみを抽出する --- (*5)
                    sub_text = text[0:300]
                    found = None
                    for author in authors:
                        if author in sub_text:
                            found = author
                            break
                    if found is None:
                        continue
                    print("結合中:", found, os.path.basename(file))
                    outfile.write(text + "\n")
            except UnicodeDecodeError:
                print(f"エラー: {file}の読込に失敗")
                continue
    print("corpus.txtを作成しました。")

def format_txt(text): # ---(*6)
    """青空文庫のテキストを整形する"""
    text = text.replace("\r\n", "\n")  # 改行コードをLFに変換
    # テキスト中に現れる記号についてを削除
    blocks = re.split("-{10,}\n", text)
    if len(blocks) >= 3:
        text = blocks[0] + "\n" + blocks[2]
        text = text.strip()
    # 末尾の情報を削除
    blocks = re.split("\n底本[：\:]", text)
    text = blocks[0]
    # ルビや注釈を削除
    text = re.sub(r"《.+?》", "", text)  # ルビを削除
    text = re.sub(r"［＃.+?］", "", text)  # 注釈を削除
    text = re.sub(r"^\s+", "", text, flags=re.MULTILINE)  # 行頭の空白を削除
    text = re.sub(r"\n+", "\n", text)  # 連続する改行を1つにまとめる
    text = re.sub(r"[｜|｜「」『』]", "", text)  # 記号を削除
    return text

if __name__ == "__main__":
    make_corpus()
