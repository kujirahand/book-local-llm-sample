"""Fine-Tuningの設定"""
# モデルとデータセットの指定 --- (*1)
MODEL_NAME = "unsloth/mistral-7b-bnb-4bit"
DATASET_NAME = "shi3z/alpaca_cleaned_ja_json"
# データセットのサイズやモデルを制限するための変数 --- (*2)
MAX_DATASET_SIZE = 500
MAX_SEQ_LENGTH = 2048
MAX_STEPS = 100 # 学習のステップ数 (テストのときは1) --- (*3)
# モデルの保存先ディレクトリ
MODEL_SAVE_DIR="./rongofu_llm"
