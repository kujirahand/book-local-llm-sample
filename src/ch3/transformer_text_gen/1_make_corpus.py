import os
import re
from config import *

# コーパスとモデルのフォルダを作成
os.makedirs(DIR_CORPUS, exist_ok=True)
os.makedirs(DIR_MODEL, exist_ok=True)

# コーパスを作成するためにテキストファイルを収集 --- (*1)
lines = []
for root, dirs, files in os.walk(DIR_CORPUS_SOURCE):
    for fname in files:
        # 拡張子を調べて、"*.md"のみを対象にする
        if not fname.endswith(".md") or fname == "README.md":
            continue
        print(fname)
        # ファイルを開く --- (*2)
        file_path = os.path.join(root, fname)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            # ソースコード部分を除去する  ---- (*3)
            text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
            text = text.replace("。", "。\n") # 改行を追加
            text = text.replace("？", "？\n") # 改行を追加
            # マークダウン記号や括弧書き、URLを削除
            text = re.sub("(\*\*|　)", "", text)
            text = re.sub(r"(\(.+?\)|（.+?）)", "", text) # ()を削除
            text = re.sub(r"(https?|mailto)\:[a-zA-Z0-9~_/@\-\.\?]+", "", text)
            # テキストを整形する --- (*4)
            for line in text.splitlines(): # 1行ずつ処理
                line = line.strip()
                if line == "":
                    continue
                # 行の先頭を確認してコーパスに含めないようにする --- (*5)
                if line[0] in "#-*|><":
                    continue
                lines.append(line)
text = "\n".join(lines)
# テキストを保存 --- (*6)
with open(FILE_CORPUS, "w", encoding="utf-8") as f:
    f.write(text)
