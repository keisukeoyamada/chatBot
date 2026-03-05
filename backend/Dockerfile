# ベースイメージとしてPythonを指定
FROM python:3.11-slim

RUN apt-get update

# curlをインストール
RUN apt-get update && apt-get install -y curl git
# 作業ディレクトリを作成
WORKDIR /app

# 必要なファイルをコンテナ内にコピー
COPY requirements.txt requirements.txt

# 必要なPythonパッケージをインストール
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# アプリのソースコードをコピー
COPY . .

# Flaskアプリケーションを起動
CMD ["python", "app.py"]
