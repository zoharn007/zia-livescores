import datetime
import time
from email import message
import uuid
from flask import Flask, request
import json
import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import random
from decimal import Decimal
import os

dynamoResource = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamoResource.Table('LiveScore')
dynamoClient = boto3.client('dynamodb', region_name='eu-west-1')

snsClient = boto3.client('sns', region_name='eu-west-1')

app = Flask(__name__)



def renderMainPage():
    return '<h1 style="text-align: center;margin-top: 50px">Hello and welcome to our Superbowl API</h1> \
    <p style="text-align: center">Try out /getAPI endpoint for more information.</p> \
    <p style="text-align: center">Or you could register by visiting /register.</p>'


@app.route('/sendSMS')
def sendSMS():
    messageBody = json.loads(request.data)

    try:
        phone = messageBody['Phone']

    except:
        return "No phone provided."

    try:
        message = messageBody['Message']

    except:
        return "No message provided."

    sendMessageToPhoneNumber(phone, message)

    return "SMS sent"


def sendSMSInternal(phone: str, message: str):
    sendMessageToPhoneNumber(phone, message)
    print(message)


@app.route('/enterCode')
def enterCode():
    messageBody = json.loads(request.data)

    try:
        code = messageBody['Code']
        phoneNumber = messageBody['Phone']

    except:
        return "No code provided."

    returnValue = checkIfCodePhoneComboExists(phoneNumber, code)

    if (returnValue > 0):

        key = {
            'Phone': {'S': str(phoneNumber)},
            'Code': {'S': str(code)}
        }

        dynamoClient.delete_item(TableName='codes', Key=key)

        registerUser(phoneNumber)

        return "Registered successfully!"

    elif (returnValue == 0):
        return "Incorrect code!"

    elif (returnValue == -1):
        return "Code expired!"


@app.route('/register')
def register():
    messageBody = json.loads(request.data)

    try:
        phoneNumber = messageBody['Phone']

    except:
        return "No phone number provided."

    if (checkIfPhoneNumberExists(phoneNumber)):
        return "Account already exists, you cannot register."

    else:
        sendCodeToUser(phoneNumber)
        return "Ok"


def sendCodeToUser(phoneNumber: str):
    seconds = time.time()

    random.seed(seconds)

    randomNumber = random.randint(0, 9999)

    addCodeToUser(phoneNumber, str(randomNumber), Decimal(seconds))
    sendSMSInternal(phoneNumber, "Here is your temporary code: " + str(randomNumber))


def sendCodeToUserAfterLastCodeExpired(phoneNumber: str):
    seconds = time.time()

    random.seed(seconds)

    randomNumber = random.randint(0, 9999)

    addCodeToUser(phoneNumber, str(randomNumber), Decimal(seconds))
    sendSMSInternal(phoneNumber, "Your previous code expired, here's your new code: " + str(randomNumber))


def addCodeToUser(phoneNumber: str, code: str, seconds: Decimal):
    user = {
        'Code': {'S': code},
        'Phone': {'S': phoneNumber},
        'Seconds': {'N': str(seconds)}
    }

    dynamoClient.put_item(Item=user, TableName='codes')


def registerUser(phoneNumber: str):
    user = {
        'ID': {'S': str(uuid.uuid4())},
        'Phone': {'S': phoneNumber}
    }

    dynamoClient.put_item(Item=user, TableName='users')


def checkIfPhoneNumberExists(phoneNumber: str):
    usersTable = dynamoResource.Table('users')

    response = usersTable.scan(
        FilterExpression=Attr('Phone').eq(phoneNumber)
    )

    itemsDict = response['Items']

    return len(itemsDict)


def checkIfCodePhoneComboExists(phone: str, code: str):
    usersTable = dynamoResource.Table('codes')

    response = usersTable.scan(
        FilterExpression=Attr('Code').eq(code) & Attr('Phone').eq(phone)
    )

    itemsDict = response['Items']

    end = time.time()

    if (validate_code(itemsDict[0]['Seconds'], end) == 0):
        sendCodeToUserAfterLastCodeExpired(itemsDict[0]['Phone'])
        return -1

    return len(itemsDict)


def validate_code(start, end):
    if (end - start > 30):
        return 0
    else:
        return 1


def sendMessageToPhoneNumber(phoneNumber: str, message: str):
    snsClient.publish(PhoneNumber=phoneNumber, Message=message)


def get_result(match):
    response = table.query(KeyConditionExpression=Key('ID').eq(match))
    return str(response['Items'][0]['Home']) + " " + str(response['Items'][0]['Score']) + " " + str(response['Items'][0]['Away'])


def get_time(match):
    response = table.query(KeyConditionExpression=Key('ID').eq(match))
    return response['Items'][0]['Time']

def checkIfTeamExists(matchID: str):
    teamsTable = dynamoResource.Table('LiveScore')

    response = teamsTable.scan(
        FilterExpression=Attr('ID').eq(matchID)
    )

    itemsDict = response['Items']

    return len(itemsDict)

@app.route ('/score')
def get_match_score():
    messageBody = json.loads(request.data)
    try:
        matchID = messageBody['MatchID']
    except:
        return "No such team, please provide a different team name."

    if checkIfTeamExists(matchID):
        return get_result(matchID)
    else:
        return "No such team, please provide a different team name."


@app.route ('/time')
def get_match_time():
    messageBody = json.loads(request.data)
    try:
        matchID = messageBody['MatchID']
    except:
        return "No such team, please provide a different team name."

    if checkIfTeamExists(matchID):
        return get_time(matchID)
    else:
        return "No such team, please provide a different team name."

