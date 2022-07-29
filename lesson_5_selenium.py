
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from pymongo import MongoClient
from pprint import pprint


client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
db_products = db.products

options = Options()
options.add_argument("start-maximized")

s = Service('./geckodriver')
driver = webdriver.Firefox(service=s)

driver.get('https://www.mvideo.ru/')

action_chains = ActionChains(driver)
scr = 0
while True:
    try:
        # driver.execute_script(f"window.scrollTo(0, {scr})")
        button = driver.find_element(
            By.XPATH, "//button[@class='tab-button ng-star-inserted']")
        button.click()
        break
    except NoSuchElementException:
        action_chains.send_keys(Keys.PAGE_DOWN).perform()
        scr += 100
        time.sleep(1)

card_trend = driver.find_elements(
    By.XPATH, '//mvid-shelf-group//mvid-product-cards-group//div[@class="title"]')
card_trend_2 = driver.find_elements(
    By.XPATH, '//mvid-shelf-group//mvid-product-cards-group//span[@class="price__main-value"]')
for i in range(len(card_trend)):
    name = card_trend[i].text
    print(name)
    link = card_trend[i].find_element(By.XPATH, './a').get_attribute('href')
    print(link)
    price = card_trend_2[i].text.replace(' ', '')
    price.split()
    int_price = int(''.join(price[:-1]))
    currency = price[-1]

    # pprint(bool(db_products.find({'link_mvideo_card': link})))

    # if not bool(db_products.find({'link_mvideo_card': link})):
    data = {
        "name": name,
        "link_mvideo_card": link,
        "price": int_price,
        "currency": currency,
        "site": 'www.mvideo.ru',
    }

    db_products.insert_one(data)

driver.close()

print()
count_i = len(list(db_products.find()))
pprint(count_i)

one = db_products.find_one({})
pprint(one)

db_products.drop()
