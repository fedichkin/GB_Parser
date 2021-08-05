# Задача: Посмотреть документацию к API GitHub, разобраться как вывести
# список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

# Скрипт должен запскаться с одним параметром, который должен содержать имя пользователя GitHub,
# для вывода списка его репозиториев

from sys import argv
import requests
import json
from fake_headers import Headers

user_name = argv[1]

print(user_name)

url = f"https://api.github.com/users/{user_name}/repos"
headers = Headers().generate()

response = requests.get(url, headers=headers)

with open("list_repo.json", "w") as f:
    json.dump(response.json(), f)
