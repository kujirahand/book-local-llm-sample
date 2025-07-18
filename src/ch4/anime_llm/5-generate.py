"""Fine-Tuning済モデルを元にテキスト生成する"""
import torch
from unsloth import FastLanguageModel
if 'get_ipython' not in globals(): # Colab環境でない場合
    from config import *

# 生成に使うプロンプト --- (*1)
GENERATE_PROMPT = """\
あなたはアニメの主人公やあらすじについて答えるアシスタントです。
以下の指示に沿って答えてください。

### 指示:
{}

### 応答:
"""

# モデルとトークナイザのロード（学習済みフォルダから） --- (*2)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = DIR_MODEL,  # 保存したフォルダ
    max_seq_length = MAX_SEQ_LENGTH,
    dtype=None,
    load_in_4bit = True,
)
model.eval()
FastLanguageModel.for_inference(model)  # 推論モードに設定

def generate(prompt): # --- (*3)
    """指示文を与えて応答を生成する関数"""
    # 指示文をプロンプトに埋め込む --- (*4)
    sys_prompt = GENERATE_PROMPT.format(prompt)
    # プロンプトをトークン列に変換 --- (*5)
    inputs = tokenizer(sys_prompt,
                return_tensors="pt").to(model.device)
    # テキストを生成する --- (*6)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=500,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            repetition_penalty=1.1,
        )
    # トークン列を文章にデコード --- (*7)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # プロンプト部分を削除 --- (*8)
    if response.startswith(sys_prompt):
        response = response[len(sys_prompt):]
    return response

if __name__ == "__main__":
    # テスト用の指示文を与えて応答を得る --- (*9)
    tests = ["ドカベン", "タッチ", "カードキャプターさくら", "ガンダムZZ", "銀魂"]
    for name in tests:
        print("------------------------")
        print(f">>> {name}")
        print("------------------------")
        prompt = f"「{name}」について主人公を教えてください。"
        print(">>>", prompt)
        print(generate(prompt))
        print("------------------------")
        prompt = f"「{name}」についてあらすじを教えてください。"
        print(">>>", prompt)
        print(generate(prompt))

