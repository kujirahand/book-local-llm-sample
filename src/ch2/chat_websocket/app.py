from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import ollama

# FlaskとSocket.IOの初期化 --- (*1)
app = Flask(__name__)
app.config["SECRET_KEY"] = "C0HThSwr" # 暗号化キーを指定
socketio = SocketIO(app)
# Ollamaの初期化
llm_model = "llama3.2"
client = ollama.Client()

# Flaskへのアクセス --- (*2)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Socket.IOのイベント --- (*3)
@socketio.on("user_message")
def handle_message(data):
    # ユーザーからのメッセージを取得 --- (*4)
    message = data["message"]
    print("[User]", message)
    # LLMにメッセージを送信 --- (*5)
    response = client.generate(
        model=llm_model,
        prompt=message)
    if "response" in response:
        response = response["response"]
        print("[Ollama]", response)
        # レスポンスをクライアントに送信 --- (*6)
        emit("bot_response", {"message": response})

if __name__ == "__main__":
    socketio.run(app, debug=True)
