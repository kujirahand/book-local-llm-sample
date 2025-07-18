import numpy as np
import pyaudio
import wave

def record_audio(wav_file):
    """音声を録音し、無音になると自動で終了する"""
    # 音声録音の設定 --- (*1)
    THRESHOLD = 500  # 無音と判断するしきい値
    CHUNK = 1024 # 録音するデータのサイズ
    SILENT_CHUNKS = 30  # この回数連続で無音なら終了（約2秒）
    WAV_FORMAT = pyaudio.paInt16  # 音声のフォーマット
    SAMPLE_RATE = 16000  # サンプリングレート
    print(">>>> 話しかけてください...")
    # 音声録音の準備 --- (*2)
    p = pyaudio.PyAudio()
    stream = p.open(format=WAV_FORMAT, channels=1, rate=SAMPLE_RATE,
                    input=True, frames_per_buffer=CHUNK)
    frames = []
    silent_count = 0
    while True:
        # 音声を録音 --- (*3)
        data = stream.read(CHUNK)
        frames.append(data)
        # 音量を計測 --- (*4)
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_data).mean()
        # 音量がしきい値以下なら無音と判断
        if volume < THRESHOLD:
            silent_count += 1
        else:
            silent_count = 0
        if silent_count > SILENT_CHUNKS:
            break
    print(">>>> 録音終了")
    stream.stop_stream()
    stream.close()
    p.terminate()
    # 録音した音声をファイルに保存 --- (*5)
    wf = wave.open(wav_file, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(WAV_FORMAT))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    record_audio("test.wav")
    print("音声録音が完了しました。")