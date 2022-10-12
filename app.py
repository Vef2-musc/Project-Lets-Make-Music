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
import requests
import shutil
import random

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

#Fire base code base
#--------
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app.secret_key = 'admin-69420'
admin = firebase_admin
#-----------
users = db.child("User").get()
notend = []
for users in users.each():
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
        insesh = session['user']
        users = db.child("User").get()
        gamers = []
        for users in users.each():
            if users.val()["email"] != insesh:
                gamers.append(users.val())
            else:
                pass
        return render_template('acthomepage.html', username=session['user'],  len = len(gamers), gamers = gamers)
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:#ef þu nærð  að logga inn virkar try
            user = auth.sign_in_with_email_and_password(email,password)
            users = db.child("User").get()
            userObj = {}
            for users in users.each():
                    if users.val()["email"] == email:
                        userObj = users.val()
                        
                    else:
                        pass
            session['user'] = userObj
            #hello
            #print(user['localId'])
            goomba = session["user"]
            #pull
            insesh = session['user']
            users = db.child("User").get()
            gamers = []
            for users in users.each():
                if users.val()["email"] != insesh:
                    gamers.append(users.val())
                else:
                    pass
                
                
            return render_template("acthomepage.html",username = session['user'],  len = len(gamers), gamers = gamers)
        except:#ef þu nærð ekki að logga inn ferð þu aftur inna login siðuna
            #messagebox("password vitlaust")
            print('ekki virkar!!!')
            return render_template("index.html")
@app.route('/home')
def home():
    if 'user' in session:
        insesh = session['user']
        users = db.child("User").get()
        gamers = []
        for users in users.each():
            if users.val()["email"] != insesh:
                gamers.append(users.val())
                
            else:
                pass
        return render_template('acthomepage.html', username=session['user'], len = len(gamers), gamers = gamers)
    return redirect(url_for('forsida'))

@app.route('/profile', methods=['GET','POST'])
def update():
    if 'user' in session:
        if request.method == "POST":
            tusername =  request.form.get("username")
            temail = request.form.get("email")
            tpwd = request.form.get("password")
            tInst = request.form.get("instruments")
            tInst1 = request.form.get("instruments1")
            tInst2 = request.form.get("instruments2")
            tInst3 = request.form.get("instruments3")
            tInst4 = request.form.get("instruments4")
            tInst5 = request.form.get("instruments5")
            tInst6 = request.form.get("instruments6")
            tdata = {"name":tusername,"email":temail,"Password":tpwd,"Instrument":[tInst,tInst1,tInst2,tInst3,tInst4,tInst5,tInst6]}
            try:
                uid = users.get("localId")
                insesh = session['user']
                users = db.child("User").get()
                for users in users.each():
                    if users.val()["email"] == insesh:
                        print("Cringe ahh failure")
                        db.child("User").child(users.key()).update({"name":tusername,"email":temail,"Password":tpwd,"Instrument":[tInst,tInst1,tInst2,tInst3,tInst4,tInst5,tInst6]})
                    else:   
                        pass
                return render_template('profile.html', username=session['user'])
            except:
                print("intial loading")
    return render_template('profile.html', username=session['user'])

                



@app.route("/search", methods=['GET', 'POST'])
def leit():
    if 'user' in session:
        if request.method == 'POST':
            recname = str(request.form.get("Search"))
            musc = str(request.form.get("instruments"))
            musc1 = str(request.form.get("instruments1"))
            musc2 = str(request.form.get("instruments2"))
            musc3 = str(request.form.get("instruments3"))
            musc4 = str(request.form.get("instruments4"))
            musc5 = str(request.form.get("instruments5"))
            musc6 = str(request.form.get("instruments6"))
        users = db.child("User").get()
        gamers = []
        for users in users.each():
            #print(users.val())
            try:
                if recname == "":
                    gamers.append(users.val())
                elif users.val()["name"] == recname:
                    gamers.append(users.val())
                elif musc != "None" or musc1 != "None" or musc2 != "None" or musc3 != "None" or musc4 != "None" or musc5 != "None" or musc6 != "None":
                    for x in users.val()["Instrument"]:
                        if musc == x:
                            gamers.append(users.val())
                            break
                        elif musc1 == x:
                            gamers.append(users.val())
                        elif musc2 == x:
                            gamers.append(users.val())
                        elif musc3 == x:
                            gamers.append(users.val())
                        elif musc4 == x:
                            gamers.append(users.val())
                        elif musc5 == x:
                            gamers.append(users.val())
                        elif musc6 == x:
                            gamers.append(users.val())
                elif musc == "None" and musc1 == "None" and musc2 == "None" and musc3 == "None" and musc4 == "None" and musc5 == "None" and musc6 == "None":
                    gamers.append(users.val())
                else:
                    pass
            except:
                gamers.append(users.val())
        return render_template('search.html', username=session['user'],len = len(gamers), gamers = gamers)
            
    return render_template("search.html")
@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        pwd = request.form.get("password")
        Inst = request.form.get("instruments")
        pfp = request.form.get("pfp")
        print(username)
        print(email)
        print(pwd)
        print(pfp)
        Inst1 = request.form.get("instruments1")
        Inst2 = request.form.get("instruments2")
        Inst3 = request.form.get("instruments3")
        Inst4 = request.form.get("instruments4")
        Inst5 = request.form.get("instruments5")
        Inst6 = request.form.get("instruments6")
        #InstLST =[Inst,Inst1,Inst2]
        instlist = []
        #if Inst != None:
            #instlist.append(Inst)
        
        #elif Inst1 != None:    
            #instlist.append(Inst1)
        #elif Inst2 != None:    
            #instlist.append(Inst2)
        #elif Inst3 != None:
            #instlist.append(Inst3)
        #elif Inst4 != None:
            #instlist.append(Inst4)
        #elif Inst5 != None:
           # instlist.append(Inst5)
        #elif Inst2 != None:
          #  instlist.append(Inst6)
        print(instlist)
        randomnum = str(random.randint(0, 1000))
        image_url = pfp
        filename = "pic"+ randomnum +".jpg"
        save_path = 'static\images'
        completeName = os.path.join(save_path, filename)
        r = requests.get(image_url, stream = True)
        instlst = []
        #for x in range[0, 8]:

        # Check image 
        if r.status_code == 200:
            
            # Preventing the downloaded image’s size from being zero.
            r.raw.decode_content = True
            
            # Open a local file
            with open(completeName, "wb") as f:
                shutil.copyfileobj(r.raw, f)
            print(f)
            print('Image successfully Downloaded: ',filename)
        else:
            print('Image Couldn\'t be retrieved')


        print('keyri hér')
        data = {"name":username,"email":email,"Password":pwd,"Instrument":[Inst,Inst1,Inst2,Inst3,Inst4,Inst5,Inst5],"pfp":completeName,"Friends":["-NDmJLe7PsxX79eeizQ4"]}
        print(data)
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
@app.route('/messages', methods=['GET','POST'])
def messages():
    friends = session['user']['Friends']
    #db.child("Friends").get(notend[1,2])
    return render_template("messages.html", username=session['user'], len = len(friends), friends = friends)
@app.errorhandler(404)
def error404(error):
	return "Site Not Found", 404


if __name__ == "__main__":
    app.run(debug=True)
