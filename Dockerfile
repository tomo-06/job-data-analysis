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
    gnupg \
    ca-certificates \
    # Google Chrome をインストール
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    # ChromeDriverをインストール
    && CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip \
    # 不要なキャッシュを削除
    && rm -rf /var/lib/apt/lists/*

# Python パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY src/ ./src

# Jupyter Notebookのポートを開放
EXPOSE 8888

# Jupyter Notebookを起動
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--NotebookApp.token=''"]

# 日本語フォントのインストール
RUN apt update && apt install -y fonts-ipafont fonts-ipaexfont && apt-get clean