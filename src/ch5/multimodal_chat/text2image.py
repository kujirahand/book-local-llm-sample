"""画像生成モジュール"""
import torch
from diffusers import StableDiffusionPipeline
from config import *
import text2text
from chat_template import *

# グローバル変数としてStableDiffusionPipelineを保持
SD_PIPE = None

# 画像生成するための関数 --- (*1)
def text2image(
    prompt, image_path, negative_prompt=NEGATIVE_PROMPT,
    num_inference_steps=30, guidance_scale=7.5):
    """画像を生成する関数"""
    global SD_PIPE
    if SD_PIPE is None:
        # デバイスの特定処理(CPU/GPU/MPS) --- (*2)
        device = "cpu"  # デフォルトはCPU
        dtype = torch.float32
        if torch.cuda.is_available():
            device = "cuda"  # GPUが利用可能ならCUDAを使用
            # fp16が使えるか判定
            supports_fp16 = False
            if not torch.cuda.is_available():
                maj, _ = torch.cuda.get_device_capability()
                supports_fp16 = maj >= 7  # RTX 20xx以降
            if supports_fp16:
                dtype = torch.float16
        elif torch.backends.mps.is_available():
            device = "mps" # Applaシリコンで利用可能ならMPSを使用
        print(f"Using device: {device}, dtype: {dtype}")
        # 画像生成モデルを読み込む --- (*3)
        SD_PIPE = StableDiffusionPipeline.from_pretrained(
            IMAGE_GEN_MODEL,
            torch_dtype=dtype,
        ).to(device)
    # 画像生成の実行 --- (*4)
    with torch.no_grad():
        img = SD_PIPE(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            allow_pickle=False,
        ).images[0]
        img.save(image_path)

# 画像生成プロンプトを利用して画像を生成する関数 --- (*5)
def text2image_easy(prompt, image_path, history=[]):
    """簡易版の画像生成関数"""
    # 画像生成のためのプロンプトを作成
    prompt_ex = TEMPLATE_IMAGE_GEN_PROMPT.format(input=prompt)
    messages = history.copy()
    messages.append({"role": "user", "content": prompt_ex})
    image_prompt = text2text.text2text(messages, show_output=False)
    print_title(f"<<< 次の画像生成プロンプトで生成します")
    print("<<<", image_prompt)
    # 画像を生成
    text2image(image_prompt, image_path)

if __name__ == "__main__":  # --- (*6)
    text2image_easy(
        "子供が公園で遊んでいる様子",
        "images/text2image_test.png")
