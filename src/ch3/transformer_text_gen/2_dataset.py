import random
from config import *
from utils import *

def make_dataset(): # --- (*1)
    """データセットを作成する"""
    result = []
    # コーパスの読み込み --- (*2)
    with open(FILE_CORPUS, "r", encoding="utf-8") as f:
        text = f.read()
        lines = text.splitlines()
        random.shuffle(lines)
        lines = lines[:CORPUS_MAX_LINES] # 行数を制限
        for i, line in enumerate(lines):
            if i % 1000 == 0:
                print(f"{i}/{len(lines)}行を処理しました")
            line = line.strip()
            # トークン化 --- (*3)
            ids = text_to_ids(line, add_new=True)
            # 文章の開始と終了を示すトークンを追加 --- (*4)
            tokens = [SOS] + ids + [EOS]
            if len(tokens) < 7 or len(tokens) > SEQ_LEN:
                continue # トークン数が長い時と短い時にスキップ
            result.append(tokens)
    # データセットの保存 --- (*5)
    save_json(result, FILE_IDS)
    # トークン辞書の保存
    save_json(token2id, FILE_TOKEN2ID)
    save_json(id2token, FILE_ID2TOKEN)
    print("データセットを保存しました")
    print(f"トークン数: {len(token2id)}")
    print(f"データ数: {len(result)}")

if __name__ == "__main__":
    make_dataset()
