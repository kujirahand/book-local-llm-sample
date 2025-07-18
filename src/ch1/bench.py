import json
import ollama
# 出力レポートファイル
report_file = "report.txt"
# テストするモデルのリスト
models = [
    "llama3.2:3b",
    "gemma3:4b",
    "qwen3:8b",
    "phi4:14b",
    "deepseek-r1:14b",
    "gemma3:27b",
    "qwen3:30b",
    "llama4:scout", # 67b
    "deepseek-r1:70b",
]
# テストするプロンプト
prompt = """
### Instruction:
次の手順で段階的に考えて、最終的に日本語で答えを提出してください。
1. 可愛いの定義を考えて述べてください。
2. 次に可愛い猫の名前を3つ考えて、その理由を答えてください。
3. 上記の名前を一つずつ精査して、最終的に1つだけを選んでください。
4. 回答を下記のJSON形式で出力してください。
### Output:
```json
{
    "answer": "<猫の名前>",
    "selection": ["名前1", "名前2", "名前3"]
}
```
"""
force_skip = False
history = []

def call_ollama(model):
    print("================================")
    # モデルの取得
    print(f"# Model: {model}")
    ollama.pull(model)
    print("---------------------------------")
    # Ollamaを呼び出す
    response = ollama.generate(
        model=model,
        prompt=prompt,
        options={"temperature": 0.7},
    )
    # 返ってきた応答の内容を表示
    print("---------------------------------")
    print("Model:", model)
    sec = 1000 ** 3
    prompt_eval_duration = response["prompt_eval_duration"] / sec
    prompt_eval_count = response["prompt_eval_count"]
    prompt_eval_rate = prompt_eval_count / prompt_eval_duration
    eval_duration = response["eval_duration"] / sec
    eval_count = response["eval_count"]
    eval_rate = eval_count / eval_duration
    print("Prompt eval duration:", prompt_eval_duration)
    print("Prompt eval count:", prompt_eval_count)
    print(f"* Prompt eval rate: {prompt_eval_rate: .3f} tokens/s")
    print("Eval duration:", eval_duration)
    print("Eval count:", eval_count)
    print(f"* Eval rate: {eval_rate:.3f} tokens/s")
    print("---------------------------------")
    print(">>>", response['response'])
    print("---------------------------------")
    history.append({
        "model": model,
        "response": response["response"],
        "eval_duration": eval_duration,
        "eval_count": eval_count,
        "prompt_eval_duration": prompt_eval_duration,
        "prompt_eval_count": prompt_eval_count,
        "eval_rate": eval_rate,
        "prompt_eval_rate": prompt_eval_rate,
    })
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
    if eval_rate < 1.0:
        print("[ERROR]: eval_rateが 1.0 を切ったので中断します")
        global force_skip
        force_skip = True

for model in models:
    if force_skip:
        break
    # モデルを呼び出す
    try:
        call_ollama(model)
    except Exception as e:
        print("[error]", e)

input("ok")




