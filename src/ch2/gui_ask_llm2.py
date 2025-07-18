import ollama
import TkEasyGUI as eg

# OllamaのAPIを使うための設定 --- (*1)
client = ollama.Client()
client_model = "llama3.2"  # モデル名を指定
default_prompt = "親しい友人に手紙を書きます。気の利いた出だしの挨拶を一つ考えてください。"

# カスタムレイアウトのウィンドウを作成 --- (*2)
layout = [
    [eg.Text("プロンプトを入力してください")],
    [eg.Multiline(default_prompt, key="-prompt-", size=(60, 3))],
    [eg.Button("実行")],
    [eg.Multiline("", key="-result-", size=(60, 10))],
]
window = eg.Window("LLMに質問する", layout)
# ウィンドウのイベントを処理する --- (*3)
while True:
    event, values = window.read() # イベントと値を取得 --- (*4)
    if event == eg.WIN_CLOSED:
        break
    if event == "実行":
        # 入力されたプロンプトを取得 --- (*5)
        prompt = values["-prompt-"]
        # LLMに質問して結果を表示 --- (*6)
        response = client.generate(model=client_model, prompt=prompt)
        result = response["response"]
        # 結果をウィンドウに表示 --- (*7)
        window["-result-"].update(result)
