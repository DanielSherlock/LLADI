from flask import Flask, render_template, request, session, redirect, url_for
from LLADI.database import users
from LLADI.functions.login import valid_login, log_in
from LLADI.functions.users import current_user

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
                return redirect(url_for('login') + '?failed=1')
        else:
            return redirect(request.args.get('next'))
    else:
        page = render_template('page/login.html')
        return render_template('global/frame.html', content=page, page="login", logged=cu)


@app.route('/logout/', methods=['GET'])
def logout():
    session.pop('username')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    else:
        return redirect(url_for('home'))


@app.route('/user/<userid>')
def user(userid):
    cu = current_user()
    pu = users.User(uuid=userid)
    if cu.uuid == pu.uuid:
        is_owner = True
    else:
        is_owner = False
    page = render_template('page/userpage.html', user=pu, is_owner=is_owner)
    return render_template('global/frame.html', content=page, page="User", logged=cu)

if __name__ == '__main__':
    app.secret_key = '~\xaa\xaf\xdf.\xb8d\xe6,\xdd\xfd\x8eD[\x94\xaeQku\xf6{\xa0\xd9a'
    app.run(debug=True)