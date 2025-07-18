import os
import glob
import json

DIR_BENCH_LOGS = "bench_logs/"
text_by_model = {}

def main():
    files = glob.glob(os.path.join(DIR_BENCH_LOGS, "*.json"))
    for f in sorted(files):
        base_name = os.path.basename(f).replace(".json", "").replace("_", " ")
        print("### ", base_name + " での検証結果:")
        print("| モデル: サイズ | 評価速度(t/秒) | 生成速度(t/秒) | 動作感 | 回答例 |")
        print("|--------------|--------------|---------------|-------|-------|")
        with open(f, "r", encoding="utf-8") as file:
            data_all = json.load(file)
            for data in data_all:
                model = data['model']
                prompt_rate = data["prompt_eval_rate"]
                eval_rate = data["eval_rate"]
                res_text = data["response"]
                res = extract_json(res_text)
                kanso = get_kanso(eval_rate)
                # 生成速度と評価速度を出力
                print(f"| {model} | {prompt_rate:.2f} | {eval_rate:.2f} | {kanso} | {res} |")
                # 生成されたテキストを保存
                if model not in text_by_model:
                    text_by_model[model] = []
                text_by_model[model].append(
                    f"### {base_name}の時:\n" + res_text + "\n\n"
                )
            # ---
            print("")

def get_kanso(eval_rate):
    kanso = "?"
    if eval_rate >= 50:
        kanso = "爆速"
    elif 50 > eval_rate >= 30:
        kanso = "高速"
    elif 30 > eval_rate >= 15:
        kanso = "快適"
    elif 15 > eval_rate >= 10:
        kanso = "普通"
    elif 10 > eval_rate >= 5:
        kanso = "低速"
    elif 5 > eval_rate >= 3:
        kanso = "遅い"
    else:
        kanso = "激遅"
    return kanso

def show_geneted_text():
    """生成されたテキストを表示"""
    for model in text_by_model:
        print("================================")
        print(f"### {model} の結果:")
        print("================================")
        for text in text_by_model[model]:
            print(text)
        print("")


def extract_json(response):
    try:
        # 長文のテキストから、```json…``` で囲まれた部分を抽出
        start = response.find("```json")
        end = response.find("```", start + 7)
        if start == -1 or end == -1:
            print("No JSON found in the response")
            return None
        json_str = response[start + 7:end].strip()
        json_data = json.loads(json_str)
        return json_data["answer"]
    except json.JSONDecodeError:
        print("JSON Decode Error")
        return "(error)"

if __name__ == "__main__":
    # テーブルを表示
    main()
    # 生成されたテキストを表示
    #vshow_geneted_text()
