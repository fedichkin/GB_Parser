# Необходимо собрать информацию по продуктам питания с сайтов:
# Роскачество официальный сайт. Исследование качества продуктов питания | Рейтинг товаров.
# Список протестированных продуктов на сайте Росконтроль.рф
# Получившийся список должен содержать:
#
# Наименование продукта.
# Категорию продукта (например «Бакалея»).
# Подкатегорию продукта (например «Рис круглозерный»).
# Параметр «Безопасность».
# Параметр «Качество».
# Общий балл.
# Сайт, откуда получена информация.
#
# Структура должна быть одинаковая для продуктов с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через Pandas.

# Буду получать данные с сайтов двумя разными способами. На сайте Роскачества сложно парсить
# без применения селениум, так как часть информации скрыта и она подгружается асинхроно без смены адреса
# в адресной строке, но у сайта есть АПИ через которое можно получить всю информацию.
# На сайте Росконтроля АПИ нет, но там очень удобно парсить.

from bs4 import BeautifulSoup
import pandas as pd
import lxml
import requests
from fake_headers import Headers
import re
from sys import argv

header = Headers(headers=True).generate()

rskrf_base_url = "https://rskrf.ru/rest/1"
rskrf_id_catalog_food = 8

roscontrol_base_url = "https://roscontrol.com"

rskrf_products = []
roscontrol_products = []


def get_categories_rskrf():
    categories = []

    url = f"{rskrf_base_url}/catalog/categories/{rskrf_id_catalog_food}/"
    response = requests.get(url, headers=header)

    data = response.json()

    for category in data["response"]:
        categories.append({
            "id": category["id"],
            "name": category["title"]
        })

    return categories


def get_sub_categories_rskrf(category_id):
    sub_categories = []

    url = f"{rskrf_base_url}/catalog/categories/{category_id}/productGroups/"
    response = requests.get(url, headers=header)

    data = response.json()

    for sub_category in data["response"]["productGroups"]:
        sub_categories.append({
            "id": sub_category["id"],
            "name": sub_category["title"]
        })

    return sub_categories


def get_products_rskrf(sub_category_id, category_name, sub_category_name):
    products = []

    url = f"{rskrf_base_url}/catalog/products/{sub_category_id}/"
    response = requests.get(url, headers=header)

    data = response.json()

    for product in data["response"]["products"]:
        safety = [rat["value"] for rat in product["criteria_ratings"] if rat["title"].strip() == "Безопасность"]
        quality = [rat["value"] for rat in product["criteria_ratings"] if rat["title"].strip() == "Качество"]

        products.append({
            "category": category_name,
            "sub_category": sub_category_name,
            "name": product["title"],
            "total_rating": product["total_rating"],
            "safety": safety[0] if len(safety) > 0 else 0,
            "quality": quality[0] if len(quality) > 0 else 0,
            "source": "https://rskrf.ru/"
        })

    return products


def get_categories_roscontrol(category_url):
    categories = []

    url = f"{roscontrol_base_url}{category_url}"
    response = requests.get(url, headers=header)

    soup = BeautifulSoup(response.text, "lxml")
    categories_items = soup.select(".catalog__category-item")

    for item in categories_items:
        categories.append({
            "name": item.select(".catalog__category-name")[0].text.strip(),
            "url": item["href"]
        })

    return categories


def get_products_roscontrol(category_url, category_name, sub_category_name):
    products = []
    page = 1

    while True:
        url = f"{roscontrol_base_url}{category_url}?page={page}"
        response = requests.get(url, headers=header)

        if response.url == f"{roscontrol_base_url}{category_url}?page=1" and page > 1:
            break

        status_code = response.status_code
        page = page + 1

        if status_code != 200:
            break

        soup = BeautifulSoup(response.text, "lxml")
        products_items = soup.select(".block-product-catalog__item")

        if len(products_items) == 0:
            break

        for item in products_items:
            name = item.select(".product__item-title")[0].text.strip()
            total_rating = item.select(".product-rating .rate")
            total_rating = total_rating[0].text.strip() if len(total_rating) > 0 else 0
            rating_items = item.select(".rating-block div.row")
            safety = "0"
            quality = "0"

            for rating_item in rating_items:
                name_rating = rating_item.select(".left")[0].text.strip()

                if name_rating == "Безопасность":
                    safety = rating_item.select(".right")[0].text.strip()

                elif name_rating == "Качество":
                    quality = rating_item.select(".right")[0].text.strip()

            products.append({
                "category": category_name,
                "sub_category": sub_category_name,
                "name": name,
                "total_rating": total_rating,
                "safety": safety,
                "quality": quality,
                "source": "https://roscontrol.com/"
            })

    return products


categories_rskrf = get_categories_rskrf()

for category_rskrf in categories_rskrf:
    sub_categories_rskrf = get_sub_categories_rskrf(category_rskrf["id"])

    for sub_category_rskrf in sub_categories_rskrf:
        rskrf_products = rskrf_products + get_products_rskrf(
            sub_category_rskrf["id"],
            category_rskrf["name"],
            sub_category_rskrf["name"]
        )

categories_roscontrol = get_categories_roscontrol("/category/produkti/")

for category_roscontrol in categories_roscontrol:
    name_category = category_roscontrol["name"]
    url_category = category_roscontrol["url"]

    sub_categories_roscontrol = get_categories_roscontrol(url_category)

    for sub_category_roscontrol in sub_categories_roscontrol:
        name_sub_category = sub_category_roscontrol["name"]
        url_sub_category = sub_category_roscontrol["url"]

        roscontrol_products = roscontrol_products + get_products_roscontrol(
            url_sub_category,
            name_category,
            name_sub_category
        )

all_products = pd.DataFrame(rskrf_products + roscontrol_products);
print(all_products)

all_products.to_csv("products.csv")
