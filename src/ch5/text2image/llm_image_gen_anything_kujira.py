"""Anything XLを利用して画像生成するプログラム"""
from diffusers import StableDiffusionXLPipeline

import llm_image_generator as lig

# プロンプトを設定 --- (*1)
PROMPT = """
「クジラ飛行机」が冒険しているイメージを描いて。
この人はいろいろなアプリを開発しています。
"""
# Anything XLのモデルパスを設定 --- (*2)
MODEL_PATH = "./models/AnythingXL_xl.safetensors"

# Anything XLのモデルを読み込む --- (*3)
pipe = StableDiffusionXLPipeline.from_single_file(
    MODEL_PATH,
    torch_dtype=lig.image_gen.DTYPE
).to(lig.image_gen.DEVICE)
lig.image_gen.pipe = pipe

# 画像を10枚生成 --- (*3)
for i in range(50):
    fname = f"./images/kujirahand_{i:02d}.png"
    print(f"画像生成: {fname}")
    lig.generate(fname, PROMPT)

