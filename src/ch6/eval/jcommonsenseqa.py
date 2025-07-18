import random
import json
import ollama

# 対象となるデータセットのJSONファイルパス
DATASET_JSON = "JGLUE/datasets/jcommonsenseqa-v1.3/valid-v1.3.json"
LIMIT = 100 # テストするデータ数
# プロンプトテンプレート --- (*1)
TMPLATE = """\
以下の質問に最も常識的に正しい答えを1つ選んでください。選択肢はAからEの中にあります。

質問: {question}

選択肢:
0. {choice_0}
1. {choice_1}
2. {choice_2}
3. {choice_3}
4. {choice_4}

正しい選択肢の番号（0〜4）のみを1文字で答えてください：
"""

# データセットの読み込み（JCommonsenseQA） --- (*2)
with open(DATASET_JSON, encoding="utf-8") as f:
    dataset_lines = f.readlines()
    random.shuffle(dataset_lines)  # ランダムにシャッフル

def do_test(model): # --- (*3)
    """テストを実行する"""
    # スコア計算用 --- (*4)
    total = 0
    correct = 0
    # データセットを一つずつ出題する --- (*5)
    for i, sample_json in enumerate(dataset_lines):
        sample_json = sample_json.strip()
        if not sample_json:
            continue
        # JSONをパースしてサンプルを取得 --- (*6)
        sample = json.loads(sample_json)
        # プロンプトの生成 --- (*7)
        input_prompt = TMPLATE.format(
            question=sample["question"],
            choice_0=sample["choice0"],
            choice_1=sample["choice1"],
            choice_2=sample["choice2"],
            choice_3=sample["choice3"],
            choice_4=sample["choice4"],
        )
        # LLMに問い合わせ --- (*8)
        res = ollama.generate(
            model=model,
            prompt=input_prompt,
            options={"temperature": 0.0, "max_tokens": 250},
            stream=False,
        )
        output = res["response"].strip()
        if "</think>" in output: # --- (*9)
            output = output.split("</think>")[-1].strip()
        # 回答の番号を取得 --- (*10)
        try:
            predicted = int(output)
        except ValueError:
            predicted = -1 # ng
        expected = sample["label"]
        # 正解チェック --- (*11)
        total += 1
        if predicted == expected:
            correct += 1
            print(f"+ [OK] {i+1}/{len(dataset_lines)}")
        else:
            print(f"+ [NG] Q: {json.dumps(sample, ensure_ascii=False)}")
            print(f"- 予測: {predicted}, 正解: {expected} (出力: {output})")
        if LIMIT <= total:
            break
    # 結果の表示 --- (*12)
    accuracy = correct / total
    print(f"✅ {model}の正答数: {correct}/{total} ({accuracy * 100:.2f}%)")
    return accuracy

if __name__ == "__main__":
    do_test("gemma3:4b")  # テスト実行
