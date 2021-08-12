from pymongo import MongoClient
import pandas as pd
import math
import re


# метод для записи данных по вакансиям из csv файла, который был создан как результат парсинга
# метод принемает в качестве параметров путь до файла, ip адрес и порт базы данных MongoDB,
# наименование базы данных и наименование коллекции куда будет производится запись
# метод не записывает в базу те поля что не имеют значения
def write_vacancies_to_mongodb(csv_file, ip, port, bd, collection):
    vacancies_df = pd.read_csv(csv_file)

    client = MongoClient(ip, port)
    db = client[bd]
    vacancies = db[collection]

    for index, row in vacancies_df.iterrows():
        record = {}

        for key, value in row.iteritems():
            if isinstance(value, float) and math.isnan(value):
                continue

            record[key] = value

        vacancies.insert_one(record)


# метод ищет и выводит в консоль те вакансии у которых указана зарплата и она больше переданной в качестве параметра
# так же в метод переводится валюта по которой стоит искать зарплату
def search_by_salary(min_salary, currency, ip, port, bd, collection):
    client = MongoClient(ip, port)
    db = client[bd]
    vacancies = db[collection]

    records = vacancies.find(
        {"$or": [
            {"min_salary": {"$gt": min_salary}},
            {"min_salary": {"$exists": False}, "max_salary": {"$gt": min_salary}}
        ],
            "currency": re.compile(currency, re.IGNORECASE)}
    )

    for record in records:
        print(record)


# метод добавляет новые вакансии из csv файла
# предпологается что в файле могут быть как новые вакансии так и уже добавленные,
# для этого перед добавлением мы ещем текущую вакансию в базе данных по url, если вакансия не найдена - добавляем её
def write_new_vacancies_to_mongodb(csv_file, ip, port, bd, collection):
    vacancies_df = pd.read_csv(csv_file)

    client = MongoClient(ip, port)
    db = client[bd]
    vacancies = db[collection]

    for index, row in vacancies_df.iterrows():
        record = {}

        if vacancies.count_documents({"url": row["url"]}) > 0:
            continue

        for key, value in row.iteritems():
            if isinstance(value, float) and math.isnan(value):
                continue

            record[key] = value

        vacancies.insert_one(record)


# write_vacancies_to_mongodb("../2_parseHTML/vacancies.csv", "localhost", 27017, "job", "vacancies")

# search_by_salary(100000, "руб", "localhost", 27017, "job", "vacancies")

# write_new_vacancies_to_mongodb("../2_parseHTML/vacancies.csv", "localhost", 27017, "job", "vacancies")
