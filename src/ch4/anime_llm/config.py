"""プロジェクトの設定"""
import os
# ディレクトリの設定 --- (*1)
if 'get_ipython' not in globals(): # Colab環境でない場合は
  DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
else:
  DIR_ROOT = "/content/"
DIR_CORPUS = os.path.join(DIR_ROOT, "corpus")
DIR_CORPUS_TEXT = os.path.join(DIR_CORPUS, "text")
DIR_MODEL = os.path.join(DIR_ROOT, "model")
# ファイルパスの指定 --- (*2)
WIKI_FILE = os.path.join(DIR_CORPUS, "jawiki-20250520-pages-articles-multistream.xml")
CORPUS_FILE = os.path.join(DIR_CORPUS, "anime_corpus.txt")
POP_ANIME_FILE = os.path.join(DIR_ROOT, "popular_anime.csv")
CORPUS_FILE_JSON = os.path.join(DIR_CORPUS, "anime_corpus.json")
CORPUS_TARGET_FILES = os.path.join(DIR_CORPUS, "anime_corpus_target_files.json")
# パラメータの指定 --- (*3)
MODEL_NAME = "unsloth/Meta-Llama-3.1-8B-bnb-4bit"
OLLAMA_TIMEOUT = 30  # Ollamaのタイムアウト時間（秒）
MAX_SEQ_LENGTH = 2048
MAX_STEPS = 500 # 学習の最大ステップ数
MAX_DATASET_SIZE = 3000 # データセットの最大サイズ
# ディレクトリの作成 --- (*4)
os.makedirs(DIR_CORPUS_TEXT, exist_ok=True)
os.makedirs(DIR_MODEL, exist_ok=True)
