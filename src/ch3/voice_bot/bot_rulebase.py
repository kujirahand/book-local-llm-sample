import requests
import json
import re
import time
import random

def get_weather(user: str) -> str: # --- (*1)
    """天気情報を取得する"""
    # どの地域の天気が知りたいかを正規表現で取得する --- (*2)
    m = re.search(r"(東京|大阪|名古屋|福岡|札幌)の天気", user)
    city = m.group(1) if m else "東京"
    # APIを呼び出して天気情報を取得する --- (*3)
    city_q = requests.utils.quote(city)
    api = f"https://api.aoikujira.com/tenki/week.php?fmt=json&city={city_q}"
    result = "すみません。天気情報を取得できませんでした。"
    response = requests.get(api)
    if response.status_code == 200:
        data = json.loads(response.text) # --- (*4)
        if city in data and len(data[city]) > 0:
            forecast = data[city][0]["forecast"]
            result = f"{city}の天気は{forecast}です。"
    return result

def generate(user: str) -> str: # --- (*5)
    """ユーザーの入力に応じて、天気や時間を返す"""
    # 正規表現でパターンマッチする --- (*6)
    if re.search(r"こんにちは|おはよう|こんばんは", user):
        return "こんにちは！今日はどんなことを知りたいですか？"
    if re.search(r"元気.*(か|？)|調子.*どう|最近どう", user):
        return "私は元気です！あなたはどうですか？"
    if re.search(r"元気(です|だ|)", user):
        return "良かったです。天気や時間が知りたいですか？"
    if re.search(r"ありがとう.*", user):
        return "どういたしまして。他にも何かお手伝いできるでしょうか？"
    if re.search(r"天気", user):
        return get_weather(user)
    if re.search(r"時間|今|何時", user):
        return f"現在の時刻は{time.strftime('%H:%M:%S')}です。"
    return "申し訳ありませんが、その質問にはお答えできません。"

def main_loop() -> None:
    """メインループ"""
    # 最初に挨拶と簡単な説明を述べる --- (*7)
    hello_list = ["こんにちは！", "おはようございます！", "どうもです！"]
    hello_help = "私は天気や時間を答えるボットです。何が知りたいですか？"
    print(random.choice(hello_list) + hello_help)
    # 繰り返し対話を行う --- (*8)
    while True:
        user = input("You> ")
        if user == "quit" or user == "さようなら" or user == "":
            print("ご利用ありがとうございました。")
            break
        response = generate(user)
        print("Bot>", response)

if __name__ == "__main__":
    main_loop()

