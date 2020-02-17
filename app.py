from flask import Flask, render_template, request, redirect, url_for, session
from db import add_user, login, get_user_id, add_task, get_tasks, change_task_status, delete_task
from sqlite3 import IntegrityError
import hashlib

app = Flask(__name__)
app.secret_key = 'bDcZ9jp6mKAHdhGy'

def hashing(password):
    passwd_hash = hashlib.sha512()
    passwd_hash.update(password.encode('utf-8'))
    return passwd_hash.hexdigest()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=error), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error=error), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['pw']
        try:
            add_user(name, email, hashing(password))
        except IntegrityError:
            return render_template('index.html', error='already_exists')
        session['user'] = name
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
        username = login(email, hashing(password))
        if username:
            session['user'] = username[0]
            return redirect(url_for('user_page', name=username[0]))
        else:
            return render_template('login.html', error='authentication_error')


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

@app.route('/change/<card_id>', methods=['GET', 'POST'])
def change(card_id):
    if request.method == 'POST':
        username = request.headers['Referer'].split('/')[-1]
        change_task_status(username, card_id)
    return redirect(url_for('user_page', name=username))

@app.route('/delete/<card_id>', methods=['GET', 'POST'])
def delete(card_id):
    if request.method == 'POST':
        username = request.headers['Referer'].split('/')[-1]
        delete_task(username, card_id)
    return redirect(url_for('user_page', name=username))

if __name__ == '__main__':
    app.run(debug=True)
