from app import app
from flask import render_template, redirect, request, session
import users
import posts

@app.route("/")
def index():
    print("indeksi")
    list = posts.get_list()
    return render_template("index.html",posts=list)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return "väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username,password):
            return redirect("/")
        else:
            return "tämä tunnus on jo olemassa"

@app.route("/new",methods=["GET","POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        content = request.form["content"]
        if posts.send(content):
            return redirect("/")
        else:
            return "epäonnistui"