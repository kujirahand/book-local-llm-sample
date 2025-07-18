"""Fine-TuninngしたモデルをGGUUF形式に変換する"""
import os
from unsloth import FastLanguageModel
if 'get_ipython' not in globals(): # Colab環境でない場合
    from config import *

# モデルの保存先ディレクトリ --- (*1)
DIR_MERGED_MODEL = os.path.join(DIR_ROOT, "model_merged")

# モデルを読み込む（LoRAを含む） --- (*2)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = DIR_MODEL, # 保存したフォルダ
    max_seq_length = MAX_SEQ_LENGTH,
    dtype = None,
    load_in_4bit = True,
)

# 推論モードに設定 --- (*3)
model.eval()
FastLanguageModel.for_inference(model)

# GGUF形式で保存（LoRAをマージして保存） --- (*4)
model.save_pretrained_gguf(
    DIR_MERGED_MODEL,  # 出力フォルダ名
    tokenizer = tokenizer,
    quantization_method = "q4_k_m",  # 量子化方法（例: f16, q4_0, q4_k_m など）
)
print(f"GGUF形式のモデルを保存しました: {DIR_MERGED_MODEL}")

