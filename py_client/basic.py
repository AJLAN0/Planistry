import requests

endpoints = "http://localhost:8000/api/"

get_response = requests.get(endpoints,json=({"produc_id":123}))
print(get_response.json())
print(get_response.status_code)