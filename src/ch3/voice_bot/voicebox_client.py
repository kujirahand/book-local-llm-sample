import json
import requests
import pyaudio
import re

# VOICEVOXの設定 --- (*1)
VOICEBOX_URL = "http://127.0.0.1:50021"
speaker_id = 1 # スピーカーID

def text_to_speech(text): # --- (*2)
    """音声合成を行い、音声を再生する"""
    print("BOT>", text)
    # 読み間違える部分を手動で修正
    text = re.sub(r"([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})", r"\1時\2分\3秒", text)
    text = re.sub(r"(晴|雨|曇)後(晴|雨|曇)", r"\1のち\2", text)
    text = text.replace("他にも", "ほかにも")
    # 音声合成の前処理のリクエストを送信 --- (*3)
    params = {
        "text": text,
        "speaker": speaker_id
    }
    query_response = requests.post(
        f"{VOICEBOX_URL}/audio_query",
        params=params
    )
    # 成功したか確認
    query_response.raise_for_status()
    query = query_response.json()
    # 音声合成のリクエストを送信 --- (*4)
    synthesis_response = requests.post(
        f"{VOICEBOX_URL}/synthesis?speaker={speaker_id}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(query)
    )
    # 成功したか確認
    synthesis_response.raise_for_status()
    # 音声ファイルとして保存 --- (*5)
    voice_file = f"voicebox.wav"
    with open(voice_file, "wb") as f:
        f.write(synthesis_response.content)
    # pyaudioで音声を再生 --- (*6)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=24000,
                    output=True)
    stream.write(synthesis_response.content)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("音声合成が完了しました。")

if __name__ == "__main__":
    text = "本日は晴天なり。"
    text_to_speech(text)
