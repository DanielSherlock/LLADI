from flask import Flask, render_template, request, session, redirect, url_for
from LLADI.database import users, follows, courses
from LLADI.functions.login import valid_login, log_in
from LLADI.functions.users import current_user
from LLADI.functions.register import register_user, validate_register
from LLADI.functions.follow import validate_follow
from LLADI.functions.feeds import create_feed
import base64

import re

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
        if len(register_username) < 8:
            errors.append('username_length')
        if len(register_password) < 8:
            errors.append('password_length')
        if len(register_display_name) == 0:
            errors.append('display_name_length')
        if len(re.findall('(^\s+|\s\s+|\s+$)', register_display_name)) != 0:
            errors.append('display_name_whitespace')
        if register_password != register_repeat_password:
            errors.append('password_no_match')
        if not validate_register(register_username):
            errors.append('username_already_exists')
        query_string = "?"
        for error in errors:
            query_string += error + "=1&"
        query_string.strip("&")
        if len(errors):
            return redirect(url_for('register') + query_string)
        else:
            register_user(register_username, register_password, register_display_name)
            return redirect(url_for('home'))
    else:
        errors = []
        if request.args.get('username_length'):
            errors.append('username_length')
        if request.args.get('password_length'):
            errors.append('password_length')
        if request.args.get('display_name_length'):
            errors.append('display_name_length')
        if request.args.get('display_name_whitespace'):
            errors.append('display_name_whitespace')
        if request.args.get('password_no_match'):
            errors.append('password_no_match')
        if request.args.get('username_already_exists'):
            errors.append('username_already_exists')
        page = render_template('page/register.html', errors=errors)
        cu = current_user()
        return render_template('global/frame.html', content=page, page="register", logged=cu)


@app.route('/user/<userid>')
def user(userid):
    cu = current_user()
    pu = users.User(uuid=userid)
    user_follows = []
    user_followed_by = []
    if len(pu.follows):
        for followed_user in pu.follows:
            user_follows.append(users.User(uuid=followed_user[0]))
    if len(pu.followed_by):
        for followed_user in pu.followed_by:
            user_followed_by.append(users.User(uuid=followed_user[0]))
    following = "no_follow"
    if cu:
        following = "False"
        for check_user in user_followed_by:
            if check_user.uuid == cu.uuid:
                following = "True"
    page = render_template('page/userpage.html', user=pu, logged=cu, follows=user_follows, followed_by=user_followed_by,
                           following=following)
    return render_template('global/frame.html', content=page, page="user", logged=cu)


@app.route('/user/', methods=['GET', 'POST'])
def user_search():
    if request.method == "POST":
        results = users.search_user(request.form['searchUser'])
        cu = current_user()
        page = render_template('page/usersearch.html', results=results)
        return render_template('global/frame.html', content=page, page="user", logged=cu)

    else:
        cu = current_user()
        page = render_template('page/usersearch.html')
        return render_template('global/frame.html', content=page, page="user", logged=cu)


@app.route('/course/', methods=['GET', 'POST'])
def course_search():
    if request.method == "POST":
        results = courses.search_course(request.form['searchCourse'])
        cu = current_user()
        page = render_template('page/coursesearch.html', results=results)
        return render_template('global/frame.html', content=page, page="course", logged=cu)

    else:
        cu = current_user()
        page = render_template('page/coursesearch.html')
        return render_template('global/frame.html', content=page, page="course", logged=cu)


@app.route('/follow/', methods=['GET', 'POST'])
def follow():
    follower = current_user().uuid
    followee = users.User(uuid=request.form['followee']).uuid
    if validate_follow(follower, followee):
        follows.new_follow(follower, followee)
    return redirect(request.args.get('next'))


@app.route('/unfollow/', methods=['GET', 'POST'])
def unfollow():
    follower = current_user().uuid
    followee = users.User(uuid=request.form['followee']).uuid
    follows.remove_follow(follower, followee)
    return redirect(request.args.get('next'))


@app.route('/feed/')
def feed():
    cu = current_user()
    if not cu:
        return redirect(url_for('login') + "?next=" + url_for('feed'))
    feed = create_feed(cu)
    feed.sort(key=lambda x: x['date'], reverse=True)
    page = render_template('page/feed.html', feed=feed)
    return render_template('global/frame.html', content=page, page="feed", logged=cu)


@app.route('/course/<courseid>')
def course(courseid):
    cu = current_user()
    if not cu:
        return redirect(url_for('login') + "?next=" + request.url)
    course_page = courses.Course(ucid=courseid)
    course_owner = users.User(uuid=course_page.owner)
    contributor_uuids = courses.get_contributors(courseid)
    lessons = courses.get_lessons(courseid)
    tier = users.get_tier_knowledge(courseid, cu.uuid)
    contributors = []
    for entry in contributor_uuids:
        contributors.append(users.User(uuid=entry))
    page = render_template('page/course.html', course=course_page, owner=course_owner, contributors=contributors,
                           lessons=lessons, tier=tier)
    return render_template('global/frame.html', content=page, page="course", logged=cu)


@app.route('/lesson/')
def lesson_redirect():
    return redirect(url_for('course_search'))


@app.route('/create/course/', methods=['GET', 'POST'])
def create_course():
    cu = current_user()
    if not cu:
        return redirect(url_for('login') + "?next=" + request.url)
    if request.method == "POST":
        create_course_name = request.form['createCourseName']
        create_course_owner = cu.uuid
        create_course_picture = str(base64.encodebytes(request.files['createCoursePicture'].stream.read())).strip(
            "b'").strip("'").replace("\\n", "\n")
        return redirect(
            "/course/" + str(courses.create_course(create_course_name, create_course_owner, create_course_picture)))
    else:
        page = render_template('page/createcourse.html')
        return render_template('global/frame.html', content=page, page="course", logged=cu)


@app.route('/lesson/<lessonid>')
def lesson(lessonid):
    cu = current_user()
    if not cu:
        return redirect(url_for('login') + "?next=" + request.url)
    page = "hello"
    return render_template('global/frame.html', content=page, page="course", logged=cu)


if __name__ == '__main__':
    app.secret_key = '~\xaa\xaf\xdf.\xb8d\xe6,\xdd\xfd\x8eD[\x94\xaeQku\xf6{\xa0\xd9a'
    app.run(debug=True)