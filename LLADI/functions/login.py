from passlib.apps import custom_app_context as pwd_context
from flask import session
from LLADI.database import users


def valid_login(username, password):
    request_user = users.User(username=username)
    if request_user.exists:
        return pwd_context.verify(password, request_user.password)
    else:
        return False


def log_in(username):
    session['username'] = username
