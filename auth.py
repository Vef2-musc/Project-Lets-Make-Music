import pyrebase

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

email = 'tst@gmail.com'
password = '123456'

#user = auth.create_user_with_email_and_password(email, password)
#print(user)

#user = auth.sign_in_with_email_and_password(email,password)
#auth.send_email_verification(user['idToken'])

auth.send_password_reset_email(email)

