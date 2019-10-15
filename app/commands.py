import click
import importlib
import os
import sys
import app.models as models
from werkzeug.security import generate_password_hash
from config.database import db

def register(app):
    @app.cli.group()
    def dbase():
        """Database commands"""
        pass

    @dbase.command()
    def create_all_tabs():
        """Creating tables in database by all models in app"""
        ArModels = models.all_models()
        db.database.create_tables(ArModels)
        #for mod in ArModels:
            #mod.create_table()
        #indir = 'app/models'
        #for address, dirs, files in os.walk(indir):
            #for f in files:
                #ind = f.find('.py')
                #if ind != -1 and f.find('.pyc') == -1:  
                    #namemod = f[0:ind]
                    #path = 'app.models.'+namemod
                    #module = importlib.import_module(path)
                    ##print(module)
                    #for cls in module.__dict__.values(): 
                        ##print(type(cls))
                        #if issubclass(type(cls), pw.ModelBase):
                            #ArModels.append(cls)
        
        
                

    @dbase.command()
    @click.argument('name')
    def create_table(name):
        """Create table in database"""
        mod = models.one_model(name)
        if mod is not None:
            mod.create_table()
        else:
            print('таблица не существует')
        #ArModels = models.one_model(name)
        #db.database.create_tables(ArModels)
        
        #indir = 'app/models'
        #for address, dirs, files in os.walk(indir):
            #for f in files:
                #ind = f.find('.py')
                #if ind != -1 and f.find('.pyc') == -1:  
                    #namemod = f[0:ind]
                    #path = 'app.models.'+namemod
                    #module = importlib.import_module(path)
                    ##print(module)
                    #if name in module.__dict__:
                        ##print(name)
                        #ArModels.append(module.__dict__[name])
                        ##print(ArModels)
        
        

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
        print('Создан администратор: '+login)
    
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
        print('Создан пользователь: '+login)
