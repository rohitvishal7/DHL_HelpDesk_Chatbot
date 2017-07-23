#!flask/bin/python
from flask import Flask,session,request
from flask import request
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pprint import pprint
from nltk.stem.wordnet import WordNetLemmatizer
from flask import make_response
import re
from textblob import TextBlob, Word
from chatterbot import ChatBot
from datetime import timedelta
import os


app = Flask(__name__)
#User's Session Setting
app.secret_key = os.urandom(24)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
app.permanent_session_lifetime = timedelta(seconds=100)


#User's Request
@app.route('/',methods = ['POST'])
def index():
    session.permanent = True

    #queries user can use to track their package
    package_query=['locate','find','track','where']

    #A json to send our frontend a response
    responsedata = {}

    #The variable that will hold user's query
    query = ""

    #expecting a POST request
    if request.method == "POST":

        #Ajax call send user's query in json with key 'user'
        query=request.form['user'].lower()

        #Correct's the typo from user's end(spelling correction)
        b = TextBlob(query)
        query=str(b.correct())

    #Natural Language processing to receive the word in base form
    tokens = nltk.word_tokenize(query)
    lmtzr = WordNetLemmatizer()

    for x in tokens:
        x=lmtzr.lemmatize(x)
        w = Word(x)
        x=w.lemmatize("v")
        '''
        A package has three attributes:-
        id(a unique id associated with every package which help us to track them),
        speed(if the user want the package to be slower or faster than schedule),
        days(the number of days with which a user want to slower or speed up their package)
        '''
        if x=='fast' or x=='slow' or x=='delay':
            session['speed']=x
            if session.get('uid')!=None:
                responsedata['HelpDesk'] = "Please provide number of days you want your package of ID " + session.get('uid') + " to be " + session['speed'] + " than schedule"
                json_data = json.dumps(responsedata)
                return json_data
        if x.isdigit() and session.get('uid')!=None and session.get('speed')!=None:
            session['days']=x
            responsedata['HelpDesk'] = "Your package of ID " + session.get('uid') + " will be reaching in "+ session['days']+" days " + session['speed']+" than schedule"
            json_data = json.dumps(responsedata)
            return json_data


        if x in package_query:
            for z in tokens:

                #We assume the id to be a combination of characters and numbers
                if any(char.isdigit() for char in z):
                    responsedata['HelpDesk'] = "Your package of ID "+ z +" will be reaching as per schedule days"
                    session['uid']=z
                    json_data = json.dumps(responsedata)
                    return json_data
            responsedata['HelpDesk'] = "Please provide a valid tracking ID "
            json_data = json.dumps(responsedata)
            return json_data


    for z in tokens:
            if any(char.isdigit() for char in z):
                responsedata['HelpDesk'] = "Your package of ID " + z + " will be reaching as per schedule days"
                session['uid'] = z
                json_data = json.dumps(responsedata)
                return json_data

    #Our chatbot is trained to have engaging general conversation as well
    chatbot = ChatBot('Ron Obvious', trainer='chatterbot.trainers.ChatterBotCorpusTrainer')

    # Train based on the english corpus
    chatbot.train("chatterbot.corpus.english")


    responsedata['HelpDesk'] = str(chatbot.get_response(query))
    json_data = json.dumps(responsedata)
    return json_data


if __name__ == '__main__':
    app.run( host="127.0.0.1", port=int("2015"))