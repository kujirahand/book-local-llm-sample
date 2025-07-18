import re
from bot_rulebase import generate
from record_audio import record_audio
from voicebox_client import text_to_speech
from whisper_client import transcribe_audio

def main_loop():
    """繰り返し対話"""
    text_to_speech("こんにちは！私は天気や時間を答えるボットです。")
    while True:
        try:
            # ユーザーの声を録音 --- (*1)
            wav_file = "whisper.wav"
            record_audio(wav_file)
            # 音声を文字起こし --- (*2)
            user = transcribe_audio(wav_file)
            if user == "さようなら":
                text_to_speech("ご利用ありがとうございました。")
                break
            if user == "" or re.match(r"\(.+\)", user):
                continue
            # チャットボットの応答を生成 --- (*3)
            com = generate(user)
            # 応答を音声合成して再生 --- (*4)
            text_to_speech(com)
        except Exception as e:
            print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main_loop()
