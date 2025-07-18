import requests
import re

# Whisper.cppのURL --- (*1)
WHISPER_URL = "http://127.0.0.1:50022/inference"

def transcribe_audio(wav_file): # --- (*2)
    """録音した音声を文字起こしする"""
    print(">>>> 音声認識中...")
    # 音声認識のリクエストを送信 --- (*3)
    with open(wav_file, "rb") as wav_file_p:
        files = {
            "file": (wav_file, wav_file_p, "audio/wav")
        }
        data = {
            "language": "ja",
            "temperature": "0.0",
            "temperature_inc": "0.2",
            "response_format": "json",
        }
        response = requests.post(WHISPER_URL, files=files, data=data)
    if response.status_code != 200:
        raise Exception(f"whisper_cppが応答しません: {response.status_code}")
    # 結果を抽出 ---- (*4)
    result = response.json()
    if "text" not in result:
        raise Exception("whisper_cppが応答しません")
    user = result["text"]
    print("YOU>", user)
    return user

if __name__ == "__main__":
    transcribe_audio("test.wav")
