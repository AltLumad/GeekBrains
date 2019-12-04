from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

if __name__ == "__main__":
    chrome_options = Options()
    #chrome_options.add_argument('start-maximized')
    #chrome_options.add_argument('--headless')
    #driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
    driver.get("https://www.mvideo.ru/")
    assert "М.Видео" in driver.title
    n = 0
    button = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "next-btn")]'))
    )[2]

    while n < 10:
        try:
            webdriver.ActionChains(driver).move_to_element(button).perform()
            button.send_keys(Keys.ENTER)
            n += 1
        except:
            break

    goods = driver.find_elements_by_xpath('//div[@data-init="gtm-push-products"]//div[contains(@class,"sel-product-tile-main")]')
    res = []
    for good in goods:
        tmp = {}

        try:
            tmp['name'] = good.find_element_by_class_name('sel-product-tile-title').text
            tmp['price'] = good.find_element_by_class_name('c-pdp-price__current').text
            res.append(tmp)
        except:
            break

    print('Сбор данных окончен')
    driver.quit()
    client = MongoClient('localhost', 27017)
    client.mvideo['mvideo_ru'].insert_many(res)
    print(f'{len(res)} products - was stored')