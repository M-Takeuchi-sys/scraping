import csv
import datetime
import re
import time
import tkinter

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import chromedriver_binary

date = datetime.datetime.now().strftime('%Y%m%d')
EXTENSION_PATH = 'rakujan1.12.1.0.crx'
# usernameの部分をパソコン環境ごとに変更する
USER_CHROME_PATH = '--user-data-dir=/Users/username/Library/Application\ Support/Google/Chrome/Default/'


def main():
    store_text = store_form.get()
    min_price = min_form.get()
    max_price = max_form.get()
    if store_text == '':
        return print('店舗IDを入力してください')
    if not store_text.isdecimal():
        return print('店舗IDが数字ではありません')
    if min_price != '' and not min_price.isdecimal():
        return print('価格（Min）が数字ではありません')
    if max_price != '' and not max_price.isdecimal():
        return print('価格（Max）が数字ではありません')
    store_id = int(store_text)
    if min_price != '':
        min_price = int(min_price)
    if max_price != '':
        max_price = int(max_price)
    url = 'https://search.rakuten.co.jp/search/mall/?max={}&min={}&sid={}'.format(max_price, min_price, store_id)

    no = 1
    file_name = '{}_{}.csv'.format(store_id, date)
    f = open(file_name, 'w', encoding='UTF-8')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['No', 'JANコード', '商品名', '価格', 'URL'])

    options = Options()
    options.add_argument(USER_CHROME_PATH)
    options.add_extension(EXTENSION_PATH)
    driver = webdriver.Chrome(options=options)
    driver.delete_all_cookies()
    driver.get(url)
    time.sleep(10)
    try:
        while True:
            soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')
            for item in soup.find_all('div', class_='searchresultitem'):
                title = item.find('h2').text.strip()
                price = int(re.sub('[^0-9]', '', item.find('span', class_='important').text))
                item_url = item.find('a').get('href')

                jan_code = None
                jan_code_container = item.find('div', id='rakujan-wrapper')
                if jan_code_container:
                    if jan_code_container.attrs['data-rakujan-jan'].isdecimal():
                        jan_code = int(jan_code_container.attrs['data-rakujan-jan'])

                if not jan_code:
                    driver.get(item_url)
                    time.sleep(5)
                    item_soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')

                    jan_code_container = item_soup.find('div', id='rakujan-wrapper')
                    if jan_code_container:
                        if jan_code_container.attrs['data-rakujan-jan'].isdecimal():
                            jan_code = int(jan_code_container.attrs['data-rakujan-jan'])
                        else:
                            jan_code = jan_code_container.attrs['data-rakujan-jan']
                    else:
                        jan_code = 'NO DATA'

                writer.writerow([no, jan_code, title, price, item_url])

                no = no + 1

            if hasattr(soup.find('a', class_='item -next nextPage'), 'text'):
                url = soup.find('a', class_='item -next nextPage').get('href')
                driver.delete_all_cookies()
                driver.get(url)
                time.sleep(10)
            else:
                print('正常に終了しました')
                break
    except Exception as e:
        print('エラーが発生しました')

    f.close()
    driver.quit()


if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('楽天スクレイピング')
    window.geometry("400x280")

    store_label = tkinter.Label(text='店舗ID')
    store_label.place(x=50, y=50)
    min_label = tkinter.Label(text='価格（Min）')
    min_label.place(x=50, y=80)
    max_label = tkinter.Label(text='価格（Max）')
    max_label.place(x=50, y=110)

    store_form = tkinter.Entry(width=20)
    store_form.place(x=130, y=50)
    min_form = tkinter.Entry(width=20)
    min_form.place(x=130, y=80)
    max_form = tkinter.Entry(width=20)
    max_form.place(x=130, y=110)

    btn = tkinter.Button(window, text='実行', command=main)
    btn.place(x=125, y=180, width=150, height=40)

    window.mainloop()
