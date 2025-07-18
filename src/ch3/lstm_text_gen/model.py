import torch.nn as nn

# LSTMモデル定義
class TokenLSTM(nn.Module):
    """テキスト生成のためのLSTMモデル"""
    def __init__(self, vocab_size, hidden_size=256): # --- (*1)
        """語彙数と隠れ層のサイズを指定して初期化する"""
        super().__init__()
        # 語彙数と隠れ層のサイズを指定して初期化する
        self.embed = nn.Embedding(vocab_size, hidden_size)
        # LSTM層を定義する
        self.lstm = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        # 出力層を定義する
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None): # --- (*2)
        """処理の流れを定義する"""
        x = self.embed(x)
        out, hidden = self.lstm(x, hidden)
        out = self.fc(out)
        return out, hidden
