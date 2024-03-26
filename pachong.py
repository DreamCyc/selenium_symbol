import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
from datetime import datetime

# 获取输入参数：时间、货币符号
parser = argparse.ArgumentParser()
parser.add_argument("time_input", help="time")
parser.add_argument("symbol", help="货币代号")
args = parser.parse_args()


def format_date(input_date):
    date_obj = datetime.strptime(input_date, '%Y%m%d')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date


def from_symbol_get_chinese_currency(symbol):
    driver = webdriver.Chrome()
    url = "https://www.11meigui.com/tools/currency"
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all('tr')
    # 遍历找到对应的中文货币符号，若无返回空，顺便写入txt
    with open(output_file, 'a', encoding='utf-8') as file:
        for row in rows:
            file.write(str(row.find_all('td')) + "\n")
    for row in rows:
        cells = row.find_all('td')
        if len(cells)>5:
            fifth_td_content = cells[4].text
            if fifth_td_content == symbol:
                second_td_content = cells[1].text
                driver.quit()
                return second_td_content
    return


def get_content(driver, time, chinese_currency):
    # 获取页面源码
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    target_rows = soup.find_all('td', class_='pjrq')
    # 提取目标表格中的元素值
    with open(output_file, 'a', encoding='utf-8') as file:
        for row in target_rows:
            file.write(str(row.find_parent('tr').find_all('td'))+ '\n')
    for row in target_rows:
        row = row.find_parent('tr')
        cells = row.find_all('td')
        if cells[0].text + " " == chinese_currency and cells[6].text == time:
            return cells[3].text
    return


if __name__ == '__main__':
    # mac OS
    chrome_driver_path = '/usr/local/bin'
    driver = webdriver.Chrome()
    output_file = "output.txt"

    # 输入数据处理
    time_input = format_date(args.time_input)
    chinese_currency = from_symbol_get_chinese_currency(args.symbol + " ")

    # 遍历各个页面，并写入并寻找结果
    for page in range(10):
        if page == 0:
            url = 'https://www.boc.cn/sourcedb/whpj/'
            driver.get(url)
            time.sleep(10)
            # 获取最终结果
            result = get_content(driver, time_input, chinese_currency)
            if result:
                print(result)
                break
        else:
            try:
                next_page_link = driver.find_element(By.CLASS_NAME, 'turn_next').find_element(By.TAG_NAME, 'a')  # 找到下一页按钮
                next_page_link.click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'turn_page')))
            except Exception as e:
                print("Failed to find next page or load next page:", e)
                break
            result = get_content(driver, time_input, chinese_currency)
            if result:
                print(result)
                break
        # print("The information of " + str(page) + " is ok.")