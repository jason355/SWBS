import requests
import json

respond = requests.get(
    "https://b9d6-2001-b011-3-141f-9cf0-369c-f75-fbfd.ngrok-free.app/104")


print(respond.content)
