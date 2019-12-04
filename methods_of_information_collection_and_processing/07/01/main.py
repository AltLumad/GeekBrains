from selenium import webdriver
from enum import Enum
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import datetime

class Action(Enum):
    click = 1
    send_keys = 2

def find_and_act(driver, id, act, wait=False, keys=None):
    if wait:
        elem = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, id))
        )
    else:
        elem = driver.find_element_by_id(id)

    if act == Action.click:
        elem.click()
    elif act == Action.send_keys:
        try:
            elem.send_keys(keys)
        except:
            elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, id))).send_keys(keys)
    elif act == Action.mouse_scroll:
        elem.location_once_scrolled_into_view()
    return elem

def find_by_xpath(driver, xpath, attr):
    try:
        elem = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
        return elem.get_attribute(attr) if attr and elem.get_attribute(attr) else elem.text
    except:
        return None


def double_esc(driver):
    #Хз. но эта хрень может на сработать с первого раза
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def parse_msg(driver, message):
    info = {}
    driver.execute_script("arguments[0].scrollIntoView();", message)
    driver.execute_script("$(arguments[0]).click();", message)
    try:
        message.click() # не понимаю почему эта хрень иногда падает
    except:
        return None
    info['sender'] = find_by_xpath(driver, '//span[@class="letter__contact-item"]', 'title')
    info['head'] = find_by_xpath(driver, '//h2', 'head')
    info['body'] = find_by_xpath(driver, '//div[@class="letter-body"]', 'body')
    info['data'] = find_by_xpath(driver, '//div[@class="letter__date"]', None)
    info['parse_date'] = str(datetime.datetime.now().date())
    double_esc(driver)
    return info

def ParseMails():
    chrome_options = Options()
    #chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()
    driver.get("https://mail.ru")
    assert "Mail.ru" in driver.title

    find_and_act(driver, "mailbox:login", Action.send_keys, keys='study.ai_172@mail.ru')
    find_and_act(driver, "mailbox:saveauth", Action.click)

    find_and_act(driver, "mailbox:submit", Action.click, wait=True)
    find_and_act(driver, "mailbox:password", Action.send_keys, keys='Password172', wait=True)

    find_and_act(driver, "mailbox:submit", Action.click)

    elems = set()
    res = []
    n = 0
    while n < 10:
        read_mores = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class,"llc")]')))
        try:
            if set(map(lambda x: x.get_attribute('data-id'), read_mores)) - elems == set():
                break
        except:
            pass

        for msg in read_mores:
            try:
                if msg.get_attribute('data-id') in elems:
                    continue
            except:
                break #esc иногда меняет объекты в памяти. Надо обновить. Костыль увеличивает сложность до n^2

            elems.add(msg.get_attribute('data-id'))
            tmp = parse_msg(driver, msg)
            if tmp:
                res.append(tmp)
            print(res[-1])
            double_esc(driver)
        n += 1
    driver.quit()
    return res


if __name__ == "__main__":
    res = ParseMails()
    client = MongoClient('localhost', 27017)
    client.mails['mail_ru'].insert_many(res)
    print(f'{len(res)} mails - was stored')