from time import sleep
import time
import requests
import json
import sys
sys.path.insert(0, '/app/secrets')
import key


def GetDataFromFootballAPI():

    baseUrl = "https://livescore-api.com/api-client/"
    apiKey = key.apiKey
    apiSecret =  key.apiSecret
    keyParam = { "key" : apiKey, "secret" : apiSecret }

    response = requests.get(baseUrl + "scores/live.json", params=keyParam) # READ

    x = json.loads(response.text)

    return x


def UpdateDatabaseWithMatchInformation(match):
    baseUrlBackend = "http://127.0.0.1:5000/"

    try:
        parameters = \
            {
                "id": str(match['id']),
                "away_name": match['away_name'],
                "competition_name": match['competition_name'],
                "country": match['country']['name'],
                "home_name": match['home_name'],
                "location": match['location'],
                "score": match['score'],
                "time": match['time'],
                "added": match['added']
            }
    except:
        print ("fail")
        return "fail"
    try:
        response = requests.get(baseUrlBackend + "repeater", json=parameters)
    except:
        print("fail")
        return "fail"
    print("test")
    return response
    # print("\n\n\n\n\n\n" + parameters + "\n\n\n\n\n\n")
   # response = requests.get(baseUrlBackend + "repeater", json=parameters) -

    #return response -

# def ClearOldMatchesFromDailyMatchesAndMoveToHistory():
#     return

def GetDataFromFootballAPIAndUpdateDatabase():
    jsonData = GetDataFromFootballAPI()


    matches = jsonData['data']['match']
    for match in matches:
        UpdateDatabaseWithMatchInformation(match)

moveToHistory = True

while True:
    currentTime = time.localtime(time.time())

    if currentTime.tm_hour == 1 and moveToHistory == True:
        # ClearOldMatchesFromDailyMatchesAndMoveToHistory()
        moveToHistory = False

    if currentTime.tm_hour == 2:
        moveToHistory = True

    GetDataFromFootballAPIAndUpdateDatabase()
    sleep(60)
