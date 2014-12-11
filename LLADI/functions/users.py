from flask import session, request
from LLADI.database import users

def current_user():
    if 'username' in session:
        return users.User(username=session['username'])
    else:
        return False