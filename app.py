#from crypt import methods
from distutils.command.config import config
import email
import os
from urllib import request
from flask import Flask,session, render_template,redirect,request
import pyrebase

app=Flask(__name__,template_folder='templates')
@app.route('/')
def hello_world():
    return render_template("hompage.html")
@app.route("/forsida")
def forsida():
    return render_template("index.html")
@app.route("/login", methods=['POST','GET'])
def login():
    if('user' in session):
        return 'Hi, {}'.format(session['user'])
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = email
        except:
            return 'Failed to login :('
    #þarf sign in siðu og lata gusta vita með það
    #þarf lika logout til að henda code þar :)
    #log out : session.pop('user')
    #return redirect ('/')
    return render_template("login.html")
@app.route("/search")
def leit():
    return render_template("search.html")
@app.route("/signup")
def signup():
    return render_template("signup.html")
@app.route("/back")
def back():
    return redirect("/")
#----------

#FIREBASE
config = {
    'apiKey': "AIzaSyDx-6TLZW_nTueInaxRaLTesOaiYW1GtJU",
    'authDomain': "lets-make-music.firebaseapp.com",
    'projectId': "lets-make-music",
    'storageBucket': "lets-make-music.appspot.com",
    'messagingSenderId': "153066543311",
    'appId': "1:153066543311:web:2efa520260bb9f2316ffba",
    'measurementId': "G-3SK39RETG9",
    'databaseURL':""
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = 'admin-69420'

#------------


if __name__ == "__main__":
    app.run(debug=True)