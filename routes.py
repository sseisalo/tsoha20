from app import app
from flask import render_template, redirect, request, session, url_for, flash
import users
import posts
import channels
import comments
import votes

@app.route("/")
def index():
    list = posts.get_posts("")
    return render_template("feed_layout.html",posts=list,channel_name="main",title="Etusivu")

@app.route("/login/",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            flash("Kirjauduttu sisään")
            return redirect("/")
        else:
            flash("Kirjautuminen epäonnistui")
            return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    users.logout()
    flash("Kirjauduttu ulos")
    return redirect("/")

@app.route("/register/",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) > 16:
            flash("Tunnus " + username + " on liian pitkä")
            return redirect(url_for("register"))
        elif len(username) < 3:
            flash("Tunnus " + username + " on liian lyhyt")
            return redirect(url_for("register"))
        elif len(password) < 6:
            flash("Salasanan tulee olla vähintään 6 merkkiä")
            return redirect(url_for("register"))
        if users.register(username,password):
            flash("Rekisteröinti onnistui")
            return redirect("/")
        else:
            flash("Tämä tunnus on jo olemassa")
            return redirect(url_for("register"))

@app.route("/ch/<string:channel_name>/new/",methods=["GET","POST"])
def new(channel_name):
    if request.method == "GET":
        return render_template("new.html",channel_name=channel_name)
    if request.method == "POST":
        content = request.form["content"]
        if len(content) < 3:
            flash("Aloitus on liian lyhyt! \n (alle 3 merkkiä)")
            return redirect(url_for("new",channel_name=channel_name))
        elif len(content) > 200:
            flash("Aloitus on liian pitkä! \n (yli 200 merkkiä)")
            return redirect(url_for("new",channel_name=channel_name))
        elif posts.send(content, channel_name) == False:
            flash("Aloituksen luominen epäonnistui")
            return redirect(url_for("new",channel_name=channel_name))
        else:
            flash("Aloitus luotu")
            return redirect(url_for("channel",channel_name=channel_name))

@app.route("/ch/<string:channel_name>/")
def channel(channel_name):
    list = posts.get_posts(channel_name)
    title = "/ch/" + channel_name
    if channels.is_channel(channel_name):
        return render_template("feed_layout.html",channel_name=channel_name,posts=list,title=title)
    else:
        flash("Kanavaa " + channel_name + " ei ole olemassa")
        return redirect("/")

@app.route("/ch/<string:channel_name>/<int:post_id>/",methods=["GET","POST"])
def post(channel_name,post_id):
    if posts.is_deleted(post_id):
        return redirect(url_for("channel",channel_name=channel_name))

    list = comments.get_comments(post_id)
    post = posts.get_post(post_id)
    
    if request.method == "GET":
        return render_template("post.html",comments=list,post=post,channel_name=channel_name,post_id=post_id)
    if request.method == "POST":
        comment = request.form["comment"]
        if len(comment) < 1:
            flash("Viesti oli tyhjä")
            return redirect(url_for("post",channel_name=channel_name,post_id=post_id))
        elif len(comment) > 5000:
            flash("Viestin koko ylitti maksimin! (5000 merkkiä)")
            return redirect(url_for("post",channel_name=channel_name,post_id=post_id))
        elif comments.send(comment, post_id) == False:
            flash("Viestin lähetys epäonnistui")
            return redirect(url_for("post",channel_name=channel_name,post_id=post_id))
        else:
            flash("Viesti lähetetty")
            return redirect(request.url)

@app.route("/ch/<string:channel_name>/search/",methods=["GET"])
def search(channel_name):
    sort = request.args.get("sort")
    query = request.args.get("query")

    if sort == "date":
        list = posts.search_posts_by_date(query)
        return render_template("search.html",channel_name=channel_name,posts=list,query=query)
    
    if sort == "votes":
        list = posts.search_posts_by_votes(query)
        return render_template("search.html",channel_name=channel_name,posts=list,query=query)

@app.route("/removepost",methods=["GET"])
def remove_post():
    post_id = request.args.get("post_id")
    if posts.delete_post(post_id):
        flash("Aloitus poistettu")
    else:
        flash("Aloituksen poisto epäonnistui")

    return redirect(request.referrer)

@app.route("/removecomment",methods=["GET"])
def remove_comment():
    comment_id = request.args.get("comment_id")
    if comments.delete_comment(comment_id):
        flash("Kommentti poistettu")
    else:
        flash("Kommentin poisto epäonnistui")

    return redirect(request.referrer)

@app.route("/votepost",methods=["GET"])
def vote_post():
    post_id = request.args.get("post_id")
    vote = request.args.get("vote")
    votes.send_post_vote(vote, post_id)

    return redirect(request.referrer)

@app.route("/votecomment",methods=["GET"])
def vote_comment():
    comment_id = request.args.get("comment_id")
    vote = request.args.get("vote")
    votes.send_comment_vote(vote, comment_id)

    return redirect(request.referrer)