"""RAGを使ったQAシステム"""
import glob
import os
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
import config

# グローバル変数
qa_chain = None
retriever = None

def initialize_system(): # --- (*1)
    """システム全体を初期化"""
    global qa_chain, retriever
    print("RAGシステムを初期化します...")
    # ドキュメントを読み込んで分割 --- (*2)
    documents = load_documents(config.DIR_TEXT_DATA)
    split_docs = split_documents(documents)
    # Embeddingモデルを設定 --- (*3)
    embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL)
    # Chromaのオブジェクトを取得 --- (*4)
    vector_store = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=config.DIR_VECTOR_DB
    )
    # Retrieverを作成 --- (*5)
    retriever = vector_store.as_retriever(
        search_type="similarity",  # 検索タイプを類似度検索に設定
        search_kwargs={"k": config.RETRIEVAL_K}  # 検索で取得する文書数
    )
    print("ベクトルDBに登録しました")
    # LLMを設定 --- (*6)
    llm = ChatOllama(
        model=config.LLM_MODEL,
        temperature=config.TEMPERATURE
    )
    def format_docs(docs): # ドキュメントの内容を整形
        return "\n\n".join(doc.page_content for doc in docs)
    # QAチェーン(処理の流れ)を作成 --- (*7)
    qa_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | ChatPromptTemplate.from_template(config.QA_TEMPLATE)
        | llm
        | StrOutputParser()
    )

def load_documents(target_dir: str) -> List[Document]: # --- (*8)
    """textディレクトリからMarkdownファイルを読み込む"""
    documents = []
    # 対象ファイルを検索 --- (*9)
    all_files = []
    for ext in config.TARGET_EXT:
        pattern = os.path.join(target_dir, f"*{ext}")
        all_files.extend(glob.glob(pattern))
    print(f"対象ファイル: {len(all_files)}個をDBに登録します")
    # 各ファイルを読み込む --- (*10)
    for file_path in all_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Documentオブジェクトを作成 --- (*11)
        doc = Document(
            page_content=content,
            metadata={
                "source": file_path,
                "filename": os.path.basename(file_path)
            }
        )
        documents.append(doc)
    return documents

def split_documents(documents: List[Document]) -> List[Document]: # --- (*12)
    """ドキュメントをチャンクに分割"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", "。", "．", " ", ""]
    )
    split_docs = text_splitter.split_documents(documents)
    print(f"チャンク分割: {len(split_docs)}個")
    return split_docs

def ask_question(question: str) -> tuple[str, List[Document]]: # --- (*13)
    """質問に対する回答を生成"""
    if not qa_chain or not retriever:
        raise ValueError("システムが初期化されていません")
    response = qa_chain.invoke(question) # 質問を処理して回答を生成
    docs = retriever.invoke(question) # 関連ドキュメントを取得
    return (response, docs)
