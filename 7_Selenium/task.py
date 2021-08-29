from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient


# метод собирает информацию о письмах с первой страницы mail.ru и записывает данные в БД
def get_letters(login, password, ip_bd, port_bd, name_bd, collection_bd):
    driver = webdriver.Chrome()

    driver.get("https://mail.ru/")

    wait = WebDriverWait(driver, 10)

    client = MongoClient(ip_bd, port_bd)
    db = client[name_bd]
    collection = db[collection_bd]

    try:
        email_input = wait.until(EC.element_to_be_clickable((By.NAME, "login")))
        email_input.send_keys(login, Keys.ENTER)

        password_input = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
        password_input.send_keys(password, Keys.ENTER)

        first_letter = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "js-letter-list-item")))

        letters = driver.find_elements_by_class_name("js-letter-list-item")
        letters_url = []

        for letter in letters:
            letters_url.append(letter.get_attribute("href"))

        for letter_url in letters_url:
            driver.get(letter_url)

            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "letter__author")))

            author = driver.find_element_by_css_selector(".letter__author .letter-contact")
            date = driver.find_element_by_css_selector(".letter__author .letter__date")
            title = driver.find_element_by_css_selector("h2.thread__subject")
            content = driver.find_element_by_css_selector(".letter-body__body-content")

            collection.insert_one(
                {"author": author.text, "date": date.text, "title": title.text, "content": content.text}
            )
    finally:
        driver.close()


# метод собирает хиты с онлайнтрейда и записывает их в БД
def get_hits_onlinetrade(ip_bd, port_bd, name_bd, collection_bd):
    driver = webdriver.Chrome()

    driver.get("https://www.onlinetrade.ru/")

    wait = WebDriverWait(driver, 10)

    client = MongoClient(ip_bd, port_bd)
    db = client[name_bd]
    collection = db[collection_bd]

    try:
        wait.until(EC.element_to_be_clickable((By.ID, "tabs_hits")))

        items = driver.find_elements_by_css_selector("#tabs_hits .indexGoods__item")
        items_url = []

        for item in items:
            items_url.append(item.find_element_by_class_name("indexGoods__item__name").get_attribute("href"))

        for item_url in items_url:
            driver.get(item_url)

            wait.until(EC.element_to_be_clickable((By.ID, "goods_content")))

            description = driver.find_element_by_css_selector("#goods_content h1").text
            price = driver.find_element_by_css_selector("#goods_content span[itemprop='price']").text

            collection.insert_one(
                {"description": description, "price": price}
            )
    finally:
        driver.close()
