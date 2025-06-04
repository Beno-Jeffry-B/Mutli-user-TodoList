from flask import render_template
from todo import app

@app.route("/")
@app.route("home")
def home_page():
    return render_template("index.html")


@app.route("login")
def login():
    return render_template("login.html")


@app.route("sign_up")
def sign_up():
    return render_template("signup.html")

@app.route("createlist")
def createlist():
    return render_template("createlist.html")

@app.route("completedtasks")
def completed_tasks():
    return render_template("completed_tasks.html")


