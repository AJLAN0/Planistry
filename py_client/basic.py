import requests

endpoints = "https://httpbin.org/anything"

get_response = requests.get(endpoints)
print(get_response.text)