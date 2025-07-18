import random
import json
import ollama

# 対象となるデータセットのJSONファイルパス
DATASET_JSON = "JGLUE/datasets/jsquad-v1.3/valid-v1.3.json"
LIMIT = 50 # テストするデータ数
# プロンプトテンプレート --- (*1)
TMPLATE = """\
次の文脈を読んで、質問に対する最も適切な答えを日本語で簡潔に答えてください。

文脈:
{context}

質問:
{question}

答え（日本語で一文）:
"""

# データ読み込み --- (*2)
with open(DATASET_JSON, encoding="utf-8") as f:
    obj = json.load(f)
    dataset = obj["data"]
    random.shuffle(dataset)  # ランダムにシャッフル

def do_test(model):
    """テストを実行する"""
    # スコア計算
    total = 0
    correct = 0
    # 繰り返しテストを行う --- (*3)
    for i, sample in enumerate(dataset):
        # データセットから問題と回答を取得 --- (*4)
        paragraph = sample["paragraphs"][0]
        question = paragraph["qas"][0]["question"]
        context = paragraph["context"]
        answers = paragraph["qas"][0]["answers"]
        # プロンプトの生成 --- (*5)
        input_prompt = TMPLATE.format(
            context=context,
            question=question,
        )
        # モデルにプロンプトを送信して応答を取得 --- (*6)
        res = ollama.generate(
            model=model,
            prompt=input_prompt,
            options={"temperature": 0.0},
            stream=False,
        )
        output = res["response"].strip()
        if "</think>" in output:
            output = output.split("</think>")[-1].strip()
        print(f"A: {output}")
        # 正解チェック --- (*7)
        ok = False
        for a in answers: # 各回答をチェック
            answer = a["text"].strip()
            if answer in output:
                ok = True
        # 結果の集計 --- (*8)
        total += 1
        if ok:
            correct += 1
            print(f"+ [OK] {i+1}/{len(dataset)} Q: {question}")
        else:
            print(f"+ [NG] Q: {json.dumps(paragraph, ensure_ascii=False)}")
            print(f"- 予測: {output}, 正解: {answers}")
            print("---")
        if LIMIT <= total:
            break
    # 結果の表示 --- (*9)
    accuracy = correct / total
    print(f"✅ {model}の正答数: {correct}/{total} ({accuracy * 100:.2f}%)")
    return accuracy

if __name__ == "__main__":
    do_test("gemma3:4b")  # テスト実行
