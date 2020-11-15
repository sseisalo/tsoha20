from db import db
import posts
import users

def get_comments(post_id):
    sql = "SELECT C.content, U.username, C.sent_at FROM Comments C, Users U WHERE C.post_id=:post_id AND U.id=C.user_id"
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchall()

def send(content, post_id):
    user_id = users.user_id()
    if user_id == None:
        return False
    sql = "INSERT INTO comments (content, user_id, post_id, sent_at) VALUES (:content, :user_id, :post_id, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id, "post_id":post_id})
    db.session.commit()
    return True