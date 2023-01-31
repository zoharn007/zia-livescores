from flask import Flask, render_template
import boto3
import os
import time
from flask import jsonify
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

import json

from flask import Flask, request
import random
dynamoClient = boto3.client('dynamodb', region_name='eu-west-1')

app = Flask(__name__)

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('Daily')
dynamoResource = boto3.resource('dynamodb', region_name='eu-west-1')
snsClient = boto3.client('sns', region_name='eu-central-1')
# Retrieve data from DynamoDB
#data = table.scan()['Items']

@app.route('/')
def index():
    # Render template and pass data as argument
    data = table.scan()['Items']
    data = sorted(data, key=lambda x: x['Date'], reverse=True)

    return render_template('template.html', data=data)


@app.route('/getdailymatches', methods = ['GET', 'POST'])
def getDailyMatches():

    currentTime = time.localtime(time.time())
    teamsTable = dynamoResource.Table('Daily')

    response = teamsTable.scan(
        FilterExpression=Attr('Day').eq(currentTime.tm_mday) and Attr('Month').eq(currentTime.tm_mon) and Attr('Year').eq(currentTime.tm_year)
    )

    itemsDict = response['Items']

    return jsonify(itemsDict)

@app.route('/register', methods = ['GET', 'POST'])
def register():

    #print(request.data)

    messageBody = json.loads(request.data)

    try:
        phoneNumber = messageBody['Phone']

    except:
        return "No phone number provided."

    if checkIfPhoneNumberExists(phoneNumber):
        return "Account already exists, you cannot register."

    else:
        sendCodeToUser(phoneNumber)
        return jsonify("Ok")


def checkIfPhoneNumberExists(phoneNumber: str):
    usersTable = dynamoResource.Table('users')

    response = usersTable.scan(
        FilterExpression=Attr('Phone').eq(phoneNumber)
    )

    itemsDict = response['Items']

    return len(itemsDict)


def sendCodeToUser(phoneNumber: str):
    seconds = time.time()

    random.seed(seconds)

    randomNumber = random.randint(0, 9999)

    addCodeToUser(phoneNumber, str(randomNumber), Decimal(seconds))
    sendSMSInternal(phoneNumber, "Here is your temporary code: " + str(randomNumber))



def addCodeToUser(phoneNumber: str, code: str, seconds: Decimal):
    user = {
        'Code': {'S': code},
        'Phone': {'S': phoneNumber},
        'Seconds': {'N': str(seconds)}
    }

    dynamoClient.put_item(Item=user, TableName='codes')


def sendSMSInternal(phone: str, message: str):
    sendMessageToPhoneNumber(phone, message)
    print(message)


def sendMessageToPhoneNumber(phoneNumber: str, message: str):
    snsClient.publish(PhoneNumber=phoneNumber, Message=message)


#if __name__ == '__main__':
#    app.run()

# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(debug=True, host='0.0.0.0', port=port)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

