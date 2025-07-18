import json
import random
import ollama

# データセットのパス（JNLI v1.3形式）
DATASET_PATH = "JGLUE/datasets/jnli-v1.3/valid-v1.3.json"
LIMIT = 100  # 最大テスト件数

# ラベルのマッピング --- (*1)
label2id = {
    "entailment": 0,
    "contradiction": 1,
    "neutral": 2,
}
id2label = {v: k for k, v in label2id.items()}

# プロンプトテンプレート --- (*2)
TEMPLATE = """\
### 指示:
次の入力の2文の関係を判断して、0-2の一つを選んでください。
### 入力:
- 前提: {premise}
- 仮説: {hypothesis}
### 出力:
以下のうちいずれかを選んで、1文字だけ出力してください。
- 0: entailment(仮説は前提から論理的に導ける)
- 1: contradiction(仮説は前提と矛盾する)
- 2: neutral(仮説は前提と関係しているが、導けない)
"""

# データの読み込み --- (*3)
with open(DATASET_PATH, encoding="utf-8") as f:
    lines = f.readlines()
    random.shuffle(lines)

def do_test(model):
    total = 0
    correct = 0
    # 繰り返しテストする --- (*4)
    for i, line in enumerate(lines):
        sample = json.loads(line.strip())
        label_text = sample["label"]
        if label_text not in label2id:
            continue  # 無効ラベルはスキップ
        # プロンプトの組み立て --- (*5)
        expected = label2id[label_text]
        prompt = TEMPLATE.format(
            premise=sample["sentence1"],
            hypothesis=sample["sentence2"]
        )
        # モデルへの問い合わせ --- (*6)
        res = ollama.generate(
            model=model,
            prompt=prompt,
            options={"temperature": 0.0},
            stream=False,
        )
        output = res["response"].strip()
        if "</think>" in output:
            output = output.split("</think>")[-1].strip()
        # 出力の解析 --- (*7)
        try:
            predicted = int(output)
        except ValueError:
            predicted = -1
        # 結果の評価 --- (*8)
        if predicted == expected:
            correct += 1
            print(f"+ [OK] {i+1}/{len(lines)}")
        else:
            print(f"+ [NG] {i+1}/{len(lines)}:")
            print(f"| 前提: {sample['sentence1']}")
            print(f"| 仮説: {sample['sentence2']}")
            print(f"| 出力: {output} → 予測={predicted}, 正解={expected} ({label_text})")

        total += 1
        if total >= LIMIT:
            break
    # 結果の集計 --- (*9)
    acc = correct / total
    print(f"✅ {model} の正答数: {correct}/{total}（{acc * 100:.2f}%）")
    return acc

if __name__ == "__main__":
    do_test("gemma3:4b")
