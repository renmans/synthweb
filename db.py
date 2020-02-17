import sqlite3
import datetime
from functools import wraps

def init_tables():

    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS users (
        id integer primary key,
        username varchar(20) unique not null,
        password varchar(128) not null,
        email varchar(40) unique not null
        )''')

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS tasks (
        id integer primary key,
        user_id integer not null,
        title varchar(40) unique not null,
        content text,
        start_date date not null default CURRENT_DATE,
        end_date date,
        status boolean default 0
        )''')

    # cursor.execute(f'''CREATE TABLE IF NOT EXISTS subtasks (
    #     id integer primary key,
    #     task_id integer not null,
    #     content varchar(?) not null,
    #     status boolean default 0
    # )''')

    connection.close()

def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with sqlite3.connect('app.db') as connection:
            cursor = connection.cursor()
            func(*args, cursor=cursor, **kwargs)
        connection.commit()
    return wrapper

@db_connection
def add_user(username, email, password, **kwargs):
    cursor = kwargs["cursor"]
    cursor.execute('''insert into users (username, password, email) 
                   values (?, ?, ?)''', [username, password, email])
    cursor.execute('select * from users')

def login(email, password):
    print(password)
    with sqlite3.connect('app.db') as connection:
        cursor = connection.cursor()
        cursor.execute('select username from users where email = ? and password = ?', 
            [email, password])
        user = cursor.fetchone()
    return user

def get_user_id(name):
    with sqlite3.connect('app.db') as connection:
        cursor = connection.cursor()
        cursor.execute('select id from users where username = ?', [name])
        user_id = cursor.fetchone()
        return user_id[0]

@db_connection
def add_task(user_id, title, content, end_date, **kwargs):
    cursor = kwargs["cursor"]
    cursor.execute('''insert into tasks (user_id, title, content, end_date) 
                    values (?, ?, ?, ?)''', [user_id, title, content, end_date])
    cursor.execute('select * from tasks')

def get_tasks(name):
    user_id = get_user_id(name)
    with sqlite3.connect('app.db') as connection:
        cursor = connection.cursor()
        cursor.execute('select * from tasks where user_id = ?', [user_id])
        user_tasks = cursor.fetchall()
        return user_tasks  # the reason why you can't use a decorator

@db_connection
def change_task_status(name, task_id, **kwargs):
    user_id = get_user_id(name)
    cursor = kwargs["cursor"]
    cursor.execute('select * from tasks where user_id = ?', [user_id])
    user_tasks = cursor.fetchall()
    task_id = int(task_id.split('_')[-1]) - 1  # card_id
    global_id = user_tasks[task_id][0]
    current_status = user_tasks[task_id][6]
    print(f'user_tasks: {user_tasks}\ntask_id: {task_id}\nglobal_id: {global_id}')
    cursor.execute('update tasks set status = ? where id = ?', 
        [not current_status, global_id])

@db_connection
def delete_task(name, task_id, **kwargs):
    user_id = get_user_id(name)
    cursor = kwargs["cursor"]
    cursor.execute('select * from tasks where user_id = ?', [user_id])
    user_tasks = cursor.fetchall()
    task_id = int(task_id.split('_')[-1]) - 1
    global_id = user_tasks[task_id][0]
    cursor.execute('delete from tasks where user_id = ? and id = ?',
        [user_id, global_id])

init_tables()
