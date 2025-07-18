import ollama

# Ollamaを呼び出す
response = ollama.generate(
    model="llama3.2",
    prompt="猫の名前を1つだけ考えてください。",
    options={"temperature": 0.7}
)
# 返ってきた応答の内容を表示
print(response['response'])
