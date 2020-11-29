from app import app
from flask import render_template, redirect, request, session, url_for
import users
import posts
import channels
import comments
import votes

@app.route("/")
def index():
    list = posts.get_posts("")
    return render_template("feed_layout.html",posts=list,channel_name="main",title="Etusivu")

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
        if len(username) > 16:
            return "liian pitkä"
        elif len(username) < 3:
            return "liian lyhyt"
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
        if len(content) < 3 or len(content) > 100 or posts.send(content, channel_name) == False:
            return "unluigo"
        else:
            return redirect(url_for("channel",channel_name=channel_name))

@app.route("/ch/<string:channel_name>")
def channel(channel_name):
    list = posts.get_posts(channel_name)
    title = "/ch/" + channel_name
    if channels.is_channel(channel_name):
        return render_template("feed_layout.html",channel_name=channel_name,posts=list,title=title)
    else: 
        return "unluigi"

@app.route("/ch/<string:channel_name>/<int:post_id>",methods=["GET","POST"])
def post(channel_name,post_id):
    list = comments.get_comments(post_id)
    post = posts.get_post(post_id)
    
    if request.method == "GET":
        return render_template("post.html",comments=list,post=post,channel_name=channel_name,post_id=post_id)
    if request.method == "POST":
        comment = request.form["comment"]
        if len(comment) < 1 or len(comment) > 5000 or comments.send(comment, post_id) == False:
            return "unluigo"
        else:
            return redirect(request.url)

@app.route("/ch/<string:channel_name>/search",methods=["GET"])
def search(channel_name):
    query = request.args.get("query")
    list = posts.search_posts(query)

    return render_template("search.html",channel_name=channel_name,posts=list,query=query)