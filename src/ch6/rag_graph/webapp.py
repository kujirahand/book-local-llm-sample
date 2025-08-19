"""RAG作図システムのWebアプリ"""
import re
from flask import Flask, request, render_template, jsonify
from langchain_ollama import ChatOllama
from rag_qa_system import ask_question, initialize_system, config

# Flaskアプリを生成 --- (*1)
app = Flask(__name__)

@app.route('/')
def index():
    """トップページ"""
    return render_template("frame.html") # --- (*2)

# APIの `/ask` にアクセスがあったときの処理 --- (*3)
@app.route('/ask', methods=['POST'])
def ask():
    """質問API"""
    try:
        # フォームから質問を取得 --- (*4)
        data = request.get_json()
        question = data.get('question', '').strip()
        if not question:
            return jsonify({'error': '質問が入力されていません'})

        # 質問を処理して回答を生成 --- (*5)
        answer, _ = ask_question(question)
        # </think>タグがある場合は除去
        if "</think>" in answer:
            answer = answer.split("</think>")[1].strip()

        # 結果を元にしてマーメイドズを出力してもらう --- (*6)
        prompt = config.ZU_TEMPLATE.format(
            question=question,
            context=answer)
        print("Mermaid図生成のためのプロンプト:", prompt)
        llm = ChatOllama(model=config.LLM_MODEL)
        a = llm.invoke(prompt)
        answer2 = a.content
        if "</think>" in answer2:
            answer2 = answer2.split("</think>")[1].strip()
        # 結果からMermaidの部分を抽出 --- (*7)
        print("Mermaid図生成の結果:", answer2)
        m = re.search(r'```mermaid(.*?)```', answer2, re.DOTALL)
        mermaid = m.group(1).strip() if m else ""
        # 結果を返す --- (*8)
        return jsonify({
            'answer': answer,
            'mermaid': mermaid
        })        
    except Exception as e:
        return jsonify({'error': str(e)})

def main():
    """メイン関数"""
    print("RAG作図（Webアプリ）を起動しています...")
    # システムを初期化
    initialize_system()
    print("★" * 60)
    print("📚 Webアプリを開始します")
    print("http://localhost:8080 でアクセスしてください")
    print("★" * 60)
    # Flaskアプリを起動 --- (*9)
    app.run(debug=True, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
