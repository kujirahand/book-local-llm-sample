import ollama

# OllamaのAPIを使うための設定 --- (*1)
client = ollama.Client()
client_model = "phi4" # モデル名を指定

# Ollamaで手軽にphi4を使うための関数を定義 --- (*2)
def generate(prompt, temperature=0.7):
    response = client.generate(
        model=client_model,
        prompt=prompt,
        options={"temperature": temperature}
    )
    return response['response']

if __name__ == "__main__":
    # プロンプトを指定 --- (*3)
    prompt = """
        次の手順で最強にユニークな猫の名前を考えてください。
        1. 10個の候補を列挙
        2. 名前のユニーク度を10段階で評価
        3.最もユニークなものを一つ選んでください。
    """
    print(generate(prompt)) # 実行 --- (*4)
