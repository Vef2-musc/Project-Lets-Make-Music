#Hér að neðan er verið að ná í extensions/frammlengingarnar
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
        insesh = session['user']
        users = db.child("User").get()
        gamers = []
        #Hér er búinn til listi og farið er í gegnum hann svo aðgangurinn sem er verið að nota síðuna sér ekki sjálfan sig á heima síðunni en er síðan leift í search síðunni
        for users in users.each():
            if users.val()["email"] != insesh:  #Ef emailið á tilvikinu(userinum) er ekki emailið sem er verið að leita eftir er userinn settur í listan sem sínist á heimasíðunni
                gamers.append(users.val())
            else:
                pass
        
        return render_template('acthomepage.html', username=session['user'],  len = len(gamers), gamers = gamers)
    elif request.method == 'POST':
        #requests.post.get('user_id')
        #db.child("Friends").push()
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
            #Hér er búinn til listi og farið er í gegnum hann svo aðgangurinn sem er verið að nota síðuna sér ekki sjálfan sig á heima síðunni en er síðan leift í search síðunni
            for users in users.each():
                if users.val()["email"] != insesh:  #Ef emailið á tilvikinu(userinum) er ekki emailið sem er verið að leita eftir er userinn settur í listan sem sínist á heimasíðunni
                    gamers.append(users.val())
                else:
                    pass
                
                
            return render_template("acthomepage.html",username = session['user'],  len = len(gamers), gamers = gamers)
        except:
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

@app.route('/profile', methods=['GET','POST'])  #Profile, hugsað var að þessi síða myndi vera notuð til að breyta um aðgangs upplýsingar
def update():
    if 'user' in session:
        if request.method == "POST":    
            tusername =  request.form.get("username")   #Hér myndi vera tekið á móti nýum upplýsingum
            temail = request.form.get("email")
            tpwd = request.form.get("password")
            tInst = str(request.form.get("instruments"))
            tInst1 = str(request.form.get("instruments1"))
            tInst2 = str(request.form.get("instruments2"))
            tInst3 = str(request.form.get("instruments3"))
            tInst4 = str(request.form.get("instruments4"))
            tInst5 = str(request.form.get("instruments5"))
            tInst6 = str(request.form.get("instruments6"))
            tdata = {"name":tusername,"email":temail,"Password":tpwd,"Instrument":{0:tInst, 1:tInst1, 2:tInst2, 3:tInst3, 4:tInst4, 5:tInst5, 6:tInst6}} #Og sett upplýsingarnar í dictionary
            try:
                uid = users.get("localId")
                insesh = session['user']
                users = db.child("User").get()
                for users in users.each():
                    if users.val()["email"] == insesh:
                        print("Cringe ahh failure")
                        users.val().update({"name":tusername,"email":temail,"Password":tpwd,"Instrument":{0:tInst, 1:tInst1, 2:tInst2, 3:tInst3, 4:tInst4, 5:tInst5, 6:tInst6}})    #á að uppfæra upplýringarnar hér ef emailin pössuðu
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
            if musc!="None":
                musc = int(0)
            elif musc1!="None":
                musc1 = int(1)
            elif musc2!="None":
                musc2 = int(2)
            elif musc3!="None":
                musc3 = int(3)
            elif musc4!="None":
                musc4 = int(4)
            elif musc5!="None":
                musc5 = int(5)
            elif musc6!="None":
                musc6 = int(6)
        users = db.child("User").get()
        gamers = []
        for users in users.each():
            #print(users.val()["Instrument"])
            try:
                if recname == "":
                    gamers.append(users.val())
                elif users.val()["name"] == recname:
                    gamers.append(users.val())
                elif musc != "None" or musc1 != "None" or musc2 != "None" or musc3 != "None" or musc4 != "None" or musc5 != "None" or musc6 != "None":
                    for x in users.val()["Instrument"]:
                        if musc == int(x) or musc == x:
                            gamers.append(users.val())
                        elif musc1 == int(x):
                            gamers.append(users.val())
                        elif musc2 == int(x):
                            gamers.append(users.val())
                        elif musc3 == int(x):
                            gamers.append(users.val())
                        elif musc4 == int(x):
                            gamers.append(users.val())
                        elif musc5 == int(x):
                            gamers.append(users.val())
                        elif musc6 == int(x):
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
        pfp = request.form.get("pfp")
        print(username)
        print(email)
        print(pwd)
        print(pfp)
        Inst = request.form.get("instruments")
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
        #Dataið heldur um notendanafn, email, pasword, mynd, "vini" og hljóðfæri(sem eiga að vera í dictionary en stundum virkar það ekki fyrir einhverja ástæðu)
        data = {"name":username,"email":email,"Password":pwd,"Instrument":{0 : Inst, 1 : Inst1, 2 : Inst2, 3 : Inst3, 4 : Inst4, 5 : Inst5, 6 : Inst6},"pfp":completeName,"Friends":["-NDmJLe7PsxX79eeizQ4"]}
        print(data)
        #try:
        user = auth.create_user_with_email_and_password(email,pwd)  #Býr til user
        print(data)
        db.child("User").push(data) #Bætir upplýsingum hanns í databaseið
        print("signup complete")
        return render_template("correct.html")
        '''except:
            print('signup failed :(')
            return render_template("incorrect.html")'''
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
		#like---
        #fr = request.POST.get('user_id')   
        #fr = requests.POST.get("user_id")
        fr = requests.post.get('user_id')
        print(fr)
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
