from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["user_name"] = username
            is_moderator()
            return True
        else:
            return False

def logout():
    if is_moderator():
        del session["user_type"]
    del session["user_id"]
    del session["user_name"]

def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,user_type) VALUES (:username,:password,0)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)

def is_moderator():
    user = user_id()

    sql = "SELECT user_type FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user})
    user_type = result.fetchone()
    if user_type[0] == 1:
        session["user_type"] = user_type[0]
        return True
    else:
        return False