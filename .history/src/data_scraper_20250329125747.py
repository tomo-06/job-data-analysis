# -*- coding: utf-8 -*-

"""
リクナビNEXTから求人情報を取得する
"""
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

SLEEP_TIME = 3
SEARCH_WORD = "データアナリスト"
CSV_NAME = "output/rikunabi.csv"

def update_page_num(driver):
    ul_element = driver.find_element(By.CSS_SELECTOR, ".rnn-pagination.rnn-textRight")
    a_element = ul_element.find_elements(By.TAG_NAME, "a") [-1]
    driver.get(a_element.get_attribute("href"))
    time.sleep(SLEEP_TIME)

def get_item_urls(driver):
    elements = driver.find_elements(By.CLASS_NAME, "rnn-linkText--black")
    item_urls = [i.get_attribute('href') for i in elements]
    return item_urls

def get_company_name(driver):
    elements = driver.find_elements(By.CLASS_NAME, "rn3-companyOfferHeader__text")
    for element in elements:
        print("候補:", element.text)  # デバッグ用
    return elements[0].text if elements else "不明"

#def get_company_name(driver):
#    company_name_element = driver.find_elements(By.CLASS_NAME, "rn3-companyOfferHeader__text")
#    return company_name_element[0].text if company_name_element else "不明"

# 20250320_"rn3-topSummaryWrapper"が含まれないページがあるため、例外処理を追加
def get_normal_info(driver):
    info_elements = driver.find_elements(By.CLASS_NAME, "rn3-topSummaryWrapper")
    data = {"会社名": get_company_name(driver)}

    if info_elements:
        info_element = info_elements[0]
        keys = [i.text for i in info_element.find_elements(By.CLASS_NAME, "rn3-topSummaryTitle")]
        values = [i.text for i in info_element.find_elements(By.CLASS_NAME, "rn3-topSummaryText")]
        data.update({k:v for k,v in zip(keys, values)})
    
    return data

def get_rcn_info(driver):
    table_elements = driver.find_elements(By.CLASS_NAME, "rnn-detailTable")
    data = {"会社名": get_company_name(driver)}

    if table_elements:
        table_html = table_elements[0].get_attribute("outerHTML")
        df = pd.read_html(table_html) [0]
        data.update({i_row[0]:i_row[1] for _, i_row in df.iterrows()})
    return data

if __name__ == "__main__":
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://next.rikunabi.com/rnc/docs/cp_s00700.jsp?leadtc=srch_submitbtn")
        time.sleep(SLEEP_TIME)

        input_element = driver.find_element(By.CLASS_NAME, "rnn-header__search__inner").find_element(By.TAG_NAME, "input")
        input_element.send_keys(SEARCH_WORD)
        button_element = driver.find_element(By.CSS_SELECTOR, ".rnn-header__search__keywordButton.js-submitKeyword")
        button_element.click()
        time.sleep(SLEEP_TIME)

        # 20250319_テストにて検索結果の先頭ページのみにするため、下記2行はコメントアウト
        total_num = int(driver.find_element(By.CSS_SELECTOR, ".rnn-pageNumber.rnn-textXl").text)
        total_page_num = total_num // 50 +1

        # 20250319_ループ処理なので、一旦テストで1回分の実行にする
        project_urls = list()
        for _ in range(total_page_num):
            project_urls.extend(get_item_urls(driver))
            update_page_num(driver)

        # 20250319_1回分の実行コードを追加
        #project_urls = get_item_urls(driver)

        result = list()
        rnc_result = list()
        for i_url in project_urls:
            template_type = i_url.split("/") [3]
            if template_type == "rnc":
                driver.get(i_url)
                time.sleep(SLEEP_TIME)
                test = get_rcn_info(driver)
                print(test)
                rnc_result.append(test)
            else:
                url_list = i_url.split("/")
                url_list[-2] = url_list[-2].replace("nxl", "nx2")
                driver.get("/".join(url_list[:-1]))
                time.sleep(SLEEP_TIME)
                test = get_normal_info(driver)
                print(test)
                result.append(test)
        pd.DataFrame(result).to_csv(CSV_NAME)
        pd.DataFrame(rnc_result).to_csv(CSV_NAME.replace(".csv", ""))
    finally:
        driver.quit()