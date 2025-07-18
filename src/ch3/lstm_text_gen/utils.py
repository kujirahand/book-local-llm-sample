import json
from janome.tokenizer import Tokenizer

T_UNKNOWN = "<unk>"  # 未知語のトークン --- (*1)
token2id = {T_UNKNOWN: 0}  # 未知語のIDを0に設定
id2token = {"0": T_UNKNOWN}  # 未知語のIDを0に設定
token_id = 1

# 形態素解析を行うためのインスタンスを作成 --- (*2)
tokenizer = Tokenizer()

def token_to_id(token, add_if_not_exist=True): # --- (*3)
    """単語をIDに変換する"""
    if token in token2id:
        return token2id[token]
    if add_if_not_exist:
        global token_id
        token2id[token] = token_id
        id2token[token_id] = token
        token_id += 1
        return token_id - 1
    return 0

def text_to_ids(text, add_if_not_exist=True): # --- (*4)
    """テキストをIDのリストに変換する"""
    ids = []
    tokens = tokenizer.tokenize(text)
    surface_list = [t.surface for t in tokens]
    for token in surface_list:
        ids.append(token_to_id(token, add_if_not_exist))
    return ids

def load_json(file_path):
    """JSONファイルを読み込む"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_json(data, file_path, indent=4):
    """JSONファイルに保存する"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
