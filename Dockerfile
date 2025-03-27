# Python 3.11 の軽量イメージを使用（Django 5.1.7 対応）
FROM python:3.11-slim

# アプリケーションの作業ディレクトリを /app に設定
WORKDIR /app

# パッケージ依存関係ファイル requirements.txt をコピー
COPY requirements.txt .

# pip をアップグレードし、必要なパッケージをインストール
RUN pip install --upgrade pip && pip install -r requirements.txt

# プロジェクト全体のコードをコンテナ内にコピー
COPY . .

# 標準出力・エラー出力をバッファリングせずに即時出力にする
ENV PYTHONUNBUFFERED=1

# Cloud Run が使用するポート番号を環境変数として定義
ENV PORT=8000

# Cloud Run 上で使用されるポートを明示的に公開
EXPOSE 8000

# アプリケーションの起動コマンド（WSGI を使用して Gunicorn 経由で起動）
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080"]