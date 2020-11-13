from db import db
import users

def get_list():
    sql = "SELECT P.content, U.username, P.sent_at FROM Posts P, Users U WHERE P.user_id = U.id ORDER BY P.id"
    result = db.session.execute(sql)
    print(result)
    print("helou")
    return result.fetchall()

def send(content):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = "INSERT INTO posts (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True