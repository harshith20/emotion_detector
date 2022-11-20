from flask import Flask, render_template, request
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import  session
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath,abspath
import requests
import pickle
import numpy as np
import json
import pandas as pd
from text_cleaning import text_cleaning
import models as dbHandler

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
model = pickle.load(open('finalized_model.pkl', 'rb'))
cv=  pickle.load(open('finalized_model_tfidf.pkl', 'rb'))
emo_la={0:'sadness',1:'joy',2:'love',3:'anger',4:'fear',5:'surprise'}

@app.route('/', methods=['POST', 'GET'])   
def home():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        dbHandler.insertUser(username, password)
        users = dbHandler.retrieveUsers()
        return render_template('login.html', users=users)
    else:
         return render_template('login.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    output=0
    if request.method == 'POST':
        sent=str(request.form['sentence'])
        text=list(str(sent).split("."))
        text=pd.Series(text)
        text=text.apply(lambda x:text_cleaning(x))
        text=text.apply(lambda x:' '.join(x))
        text = cv.transform(text)
        output=[emo_la[s] for s in model.predict(text)]
        return render_template("output.html",prediction=output)
    return render_template("predict.html")

if __name__=="__main__":
    app.run(debug=True)
