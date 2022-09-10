import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import chromedriver_binary


def main():
    BASE_URL = 'https://netmall.hardoff.co.jp/product/2801257/?sci_refl=1A30'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    time.sleep(2)
    try:
        prefectures_select_button = driver.find_element(By.CLASS_NAME, 'm-select-styled')
        driver.execute_script('arguments[0].click();', prefectures_select_button)
        time.sleep(1)
        kyoto_button = driver.find_element(By.XPATH, '//*[@id="pagebody"]/div[2]/div[2]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div/ul/li[27]/button')
        driver.execute_script('arguments[0].click();', kyoto_button)
        time.sleep(1)
        element = driver.find_element(By.CLASS_NAME, 'product-detail-postage-price__main')
        postage = element.get_attribute('textContent')
        print(postage)
    except Exception as e:
        print('エラーが発生しました')

    driver.quit()


if __name__ == '__main__':
    main()

