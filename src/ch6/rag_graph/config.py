"""RAG設定ファイル"""
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
TEMPERATURE = 0.7
# 検索設定 --- (*4)
CHUNK_SIZE = 1000 # テキストを分割するチャンクのサイズ
CHUNK_OVERLAP = 200 # 分割時の重ね合わせのサイズ
RETRIEVAL_K = 20  # 検索で取得する関連文書数
# QAのためのテンプレート --- (*5)
QA_TEMPLATE = """\
### 指示:
以下のコンテキストに基づいて、情報をまとめて箇条書きで出力してください。
コンテキストに答えがない場合は「情報なし」と答えてください。
### コンテキスト:
{context}
### 中心テーマ:
{question}
"""
# Mermaid図生成のためのテンプレート --- (*6)
ZU_TEMPLATE = """\
### 指示:
以下のコンテキストに基づいて、Mermaid図を出力してください。
中心テーマは「{question}」です。
### コンテキスト:
```
{context}
```
### 出力例:

```mermaid
mindmap
    top((diagram))
        flowchart
            element
                node
                edge
```
"""
