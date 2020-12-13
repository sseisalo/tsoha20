from db import db
from flask import session
import users
import channels

def get_posts(channel_name):
    if channel_name == "":
        sql = "SELECT P.content, U.username, P.sent_at, C.name, P.id, P.user_id FROM Posts P, Users U, Channels C WHERE P.user_id=U.id AND C.id=P.channel_id AND P.visible=1 ORDER BY P.id DESC"
        result = db.session.execute(sql)
    else:
        sql = "SELECT P.content, U.username, P.sent_at, C.name, P.id, P.user_id FROM Posts P, Users U, Channels C WHERE P.user_id = U.id AND C.name=LOWER(:channel_name) AND C.id=P.channel_id AND P.visible=1 ORDER BY P.id DESC"
        result = db.session.execute(sql, {"channel_name":channel_name})
    return result.fetchall()

def send(content, channel_name):
    user_id = users.user_id()
    channel_id = channels.get_channel_id(channel_name)
    if user_id == 0:
        return False

    sql = "INSERT INTO posts (content, channel_id, user_id, sent_at, visible) VALUES (:content, :channel_id, :user_id, NOW(), 1)"
    db.session.execute(sql, {"content":content, "channel_id":channel_id, "user_id":user_id})
    db.session.commit()
    return True

def get_post(post_id):
    sql = "SELECT P.content, U.username, P.user_id, P.id FROM Posts P, Users U WHERE P.id=:post_id AND U.id=P.user_id AND P.visible=1"
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchone()

def search_posts(query):
    sql = "SELECT P.content, U.username, P.sent_at, C.name, P.id FROM Posts P, Users U, Channels C WHERE U.id=P.user_id AND C.id=P.channel_id AND (P.content ILIKE :query OR C.name=:query_channel) AND P.visible=1"
    query_channel = query.lower()
    query = "%"+query+"%"
    print(query_channel)
    result = db.session.execute(sql, {"query":query.lower(), "query_channel":query_channel})
    return result.fetchall()

def delete_post(post_id):
    if users.is_moderator() or is_users_post(post_id):
        sql = "UPDATE posts SET visible=0 WHERE id=:post_id"
        db.session.execute(sql, {"post_id":post_id})
        db.session.commit()

def is_users_post(post_id):
    user_id = users.user_id()
    sql = "SELECT * FROM posts WHERE user_id=:user_id AND id=:post_id"
    result = db.session.execute(sql, {"user_id":user_id, "post_id":post_id})
    if result.fetchone() != None:
        return True
    else:
        return False

def is_deleted(post_id):
    sql = "SELECT visible FROM posts WHERE id=:post_id"
    result = db.session.execute(sql, {"post_id":post_id}).fetchone()

    if result[0] == 0:
        return True
    else:
        return False