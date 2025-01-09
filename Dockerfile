# Alpine上のPython3.12.8環境を指定
FROM python:3.12.8-alpine

# 作業ディレクトリを設定
WORKDIR /code

# 必要なファイルをコンテナにコピー
COPY requirements.txt /code/

# 必要なライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクト全体をコンテナにコピー
COPY . /code/

# デフォルトで Django を起動し、FastAPI をバックグラウンドで動かす
CMD ["/bin/sh", "-c", "python manage.py runserver 0.0.0.0:8000 & uvicorn app.main:app --host 0.0.0.0 --port 8001"]