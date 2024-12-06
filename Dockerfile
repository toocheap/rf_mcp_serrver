FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係のコピーとインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# ログディレクトリの作成
RUN mkdir -p /var/log/gunicorn

# 環境変数の設定
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 実行ユーザーの作成
RUN useradd -m appuser && chown -R appuser:appuser /app /var/log/gunicorn
USER appuser

# Gunicornでの起動
CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:app"]
