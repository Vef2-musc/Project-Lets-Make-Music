from distutils.command.config import config
import email
import pyrebase
import os
from flask import Flask, render_template,redirect

app=Flask(__name__,template_folder='templates')
@app.route("/")
def hello_world():
    return render_template("hompage.html")
@app.route("/forsida")
def forsida():
    return render_template("index.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/search")
def search():
    return render_template("search.html")
@app.route("/signup")
def search():
    return render_template("signup.html")
@app.route("/back")
def back():
    return redirect("/")

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

email = 'test@gmail.com'
password = '12345g'

user = auth.create_user_with_email_and_password(email,password)
print(user)

if __name__ == "__main__":
    app.run(debug=True)