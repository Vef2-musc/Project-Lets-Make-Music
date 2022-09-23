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
def hello_world():
    return render_template("hompage.html")
@app.route("/login", methods=['GET','POST'])
def forsida():
    if('user' in session):
        print("virkar..")
        #return render_template('homepage.html')
        return 'Hi, {}'.format(session['user'])
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            session['user'] = email
            return 'success...'
        except:
            return 'Failed to login :('
    return render_template("index.html")
@app.route("/login", methods=['GET','POST'])
def login():
    
    return render_template("login.html")
@app.route("/search")
def leit():
    return render_template("search.html")
@app.route("/signup", methods=['POST','GET'])
def signup():
    return render_template("signup.html")
@app.route("/back")
def back():
    return redirect("/")
@app.route('/signout')
def signout():
    session.pop('loggedin', None)
    session.pop('user', None)
    session.pop('nafn', None)
    return redirect(url_for('login'))
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
