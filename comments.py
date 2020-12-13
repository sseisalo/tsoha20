from db import db
from flask import session
import posts
import users

def get_comments(post_id):
    user_id = users.user_id()

    sql = "SELECT C.content, U.username, C.sent_at, C.id, C.visible, C.user_id, (SELECT COALESCE(SUM(vote),0) FROM votes V WHERE V.comment_id=C.id), (SELECT COALESCE(SUM(vote),0) FROM votes VO WHERE VO.user_id=:user AND VO.comment_id=C.id) FROM Comments C, Users U WHERE C.post_id=:post_id AND U.id=C.user_id ORDER BY C.id DESC"
    result = db.session.execute(sql, {"user":user_id, "post_id":post_id})
    return result.fetchall()

def send(content, post_id):
    user_id = users.user_id()
    if user_id == None:
        return False
    sql = "INSERT INTO comments (content, user_id, post_id, sent_at, visible) VALUES (:content, :user_id, :post_id, NOW(), 1)"
    db.session.execute(sql, {"content":content, "user_id":user_id, "post_id":post_id})
    db.session.commit()
    return True

def delete_comment(comment_id):
    if users.is_moderator() or is_users_comment(comment_id):
        sql = "UPDATE comments SET visible=0 WHERE id=:comment_id"
        db.session.execute(sql, {"comment_id":comment_id})
        db.session.commit()
        return True

    return False

def is_users_comment(comment_id):
    user_id = users.user_id()
    sql = "SELECT * FROM comments WHERE user_id=:user_id AND id=:comment_id"
    result = db.session.execute(sql, {"user_id":user_id, "comment_id":comment_id})
    if result.fetchone() != None:
        return True
    else:
        return False