"""Wikipediaのダンプファイルからアニメに関するテキストを抽出するスクリプト"""
import os
import mwxml
import mwparserfromhell

import config

def is_anime(text: str) -> bool: # --- (*1)
    """アニメに関するテキストかどうかを判定"""
    return "Category:アニメ" in text

def extract_text(file_obj):
    """指定されたファイルからテキストを抽出する関数"""
    dump = mwxml.Dump.from_file(file_obj) # --- (*2)
    counter = 0
    for i, page in enumerate(dump):
        if i % 100000 == 0:
            print(f">>> ページ {i:8d}")
        for rev in page:
            if rev.text and is_anime(rev.text): # --- (*3)
                save_text(page.title, rev.text, counter)
                counter += 1
    print(f"抽出完了: {counter} ページのテキストを {config.DIR_CORPUS_TEXT} に保存しました。")

def save_text(title: str, text: str, cnt: int): # --- (*4)
    """抽出したテキストをファイルに保存する関数"""
    # テキストを抽出して保存
    savedir = os.path.join(config.DIR_CORPUS_TEXT, f"{cnt // 100 * 100:06d}")
    fname = os.path.join(savedir, f"{cnt:06d}.txt")
    if cnt % 100 == 0:
        print(f"  - [保存]: ({cnt:06d}) {title}")
        os.makedirs(savedir, exist_ok=True)
    wikicode = mwparserfromhell.parse(text)
    plain_text = f"# {title}\n" + wikicode.strip_code()
    subtext = plain_text.split("\n")[:50]  # 最初の50行を取得 --- (*5)
    with open(fname, "w", encoding="utf-8") as f:
        f.write("\n".join(subtext) + "\n")

if __name__ == "__main__": # --- (*6)
    if not os.path.exists(config.WIKI_FILE):
        print("[ERROR] Wikipediaからダンプファイルをダウンロードしてください。")
        quit()
    with open(config.WIKI_FILE, "rb") as fp:
        extract_text(fp)
