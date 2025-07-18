"""LLMを使ってWikipediaからコーパスを自動生成するスクリプト"""
import json
import requests

from config import *

# モデル名とOllamaのURL（必要に応じて変更） --- (*1)
MODEL_NAME = "qwen3:14b"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# テキストからあらすじを生成するプロンプト --- (*2)
GENERATE_PROMPT = """
### 指示:
/think `{title}`に関する以下の入力を400字以内で要約してください。
もし、内容の記述がない場合は「記載なし」と答えてください。
冒頭で主人公に言及し、その後、物語のあらすじを教えてください。
ただし、作者や放送年、声優やスタッフなどの情報は含めないでください。
日本語で出力してください。

### 入力:
```
{text}
```
"""
# テキストから主人公を抽出するプロンプト --- (*3)
GENERATE_PROMPT_CHAR = """
### 指示:
/no_think `{title}`に関する入力から、物語の主人公を調べて教えてください。 
{instruction}
もし、記載がない場合は「記載なし」と答えてください。
主人公の名前とその情報を日本語で出力してください。
なお、声優やスタッフの情報は不要です。

### 入力:
```
{text}
```
"""

def ask_ollama(prompt): # --- (*4)
    """Ollama APIにプロンプトを送信して応答を取得する関数"""
    for _ in range(3):
        try:
            response = requests.post(OLLAMA_API_URL, json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }, timeout=OLLAMA_TIMEOUT)
            response.raise_for_status()  # HTTPエラーをチェック
            result = response.json().get("response", "").strip()
            if '</think>' in result:
                result = result.split('</think>')[1].strip()
            if "Summary" in result or "is" in result: # 英語なら出力失敗
                raise ValueError("API応答が不正です。内容を確認してください。")
            return result
        except Exception as e:
            print(f"*** APIエラー: {e} - 再試行します...")
    return None

def generate_alpaca_format(file_list): # --- (*5)
    """指定されたファイルリストからAlpaca形式のデータを生成する関数"""
    # Alpaca形式で出力するリスト
    alpaca_data = []
    # テキストを読んで、Alpaca形式に変換する
    for i, filepath in enumerate(file_list):
        with open(filepath, "r", encoding="utf-8") as f:
            input_text = f.read()
        title = input_text.split("\n")[0]  # 最初の行がタイトル
        title = title[1:].strip() # *を除去してタイトルを取得
        title = title.replace("の登場人物", "")
        title = title.replace("（アニメ）", "")
        print("------------------------------")
        print(f"*** タイトル: {title} ({i+1}/{len(file_list)})")
        # 要約プロンプトを実行 --- (*6)
        prompt = GENERATE_PROMPT.format(title=title, text=input_text)
        try:
            summary = ask_ollama(prompt)
        except Exception as e:
            print(f"*** エラー: {e}")
            continue
        print(f"*** 要約結果: {summary}")
        if summary is None or "記載なし" in summary:
            continue
        # データに追加
        alpaca_data.append({
            "instruction": "あらすじを教えてください。",
            "input": title,
            "output": summary
        })
        # 主人公の名前を抽出 --- (*7)
        inst_list = [
            "主人公について教えてください。",
            "主人公の名前や特徴を教えてください。",
            "主人公は誰ですか？"
        ]
        for i in range(3):  # 最大3回試行
            instruction = inst_list[i % len(inst_list)]
            prompt = GENERATE_PROMPT_CHAR.format(
                title=title, text=input_text,
                instruction=instruction)
            try:
                name_text = ask_ollama(prompt)
            except Exception as e:
                print(f"*** エラー: {e}")
                continue
            print(f"*** [名前] {instruction}: {name_text}")
            if name_text is None or "記載なし" in name_text:
                continue
            alpaca_data.append({
                "instruction": instruction,
                "input": title,
                "output": name_text
            })
    # Alpaca形式で出力 --- (*8)
    with open(CORPUS_FILE_JSON, "w", encoding="utf-8") as fp:
        json.dump({"train": alpaca_data}, fp,
                  ensure_ascii=False, indent=2)
    print("Alpaca形式のJSONを出力しました。")

if __name__ == "__main__":
    # corpusディレクトリから対象ファイルを読み込む --- (*9)
    with open(CORPUS_TARGET_FILES, "r", encoding="utf-8") as f:
        target_files = json.load(f)
        generate_alpaca_format(target_files)
