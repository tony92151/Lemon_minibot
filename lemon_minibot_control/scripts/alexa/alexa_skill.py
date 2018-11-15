#!/usr/bin/python

#refense https://www.youtube.com/watch?v=DFiCsMcipr4&index=1&list=PLQVvvaa0QuDe3E0TlV7q7bFyMqbnO5-TL

# sudo apt-get install ngrok-client
# sudo pip install request
# sudo pip install flask
# sudo pip install flask-ask
# sudo pip install requests
# sudo pip install unidecode

from flask import Flask

from flask_ask import Ask , statement , question , session

import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/minibot_controller")



@ask.launch
def launch():
    speech_text = 'Welcome to the lemon minibot, I am your personal guiding robot,If you would like to control me, just say go and command, like, Go forward, or Go backward, or go left, or go right'
    return question(speech_text)

@ask.intent('HelloIntent', default={'name': 'World'})
def hello(name):
    return statement('Hello, {}'.format(name))

@ask.intent('action')
def hello_world():
    speech_text = 'kick me'
    return statement(speech_text).simple_card('HelloWorld', speech_text)


@ask.intent('')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    app.run(debug=True)