@app.route ('/repeater')
def get_from_repeater():

    try:
        messageBody = json.loads(request.data)

        id = messageBody['id']
        away = messageBody['away_name']
        competition = messageBody['competition_name']
        country = messageBody['country']
        home = messageBody['home_name']
        location = messageBody['location']
        score = messageBody['score']
        time1 = messageBody['time']
        date = messageBody['added']

        parsedDayTime = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
        
        day = parsedDayTime.day
        month = parsedDayTime.month
        year = parsedDayTime.year

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return "Problem with json input!"

    table.put_item(
        Item={
            'ID': id,
            'Away': away,
            'Competition': competition,
            'Country': country,
            'Home': home,
            'Location': location,
            'Score': score,
            'Time': time1,
            'Date': date,
            'Day': day,
            'Month': month,
            'Year': year
        }
    )

    print("import to DB completed successfully")

    return "import to DB completed successfully"
    #if checkIfTeamExists(id):
    #    return get_time(id)
    #else:
    #    return "No such team, please provide a different team name."

@app.route('/sign_in')
def sign_in():
    messageBody = json.loads(request.data)
    try:
        phoneNumber = messageBody['Phone']

    except:

        return "No phone number provided."
    if (checkIfPhoneNumberExists(phoneNumber)):

        setLoggedInFlagInDatabase(phoneNumber, True)

        return "successfully logged in"
    else:
        return "phone number not found please register"

def setLoggedInFlagInDatabase(phoneNumber, state):

    if(checkIfPhoneNumberExists(phoneNumber)):

        user = {
            'Phone': {'S': phoneNumber},
            'LoggedIn': {'S': state}
        }

        dynamoClient.put_item(Item=user, TableName='users')

    return

def checkLoggedInFlag(phoneNumber):

    usersTable = dynamoResource.Table('users')

    response = usersTable.scan(
        FilterExpression=Attr('Phone').eq(phoneNumber)
    )

    itemsDict = response['Items']

    print(itemsDict[0]['LoggedIn'])

    return itemsDict[0]['LoggedIn']

def subscribePhoneNumberToMatchID(phoneNumber, matchID):

    if(not checkLoggedInFlag(phoneNumber)):
        return "Not logged in"

    if(checkIfPhoneNumberAndMatchIDComboExistInSubscriptionsTable(phoneNumber, matchID)):
        return "Duplicate subscription detected"

    user = {
        'ID': {'S': uuid.uuid4()},
        'Phone': {'S': phoneNumber}, 
        'MatchID': {'S': matchID}
    }

    dynamoClient.put_item(Item=user, TableName='Subscriptions')

    return

def checkIfPhoneNumberAndMatchIDComboExistInSubscriptionsTable(phoneNumber, matchID):

    subscriptionsTable = dynamoResource.Table('Subscriptions')

    response = subscriptionsTable.scan(
        FilterExpression=Attr('Phone').eq(phoneNumber) and Attr('MatchID').eq(matchID)
    )

    itemsDict = response['Items']

    return len(itemsDict)

@app.route('/hey')
def checkDatabaseForScoreChangesInMatchesAndSendSMSWithResult():

    dailyMatches = getListOfDailyMatches()

    try:
        for match in dailyMatches:

            if(match['Time'] == "FT"):

                subscriptionList = getSubscriptionListByMatchID(match['id'])

                for subscriber in subscriptionList:

                    sendSMSInternal(str(subscriber['Phone']), str(match['score']))
                    deleteSubscription(subscriber['Phone'], match['id'])

    except:

        return "not ok"

    return "ok"

def getScoreByMatchID(matchID):
    
    if checkIfTeamExists(matchID):
        return get_result(matchID)
    else:
        return "No such team, please provide a different team name."

def getListOfDailyMatches():

    currentTime = time.localtime(time.time())

    teamsTable = dynamoResource.Table('LiveScore')

    response = teamsTable.scan(
        FilterExpression=Attr('Day').eq(currentTime.tm_mday) and Attr('Month').eq(currentTime.tm_mon) and Attr('Year').eq(currentTime.tm_year)
    )

    itemsDict = response['Items']

    return itemsDict

def getListOfHistoryMatches(startDate, endDate): #inclusive

    startTime = time.localtime(startDate)
    endTime = time.localtime(endDate)

    teamsTable = dynamoResource.Table('LiveScore')

    response = teamsTable.scan(
        FilterExpression=
            (Attr('Day').gte(startTime.tm_mday) and Attr('Month').gte(startTime.tm_mon) and Attr('Year').gte(startTime.tm_year))
            and
            (Attr('Day').lte(endTime.tm_mday) and Attr('Month').lte(endTime.tm_mon) and Attr('Year').lte(endTime.tm_year))

    )

    itemsDict = response['Items']

    return itemsDict

def deleteSubscription(phoneNumber, matchID):

    key = {
        'Phone': {'S': phoneNumber},
        'MatchID': {'S': matchID}
    }

    dynamoClient.delete_item(TableName = 'Subscriptions', Key = key)

    return

def getSubscriptionListByMatchID(matchID):

    teamsTable = dynamoResource.Table('Subscriptions')

    response = teamsTable.scan(
        FilterExpression=Attr('MatchID').eq(matchID)
    )

    return response['Items']






#if __name__ == '__main__':
#    app.run()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

