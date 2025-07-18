"""物語から動画生成プロンプトを生成し、動画を生成するプログラム"""
import json
import text2video

# 物語から動画生成のためのプロンプトを生成するプロンプト --- (*1)
STORY_PROMPT = """\
### 指示:
南国の海辺を黒猫が散歩する動画を作成します。
4つのシーンを含む動画を生成するプロンプトを考えてください。
黒猫の要素(毛並みや表情)を作成し、全てのシーンに共通の設定として出力してください。
### 出力例:
以下のJSON形式で出力してください。
```json
{
    "cat": "黒猫は(説明)",
    "scene": ["(シーン1)","(シーン2)","(シーン3)","(シーン4)"]
}
```
"""

def make_story_prompt(): # --- (*2)
    """動画生成プロンプトを生成する"""
    # Ollama APIを呼び出して物語を生成 --- (*3)
    json_str = text2video.ollama_generate(STORY_PROMPT)
    # 応答からJSONデータを抽出 --- (*4)
    if "```json" in json_str:
        json_str = json_str.split("```json")[1].split("```")[0].strip()
    try:
        story = json.loads(json_str)
    except json.JSONDecodeError:
        print("JSONの解析に失敗しました。出力を確認してください。")
        return
    if "cat" not in story or "scene" not in story:
        print("JSONの形式が正しくありません。")
        return
    # 動画生成プロンプトを抽出 --- (*5)
    cat = story.get("cat", "").strip()
    scene_list = story.get("scene", [])
    scene_list = [cat + s.strip() for s in scene_list]
    print("schene_list:", scene_list)
    # 動画を生成 --- (*6)
    text2video.generate_video(scene_list)

if __name__ == "__main__":
    make_story_prompt()
