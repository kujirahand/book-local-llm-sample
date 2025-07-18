import requests

# OllamaのAPIエンドポイント --- (*1)
API_ENDPOINT = "http://localhost:11434"

# /api/generateを呼び出す関数を定義 --- (*2)
def generate(prompt, model="llama3.2"):
    # URLを指定
    url = API_ENDPOINT + "/api/generate"
    # リクエストボディ --- (*3)
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7
    }
    # HTTP POSTでAPIを呼び出す --- (*4)
    response = requests.post(url, json=payload)
    # 結果を確認 --- (*5)
    if response.status_code == 200:
        data = response.json()
        return data["response"]
    else:
        raise Exception(
            f"API呼び出しに失敗:{response.status_code})" + \
            response.text)

if __name__ == "__main__": 
    # 猫の名前を考えるよう指示 ---- (*6)
    print(generate("猫の名前を1つだけ考えてください。"))
