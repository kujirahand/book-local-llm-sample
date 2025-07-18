from ollama import Client

# 接続したいPCのIPアドレスを指定してクライアントを作成(★★書換えが必要)
client = Client(host="http://192.168.1.28:11434")

# モデルとプロンプトを指定
model = "llama3.2"
prompt = "猫の名前を3つ考えてください。"

# Ollamaにアクセスして答えを得る
response = client.generate(model=model, prompt=prompt)
print(response["response"])
