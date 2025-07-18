"""チャットのテンプレートを定義したもの"""
# タスクを選択するためのテンプレート --- (*1)
TEMPLATE_SELECT_TASK = """\
### 指示:
ユーザーの入力を元にそのタスクを選択してください。
1つ選んで選択肢だけを出力してください。
### 選択肢:
- Text-to-Image
- Text-to-Text
### 入力:
```{input}```
### 出力例:
Text-to-Text
"""

# 画像を説明するプロンプト --- (*2)
TEMPLATE_IMAGE_PROMPT = "次の画像について説明してください。"

# 画像生成プロンプトを生成するプロンプト --- (*3)
TEMPLATE_IMAGE_GEN_PROMPT = """\
### 指示:
ユーザーの入力を元に画像生成のプロンプトを英語で生成してください。
出力は画像生成のプロンプトだけを出力してください。
### 備考:
画像生成には、Stable Diffusionを使用します。
出力に`masterpiece`や`best quality`を加えてください。
### 入力:
```{input}```
"""

# 画像生成で使うネガティブプロンプト --- (*4)
NEGATIVE_PROMPT = """\
low quality, blurry, bad anatomy, worst quality, low quality,
normal quality, jpeg artifacts, signature, watermark
"""
