# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
# с сайтов Superjob и HH. Приложение должно анализировать несколько страниц сайта
# (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
#
# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
#
# (например, работодателя и расположение). Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.


# Приложение вызывается с аргументами, первый аргумент наименование вакансии, второй количество страниц для просмотра
from bs4 import BeautifulSoup
import pandas as pd
import lxml
import requests
from fake_headers import Headers
import re
from sys import argv

header = Headers(headers=True).generate()

vacancy = argv[1]
count_pages = int(argv[2])

superjob_base_url = "https://www.superjob.ru"
hh_base_url = "https://hh.ru"

superjob_vacancies = []
hh_vacancies = []


# парсим строку с зарплатой и вытаскиваем от туда минимальное и максимальное значение, если они есть
def get_info_salary(text_salary):
    min_template = r"от\s(\d+\s\d+)\s(.+)$"
    max_template = r"до\s(\d+\s\d+)\s(.+)$"
    all_template = r"(\d+\s\d+)\s[—,–]\s(\d+\s\d+)\s(.+)$"

    result = re.search(min_template, text_salary)

    if result:
        min_salary_text = result.group(1)
        min_salary_text = re.sub(r"\s", "", min_salary_text)

        currency = result.group(2).replace(".", "").replace("/месяц", "")

        return {"min": int(min_salary_text), "max": "", "currency": currency}

    result = re.search(max_template, text_salary)

    if result:
        max_salary_text = result.group(1)
        max_salary_text = re.sub(r"\s", "", max_salary_text)

        currency = result.group(2).replace(".", "").replace("/месяц", "")

        return {"min": "", "max": int(max_salary_text), "currency": currency}

    result = re.search(all_template, text_salary)

    if result:
        min_salary_text = result.group(1)
        min_salary_text = re.sub(r"\s", "", min_salary_text)

        max_salary_text = result.group(2)
        max_salary_text = re.sub(r"\s", "", max_salary_text)

        currency = result.group(3).replace(".", "").replace("/месяц", "")

        return {"min": int(min_salary_text), "max": int(max_salary_text), "currency": currency}

    return {"min": "", "max": "", "currency": ""}


# метож парсит страницу сайта superjob
def parse_page_superjob(page):
    data = []

    url = f"{superjob_base_url}/vacancy/search/?keywords={vacancy}&geo[t][0]=4&page={page}"
    response = requests.get(url, headers=header)

    if response.status_code != 200:
        return data

    soup = BeautifulSoup(response.text, "lxml")
    vacancy_items = soup.select(".f-test-search-result-item .f-test-vacancy-item")

    if len(vacancy_items) == 0:
        return data

    for item in vacancy_items:
        vacancy_link = item.select("[class*='f-test-link'][href*='/vakansii']")[0]
        vacancy_salary = item.select(".f-test-text-company-item-salary")[0].text
        vacancy_url = superjob_base_url + vacancy_link["href"]
        salary = get_info_salary(vacancy_salary.strip())

        data.append({
            "name": vacancy_link.text,
            "url": vacancy_url,
            "min_salary": salary["min"],
            "max_salary": salary["max"],
            "currency": salary["currency"],
            "resource": "www.superjob.ru"
        })

    return data


# метож парсит страницу сайта hh
def parse_page_hh(page):
    data = []

    url = f"{hh_base_url}/search/vacancy?fromSearchLine=true&st=searchVacancy&text={vacancy}t&area=1&page={page}"
    response = requests.get(url, headers=header)

    if response.status_code != 200:
        return data

    soup = BeautifulSoup(response.text, "lxml")
    vacancy_items = soup.select(".vacancy-serp-item")

    if len(vacancy_items) == 0:
        return data

    for item in vacancy_items:
        vacancy_info = item.select(".resume-search-item__name")[0]
        vacancy_name = vacancy_info.text
        vacancy_url = vacancy_info.select("a")[0]["href"]
        vacancy_salary = item.select("[data-qa='vacancy-serp__vacancy-compensation']")

        if len(vacancy_salary) > 0:
            salary = get_info_salary(vacancy_salary[0].text.strip())
        else:
            salary = {"min": "", "max": "", "currency": ""}

        data.append({
            "name": vacancy_name,
            "url": vacancy_url,
            "min_salary": salary["min"],
            "max_salary": salary["max"],
            "currency": salary["currency"],
            "resource": "www.hh.ru"
        })

    return data


# У superjob номера старницы начинаются с 1
for index in range(1, count_pages + 1):
    vacancies = parse_page_superjob(index)

    if len(vacancies) > 0:
        superjob_vacancies = superjob_vacancies + vacancies
    else:
        break

# У hh номера старницы начинаются с 0
for index in range(0, count_pages):
    vacancies = parse_page_hh(index)

    if len(vacancies) > 0:
        hh_vacancies = hh_vacancies + vacancies
    else:
        break

result_data = pd.DataFrame(superjob_vacancies + hh_vacancies)

print(result_data)

result_data.to_csv("vacancies.csv")
