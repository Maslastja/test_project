import peewee as pw
from flask import request, session, redirect, url_for
from functools import wraps
from werkzeug.security import check_password_hash
from app.models.users import User

# возврат соответствия логина и пароля
def check_logpass():
    username = request.form.get('username')
    password = request.form.get('password')
    sel = User.select().where(User.username == username)
    
    if len(sel) == 0:
        return (None, 'Неверный логин')
    else:
        usr = sel.get()
        if check_password_hash(usr.password, password):
            return (usr, '')
        else:
            return (None, 'Неверный пароль')

#декоратор ограничения использования функций только авториз. пользователей
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

