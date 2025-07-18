import ollama

client = ollama.Client()
client_model = "llama3.2"  # モデル名を指定
prompt = "親しい友人に愛情溢れた手紙を書いてください。"

# ストリームモードでLLMに質問 --- (*1)
stream = client.generate(
    model=client_model,
    stream=True,
    prompt=prompt)

# 順次結果を画面に表示 --- (*2)
for chunk in stream:
    subtext = chunk["response"]
    print(subtext, end="", flush=True)
print()  # 最後に改行

