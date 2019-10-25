import click
import app.models as models
from flask.cli import AppGroup
from werkzeug.security import generate_password_hash
from config.database import db

dbase = AppGroup('dbase')

@dbase.command()
def create_all_tabs():
    """Creating tables in database by all models in app"""
    ArModels = models.all_models()
    print(ArModels)
    db.database.create_tables(ArModels)

@dbase.command()
@click.argument('name')
def create_table(name):
    """Create table in database"""
    mod = models.one_model(name)
    if mod is not None:
        mod.create_table()
    else:
        print('таблица не существует')        
        
@dbase.command()
@click.argument('login')
@click.argument('password')
def create_admin(login, password):
    username = login
    #print(username)
    password = password
    hashpwd = generate_password_hash(password)
    #print(password)
    row = models.User(
        username=username,
        password=hashpwd,
        isadmin=True)
    row.save()
    print(f'Создан администратор: {login}')
    
@dbase.command()
@click.argument('login')
@click.argument('password')
def create_user(login, password):
    username = login
    #print(username)
    password = password
    hashpwd = generate_password_hash(password)
    #print(password)
    row = models.User(
        username=username,
        password=hashpwd)
    row.save()
    print(f'Создан пользователь: {login}')
