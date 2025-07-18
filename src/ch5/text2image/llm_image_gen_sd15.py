"""モデルを変更して画像生成するプログラム"""
import llm_image_generator as lig

# モデル名を指定 --- (*1)
MODEL = "runwayml/stable-diffusion-v1-5"
# プロンプトを設定 --- (*2)
PROMPT = "南国の海辺を歩くモナリザを描いて。"
lig.set_image_model(MODEL)
# 画像を10枚生成 --- (*3)
for i in range(10):
    fname = f"./images/sd15_image_{i:02d}.png"
    print(f"画像生成: {fname}")
    lig.generate(fname, PROMPT)

