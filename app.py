#Hæ
#from crypt import methods
from distutils.command.config import config
import email
import os
import pyrebase
from urllib import request
from flask import Flask, render_template, request, redirect, url_for, session
import re


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
    'databaseURL':""
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = 'admin-69420'

#-------------

@app.route('/')
def index():
    return render_template("index.html")
@app.route("/login", methods=['GET','POST'])
def forsida():
    if('user' in session):
        #print("virkar..")
        #return render_template('homepage.html')
        return render_template('acthomepage.html')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            session['user'] = email
            print('virkar')
            goomba = session["user"]
            return render_template("correct.html",grom = session['user'])
        except:
            print('ekki virkar!!!')
            return render_template("incorrect.html")
    return render_template("acthomepage.html")
@app.route("/home")
def home():
    return render_template("acthomepage.html")
#@app.route("/login", methods=['GET','POST'])
#def login():
    
    #return render_template("login.html")
#@app.route('/loggedin')
#def loggedin():
    #return render_template("acthomepage.html")

@app.route("/search")
def leit():
    return render_template("search.html")
@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get("username")
        pwd = request.form.get("password")
        try:
            user = auth.create_user_with_email_and_password(email,pwd)
            print("signin complete")
            return render_template("correct.html")
        except:
            print('ekki virkar!!!')
            return render_template("incorrect.html")
    return render_template("index.html")
@app.route("/back")
def back():
    return redirect("/")
@app.route('/signout')
def signout():
    session.pop('user', None)
    session.pop('nafn', None)
    return redirect(url_for('forsida'))

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

#----------

#allt commentaða er eftir Guðjón og var bara að fikta svo ég gæti unnið betur í CSS
#@app.route('/', methods=['GET', 'POST'])
#def login():
#    msg = ''
#    if request.method == 'POST' and 'user' in request.form and 'pass' in request.form:
#        username = request.form['user']
#        password = request.form['pass']
#    cursor = pyrebase.connection.cursor(pyrebase.cursors.DictCursor)
#    cursor.execute('SELECT * FROM users WHERE user = %s AND pass = %s', (user, pass))
#    users = cursor.fetchone()
#    if account:
#            session['loggedin'] = True
#            session['user'] = account['user']
#            session['nafn'] = account['nafn']
#            return 'Logged in successfully!'
#        else:
#            msg = 'Incorrect username or password!'
#    return render_template('index.html', msg='') 



#@app.route('/signout')
#def signout():
#    session.pop('loggedin', None)
#    session.pop('user', None)
#    session.pop('nafn', None)
#    return redirect(url_for('login'))

#@app.route('/register', methods=['GET', 'POST'])
#def register():
#    msg = ''
#    if request.method == 'POST' and 'user' in request.form and 'pass' in request.form:
#        username = request.form['user']
#        password = request.form['pass']
#    elif request.method == 'POST':
#        msg = 'Please fill out the form!'
#    return render_template('signup.html', msg=msg)

#@app.route('/home')
#def home():
#    if 'loggedin' in session:
#        return render_template('homepage.html', username=session['user'])
#    return redirect(url_for('login'))

#FIREBASE


#hjalp :D

if __name__ == "__main__":
    app.run(debug=True)
