import json
import random
import ollama
from sklearn.metrics import mean_squared_error

# データセットのパス（JGLUEのJSTS）
DATASET_PATH = "JGLUE/datasets/jsts-v1.3/valid-v1.3.json"
LIMIT = 100  # テストする最大件数

# プロンプトテンプレート --- (*1)
TEMPLATE = """\
以下の2つの文の意味の類似度を0-5のスケールで評価してください。
5が最も意味が近く、0が最も意味が異なります。

文1: {sentence1}
文2: {sentence2}

0-5の数字のみを1つだけ出力してください（小数点以下も可）：
"""

# データの読み込み --- (*2)
with open(DATASET_PATH, encoding="utf-8") as f:
    lines = f.readlines()
    random.shuffle(lines)

def do_test(model):
    """テストを実行"""
    y_true = []
    y_pred = []
    total = 0
    # 繰り返しテストする --- (*3)
    for i, line in enumerate(lines):
        # プロンプトの組み立て --- (*4)
        sample = json.loads(line.strip())
        prompt = TEMPLATE.format(
            sentence1=sample["sentence1"],
            sentence2=sample["sentence2"]
        )
        # LLMに問い合わせ --- (*5)
        res = ollama.generate(
            model=model,
            prompt=prompt,
            options={"temperature": 0.0, "max_tokens": 50},
            stream=False,
        )
        output = res["response"].strip()
        if "</think>" in output:
            output = output.split("</think>")[-1].strip()
        # 結果の処理 --- (*6)
        try:
            score = float(output)
        except ValueError:
            score = -1.0  # 無効値
        expected = float(sample["label"])
        y_true.append(expected)
        y_pred.append(score)
        print(f"{i+1}: 予測={score:.2f}, 正解={expected:.2f}")
        total += 1
        if total >= LIMIT:
            break
    # 精度評価（MSE） --- (*7)
    mse = mean_squared_error(y_true, y_pred)
    print(f"✅ {model} の平均二乗誤差 (MSE): {mse:.4f}")
    return mse

if __name__ == "__main__":
    do_test("gemma3:4b")
