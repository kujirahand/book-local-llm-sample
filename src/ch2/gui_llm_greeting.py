import ollama
import TkEasyGUI as eg

# LLMに与えるプロンプトを指定 --- (*1)
default_prompt = """
親しい友人に手紙を書きます。
気の利いた出だしの挨拶を一つだけ考えてください。
簡潔で、心に残るものをお願いします。
"""
client_model = "phi4"  # モデル名を指定
client = ollama.Client()

# プロンプトを提示 --- (*2)
prompt = eg.popup_memo(
    default_prompt.strip(),
    header="以下のプロンプトで挨拶文を作成します:",
    title="LLMに与えるプロンプト")
if prompt is None:
    quit()

# 繰り返しLLMに挨拶文を考えてもらう --- (*3)
while True:
    # LLMに質問して結果を表示 --- (*4)
    response = client.generate(model=client_model, prompt=prompt)
    result = response["response"]
    # メモに答えをメモダイアログに表示 --- (*5)
    r = eg.popup_memo(
        result,
        header="続けて挨拶文を生成する場合[OK]を押してください。",
        title="LLMによる挨拶文")
    if r is None:
        break
