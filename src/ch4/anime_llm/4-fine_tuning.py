"""Fine-Tuningの実行スクリプト"""
import json
import random
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments
import torch
from datasets import Dataset
if 'get_ipython' not in globals(): # Colab環境でない場合は
    from config import *

# Fine-Tuningに使うプロンプト --- (*1)
FINE_TUNING_PROMPT = """\
あなたはアニメの主人公やあらすじについて答えるアシスタントです。
以下の指示に沿って答えてください。

### 指示:
「{input}」について、{instruction}

### 応答:
{output}"""

# データセットの読み込み --- (*2)
with open(CORPUS_FILE_JSON, "r", encoding="utf-8") as f:
    corpus_data = json.load(f)["train"]
# データサイズを制限する場合
if MAX_DATASET_SIZE < len(corpus_data):
    random.shuffle(corpus_data) # データセットをシャッフル
    corpus_data = corpus_data[:MAX_DATASET_SIZE]
print(f"データセットのサイズ: {len(corpus_data)}件")

# モデルとトークナイザの読み込み --- (*3)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=None,
    load_in_4bit=True,
)
# PEFTのLoRAを適用 --- (*4)
target_modules = ["q_proj", "k_proj", "v_proj", "up_proj", "down_proj", "o_proj", "gate_proj"]
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Suggested 8, 16, 32, 64, 128
    target_modules=target_modules,
    lora_alpha = 16,
    lora_dropout = 0,
    bias="none",
    # unslothモデルの場合は勾配チェックポイントを有効化
    use_gradient_checkpointing = "unsloth" in MODEL_NAME,
    use_rslora = False,
    loftq_config = None,
)
# トークナイザーのEOSトークンを確認 --- (*5)
EOS_TOKEN = tokenizer.eos_token
print(f"EOS_TOKEN={EOS_TOKEN}")

# データセットの整形を適用 --- (*6)
def format_example(example):
    """テキストを整形する関数"""
    instruction = example["instruction"].strip()
    input_s = example["input"].strip()
    output_s = example["output"].strip()
    text = FINE_TUNING_PROMPT.format(instruction=instruction,
        input=input_s, output=output_s) + EOS_TOKEN
    return {"text": text}
corpus_data = list(map(format_example, corpus_data)) # 整形を適用
print(f"データセットのサイズ: {len(corpus_data)}")
dataset = Dataset.from_list(corpus_data) # Dataset形式に変換
print(dataset[:3]) # データセットの最初の3件を表示

# 学習のための設定 --- (*7)
training_args = TrainingArguments(
    output_dir=DIR_MODEL,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=5,
    max_steps=MAX_STEPS,
    learning_rate=2e-4,
    optim="adamw_8bit",
    logging_dir="./logs",
    weight_decay=0.01,
    lr_scheduler_type="linear",
    fp16 = not torch.cuda.is_bf16_supported(),
    bf16 = torch.cuda.is_bf16_supported(),
    report_to="none",  # W&Bなどの外部ログを無効化
)
# 学習を実行 --- (*8)
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,  # 学習に使うデータセットを指定
    dataset_text_field="text",  # データセットのフィールド名を指定
    dataset_num_proc = 2,
    packing = False,  # Packingを無効化
    args=training_args,
)
trainer.train()

# 学習したモデルを保存 --- (*9)
model.save_pretrained(DIR_MODEL)
tokenizer.save_pretrained(DIR_MODEL)
