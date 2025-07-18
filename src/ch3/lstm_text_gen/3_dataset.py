import random
from janome.tokenizer import Tokenizer

from config import *
from utils import *

# トークンの数を制限する値 --- (*1)
MAX_TOKENS = 20000
# トークン列を初期化 --- (*2)
ids = []

# コーパスを読み込む --- (*3)
file_size = os.path.getsize(FILE_CORPUS_TXT) # ファイルサイズ
read_size = 0
with open(FILE_CORPUS_TXT, "r", encoding="utf-8") as f:
    lines = list(f.readlines())
    random.shuffle(lines)  # ランダムに並び替え
# 1行ずつ読み込んでトークン化する --- (*4)
for i, line in enumerate(lines):
    if i % 10 == 0:
        per = int(read_size / file_size * 100)
        print(f"読み込み中... {i}行目 ({per}%)")
    # トークンの数が上限を超えたら終了する --- (*5)
    if len(token2id) > MAX_TOKENS:
        print("読み込み完了")
        break
    read_size += len(line)
    # トークン化する --- (*6)
    tokens = text_to_ids(line, True)
    ids.extend(tokens)  # トークンを追加する

# ファイルに保存 --- (*7)
save_json(token2id, FILE_TOKEN2ID)
save_json(id2token, FILE_ID2TOKEN)
save_json(ids, FILE_IDS, indent=0)
print("保存しました。トークン数:", len(token2id))
