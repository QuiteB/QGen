import requests
import json

url = "https://qzzer-12e5.restdb.io/rest/results"

payload = json.dumps( {"username": "xyz","score": "45","datetime": "21:07:22 16/05/2022","musername": "ola","quiz-id": "54i32"} )
headers = {
    'content-type': "application/json",
    'x-apikey': "bfa1088aaa5530a2628324f31064aa3d06a4f",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)