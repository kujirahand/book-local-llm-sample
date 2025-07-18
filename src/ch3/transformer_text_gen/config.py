"""プロジェクト全体の設定をまとめたもの"""
import os
# コーパスのソースを指定
DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_CORPUS_SOURCE = os.path.abspath(os.path.join(DIR_ROOT, "..", "kinokobooks"))
# コーパス --- (*1)
DIR_CORPUS = os.path.join(DIR_ROOT, "corpus")
FILE_CORPUS = os.path.join(DIR_CORPUS, "corpus.txt")
CORPUS_MAX_LINES = 20000
# モデル --- (*2)
DIR_MODEL = os.path.join(DIR_ROOT, "model")
FILE_IDS = os.path.join(DIR_MODEL, "ids.json")
FILE_TOKEN2ID = os.path.join(DIR_MODEL, "token2id.json")
FILE_ID2TOKEN = os.path.join(DIR_MODEL, "id2token.json")
FILE_MODEL = os.path.join(DIR_MODEL, "model_transformer.pth")
# ハイパーパラメータ --- (*3)
EMBED_DIM = 512
NUM_HEADS = 8
NUM_LAYERS = 4
SEQ_LEN = 50
BATCH_SIZE = 64
OPTIMIZER_LR = 1e-5
EPOCHS = 500
EARLY_STOPPING_LOSS = 1.8

