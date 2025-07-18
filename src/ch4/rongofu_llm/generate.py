"""Fine-Tuning済みモデルでテキスト生成する"""
from unsloth import FastLanguageModel
import torch
if 'get_ipython' not in globals(): # Colab環境でない場合は
    from config import *

# モデルフォルダからモデルとトークナイザーを読み込む --- (*1)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL_SAVE_DIR,  # 保存したフォルダ
    max_seq_length = MAX_SEQ_LENGTH,
    dtype=None,
    load_in_4bit = True,
)
# モデルを推論モードに設定
model.eval()

# プロンプトのテンプレート --- (*2)
PROMPT_TEMPLATE = """\
あなたは偉い先生である。次のタスクに対する指示文に対して内容に基づいて論語風に答えよ。

### 指示:
{}

### 応答:
"""


# テキストを生成する処理 --- (*3)
def generate(prompt):
    """指示文を与えて応答を生成する関数"""
    # プロンプトの作成 --- (*4)
    sys_prompt = PROMPT_TEMPLATE.format(prompt)
    # 入力をトークナイズ --- (*5)
    inputs = tokenizer(sys_prompt, return_tensors="pt").to(model.device)
    # 文章を生成する --- (*6)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=500,
            do_sample=True,
            temperature=0.8,
            top_p=0.95,
            repetition_penalty=1.1,
        )
    # 生成されたトークン列をテキストに戻す --- (*7)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 出力からプロンプトを除去 --- (*8)
    if sys_prompt in response:
        response = response.replace(sys_prompt, "")
    return response.strip()

if __name__ == "__main__":
    print("\n<<< 論語風ミストラル - [q]で終了します。\n")
    # テスト用の指示文を与えて応答を得る --- (*9)
    tests = [
        "良いプログラムの条件は？",
        "健康になるために最も大切なことは何？",
        "水を表す元素記号は？",
        "ネコとネズミはどちらが強い？",
        "人間の本質を教えて。",
        "素数とは何？",
        "持ち家と賃貸、どちらが良い？",
    ]
    for inst in tests:
        print(f">>> {inst}")
        print(generate(inst))
        print("------------------------")
    # ユーザーからの入力を受け付けて応答を生成 --- (*10)
    while True:
        prompt = input(">>> ")
        if prompt.lower() == "q":
            print("終了します。")
            break
        print(generate(prompt))
        print("------------------------")
