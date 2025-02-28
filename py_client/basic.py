import requests

endpoints = "http://localhost:8000/"

get_response = requests.get(endpoints)
print(get_response.text)
print(get_response.status_code)