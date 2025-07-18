"""popular_anime.csvを元に対象テキストファイルを抽出する"""
import json
import os
import re

import config

def extract_files_from_corpus():
    """corpusディレクトリからテキストファイルを抽出する関数"""
    # 覚えたいアニメの一覧を読み込む --- (*1)
    with open(config.POP_ANIME_FILE, "r", encoding="shift_jis") as f:
        pop_anime = f.read().split("\n")
    # corpusディレクトリ内のテキストファイルを取得 --- (*2)
    file_list = []
    for root, _dirs, files in os.walk(config.DIR_CORPUS_TEXT):
        for file in files:
            if not file.endswith(".txt"):
                continue
            # テキストファイルを読み込む --- (*3)
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                text_raw = f.read()
                title = text_raw.split("\n")[0]
                text = re.sub(r'Category:\S+', '', text_raw)
                text = re.sub(r'\s+', ' ', text)
                # 短いテキストは無視する --- (*4)
                if len(text) < 300:
                    continue
                # サウンドトラックやアルバムは除外
                if "サウンドトラック" in title or "アルバム" in title or "シングル" in title:
                    continue
                if "アニメーター" in title or "シンガーソングライター" in text_raw or \
                    "アニメーション監督" in title:
                    continue
                # アニメのタイトルが含まれているかチェック ---- (*5)
                if any(anime in title for anime in pop_anime):
                    file_list.append(os.path.join(root, file))
                    print(f"- 対象ファイル: {title} ({os.path.join(root, file)})")
    print(f"対象のファイル数: {len(file_list)}")
    # 対象ファイルをJSON形式で保存 --- (*6)
    with open(config.CORPUS_TARGET_FILES, "w", encoding="utf-8") as f:
        json.dump(file_list, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    extract_files_from_corpus()
