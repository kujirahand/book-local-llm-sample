from janome.tokenizer import Tokenizer
from config import *

# 形態素解析のためにJanomeを使用 --- (*1)
tokenizer = Tokenizer()
# 特殊トークンを定義 --- (*2)
UNK = 0 # 未知語
SOS = 1 # 文の開始
EOS = 2 # 文の終了
PAD = 3 # パディング
# トークン辞書を初期化 --- (*3)
token2id = {"<UNK>": UNK, "<SOS>": SOS, "<EOS>": EOS, "<PAD>": PAD}
id2token = {"0": "<UNK>", "1": "<SOS>", "2": "<EOS>", "3": "<PAD>"}

# トークンとIDを相互に変換する関数群を定義 --- (*4)
def token_to_id(word, add_new=True):
    """トークンをIDに変換する"""
    if word not in token2id:
        if not add_new:
            return token2id["<UNK>"]
        new_id = len(token2id)
        token2id[word] = new_id
        id2token[str(new_id)] = word
    return token2id[word]

def text_to_ids(text, add_new=True):
    """テキストをIDに変換する"""
    ids = []
    for token in tokenizer.tokenize(text):
        token_id = token_to_id(token.surface, add_new)
        ids.append(token_id)
    return ids

def ids_to_text(ids, skip_special=True, split_mark=""):
    """IDをテキストに変換する"""
    result = []
    for id_ in ids:
        if skip_special and id_ in [UNK, SOS, EOS, PAD]:
            continue
        if str(id_) in id2token:
            result.append(id2token[str(id_)])
        else:
            result.append("<UNK>")
    return split_mark.join(result)

# トークンをパディングする関数を定義 --- (*5)
def pad_sequence(ids, seq_len, pad_id=PAD):
    """シーケンスをパディングする"""
    return ids + [pad_id] * (seq_len - len(ids))

## JSON形式でデータを保存・読み込みする関数を定義 --- (*6)
def save_json(data, file_path):
    """データをJSON形式で保存する"""
    import json
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_json(file_path):
    """JSON形式のデータを読み込む"""
    import json
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
