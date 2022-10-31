from flask import Flask, request
import json
import requests
import config

app = Flask(__name__)


@app.route('/')

def mainPage():
    return renderMainPage()

def renderMainPage():
    return '<h1 style="text-align: center;margin-top: 50px">Hello and welcome to our Superbowl API</h1> \
    <p style="text-align: center">Try out /getAPI endpoint for more information.</p> \
    <p style="text-align: center">Or you could register by visiting /register.</p>'


@app.route('/itay')
def itay():
    return 'hey itay'


@app.route('/getAPI')
def getAPI():
    baseUrl = "https://livescore-api.com/api-client/"

    keyParam = {"key": config.apiKey, "secret": config.apiSecret}

    response = requests.get(baseUrl + "scores/live.json", params=keyParam)

    return response.json()


@app.route('/register')
def register():
    user = json.loads(request.data)

    return user['name']


if __name__ == '__main__':
    app.run()
