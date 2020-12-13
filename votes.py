from db import db
import posts
import comments
import users

def get_post_votes(post_id):
    sql = "SELECT COALESCE(SUM(vote),0) FROM votes WHERE post_id=:post_id"
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchone()

def get_comment_votes(comment_id):
    sql = "SELECT COALESCE(SUM(vote),0) FROM votes WHERE comment_id=:comment_id"
    result = db.session.execute(sql, {"comment_id":comment_id})
    return result.fetchone()

def send_post_vote(vote, post_id):
    user_id = users.user_id()
    if not user_id:
        return False

    sql = "SELECT COALESCE(COUNT(vote),0), COALESCE(SUM(vote),0) FROM votes WHERE post_id=:post_id AND user_id=:user_id"
    result = db.session.execute(sql, {"post_id":post_id, "user_id":user_id}).fetchone()
    
    if result[0] == 0:
        sql = "INSERT INTO votes (vote, user_id, post_id) VALUES (:vote, :user_id, :post_id)"
        db.session.execute(sql, {"vote":vote, "post_id":post_id, "user_id":user_id})
        db.session.commit()
    else:
        sql = "UPDATE votes SET vote=:vote WHERE post_id=:post_id AND user_id=:user_id"
        db.session.execute(sql, {"vote":vote, "post_id":post_id, "user_id":user_id})
        db.session.commit()
    
def send_comment_vote(vote, comment_id):
    user_id = users.user_id()
    if not user_id:
        return False

    sql = "SELECT COALESCE(COUNT(vote),0), COALESCE(SUM(vote),0) FROM votes WHERE comment_id=:comment_id AND user_id=:user_id"
    result = db.session.execute(sql, {"comment_id":comment_id, "user_id":user_id}).fetchone()
    
    if result[0] == 0:
        sql = "INSERT INTO votes (vote, user_id, comment_id) VALUES (:vote, :user_id, :comment_id)"
        db.session.execute(sql, {"vote":vote, "comment_id":comment_id, "user_id":user_id})
        db.session.commit()
    else:
        sql = "UPDATE votes SET vote=:vote WHERE comment_id=:comment_id AND user_id=:user_id"
        db.session.execute(sql, {"vote":vote, "comment_id":comment_id, "user_id":user_id})
        db.session.commit()