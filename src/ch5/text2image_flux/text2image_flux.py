"""FLUX.1で画像生成するプログラム"""
import os
import torch
from diffusers import FluxPipeline

# モデルの指定 --- (*1)
IMAGE_GEN_MODEL = "black-forest-labs/FLUX.1-dev"

# デバイスの特定(CPU/GPU/MPS) --- (*2)
def supports_fp16():
    """fp16が使えるか判定する関数"""
    if not torch.cuda.is_available():
        return False
    major, _minor = torch.cuda.get_device_capability() 
    return major >= 7  # Volta以降ならOK（例: RTX 20xx以降）

DEVICE = "cpu"  # デフォルトはCPU
DTYPE = torch.float32
if torch.cuda.is_available():
    DEVICE = "cuda"  # GPUが利用可能ならCUDAを使用
    if supports_fp16():
        DTYPE = torch.float16
elif torch.backends.mps.is_available():
    DEVICE = "mps"
print(f"Using device: {DEVICE}, dtype: {DTYPE}")

# 画像生成AIのためにパイプラインの読み込み --- (*3)
sd_pipe = FluxPipeline.from_pretrained(
    IMAGE_GEN_MODEL,
    torch_dtype=DTYPE,
).to(DEVICE) # Hugging Faceからモデルを読み込む

def text2image(prompt, image_path, negative_prompt="",
    num_inference_steps=50, guidance_scale=7.5): # --- (*4)
    """画像を生成する関数"""
    with torch.no_grad(): # --- (*5)
        img = sd_pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
        ).images[0]
        img.save(image_path)

if __name__ == "__main__":
    os.makedirs("images", exist_ok=True)  # 保存先ディレクトリの作成
    # 画像を生成 --- (*6)
    prompt = ("A beautiful giraf in the city."
        " anime style, best quality, high resolution")
    test_image_path = "images/flux_image01.png"
    text2image(prompt, test_image_path)
    print(f"保存しました: {test_image_path}")
    