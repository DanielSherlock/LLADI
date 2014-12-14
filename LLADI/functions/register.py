from passlib.apps import custom_app_context as pwd_context
from LLADI.database import users


def register_user(username, password, display_name):
    users.new_user(username, pwd_context.encrypt(password), display_name)

def validate_register(username):
    duplicate_user = users.User(username=username)
    if duplicate_user.exists:
        return False
    else:
        return True