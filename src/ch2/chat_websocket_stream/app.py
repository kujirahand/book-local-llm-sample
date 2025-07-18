from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import ollama

# FlaskとSocket.IOの初期化
app = Flask(__name__)
app.config["SECRET_KEY"] = "C0HThSwr" # 暗号化キーを指定
socketio = SocketIO(app)
# Ollamaの初期化
llm_model = "llama3.2"
client = ollama.Client()

# Flaskへのアクセス
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Socket.IOのイベント --- (*1)
@socketio.on("user_message")
def handle_message(data):
    # ユーザーからのメッセージを取得 --- (*2)
    messages = data["messages"]
    print("[User]", messages)
    # LLMにメッセージを送信 --- (*3)
    response = client.chat(
        model=llm_model,
        messages=messages,
        stream=True)
    # ストリームモードで逐次受信 --- (*4)
    text = ""
    for chunk in response:
        # チャンクを受信したら、クライアントに送信 --- (*5)
        if "message" in chunk:
            subtext = chunk["message"]["content"]
            emit("bot_stream", {"chunk": subtext})
            text += subtext
    # ストリームの終了を通知 --- (*6)
    emit("bot_stream_end", {"text": text})
    print("[Bot]", text)

if __name__ == "__main__":
    socketio.run(app, debug=True)
