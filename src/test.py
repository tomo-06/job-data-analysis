import os
import shutil
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Chromeのユーザディレクトリ
chrome_user_data_dir = "/tmp/chrome_user_data"

# 既存のディレクトリがあれば削除
if os.path.exists(chrome_user_data_dir):
    shutil.rmtree(chrome_user_data_dir)

# Chromeオプションを設定
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://next.rikunabi.com/rnc/docs/cp_s00700.jsp?leadtc=srch_submitbtn")