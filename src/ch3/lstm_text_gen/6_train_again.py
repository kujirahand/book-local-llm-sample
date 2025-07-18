import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from config import *
from utils import *
from model import TokenLSTM

# データ読み込み
token2id = load_json(FILE_TOKEN2ID)
id2token = load_json(FILE_ID2TOKEN)
ids = load_json(FILE_IDS)
print("データを読み込みました。")
# トークン数を取得
vocab_size = len(token2id)
print("トークン数:", vocab_size)

vocab_size = len(token2id)
model = TokenLSTM(vocab_size)
model.load_state_dict(torch.load(FILE_MODEL))

# データセット定義
class TokenDataset(Dataset):
    def __init__(self, data, seq_len=50):
        self.data = data
        self.seq_len = seq_len

    def __len__(self):
        return len(self.data) - self.seq_len

    def __getitem__(self, idx):
        return (
            torch.tensor(self.data[idx:idx+self.seq_len]),
            torch.tensor(self.data[idx+1:idx+self.seq_len+1]),
        )

dataset = TokenDataset(ids)
data_loader = DataLoader(dataset, batch_size=64, shuffle=True)

optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
criterion = nn.CrossEntropyLoss()

# 学習ループ
print("モデルの学習を開始します。")
for epoch in range(3):
    size = len(data_loader)
    n = 0
    for i, (x, y) in enumerate(data_loader):
        per = int(i / size * 100)
        if n < per:
            print(f" - 学習中... {i:4} / {size:4} ({per:3}%)")
            n = per + 10
        optimizer.zero_grad()
        out, _ = model(x)
        loss = criterion(out.view(-1, vocab_size), y.view(-1))
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# モデル保存
torch.save(model.state_dict(), FILE_MODEL)
print("モデルを保存しました。")
