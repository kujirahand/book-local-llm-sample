"""RAG QA設定ファイル"""
import os
# パスの指定 --- (*1)
DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_TEXT_DATA = os.path.join(DIR_ROOT, "text")
DIR_VECTOR_DB = os.path.join(DIR_ROOT, "chroma_db")
TARGET_EXT = [".md", ".txt"] # 対象ファイルの拡張子
# OllamaのEmbeddingのモデル設定 --- (*2)
EMBEDDING_MODEL = "granite-embedding:278m"
# LLMモデル設定 --- (*3)
LLM_MODEL = "qwen3:8b"
TEMPERATURE = 0.4
# 検索設定 --- (*4)
CHUNK_SIZE = 1000 # テキストを分割するチャンクのサイズ
CHUNK_OVERLAP = 200 # 分割時の重ね合わせのサイズ
RETRIEVAL_K = 3  # 検索で取得する関連文書数
# QAのためのテンプレート --- (*5)
QA_TEMPLATE = """\
### 指示:
以下のコンテキストに基づいて質問に簡潔に答えてください。
コンテキストに答えがない場合は「提供されたコンテキストでは答えられません」と答えてください。
### コンテキスト:
{context}
### 質問:
{question}
"""
