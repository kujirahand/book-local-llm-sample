import json
import os
import random
from janome.tokenizer import Tokenizer

# 初期化処理
HEAD = "<HEAD>"
tokenizer = Tokenizer()
model = {}

def train(model, text): # --- (*1)
    """テキストを学習してモデルを生成する"""
    # 句点や改行で分割する
    text = text.replace("。", "。\n")
    sentences = text.split("\n")
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence == "":
            continue
        # 形態素解析 --- (*2)
        tokens = tokenizer.tokenize(sentence)
        # トークンをリストに変換
        words = [token.surface for token in tokens]
        # 3-gramを生成 --- (*3)
        ngrams = []
        for i in range(len(words) - 2):
            ngram = (words[i], words[i + 1], words[i + 2])
            ngrams.append(ngram)
        # 3-gramをモデルに追加 --- (*4)
        is_head = True
        for ngram in ngrams:
            if is_head:
                # 文頭は特別扱いとする
                key = f"{HEAD}:{ngram[0]}"
                add_model(model, key, ngram[1])
                is_head = False
            key = f"{ngram[0]}:{ngram[1]}"
            add_model(model, key, ngram[2])

def add_model(model, key, value):
    """辞書型のモデルに値を追加する"""
    if key not in model:
        # モデルにキーが存在しない場合は新規作成
        model[key] = []
    # モデルに値を追加
    if value not in model[key]:
        # 同じ値が存在しない場合のみ追加
        model[key].append(value)

def generate(model, start_word=None, max_length=100): # --- (*5)
    """モデルから文章を生成する"""
    if start_word is None:
        # ヘッダから始まるキーの一覧を取得 --- (*6)
        head_keys = [key for key in model.keys()
                     if key.startswith(HEAD)]
        # ランダムに文頭を選ぶ
        start_word = random.choice(head_keys)
    else:
        # 指定された単語から生成を開始する
        start_word = f"{HEAD}:{start_word}"
    # 繰り返し形態素のつながりを探しながら文章を生成する --- (*7)
    result = [start_word.split(":")[1]]
    current_word = start_word
    for _ in range(max_length):
        if current_word not in model: # 続きがなければ終了
            break
        # 現在の単語から次の単語をランダムに選ぶ --- (*8)
        next_word = random.choice(model[current_word])
        result.append(next_word)
        # 次の単語を現在の単語に更新 --- (*9)
        current_word = f"{current_word.split(':')[1]}:{next_word}"
    return "".join(result)

if __name__ == "__main__": # --- (*10)
    MODEL_FILE = "markov_model_ranpo.json"
    if os.path.exists(MODEL_FILE):
        # モデルが存在する場合は読み込む
        with open(MODEL_FILE, "r", encoding="utf-8") as f:
            model = json.load(f)
    else:
        # モデルが存在しない場合は学習する
        model = {}
        with open("shinri_shiken_fix.txt", "r", encoding="utf-8") as f:
            train(model, f.read())
        # モデルを保存する
        with open(MODEL_FILE, "w", encoding="utf-8") as f:
            json.dump(model, f, ensure_ascii=False, indent=4)
    # 文章を3つ生成する --- (*11)
    for _ in range(3):
        print("-", generate(model))
