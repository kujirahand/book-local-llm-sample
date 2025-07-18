"""Anything XLを利用して画像生成するプログラム"""
# diffusersのStableDiffusionXLPipelineをインポート --- (*1)
from diffusers import StableDiffusionXLPipeline
import llm_image_generator as lig

# プロンプトを設定 --- (*2)
PROMPT = "南国の海辺を歩くモナリザを描いて。"
# Anything XLのモデルパスを設定 --- (*3)
MODEL_PATH = "./models/AnythingXL_xl.safetensors"

# Anything XLのモデルを読み込む --- (*4)
pipe = StableDiffusionXLPipeline.from_single_file(
    MODEL_PATH,
    torch_dtype=lig.image_gen.DTYPE
).to(lig.image_gen.DEVICE)
lig.image_gen.pipe = pipe

# 画像を10枚生成 --- (*5)
for i in range(10):
    fname = f"./images/anything_image_{i:02d}.png"
    print(f"画像生成: {fname}")
    lig.generate(fname, PROMPT)

