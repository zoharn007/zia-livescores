import requests
import json
import config

baseUrl = "https://livescore-api.com/api-client/"

keyParam = {"key": config.apiKey, "secret": config.apiSecret}

response = requests.get(baseUrl + "scores/live.json", params=keyParam)  # READ
# getting the information from the API website

x = json.loads(response.text)
# help us to read the information from the API


print(x['success'])  # Filtering information from the data we got from the api

print(x['data']['match'][1]['odds'])  # Filtering the data throughout matches by picking them with these filters.
