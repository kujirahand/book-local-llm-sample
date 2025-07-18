"""Fine-Tunigを行う"""
from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments

if 'get_ipython' not in globals(): # Colab環境でない場合は
    from config import *
    from dataset_formatter import dataset

# モデルとトークナイザーのロード --- (*1)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=None,
    load_in_4bit=True,
)

# PEFT(LoRAの適用) --- (*2)
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    bias="none",
)

# データセットをトークナイズ ---- (*3)
def dataset_tokenize(example):
    """データセットのテキストをトークナイズする関数"""
    print("tokenize:", example["text"])
    return tokenizer(
        example["text"],
        padding="max_length",
        truncation=True,
        max_length=MAX_SEQ_LENGTH,
    )
tokenized_dataset = dataset.map(dataset_tokenize,
    remove_columns=dataset.column_names)

# Fine-Tuningを実行する --- (*4)
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=tokenized_dataset,
    args=TrainingArguments(
        output_dir=MODEL_SAVE_DIR,
        max_steps=MAX_STEPS, # 最大ステップ数 --- (*4-1)
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        learning_rate=2e-4,
        logging_steps=1,
        optim="adamw_8bit", # 8bit AdamWを使用 --- (*4-2)
        fp16 = not torch.cuda.is_bf16_supported(), # --- (*4-3)
        bf16 = torch.cuda.is_bf16_supported(),
        report_to="none" # ログを出力しない --- (*4-4)
    ),
)
trainer.train()

# Fine-Tuningの結果を保存 --- (*5)
model.save_pretrained(MODEL_SAVE_DIR)
