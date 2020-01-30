from flask import Flask, render_template, request, redirect, url_for, session
from db import add_user, login, get_user_id, add_task, get_tasks
from sqlite3 import IntegrityError

app = Flask(__name__)
app.secret_key = 'iamiwhoami'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['pw']
        password_check = request.form['pw_check']
        print(email, name, password, password_check)
        try:
            add_user(name, email, password)
        except IntegrityError:
            return render_template('index.html', error='already_exists')
        session['user'] = name
        print(session['user'], name)
        return redirect(url_for('user_page', name=name))
    return render_template('index.html', error='')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['pw']
        # remember = request.form['remember']
        username = login(email, password)
        if username:
            session['user'] = username[0]
            return redirect(url_for('user_page', name=username[0]))
        else:
            return redirect(url_for('login_user'))


@app.route('/users/<name>', methods=['GET', 'POST'])
def user_page(name):
    if request.method == 'POST':
        user_id = get_user_id(name)
        title = request.form['title']
        content = request.form['content']
        end_date = request.form['end_date']
        add_task(user_id, title, content, end_date)
    user_tasks = get_tasks(name)
    return render_template('user.html', name=name, tasks=user_tasks)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

app.run(debug=True)