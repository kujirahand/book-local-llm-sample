"""LLMでプロンプトを生成して画像生成するプログラム"""
import os
import requests
import image_generator as image_gen

# 画像生成プロンプトのテンプレート --- (*1)
PROMPT_TPL = """
### 指示:
あなたはプロのイラストレーターです。
入力に基づいて、画像生成AI(Stable Diffusion)を使用してイラストを作成するプロンプトを作成してください。

### 入力:
```{prompt}```

#### 出力:
解説メッセージは不要で、画像生成用プロンプトのみを出力してください。
プロンプトは英語で出力し、`masterpiece`や`best quality`などの適切なキーワードを含めてください。
"""

# 環境変数OLLAMA_HOSTを得る --- (*2)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost:11434")

def ollama_generate(user_prompt, model="gemma3:4b"): # ---(*3)
    """Ollamaを利用して画像生成用のプロンプトを作成する"""
    prompt = PROMPT_TPL.format(prompt=user_prompt)
    url = f"http://{OLLAMA_HOST}/api/generate"
    print(url)
    data = {
        "model": model,
        "prompt": prompt,
        "temperature": 0.7,
        "stream": False,
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()
    return result["response"]

# 画像生成を行う関数 --- (*4)
def generate(savepath, user_prompt):
    """画像生成を行う"""
    prompt = ollama_generate(user_prompt)
    print(f"prompt: {prompt}")
    image_gen.generate_image(savepath, prompt)

def set_image_model(model_name):
    """画像生成モデルを設定する"""
    image_gen.pipe = image_gen.load_model(model_name)

if __name__ == "__main__": # --- (*5)
    USER_PROMPT = "水族館ではしゃぐ子供のパステル調のイラストを描いて。"
    for i in range(10):
        png = os.path.join(image_gen.DIR_IMAGES, f"llm_image{i:03}.png")
        generate(png, USER_PROMPT)
