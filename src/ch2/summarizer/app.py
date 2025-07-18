from flask import Flask, request, render_template
import ollama

# Flaskアプリケーションの作成 --- (*1)
app = Flask(__name__)
# Ollamaクライアントの作成 --- (*2)
client = ollama.Client()
client_model = "llama3.2"  # 使用するモデルの指定

# ルートURLにアクセスしたときの処理 --- (*3)
@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    original_text = ""
    # POSTリクエストが送信されたときの処理 --- (*4)
    if request.method == 'POST':
        # フォームから送信されたテキストを取得 --- (*5)
        original_text = request.form['text']
        # Ollamaにアクセスして要約を生成 --- (*6)
        prompt = f"次の文章を1文で要約してください:\n\n{original_text}"
        response = client.generate(model=client_model, prompt=prompt)
        summary = response['response']
    # HTMLテンプレートをレンダリング --- (*7)
    return render_template('index.html', summary=summary, text=original_text)

if __name__ == '__main__':
    app.run(debug=True)
