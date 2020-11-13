from app import app
from flask import render_template, redirect, request, session
import users
import posts
import channels

@app.route("/")
def index():
    list = posts.get_list("")
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

@app.route("/ch/<string:channel_name>/new",methods=["GET","POST"])
def new(channel_name):
    if request.method == "GET":
        return render_template("new.html",channel_name=channel_name)
    if request.method == "POST":
        content = request.form["content"]
        if posts.send(content,channel_name):
            return redirect("/")
        else:
            return "epäonnistui"

@app.route("/ch/<string:channel_name>")
def channel(channel_name):
    list = posts.get_list(channel_name)
    if channels.is_channel(channel_name):
        return render_template("channel.html",channel_name=channel_name,posts=list)
    else: 
        return "unluigi"

@app.route("/ch/<string:channel_name>/<int:post_id>")
def post(channel_name,post_id):
    return render_template("post.html")