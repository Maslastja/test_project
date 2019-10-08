import peewee as pw
from flask import request
from werkzeug.security import generate_password_hash
from app.models.users import User

def create_user():
    username = request.form.get('username')
    #print(username)
    password = request.form.get('password')
    hashpwd = generate_password_hash(password)
    #print(password)
    row = User(
        username=username,
        password=hashpwd)
    row.save()
    req = (f'Создан пользователь {username}')
        
    return req

