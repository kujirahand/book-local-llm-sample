"""RAG QAシステムの対話CLI"""
from rag_qa_system import *

print("RAGシステム（対話モード）を起動しています...")
try:
    # システムを初期化 --- (*1)
    initialize_system()
    print("★" * 60)
    print("📚 RAG QAシステムを開始します")
    # 繰り返し対話する --- (*2)
    while True:
        print("★" * 60)
        print("<<< 終了する場合は'q' を入力してください。")
        question = input(">>> ").strip()
        if question == "q": # --- (*3)
            break
        if not question:
            continue
        # 質問を処理して回答を生成 --- (*4)
        answer, docs = ask_question(question)
        if "</think>" in answer:
            answer = answer.split("</think>")[1].strip()
        print(f"<<< 😊 回答:\n{answer}")
        # 関連ドキュメントの表示 --- (*5)
        print("<<< 📖 参考ドキュメント:")
        for doc in docs:
            filename = doc.metadata.get("filename", "?")
            # ファイル内容から先頭部分を表示
            preview = doc.page_content[:30].replace("\n", "")
            print(f"- {filename}: {preview}...")

except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"[ERROR] {e}")
