import ollama
import TkEasyGUI as eg

# OllamaのAPIを使うための設定 --- (*1)
client = ollama.Client()
# client_model = "llama3.2"  # モデル名を指定
client_model = "phi4"  # モデル名を指定
default_prompt = "親しい友人に手紙を書きます。気の利いた出だしの挨拶を一つ考えてください。"

# カスタムレイアウトのウィンドウを作成 --- (*2)
layout = [
    [eg.Text("プロンプトを入力してください")],
    [eg.Multiline(default_prompt, key="-prompt-", size=(60, 3))],
    [eg.Button("実行")],
    [eg.Multiline("", key="-result-", size=(60, 10))],
]
window = eg.Window("LLMに質問する", layout)

# マルチスレッドでLLMに質問する関数を定義 --- (*3)
def thread_llm(prompt):
    # LLMに質問して結果を表示 --- (*4)
    response = client.generate(model=client_model, prompt=prompt)
    result = response["response"]
    # イベントをポストしてウィンドウを更新 --- (*5)
    window.post_event("実行完了", {"result": result})

# ウィンドウのイベントを処理する --- (*6)
while True:
    event, values = window.read() # イベントと値を取得
    if event == eg.WIN_CLOSED:
        break
    if event == "実行":
        # 入力されたプロンプトを取得 --- (*7)
        prompt = values["-prompt-"]
        # ボタンを押せないように変更 --- (*8)
        window["実行"].update(disabled=True)
        # LLMに質問して結果を表示 --- (*9)
        window.start_thread(thread_llm, prompt=prompt)
    elif event == "実行完了":
        # 結果を表示 --- (*10)
        result = values["result"]
        window["-result-"].update(result)
        # ボタンを押せるように変更 --- (*11)
        window["実行"].update(disabled=False)
