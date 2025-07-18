"""画像を分類して結果をHTMLに保存するプログラム"""
import os
import re
import json

import image2text as i2t

# 画像分類のためのカテゴリ一覧 --- (*1)
CATEGORIES = [
    "ラーメン",
    "パスタ",
    "チャーハン",
    "ピザ",
    "その他"
]
# 画像分類に利用するプロンプト --- (*2)
PROMPT = f"""
### 指示:
1. 写真には何が写っていますか？
2. それは、`カテゴリ一覧`のどれに相応しいですか。
3. 選んだカテゴリのみを出力してください。

### カテゴリ一覧:
```json
{json.dumps(CATEGORIES, ensure_ascii=False)}
```

### 備考:
- カテゴリ一覧に当て浜ならなければ`その他`を出力してください。

### 出力例:
その他
"""
print(PROMPT) # プロンプトの内容を確認

def main(): # --- (*3)
    """画像を分類してHTMLファイルに保存するメイン関数"""
    # imagesフォルダの画像ファイル一覧を列挙 --- (*4)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(root_dir, "images")
    pattern = re.compile(r'.*\.(png|jpg|jpeg)$', re.IGNORECASE)
    files = [
        os.path.join(target_dir, f) for f in os.listdir(target_dir)
        if pattern.match(f)
    ] # 全ファイルから画像ファイルのみを抽出 --- (*5)

    # 全ての画像ファイルを処理する --- (*6)
    result = {}
    for file in sorted(files):
        fname = os.path.basename(file)
        print(f"┏━ 処理開始: {fname}")
        answer = ""
        # 分類に失敗したらやり直すためのループ --- (*7)
        for _ in range(5):
            answer = i2t.image_to_text(file, PROMPT).strip()
            # 結果がカテゴルに一致するか確認 --- (*8)
            if answer in CATEGORIES:
                break
            print(f"┣━━ 分類失敗: {answer}")
            answer = "分類失敗"
        print(f"┗━━━ 分類結果: {answer}")
        # 分類結果を辞書に保存 --- (*9)
        if answer not in result:
            result[answer] = []
        result[answer].append(fname)

    # 分類ごとに写真を表示 --- (*10)
    html = "<html><meta charset='utf-8'><body>"
    for category, images in result.items():
        html += f"<hr>\n<h3>{category}</h3>\n"
        for image in images:
            html += f"<img src='images/{image}' width='280'>"
    html += "</body></html>"
    with open("classify.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("分類結果を classify.html に保存しました。")

if __name__ == "__main__":
    main()
