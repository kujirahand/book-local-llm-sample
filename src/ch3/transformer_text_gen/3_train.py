from datetime import datetime
import torch
from torch.utils.data import Dataset, DataLoader
from config import *
import utils
from model_transformer import *

# トークンを読み出す --- (*1)
utils.id2token = utils.load_json(FILE_ID2TOKEN)
utils.token2id = utils.load_json(FILE_TOKEN2ID)
vocab_size = len(utils.token2id)
ids = utils.load_json(FILE_IDS)

# データセットを定義 --- (*2)
class TokenDataset(Dataset):
    """トークンデータセット"""
    def __init__(self, data):
        """初期化"""
        items = []
        # データ長をSEQ_LENと揃える --- (*3)
        for tokens in data:
            if len(tokens) < SEQ_LEN:
                # トークン数がSEQ_LENより少ない場合はパディング
                tokens = utils.pad_sequence(tokens, SEQ_LEN)
            # トークン数がSEQ_LENより多い場合は切り詰める
            tokens = tokens[:SEQ_LEN]
            items.append(torch.tensor(tokens))
        self.data = items

    def __len__(self):
        """データセットの長さを返す"""
        return len(self.data)

    def __getitem__(self, idx):
        """データセットの要素を返す"""
        tokens = self.data[idx] # --- (*4)
        x = tokens[:-1] # 入力データは先頭から
        y = tokens[1:]  # 出力データは1つずらしたもの
        return x, y

def check_xy(x, y): # --- (*5)
    """xとyのトークンを表示する"""
    text_x = utils.ids_to_text(x.tolist(), skip_special=False, split_mark="|")
    text_y = utils.ids_to_text(y.tolist(), skip_special=False, split_mark="|")
    print(f"  x: {text_x.replace('<PAD>','')}")
    print(f"  y: {text_y.replace('<PAD>','')}")

# 学習準備 --- (*6)
model = TransformerModel(vocab_size, EMBED_DIM, NUM_HEADS, NUM_LAYERS).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=OPTIMIZER_LR)
criterion = nn.CrossEntropyLoss(ignore_index=PAD)
# データセットの読み込み --- (*7)
dataset = TokenDataset(ids)
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# 学習ループ --- (*8)
loss_history = []
loss_val = 0
for epoch in range(EPOCHS):
    # 学習データを読み出して学習 --- (*9)
    data_size = len(loader)
    for i, (x, y) in enumerate(loader):
        x, y = x.to(device), y.to(device)
        logits = model(x) # モデルに入力
        loss = criterion(logits.view(-1, vocab_size), y.view(-1)) # 損失計算
        optimizer.zero_grad() # 勾配を初期化
        loss.backward() # 勾配計算
        optimizer.step() # 重み更新
        loss_val = loss.item() # 損失値を取得
        if i % 50 == 0:
            per = int(i / data_size * 100)
            print(f"  - {i:3}/{data_size}({per:2}%), Loss: {loss_val:.4f}")
            check_xy(x[0], y[0]) # --- (*10)
    # 学習データの損失値を履歴に記録 --- (*11)
    history = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "epoch": epoch + 1,
        "loss": loss_val,
        "saved": False
    }
    # 学習経過の調査のために定期的にモデルを保存 --- (*12)
    if epoch % 10 == 9:
        history["saved"] = True
        torch.save(model.state_dict(), FILE_MODEL + f"_{epoch + 1}.pt")
    loss_history.append(history)
    print(f"* Epoch: {epoch + 1:03}/{EPOCHS}, Loss: {loss_val:.4f}")
    if loss_val < EARLY_STOPPING_LOSS:
        print(f"Early stopping at epoch {epoch + 1}, Loss:{loss_val:.4f}")
        break # --- (*13)

# モデルの保存 --- (*14)
torch.save(model.state_dict(), FILE_MODEL)
save_json(loss_history, FILE_MODEL + "_history.json")
print("モデルを保存しました")
