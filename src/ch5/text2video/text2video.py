"""テキストから動画を生成するプログラム"""
import os
import subprocess
import yaml
import requests
import random

# Ollama APIの設定 --- (*1)
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_API_MODEL = "qwen3:8b"
# プロンプトのテンプレート --- (*2)
PROMPT_TEMPLATE = """\
### 指示:
あなたは最高の動画を生成するプロンプトエンジニアです。
次の入力を元にして、動画生成プロンプトを生成してください。
動画生成には、AnimateDiffを利用します。
プロンプトは英語で出力し、次のようなキーワードを含めてください。
- best quality, masterpiece, dramatic lighting
- dynamic movement, full body, motion blur
説明は不要で、プロンプトのみを出力してください。
### 入力:
```{input}```
"""
# 動画生成の設定 --- (*3)
DREAMBOOTH_PATH = "models/DreamBooth_LoRA/leosamsHelloworldXL_filmGrain20.safetensors"
ROLA_MODE_PATH = "models/DreamBooth_LoRA/TUSUN.safetensors"
INFERENCE_CONFIG = "configs/inference/inference-v3.yaml"
MOTION_MODULE = "models/Motion_Module/v3_sd15_mm.ckpt"
STEPS = 25
# ディレクトリの設定 --- (*4)
DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_ANIMATE_DIFF = os.path.join(DIR_ROOT, "AnimateDiff")
FILE_YAML = os.path.join(DIR_ANIMATE_DIFF, "video_generation.yaml")
APP_PY = os.path.join(DIR_ANIMATE_DIFF, "app.py")
if not os.path.exists(APP_PY):
    print("プログラム直下にAnimateDiffをインストールしてください")
    quit()

def ollama_generate(prompt): # --- (*5)
    """Ollama APIを呼び出す"""
    data = {
        "model": OLLAMA_API_MODEL,
        "prompt": prompt,
        "temperature": 0.7,
        "stream": False,
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        OLLAMA_API_URL, headers=headers, json=data, timeout=60
    )
    response.raise_for_status()
    result = response.json()
    res = result.get("response", "")
    print("PROMPT:", res)
    if "</think>" in res: # --- (*6)
        res = res.split("</think>")[1]
    return res.strip()

def generate_prompt(input_text): # --- (*7)
    """入力テキストから動画生成プロンプトを生成する"""
    prompt = PROMPT_TEMPLATE.format(input=input_text)
    return ollama_generate(prompt)

def generate_video(text_list): # --- (*8)
    """動画を生成する"""
    # 動画生成用のプロンプトを生成 --- (*9)
    prompt_lsit = []
    for input_text in text_list:
        prompt = generate_prompt(input_text)
        prompt_lsit.append(prompt)
    # ランダムなシード値を生成
    seed = random.randint(1, 1000000)
    # YAMLファイルの生成 --- (*10)
    yaml_data = [{
        "dreambooth_path": DREAMBOOTH_PATH,
        "rola_mode_path": ROLA_MODE_PATH,
        "inference_config": INFERENCE_CONFIG,
        "motion_module": MOTION_MODULE,
        "steps": STEPS,
        "lora_alpha": 0.6,
        "prompt": prompt_lsit,
        "n_prompt": ["worst quality, low quality" for _ in prompt_lsit],
        "seed": [seed for _ in prompt_lsit],
        "guidance_scale": 7.5,
    }]
    with open(FILE_YAML, "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True)
    print(f"YAMLファイルを生成しました: {FILE_YAML}")
    # AnimateDiffの動画生成コマンドの実行 --- (*11)
    cmd = [
        "python", "-m", "scripts.animate",
        "--config", FILE_YAML,
    ]
    subprocess.call(cmd, cwd=DIR_ANIMATE_DIFF)
    print("動画の生成が完了しました。")

if __name__ == "__main__": # --- (*12)
    generate_video(["田園風景で田植えをする人が踊りまくる動画を作成してください。"])
