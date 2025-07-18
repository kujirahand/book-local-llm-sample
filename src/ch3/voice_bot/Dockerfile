FROM ubuntu:24.04

# Whisper.cppのビルドに必要なパッケージを追加 --- (*1)
RUN rm -rf /var/lib/apt/lists/* \
 && apt-get clean \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
    curl git build-essential cmake ca-certificates \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
ENV WORKDIR=/app/whisper.cpp

# Whisper.cppのインストール先を作成 --- (*2)
RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR
# GitHubからリポジトリの取得 --- (*3)
RUN git clone --branch v1.7.5 \
    https://github.com/ggerganov/whisper.cpp.git $WORKDIR
# ビルド --- (*4)
RUN make
# モデルのダウンロード --- (*5)
RUN make -j small

# Whisper.cppのサーバーを起動 --- (*6)
CMD ["./build/bin/whisper-server", \
    "-m", "./models/ggml-small.bin", \
    "--port", "50022", "--host", "0.0.0.0"]

