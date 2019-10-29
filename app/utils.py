import os
import importlib
from logging.handlers import RotatingFileHandler
from peewee import logging

def logapp(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', 
                                            maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: '
        '%(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('test app')

def register_bp(app):
    #print(app.import_name)
    #возможно можно использовать import_name т.к. это название папки 
    #приложения, в которой находятся все дополнительные папки и файлы
    for address, dirs, files in os.walk(f'{app.import_name}'):
        for d in dirs:
            try:
                #print(f'{address}.{d}')
                module = importlib.import_module(f'{address}.{d}')
                if 'bp' in module.__dict__:
                    bp = module.bp
                    if 'options' in module.__dict__:
                        opt = module.options
                    else:
                        opt = {}
                    app.register_blueprint(bp, **opt)
            except(Exception):
                #if d == 'admin':
                    #module = importlib.import_module(f'app.{d}')
                continue
