from flask import Flask, render_template, request, session, redirect, url_for, re
from LLADI.database import users
from LLADI.functions.login import valid_login, log_in
from LLADI.functions.users import current_user
from LLADI.functions.register import register_user

app = Flask(__name__)


@app.route('/')
def home():
    cu = current_user()
    page = render_template('page/welcome.html')
    return render_template('global/frame.html', content=page, page="home", logged=cu)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' not in request.cookies:
            if valid_login(request.form['loginUsername'], request.form['loginPassword']):
                log_in(request.form['loginUsername'])
                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                else:
                    return redirect(url_for('home'))
            else:
                if request.args.get('next'):
                    return redirect(url_for('login') + '?failed=1&next=' + request.args.get('next'))
                else:
                    return redirect(url_for('login') + '?failed=1')
        else:
            return redirect(request.args.get('next'))
    else:
        cu = current_user()
        failure = request.args.get('failed')
        page = render_template('page/login.html', failure=failure)
        return render_template('global/frame.html', content=page, page="login", logged=cu)


@app.route('/logout/', methods=['GET'])
def logout():
    session.pop('username')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    else:
        return redirect(url_for('home'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        register_username = request.form['registerUsername']
        register_password = request.form['registerPassword']
        register_repeat_password = request.form['registerRepeatPassword']
        register_display_name = request.form['registerDisplayName']
        errors = []
        if len(register_username) <= 8:
            errors.append('username_length')
        if len(register_password) <= 8:
            errors.append('password_length')
        if len(register_display_name) <= 1:
            errors.append('display_name_length')
        if len(re.findall('(^\s+|\s\s+|\s+$)', register_display_name)) != 0:
            errors.append('display_name_whitespace')
        if register_password != register_repeat_password:
            errors.append('password_no_match')
        query_string = "?="
        for error in errors:
            query_string += error + "&"
        query_string.strip("&")
        if len(errors):
            return redirect(url_for('register') + query_string)
        else:
            register_user(register_username, register_password, register_display_name)


@app.route('/user/<userid>')
def user(userid):
    cu = current_user()
    pu = users.User(uuid=userid)
    page = render_template('page/userpage.html', user=pu)
    return render_template('global/frame.html', content=page, page="User", logged=cu)


if __name__ == '__main__':
    app.secret_key = '~\xaa\xaf\xdf.\xb8d\xe6,\xdd\xfd\x8eD[\x94\xaeQku\xf6{\xa0\xd9a'
    app.run(debug=True)