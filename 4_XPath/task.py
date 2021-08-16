# Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

from lxml import html
import requests
import pandas as pd
from fake_headers import Headers
import re

header = Headers(headers=True).generate()


def parse_mail():
    data = []
    mail_url = "https://mail.ru/"

    response = requests.get(mail_url, headers=header)
    root = html.fromstring(response.text)

    items = root.xpath("//li[@data-testid=\"general-news-item\"]")

    for item in items:
        title = item.xpath(".//a/div/p/text()")
        href = item.xpath(".//a/@href")
        date = []

        if len(title) == 0:
            title = item.xpath(".//div/a/text()")

        if len(href) > 0:
            response = requests.get(href[0], headers=header)
            root = html.fromstring(response.text)

            date = root.xpath("//div[@data-news-id]/div[1]/span[1]/span/span/@datetime")

        data.append({
            "source": "mail.ru",
            "title_news": re.sub(r"\s", " ", title[0].strip()) if len(title) > 0 else "",
            "url_news": href[0].strip() if len(href) > 0 else "",
            "date": date[0].strip() if len(date) > 0 else ""
        })

    return data


def parse_lenta():
    data = []
    lenta_url = "https://lenta.ru/"

    response = requests.get(lenta_url, headers=header)
    root = html.fromstring(response.text)

    items = root.xpath("//*[@id='root']/section[2]/div/div/div[1]/section[1]/div[1]/div[1]")
    items = items + root.xpath("//*[@id='root']/section[2]/div/div/div[1]/section[1]/div[2]/div[contains(@class, 'item')]")

    for item in items:
        title = item.xpath(".//h2/a/text()")
        href = item.xpath(".//a/@href")
        date = item.xpath(".//time/@title")

        if len(title) == 0:
            title = item.xpath(".//a/text()")

        data.append({
            "source": "lenta.ru",
            "title_news": re.sub(r"\s", " ", title[0].strip()) if len(title) > 0 else "",
            "url_news": href[0].strip() if len(href) > 0 else "",
            "date": date[0].strip() if len(date) > 0 else ""
        })

    return data


result_data = pd.DataFrame(parse_mail() + parse_lenta())

print(result_data)

result_data.to_csv("news.csv", index=False)
