import time
import requests
import json
import sys
sys.path.insert(0, '/app/secrets')
import key, key2




def GetDataFromFootballAPI():
    baseUrl = "https://livescore-api.com/api-client/"
    apiKey = key.apiKey
    apiSecret = key2.apiSecret
    keyParam = { "key" : apiKey, "secret" : apiSecret }

    response = requests.get(baseUrl + "scores/live.json", params=keyParam) # READ

    x = json.loads(response.text)

    return x


def UpdateDatabaseWithMatchInformation(match):
    baseUrlBackend = "http://backend-app-dev.dev:5000/"

    try:
        parameters = \
            {
                "id": str(match['id']),
                "away_name": match['away_name'],
                "competition_name": match['competition_name'],
                "home_name": match['home_name'],
                "location": match['location'],
                "score": match['score'],
                "time": match['time'],
                "added": match['added'],
                "country": match['country']['name'],
            }
    except:
        print("country is none, fixed it.")
        parameters = \
            {
                "id": str(match['id']),
                "away_name": match['away_name'],
                "competition_name": match['competition_name'],
                "home_name": match['home_name'],
                "location": match['location'],
                "score": match['score'],
                "time": match['time'],
                "added": match['added'],
                "country": "N/A"
            }
    try:
        response = requests.get(baseUrlBackend + "repeater", json=parameters)
    except Exception as e:
        print(e)
        print("faill")
        return "faill"
    print("test")
    return response
    # print("\n\n\n\n\n\n" + parameters + "\n\n\n\n\n\n")
   # response = requests.get(baseUrlBackend + "repeater", json=parameters) -

    #return response -

# def ClearOldMatchesFromDailyMatchesAndMoveToHistory():
#     return

def CheckForFinishedMatches():
    baseUrlBackend = "http://backend-app-dev.dev:5000/"

    try:
        response = requests.get(baseUrlBackend + "checkMatches")
    except Exception as e:
        print(e)

    if response.text == "not ok":
        print("woopsie poopsie")

    else:
        print("OKAYYYYY")

    return


def GetDataFromFootballAPIAndUpdateDatabase():
    jsonData = GetDataFromFootballAPI()

    matches = jsonData['data']['match']
    for match in matches:
        UpdateDatabaseWithMatchInformation(match)

moveToHistory = True
prevTime = 1

while True:
    currentTime = time.time()

    if currentTime - prevTime > 60:
        GetDataFromFootballAPIAndUpdateDatabase()
        CheckForFinishedMatches()

        prevTime = currentTime
