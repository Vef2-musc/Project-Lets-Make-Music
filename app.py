#Hæ
#from crypt import methods
from distutils.command.config import config
import email
import os
from plistlib import UID
from tkinter import messagebox
from unicodedata import name
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.auth import get_user
from urllib import request
from flask import Flask, render_template, request, redirect, url_for, session
import re

print("hello")
app=Flask(__name__,template_folder='templates')

#FIREBASE
config = {
    'apiKey': "AIzaSyDx-6TLZW_nTueInaxRaLTesOaiYW1GtJU",
    'authDomain': "lets-make-music.firebaseapp.com",
    'projectId': "lets-make-music",
    'storageBucket': "lets-make-music.appspot.com",
    'messagingSenderId': "153066543311",
    'appId': "1:153066543311:web:2efa520260bb9f2316ffba",
    'measurementId': "G-3SK39RETG9",
    'databaseURL':"https://lets-make-music-default-rtdb.firebaseio.com/"#link a realtime database
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app.secret_key = 'admin-69420'
admin = firebase_admin
#-----------
#data={"name":"gusti","password":"abc123","music":["trommur","flautur"]}
#db.push(data)
users = db.child("User").get()
notend = []
for users in users.each():

    #print(users.val())
    notend.append(users.val())

#print(notend[1])

#-------------

@app.route('/')
def index():
    return render_template("index.html")
@app.route("/index", methods=['GET','POST'])
def forsida():
    if('user' in session):
        #print("virkar..")
        #return render_template('homepage.html')
        #-----
        users = db.child("User").get()
        gamers = []
        for users in users.each():

            #print(users.val())
            gamers.append(users.val())
        return render_template('acthomepage.html', username=session['user'],  len = len(gamers), gamers = gamers)
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:#ef þu nærð  að logga inn virkar try
            user = auth.sign_in_with_email_and_password(email,password)
            session['user'] = email
            print('virkar')
            
            #print(user['localId'])
            goomba = session["user"]
            #pull
            users = db.child("User").get()
            gamers = []
            for users in users.each():

                #print(users.val())
                gamers.append(users.val())
                
                
            return render_template("acthomepage.html",username = session['user'],  len = len(gamers), gamers = gamers)
        except:#ef þu nærð ekki að logga inn ferð þu aftur inna login siðuna
            #messagebox("password vitlaust")
            print('ekki virkar!!!')
            return render_template("index.html")
@app.route('/home')
def home():
    if 'user' in session:
        users = db.child("User").get()
        gamers = []
        for users in users.each():

            #print(users.val())
            gamers.append(users.val())
        return render_template('acthomepage.html', username=session['user'], len = len(gamers), gamers = gamers)
    return redirect(url_for('forsida'))

@app.route("/search", methods=['GET', 'POST'])
def leit():
    if 'user' in session:
        if request.method == 'POST':
            recname = str(request.form.get("Search"))
            Inst = request.form.get("instruments")
            Inst1 = request.form.get("instruments1")
            Inst2 = request.form.get("instruments2")
            print(Inst)
            print(Inst1)
            print(Inst2)
            print(recname)
        users = db.child("User").get()
        instrumm = db.child("User").child("Instrument").get()
        gamers = []
        for users in users.each():
            #print(users.val())
            if recname == "":
                gamers.append(users.val())
            elif users.val()["name"] == recname:
                gamers.append(users.val())
            else:
                pass
        return render_template('search.html', username=session['user'],len = len(gamers), gamers = gamers)
            
    return render_template("search.html")
@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        pwd = request.form.get("password")
        Inst = request.form.get("instruments")
        print(username)
        print(email)
        print(pwd)
        Inst1 = request.form.get("instruments1")
        Inst2 = request.form.get("instruments2")
        #InstLST =[Inst,Inst1,Inst2]
        print(Inst)
        print(Inst1)
        print(Inst2)
        data = {"name":username,"email":email,"Password":pwd,"Instrument":[Inst,Inst1,Inst2]}
        try:
            user = auth.create_user_with_email_and_password(email,pwd)
            print(data)
            db.child("User").push(data)
            print("signup complete")
            return render_template("correct.html")
        except:
            print('signup failed :(')
            return render_template("incorrect.html")
    return render_template("signup.html")
@app.route("/back")
def back():
    return redirect("/")
@app.route('/signout')
def signout():
    session.pop('user', None)
    session.pop('nafn', None)
    return redirect(url_for('index'))

@app.route('/yfirlit', methods=['GET','POST'])
def yfirlit():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
	liked = []
	session['liked'] = liked
	return render_template("yfirlit.html", liked=liked, name=name, email=email)

@app.errorhandler(404)
def error404(error):
	return "Site Not Found", 404


if __name__ == "__main__":
    app.run(debug=True)
