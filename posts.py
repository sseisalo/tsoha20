from db import db
import users
import channels

def get_list(channel_name):
    if channel_name == "":
        sql = "SELECT P.content, U.username, P.sent_at, C.name, P.id FROM Posts P, Users U, Channels C WHERE P.user_id = U.id AND C.id=P.channel_id ORDER BY P.id"
        result = db.session.execute(sql)
    else:
        sql = "SELECT P.content, U.username, P.sent_at, C.name, P.id FROM Posts P, Users U, Channels C WHERE P.user_id = U.id AND C.name=:channel_name AND C.id=P.channel_id ORDER BY P.id"
        result = db.session.execute(sql, {"channel_name":channel_name})
    return result.fetchall()

def send(content, channel_name):
    user_id = users.user_id()
    channel_id = channels.get_channel_id(channel_name)
    if user_id == 0:
        return False

    sql = "INSERT INTO posts (content, channel_id, user_id, sent_at) VALUES (:content, :channel_id, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "channel_id":channel_id, "user_id":user_id})
    db.session.commit()
    return True