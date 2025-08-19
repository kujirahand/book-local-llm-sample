"""Wikipediaのダンプファイルからテキストを抽出するスクリプト"""
import os
import mwxml
import mwparserfromhell

# パスとファイルを指定
DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_CORPUS = os.path.join(DIR_ROOT, "text")
FILE_WIKI = os.path.join(DIR_ROOT, "jawiki-20250520-pages-articles-multistream.xml")
os.makedirs(DIR_CORPUS, exist_ok=True)

def check_keyword(text: str) -> bool: # --- (*1)
    """カテゴリを判定"""
    return "Category:蕎麦" in text

def extract_text(file_obj):
    """指定されたファイルからテキストを抽出する関数"""
    dump = mwxml.Dump.from_file(file_obj) # --- (*2)
    counter = 0
    for i, page in enumerate(dump):
        if i % 100000 == 0:
            print(f">>> ページ {i:8d} 処理中...", counter)
        for rev in page:
            if rev.text and check_keyword(rev.text): # --- (*3)
                save_text(page.title, rev.text, counter)
                counter += 1
    print(f"抽出完了: {counter} ページのテキストを保存しました。")

def save_text(title: str, text: str, cnt: int): # --- (*4)
    """抽出したテキストをファイルに保存する関数"""
    # テキストを抽出して保存
    fname = os.path.join(DIR_CORPUS, f"{cnt:06d}.txt")
    wikicode = mwparserfromhell.parse(text)
    plain_text = f"# {title}\n" + wikicode.strip_code()
    with open(fname, "w", encoding="utf-8") as f:
        f.write(plain_text + "\n")

if __name__ == "__main__": # --- (*6)
    if not os.path.exists(FILE_WIKI):
        print("[ERROR] Wikipediaからダンプファイルをダウンロードしてください。")
        quit()
    with open(FILE_WIKI, "rb") as fp:
        extract_text(fp)
