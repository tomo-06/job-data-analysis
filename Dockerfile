# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリ
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    git \
    wget \
    unzip \
    curl \
    gnupg && \
    rm -rf /var/lib/apt/lists/*

# Google Chrome をインストール
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Python パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY src/ ./src

# Jupyter Notebookのポートを開放
EXPOSE 8888

# Jupyter Notebookを起動
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--NotebookApp.token=''"]
