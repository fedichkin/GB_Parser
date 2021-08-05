# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# Буду использовать api от last.fm, будет передаваться название музыкального альбома на английском
# и по нему будет осуществляться поиск. Альбом будет передаваться как параметр при запуске скрипта

from sys import argv
import requests
import json
from fake_headers import Headers

music_album = argv[1]
api_key = "e93fdb1d84babe80cd8181d258207bc0"

url = f"http://ws.audioscrobbler.com/2.0/?method=album.search&album={music_album}&api_key={api_key}&format=json"
headers = Headers().generate()

response = requests.request("GET", url, headers=headers)

with open("album_search.json", "w") as f:
    json.dump(response.json(), f)
