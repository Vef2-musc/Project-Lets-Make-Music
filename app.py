import os
from flask import Flask, render_template

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
@app.route("/back")
def search():
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)