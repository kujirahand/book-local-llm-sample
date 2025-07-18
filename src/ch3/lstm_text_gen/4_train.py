import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from config import *
from utils import *
from model import TokenLSTM

# 作成するモデルを保存するフォルダを作成
os.makedirs(DIR_MODEL, exist_ok=True)

# 入力データ読み込み --- (*1)
token2id = load_json(FILE_TOKEN2ID)
id2token = load_json(FILE_ID2TOKEN)
ids = load_json(FILE_IDS)
print("データを読み込みました。")
# トークン数を取得 --- (*2)
vocab_size = len(token2id)
print("トークン数:", vocab_size)

# データセット定義 --- (*3)
class TokenDataset(Dataset):
    def __init__(self, data, seq_len=50):
        """データセットを初期化する"""
        self.data = data
        self.seq_len = seq_len

    def __len__(self):
        """データセットのサイズを返す"""
        return len(self.data) - self.seq_len

    def __getitem__(self, idx):
        """データセットの要素を取得する"""
        return (
            torch.tensor(self.data[idx:idx+self.seq_len]),
            torch.tensor(self.data[idx+1:idx+self.seq_len+1]),
        )

# データローダー定義 --- (*4)
dataset = TokenDataset(ids)
data_loader = DataLoader(dataset, batch_size=64, shuffle=True)

# モデルのインスタンスを生成 --- (*5)
model = TokenLSTM(vocab_size)

# オプティマイザーと損失関数を定義 --- (*6)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# 学習ループ --- (*7)
print("モデルの学習を開始します。")
for epoch in range(20):
    size = len(data_loader)
    # データを読み出して学習する --- (*8)
    for i, (x, y) in enumerate(data_loader):
        # 学習経過を表示 --- (*9)
        if i % 100 == 0:
            per = int(i / size * 100)
            print(f" - 学習中... {i} / {size} ({per}%)")
            n = per + 10
        # 学習を実行 --- (*10)
        optimizer.zero_grad()
        out, _ = model(x)
        loss = criterion(out.view(-1, vocab_size), y.view(-1))
        loss.backward()
        optimizer.step()
    # 損失を確認して処理を中断する --- (*11)
    if loss < 1.8:
        print(f"Epoch {epoch+1}回目で、損失が1.8を下回ったので学習を終了します。")
        break
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# モデル保存 --- (*12)
torch.save(model.state_dict(), FILE_MODEL)
print("モデルを保存しました。")
