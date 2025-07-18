"""画像生成するプログラム"""
import os
import sys
import torch
from diffusers import StableDiffusionPipeline

# モデル名を指定 --- (*1)
MODEL = "hakurei/waifu-diffusion"
# プロンプトとネガティブプロンプトを設定 --- (*2)
PROMPT = """\
a refreshing and cute anime girl sitting on a bench 
under fully bloomed cherry blossom trees, petals falling gently,
spring atmosphere, soft lighting, wearing a light dress,
masterpiece, best quality, highly detailed, vibrant colors
"""
NEGATIVE_PROMPT = """\
low quality, blurry, bad anatomy, worst quality, low quality,
normal quality, jpeg artifacts, signature, watermark
"""
# 保存フォルダを指定 --- (*3)
DIR_IMAGES = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(DIR_IMAGES, exist_ok=True)
# パラメータの設定 --- (*4)
DEVICE = "cpu"
DTYPE = torch.float32
if torch.cuda.is_available():
    DEVICE = "cuda"
    if torch.cuda.is_bf16_supported():
        DTYPE = torch.bfloat16
elif torch.backends.mps.is_available():
    DEVICE = "mps" # macOSの場合はMetal Performance Shadersを使用
print(f"Using device: {DEVICE}, dtype: {DTYPE}")
pipe = None

def load_model(model_name=MODEL):
    """モデルを読み込む関数"""
    # モデルを読む --- (*5)
    pipe = StableDiffusionPipeline.from_pretrained(
        model_name,
        torch_dtype=DTYPE,
        # safety_checker=None  # セーフティチェッカー --- (*6)
    ).to(DEVICE)
    pipe.enable_attention_slicing() # メモリ使用量を削減する --- (*7)
    return pipe

def generate_image(file_path, prompt, negative=NEGATIVE_PROMPT):
    """画像を生成する関数"""
    global pipe
    if pipe is None: # 初回のみモデルを読み込む
        pipe = load_model()
    # 画像を生成 --- (*8)
    image = pipe(
        prompt,
        negative_prompt=negative,
        num_inference_steps=40,
        guidance_scale=7.5,
    ).images[0]
    image.save(file_path) # 画像を保存 --- (*9)

if __name__ == "__main__":
    # 連続で画像を生成 --- (*10)
    for i in range(10):
        fname = os.path.join(DIR_IMAGES, f"girl_{i:02d}.png")
        generate_image(fname, PROMPT, NEGATIVE_PROMPT)
        print(f"Saved image to {fname}")
