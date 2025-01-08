# Alpine上のPython3.12.8環境を指定
FROM python:3.12.8-alpine

# コンテナ内の作業ディレクトリを設定
WORKDIR /workspace

# 管理者権限で実行
USER root

# 必要なパッケージをインストール
RUN apk update && apk add --no-cache \
    git \
    iptables \
    && rm -rf /var/cache/apk/*

# requirements.txtをコンテナにコピー
COPY requirements.txt .

# Pythonパッケージをインストール
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# ポートの開放宣言
EXPOSE 8000
EXPOSE 80
EXPOSE 8080
