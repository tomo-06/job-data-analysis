import os
import shutil
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Chromeのオプション設定
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")  # 必須オプション（WSL環境用）
chrome_options.add_argument("--disable-dev-shm-usage")  # 必須オプション（WSL環境用）
#chrome_options.add_argument("--remote-debugging-port=9222")  # デバッグ用
chrome_options.add_argument("--lang=ja")


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://next.rikunabi.com/rnc/docs/cp_s00700.jsp?leadtc=srch_submitbtn")
time.sleep(3)